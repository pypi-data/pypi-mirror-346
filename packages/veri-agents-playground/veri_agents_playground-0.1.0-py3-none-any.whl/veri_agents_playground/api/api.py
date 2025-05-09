import asyncio
import logging
import os
from contextlib import asynccontextmanager
from io import BytesIO
from pathlib import Path
from typing import Any, AsyncGenerator, Tuple

from veri_agents_playground.agents.persistence import AsyncSqliteSaverPlus

import aiohttp
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from hydra import compose, initialize
from langchain_core.callbacks import AsyncCallbackHandler
from veri_agents_playground.schema.schema import DocumentMetadata
from veri_agents_api.fastapi.thread import ChatMessage

from veri_agents_playground.schema import (
    WorkspaceMetadata,
    WorkflowMetadata,
)

from veri_agents_knowledgebase import KnowledgebaseMetadata
from veri_agents_playground.agents.providers import (
    LLMProvider,
    AssetsManager,
    ainit_from_config,
    WorkspaceProvider,
    WorkflowProvider,
    KnowledgebaseProvider,
)

from veri_agents_playground.agents.access import is_admin, has_workspace_access

log = logging.getLogger(__name__)


class TokenQueueStreamingHandler(AsyncCallbackHandler):
    """LangChain callback handler for streaming LLM tokens to an asyncio queue."""

    def __init__(self, queue: asyncio.Queue):
        self.queue = queue

    async def on_llm_new_token(self, token: str, **kwargs) -> None:
        if token:
            await self.queue.put(token)


@asynccontextmanager
async def lifespan(app: FastAPI):
    config_path = os.getenv("VERI_AGENTS_PlAYGROUND_CONF", "../../../conf")

    # Construct agent with Sqlite checkpointer
    with initialize(
        version_base=None, config_path=config_path, job_name="veritone_agents_api"
    ):
        cfg = compose(config_name="config")
        # print(OmegaConf.to_yaml(cfg))
        await ainit_from_config(cfg)
        app.state.cfg = cfg

    checkpoints_path = Path(cfg.chat_storage.location)
    checkpoints_path.mkdir(parents=True, exist_ok=True)
    checkpoints_db_path = checkpoints_path / "checkpoints.db"

    # TODO: once we use the toolkit
    # this will work once we have the new router from the toolkit
    # async with AsyncSqliteSaver.from_conn_string(str(checkpoints_db_path)) as saver:
    async with AsyncSqliteSaverPlus.from_conn_string(str(checkpoints_db_path)) as saver:
        for workflow in WorkflowProvider.get_workflows().values():
            workflow.set_checkpointer(saver)
        app.state.workflows = WorkflowProvider.get_workflows()
        app.state.threads = {}
        app.state.checkpointer = saver

        # TODO: once we use the toolkit
        # threads = await ThreadsCheckpointerUtil.list_threads(saver)
        # for t in threads:
        async for t in saver.alist_threads():
            log.debug(t)
            app.state.threads[t.thread_id] = t
        yield
    # context manager will clean up the AsyncSqliteSaver on exit


app = FastAPI(lifespan=lifespan)

