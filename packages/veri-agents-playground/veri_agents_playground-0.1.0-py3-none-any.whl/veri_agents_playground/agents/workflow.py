"""Workflow definitions for agents. System users can call (agentic) workflows to perform tasks."""

import logging
from typing import Optional
from uuid import uuid4, UUID

from pydantic import BaseModel, Field
from hydra.utils import instantiate
from omegaconf import DictConfig, OmegaConf
from veri_agents_playground.agents.access import AccessControl, AccessControlNone, AuthorizationError
from veri_agents_playground.schema.schema import WorkflowMetadata
from langchain_core.runnables.config import RunnableConfig
from langgraph.graph.graph import CompiledGraph

log = logging.getLogger(__name__)


class Workflow:
    """A workflow is a graph of tasks.
    This is the general abstraction, actual implementations are done in the workflows package.
    Workflows are generally implemented using LangGraph graphs.
    """

    workflows: dict[str, "Workflow"] = {}

    def __init__(
        self,
        name: str,
        description: str,
        workspace: str = "public",
        icon: str = ":material/settings:",
        input_schema: Optional[type[BaseModel]] = None,
        output_schema: Optional[type[BaseModel]] = None,
        access_control: Optional[AccessControl] = None,
    ):
        self._metadata = WorkflowMetadata(
            name=name,
            workspace=workspace,
            description=description,
            icon=icon,
            input_schema=input_schema.model_json_schema() if input_schema else {},
            output_schema=output_schema.model_json_schema() if output_schema else {},
        )
        self.access_control = access_control or AccessControlNone()

    def get_graph(self):
        """Get the graph of the workflow."""
        raise NotImplementedError

    @property
    def metadata(self):
        """Get the metadata for the workflow."""
        return self._metadata

    @property
    def input_schema(self):
        """Get the input schema for the workflow."""
        return self.metadata.input_schema

    @property
    def output_schema(self):
        """Get the output schema for the workflow."""
        return self.metadata.output_schema

    @staticmethod
    def get_user_from_config(config: RunnableConfig) -> Optional[str]:
        """Get the user for this workflow."""
        return config["configurable"].get("user") # pyright: ignore[reportTypedDictNotRequiredAccess]

    @staticmethod
    def get_thread_id_from_config(config: RunnableConfig) -> Optional[str]:
        """Get the thread ID for this workflow."""
        return config["configurable"].get("thread_id") # pyright: ignore[reportTypedDictNotRequiredAccess]

    @staticmethod
    def get_args_from_config(config: RunnableConfig, arg: str) -> Optional[str]:
        """Get the arguments for this workflow."""
        return config["configurable"].get("args", {}).get(arg) # pyright: ignore[reportTypedDictNotRequiredAccess]


    async def ainvoke(
        self,
        message: str,
        args: dict = {},
        thread_id: Optional[str] = None,
        app: Optional[str] = None,
        user: Optional[str] = None,
        run_id: Optional[UUID] = None,
    ):  # -> ChatMessage: # TODO: discuss this
        """
        Async Invoke the workflow given a specific input to retrieve a final response.

        Use thread_id to persist and continue a multi-turn conversation when a checkpointer is set.
        """
        if not self.access_control.has_workspace_access(user, self.metadata.workspace):
            raise AuthorizationError(
                f"User {user} is not allowed to access workflow {self.metadata.name}."
            )

        agent: CompiledGraph = self.get_graph()

        if run_id is None:
            run_id = uuid4()

        input_message = ChatMessage(type="human", content=message)
        input = {"messages": [input_message.to_langchain()]}
        run_config = RunnableConfig(
            configurable={
                "thread_id": thread_id,
                "user": user,
                "args": args,
            },
            run_id=run_id,
        )

        # TODO: check how we do this best without having to check the DB every time
        # store this thread in the database if a new one
        # if user_input.thread_id not in app.state.threads:
        #    thread_info = ThreadInfo(
        #        thread_id=user_input.thread_id,
        #        user=principal,
        #        workflow_id=user_input.workflow,
        #        name=user_input.message[:50],
        #        metadata={"app": user_input.app},
        #    )
        #    app.state.threads[user_input.thread_id] = thread_info
        #    await agent.checkpointer.aput_thread(thread_info)
        # langfuse_handler = CallbackHandler(
        #    public_key=app.state.cfg.logging.langfuse.public_key,
        #    secret_key=app.state.cfg.logging.langfuse.secret_key,
        #    host=app.state.cfg.logging.langfuse.host,
        #    user_id=principal,
        #    session_id=user_input.thread_id,
        #    trace_name=user_input.message[:50],
        # )
        # kwargs["config"]["callbacks"] = [langfuse_handler]
        # kwargs["config"]["configurable"]["workflow_id"] = user_input.workflow

        # TODO: decide if we want to return ChatMessage or the LangChain response
        response = await agent.ainvoke(input=input, config=run_config)
        return response
        # output = ChatMessage.from_langchain(response["messages"][-1])
        # output.run_id = str(run_id)
        # return output

    def set_checkpointer(self, checkpointer):
        """Set the checkpointer for the workflow."""
        self.get_graph().checkpointer = checkpointer