origins = ["http://localhost"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"https://(.*\.)?(veritone\.com|aiware.run)(\:.*)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def check_auth_header(request: Request, call_next):
    if (
        request.url.path.startswith("/docs")
        or request.url.path.startswith("/openapi.json")
        or request.url.path.startswith("/redoc")
    ):
        # skip auth for docs and openapi
        return await call_next(request)

    # allow all CORS preflight requests
    if request.method == "OPTIONS":
        return await call_next(request)

    request.state.is_admin = False

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return Response(status_code=401, content="Missing or invalid token")

    auth_token = auth_header[7:]

    # token matches auth secret, in this case we probably coming from streamlit or some dev mode
    # in this case we can rely on the user id in the header
    auth_secret = os.getenv("AUTH_SECRET")
    if auth_secret:
        if auth_token == auth_secret:
            request.state.user_name = request.headers.get(
                "X-User-Id", "nobody@veritone.com"
            )
            request.state.is_admin = is_admin(request.state.user_name)
            return await call_next(request)

    # TODO: probably have to decide which aiware we want to auth against
    # otherwise we see if the token is an aiware user, this might be a call directly from a frontend
    # so we have to verify the token
    api_base_url = os.getenv("AISG_AIWARE_BASE_URL", "https://api.us-1.veritone.com")
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{api_base_url}/v1/admin/current-user",
            headers={
                "accept": "*/*",
                "content-type": "application/json",
                "Authorization": f"Bearer {auth_token}",
            },
        ) as response:
            if response.status != 200:
                return Response(status_code=401, content="Invalid token")
            user_name = (await response.json()).get("userName")
            request.state.user_name = user_name
            request.state.is_admin = is_admin(request.state.user_name)
    return await call_next(request)


def get_viewer(request: Request) -> str:
    return request.state.user_name


def assert_viewer_can_assume_identity(request: Request, principal: str):
    viewer = get_viewer(request)

    if request.state.is_admin:
        return

    if not principal:
        # handle threads created with user "" (public)
        return

    if viewer != principal:
        raise HTTPException(status_code=403, detail="Forbidden")


def assert_viewer_is_admin(request: Request):
    if not request.state.is_admin:
        raise HTTPException(status_code=403, detail="Forbidden")


# ============================================================================
# TODO: remove this once we use the toolkit
# ============================================================================
import json
from langchain_core.runnables import RunnableConfig
from veri_agents_playground.schema import (
    WorkspaceMetadata,
    DocumentMetadata,
    OldStreamInput,
    OldInvokeInput,
    OldThreadInfo,
    WorkflowMetadata,
    OldFeedback,
)
from langfuse.callback import CallbackHandler
from langgraph.graph.graph import CompiledGraph

WorkflowInput = OldInvokeInput


def _parse_input(user_input: WorkflowInput) -> Tuple[dict[str, Any], str]:
    from uuid import uuid4

    run_id = uuid4()
    thread_id = user_input.thread_id
    input_message = ChatMessage(type="human", content=user_input.message)
    kwargs = dict(
        input={"messages": [input_message.to_langchain()]},
        config=RunnableConfig(
            configurable={
                "thread_id": thread_id,
                "user": user_input.user,
                "args": user_input.workflow_args,
            },
            run_id=run_id,
        ),
    )
    return kwargs, str(run_id)


@app.post("/invoke")
async def invoke(user_input: WorkflowInput, request: Request) -> ChatMessage:
    """
    Invoke the agent with user input to retrieve a final response.

    Use thread_id to persist and continue a multi-turn conversation. run_id kwarg
    is also attached to messages for recording feedback.
    """
    principal = user_input.user or get_viewer(request)

    # is the authenticated user allowed to act on behalf of the user in the request?
    assert_viewer_can_assume_identity(request, principal=principal)

    if user_input.workflow not in app.state.workflows:
        raise HTTPException(
            status_code=500, detail=f"Unknown workflow: {user_input.workflow}"
        )

    # check if this user is allowed to use this workflow
    if not has_workspace_access(
        principal,
        app.state.workflows[user_input.workflow].metadata.workspace,
        app.state.cfg,
    ):
        raise HTTPException(status_code=403, detail="Forbidden")

    agent: CompiledGraph = app.state.workflows[user_input.workflow].get_graph()
    kwargs, run_id = _parse_input(user_input)

    # store this thread in the database if a new one
    if user_input.thread_id not in app.state.threads:
        thread_info = OldThreadInfo(
            thread_id=user_input.thread_id,
            user=principal,
            workflow_id=user_input.workflow,
            name=user_input.message[:50],
            metadata={"app": user_input.app},
        )
        app.state.threads[user_input.thread_id] = thread_info
        await agent.checkpointer.aput_thread(thread_info) # type: ignore

    langfuse_handler = CallbackHandler(
        public_key=app.state.cfg.logging.langfuse.public_key,
        secret_key=app.state.cfg.logging.langfuse.secret_key,
        host=app.state.cfg.logging.langfuse.host,
        user_id=principal,
        session_id=user_input.thread_id,
        trace_name=user_input.message[:50],
    )
    kwargs["config"]["callbacks"] = [langfuse_handler]
    kwargs["config"]["configurable"]["workflow_id"] = user_input.workflow
    try:
        response = await agent.ainvoke(**kwargs)
        output = ChatMessage.from_langchain(response["messages"][-1])
        output.run_id = str(run_id)
        return output
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def message_generator(
    user_input: OldStreamInput, principal: str
) -> AsyncGenerator[str, None]:
    """
    Generate a stream of messages from the agent.

    This is the workhorse method for the /stream endpoint.
    """
    if user_input.workflow not in app.state.workflows:
        raise HTTPException(
            status_code=500, detail=f"Unknown workflow: {user_input.workflow}"
        )
    # check if this user is allowed to use this workflow
    if not has_workspace_access(
        principal,
        app.state.workflows[user_input.workflow].metadata.workspace,
        app.state.cfg,
    ):
        raise HTTPException(status_code=403, detail="Forbidden")

    log.info("Streaming agent running workflow %s", user_input.workflow)
    agent: CompiledGraph = app.state.workflows[user_input.workflow].get_graph()
    kwargs, run_id = _parse_input(user_input)

    # store this thread in the database if a new one
    if user_input.thread_id not in app.state.threads:
        thread_info = OldThreadInfo(
            thread_id=user_input.thread_id,
            user=principal,
            workflow_id=user_input.workflow,
            name=user_input.message[:50],
            metadata={"app": user_input.app},
        )
        app.state.threads[user_input.thread_id] = thread_info
        await agent.checkpointer.aput_thread(thread_info) # type: ignore

    # Use an asyncio queue to process both messages and tokens in
    # chronological order, so we can easily yield them to the client.
    output_queue = asyncio.Queue(maxsize=10)

    langfuse_handler = CallbackHandler(
        public_key=app.state.cfg.logging.langfuse.public_key,
        secret_key=app.state.cfg.logging.langfuse.secret_key,
        host=app.state.cfg.logging.langfuse.host,
        user_id=principal,
        session_id=user_input.thread_id,
        trace_name=user_input.message[:50],
    )
    if user_input.stream_tokens:
        kwargs["config"]["callbacks"] = [
            TokenQueueStreamingHandler(queue=output_queue),
            langfuse_handler,
        ]
    kwargs["config"]["configurable"]["workflow_id"] = user_input.workflow

    # Pass the agent's stream of messages to the queue in a separate task, so
    # we can yield the messages to the client in the main thread.
    async def run_agent_stream():
        async for s in agent.astream(**kwargs, stream_mode="updates"):
            await output_queue.put(s)
        await output_queue.put(None)

    stream_task = asyncio.create_task(run_agent_stream())

    # Process the queue and yield messages over the SSE stream.
    while s := await output_queue.get():
        log.info("Got from queue: %s: %s", type(s), s)
        if isinstance(s, str):
            # str is an LLM token
            yield f"data: {json.dumps({'type': 'token', 'content': s})}\n\n"
            continue

        # Otherwise, s should be a dict of state updates for each node in the graph.
        # s could have updates for multiple nodes, so check each for messages.
        new_messages = []
        for _, state in s.items():
            new_messages.extend(state["messages"])
        for message in new_messages:
            try:
                chat_message = ChatMessage.from_langchain(message)
                chat_message.run_id = str(run_id)
            except Exception as e:
                yield f"data: {json.dumps({'type': 'error', 'content': f'Error parsing message: {e}'})}\n\n"
                continue
            # LangGraph re-sends the input message, which feels weird, so drop it
            if (
                chat_message.type == "human"
                and chat_message.content == user_input.message
            ):
                continue
            yield f"data: {json.dumps({'type': 'message', 'content': chat_message.dict()})}\n\n"

    await stream_task
    yield "data: [DONE]\n\n"


@app.post("/stream")
async def stream_agent(user_input: OldStreamInput, request: Request):
    """
    Stream the agent's response to a user input, including intermediate messages and tokens.

    Use thread_id to persist and continue a multi-turn conversation. run_id kwarg
    is also attached to all messages for recording feedback.
    """
    principal = user_input.user or get_viewer(request)

    # is the authenticated user allowed to act on behalf of the user in the request?
    assert_viewer_can_assume_identity(request, principal=principal)

    return StreamingResponse(
        message_generator(user_input, principal=principal),
        media_type="text/event-stream",
    )


# =================================================================================
# END OF REMOVE THIS ONCE REFACTOR IS DONE
# =================================================================================


# =====
# THIS WILL BE THE NEW toolkit mechanism
# =====

# async def _get_workflow_from_request(request: Request) -> Workflow:
#     request_json = await request.json()
#     if workflow_name := request_json.get("workflow"):
#         workflow = app.state.workflows.get(workflow_name)
#     else:
#         raise HTTPException(
#             status_code=400, detail=f"Workflow not provided"
#         )

#     if workflow:
#         return workflow
#     else:
#         raise HTTPException(
#             status_code=404, detail=f"Unknown workflow: {workflow_name}"
#         )

# async def _get_graph_from_request(request: Request):
#     workflow = await _get_workflow_from_request(request)
#     return workflow.get_graph()

# async def _allow_access_thread(_thread_id: str, _thread_info: ThreadInfo | None, assume_user: str | None, request: Request):
#     principal = assume_user or get_viewer(request)

#     # is the authenticated user allowed to act on behalf of the user in the request?
#     assert_viewer_can_assume_identity(request, principal=principal)

#     workflow = await _get_workflow_from_request(request)

#     # check if this user is allowed to use this workflow
#     if not has_workspace_access(
#             principal,
#             workflow.metadata.workspace,
#             app.state.cfg,
#     ):
#         raise HTTPException(status_code=403, detail="Forbidden")

#     return True

# async def allow_access_thread(thread_id: str, thread_info: ThreadInfo | None, request: Request):
#     return await _allow_access_thread(thread_id, thread_info, None, request)

# async def allow_invoke_thread(thread_id: str, thread_info: ThreadInfo | None, invoke_input: InvokeInput, request: Request):
#     return await _allow_access_thread(thread_id, thread_info, invoke_input.user, request)

# threads_router = create_threads_router(
#     get_graph=_get_graph_from_request,
#     allow_access_thread=allow_access_thread,
#     allow_invoke_thread=allow_invoke_thread,
#     # InvokeInputCls=UserInput # TODO: update to use UserInput
#     # TODO: update to pass workflow to checkpointer
# )


@app.get("/llms")
async def get_llms(request: Request) -> list[str]:
    """Get all LLMs available."""
    return LLMProvider.get_llm_names()


@app.get("/workspaces")
async def get_workspaces(request: Request) -> dict[str, WorkspaceMetadata]:
    """Get all workspaces the user has access to."""
    # infer principal from request
    principal = get_viewer(request)
    return {
        k: v.metadata
        for (k, v) in WorkspaceProvider.get_workspaces().items()
        if has_workspace_access(principal, k, app.state.cfg)
    }


@app.get("/workspaces/{workspace}/workflows")
async def get_workflows_for_workspace(
    workspace: str, request: Request
) -> dict[str, WorkflowMetadata]:
    """Get all workflows in a workspace the user has access to.

    Arguments:
        workspace: The id of the workspace to get workflows from.
    """
    # infer principal from request
    principal = get_viewer(request)
    if not has_workspace_access(principal, workspace, app.state.cfg):
        raise HTTPException(status_code=403, detail="Forbidden")
    return {
        k: v.metadata
        for (k, v) in WorkflowProvider.get_workflows().items()
        if v.metadata.workspace == workspace
    }


@app.get("/workspaces/{workspace}/knowledgebases")
async def get_knowledgebases_for_workspace(
    workspace: str, request: Request
) -> dict[str, KnowledgebaseMetadata]:
    """Get all knowledgebases in a workspace the user has access to.

    Arguments:
        workspace: The id of the workspace to get knowledgebases from.
    """
    # infer principal from request
    principal = get_viewer(request)
    if not has_workspace_access(principal, workspace, app.state.cfg):
        raise HTTPException(status_code=403, detail="Forbidden")
    # TODO: no idea how we'll handle this in the future, for now we assume
    # the workspace field is here, injected into the KB by Hydra
    # probably our workspaces will have to have a list of knowledgebases or similar
    return {
        k: v.metadata
        for (k, v) in KnowledgebaseProvider.get_knowledgebases().items()
        # TODO if v.metadata.workspace == workspace
    }


@app.get("/workspaces/{workspace}/threads")
async def get_threads_for_workspace(workspace: str, request: Request):
    """Get all threads in a workspace the user has access to.

    Arguments:
        workspace: The id of the workspace to get threads from.
    """
    # infer principal from request
    principal = get_viewer(request)
    workflows = WorkflowProvider.get_workflows()
    if not has_workspace_access(principal, workspace, app.state.cfg):
        raise HTTPException(status_code=403, detail="Forbidden")
    # FIXME
    return [
        t.dict()
        for t in sorted(
            app.state.threads.values(), key=lambda t: t.creation, reverse=True
        )
        if t.workflow_id in workflows
        and workflows[t.workflow_id].metadata.workspace == workspace
    ]


@app.get("/workflows")
async def get_workflows(request: Request) -> dict[str, WorkflowMetadata]:
    """Get all workflows the user has access to."""
    principal = get_viewer(request)
    return {
        k: v.metadata
        for (k, v) in WorkflowProvider.get_workflows().items()
        if has_workspace_access(principal, v.metadata.workspace, app.state.cfg)
    }


@app.get("/workflow/{workflow_id}")
async def get_workflow_by_id(request: Request, workflow_id: str) -> WorkflowMetadata:
    """Get a workflow by its ID.

    Arguments:
        workflow_id: The id of the workflow to get.
    """
    principal = get_viewer(request)
    workflow = WorkflowProvider.get_workflow(workflow_id)
    if workflow is None:
        raise HTTPException(status_code=404, detail=f"Workflow {workflow_id} not found")
    if not has_workspace_access(principal, workflow.metadata.workspace, app.state.cfg):
        raise HTTPException(status_code=403, detail="Forbidden")
    return workflow.metadata


@app.get("/knowledgebases")
async def get_knowledgebases(request: Request) -> dict[str, KnowledgebaseMetadata]:
    """Get all knowledgebases the user has access to."""
    principal = get_viewer(request)
    # print metadatas beforehand
    for k, m in KnowledgebaseProvider.get_knowledgebases().items():
        print(k, flush=True)
        print(m.metadata.json())
    # TODO: no idea how we'll handle this in the future, for now we assume
    # the workspace field is here, injected into the KB by Hydra
    # probably our workspaces will have to have a list of knowledgebases or similar
    return {
        k: v.metadata
        for (k, v) in KnowledgebaseProvider.get_knowledgebases().items()
        #if has_workspace_access(principal, v.metadata.workspace, app.state.cfg)
    }


@app.get("/knowledgebases/{kb_id}/documents")
async def get_documents(kb_id: str, request: Request) -> dict[str, DocumentMetadata]:
    """Get all documents in a knowledgebase

    Arguments:
        kb_id: The id of the knowledgebase to get documents from.
    """
    kb = KnowledgebaseProvider.get_knowledgebases().get(kb_id, None)
    if kb is None:
        raise HTTPException(status_code=404, detail=f"Knowledgebase {kb_id} not found")
    # TODO: no idea how we'll handle this in the future, for now we assume
    # the workspace field is here, injected into the KB by Hydra
    # probably our workspaces will have to have a list of knowledgebases or similar
    #if not has_workspace_access(
    #    get_viewer(request), kb.metadata.workspace, app.state.cfg
    #):
    #    raise HTTPException(status_code=403, detail="Forbidden")
    return {
        d.metadata["source"]: DocumentMetadata(
            id=d.id if d.id is not None else "MISSING", metadata=d.metadata
        )
        for d in kb.get_documents()
    }


@app.get("/knowledgebases/{kb_id}/tags")
async def get_tags(kb_id: str, request: Request) -> dict[str, str]:
    """Get all tags in a knowledgebase

    Arguments:
        kb_id: The id of the knowledgebase to get tags from.
    """
    kb = KnowledgebaseProvider.get_knowledgebase(kb_id)
    if kb is None:
        raise HTTPException(status_code=404, detail=f"Knowledgebase {kb_id} not found")

    # TODO: no idea how we'll handle this in the future, for now we assume
    # the workspace field is here, injected into the KB by Hydra
    # probably our workspaces will have to have a list of knowledgebases or similar
    #if not has_workspace_access(
    #    get_viewer(request), kb.metadata.workspace, app.state.cfg
    #):
    #    raise HTTPException(status_code=403, detail="Forbidden")
    return kb.tags


@app.get("/assets/{asset_id}")
async def get_asset(asset_id: str):
    """Get an asset by its ID.

    Arguments:
        asset_id: The ID of the asset to get.
    """
    # TODO: user where
    asset = AssetsManager.get_storage().load_binary("veritone_voice", asset_id)
    return StreamingResponse(
        content=BytesIO(asset), media_type="application/octet-stream"
    )


# TODO: use the toolkit for this
@app.get("/history/{workflow}/{thread_id}")
async def get_history(
    workflow: str, thread_id: str, request: Request
) -> list[ChatMessage]:
    """
    Get the history of a thread.

    Arguments:
        workflow: The workflow ID.
        thread_id: The thread ID.
    """
    if thread_id not in app.state.threads:
        raise HTTPException(status_code=404, detail=f"Unknown thread: {thread_id}")

    principal = app.state.threads[thread_id].user

    # check if this user is allowed to see this thread
    assert_viewer_can_assume_identity(request, principal=principal)
    if workflow not in app.state.workflows:
        raise HTTPException(status_code=500, detail=f"Unknown workflow: {workflow}")

    agent: CompiledGraph = app.state.workflows[workflow].get_graph()
    config = RunnableConfig(configurable={"thread_id": thread_id})
    state = await agent.aget_state(config)
    messages = state.values.get("messages", [])

    converted_messages: list[ChatMessage] = []
    for message in messages:
        try:
            chat_message = ChatMessage.from_langchain(message)
            converted_messages.append(chat_message)
        except Exception as e:
            log.error(f"Error parsing message: {e}")
            continue
    return converted_messages


# TODO: use the toolkit for this
@app.get("/threads")
async def get_threads(request: Request, user: str | None = None):
    """Get all threads the user has access to."""
    principal = user or get_viewer(request)

    # allowed to get only own threads
    assert_viewer_can_assume_identity(request, principal=principal)
    return [
        t.dict()
        for t in sorted(
            app.state.threads.values(), key=lambda t: t.creation, reverse=True
        )
        if (t.user == principal if t.user else True)
    ]


@app.get("/threads/app/{app_name}")
async def get_threads_for_app_user(
    request: Request, app_name: str, user: str | None = None
):
    """Get all threads for a given app that the user has access to."""
    principal = user or get_viewer(request)

    assert_viewer_can_assume_identity(request, principal=principal)
    return [
        t.dict()
        for t in sorted(
            app.state.threads.values(), key=lambda t: t.creation, reverse=True
        )
        if (t.user == principal if t.user else True)
        and t.metadata.get("app", "") == app_name
    ]


# TODO: use the toolkit for this
@app.get("/thread/{thread_id}")
async def get_thread_by_id(request: Request, thread_id: str, user: str | None = None):
    """Get a thread by its ID.

    Arguments:
        thread_id: The ID of the thread to get.
    """
    principal = user or get_viewer(request)

    assert_viewer_can_assume_identity(request, principal=principal)
    try:
        return [
            t.dict()
            for t in app.state.threads.values()
            if (t.thread_id == thread_id and (t.user == principal if t.user else True))
        ][0]
    except:
        raise HTTPException(status_code=404, detail="Thread not found")


# TODO: everything from here use the toollkit in future
@app.get("/admin/threads")
async def admin_get_threads(request: Request):
    """Get all threads in the system.

    Requries admin access.
    """
    assert_viewer_is_admin(request)
    return [
        t.dict()
        for t in sorted(
            app.state.threads.values(), key=lambda t: t.creation, reverse=True
        )
    ]


@app.get("/admin/thread/{thread_id}")
async def admin_get_thread_by_id(thread_id: str, request: Request):
    """Get a thread by its ID, independent of the user.
    Requires admin access.

    Arguments:
        thread_id: The ID of the thread to get.
    """
    assert_viewer_is_admin(request)
    try:
        return [
            t.dict() for t in app.state.threads.values() if (t.thread_id == thread_id)
        ][0]
    except:
        raise HTTPException(status_code=404, detail="Thread not found")


@app.get("/feedback/thread/{thread_id}")
async def get_feedback(request: Request, thread_id: str):
    """Get all feedback for a thread.

    Arguments:
        thread_id: The ID of the thread to get feedback for.
    """
    if thread_id not in app.state.threads:
        raise HTTPException(status_code=404, detail=f"Unknown thread: {thread_id}")
    assert_viewer_can_assume_identity(
        request, principal=app.state.threads[thread_id].user
    )
    feedback = [
        f.model_dump(mode="json")
        async for f in app.state.checkpointer.alist_feedback(thread_id=thread_id)
    ]
    return feedback


@app.post("/feedback")
async def feedback(feedback: OldFeedback, request: Request):
    """
    Record feedback for a run of the agent.

    Arguments:
        feedback: The feedback to record.
    """
    if feedback.thread_id not in app.state.threads:
        raise HTTPException(
            status_code=404, detail=f"Unknown thread: {feedback.thread_id}"
        )
    assert_viewer_can_assume_identity(
        request, principal=app.state.threads[feedback.thread_id].user
    )

    # store in database
    try:
        await app.state.checkpointer.aput_feedback(feedback)
        db_status = "success"
    except Exception as e:
        log.error(f"Error storing feedback in database: {e}")
        db_status = "error"

    ## Also store in Langfuse
    ## We don't have the run_id, but need it for Langfuse
    ## The run_id is currently not store in the database.
    # try:
    #     langfuse = Langfuse(
    #         public_key=app.state.cfg.logging.langfuse.public_key,
    #         secret_key=app.state.cfg.logging.langfuse.secret_key,
    #         host=app.state.cfg.logging.langfuse.host,
    #     )
    #     langfuse.score(
    #         trace_id=feedback.run_id,
    #         name=feedback.key,
    #         value=feedback.score,
    #         comment=feedback.kwargs.get("comment", ""),
    #     )
    #     langfuse_status = "success"
    # except Exception as e:
    #     log.error(f"Error storing feedback in Langfuse: {e}")
    #     langfuse_status = "error"

    langfuse_status = "not implemented"

    return {"db_status": db_status, "langfuse_status": langfuse_status}
