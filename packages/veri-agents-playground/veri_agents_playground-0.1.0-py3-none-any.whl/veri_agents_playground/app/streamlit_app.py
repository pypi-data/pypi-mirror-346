import asyncio
import json
import os
import sys
from typing import Any, AsyncGenerator

import streamlit as st

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from veri_agents_playground.client import AgentClient
from veri_agents_playground.schema import OldThreadInfo, WorkflowMetadata
from veri_agents_api.fastapi.thread import ChatMessage
from streamlit_utils import (
    find_dmh_items,
    get_agent_client,
    get_ai_avatar,
    get_audio_asset,
    get_current_thread_id,
    get_current_workflow,
    get_human_avatar,
    get_or_create_current_thread_id,
    get_threads,
    get_user,
    get_workflows,
    get_knowledgebases,
    new_thread,
    set_current_thread_id,
    set_current_workflow,
    get_documents,
    get_llms,
    get_tags,
)

APP_TITLE = "Veritone Agents"
APP_NAME = "veritone_agents"
current_artifacts: list[dict] = []


def create_thread_page(thread: OldThreadInfo, workflow: WorkflowMetadata | None = None):
    """Creates a streamlit page for a specific thread"""
    return st.Page(
        page=lambda wid=thread.workflow_id, tid=thread.thread_id: asyncio.run(
            show_chat(wid, tid)
        ),
        title=f"{thread.name} ({thread.creation.strftime('%x')})",
        url_path=f"thread_{thread.thread_id}",
        icon=workflow.icon if workflow else ":material/chat:",
    )


@st.dialog("Thread history", width="large")
def show_thread_dialog(threads):
    """Shows a dialog with the thread history"""
    for t in threads[::-1]:
        but_col, name_col, date_col = st.columns([0.15, 0.55, 0.3])
        with but_col:
            if st.button(
                "Open",
                use_container_width=True,
                key=f"dialog-button-{t.thread_id}",
            ):
                set_current_thread_id(t.thread_id)
                history = get_agent_client().get_history(
                    get_current_workflow(), get_or_create_current_thread_id()
                )
                st.session_state.messages = history
                st.session_state.last_message = history[-1] if history else None
                st.rerun()
        with name_col:
            st.write(t.name)
        with date_col:
            st.write(t.creation.strftime("%c"))


def show_documents_bar_plot(documents, field):
    products = [v.metadata[field] for v in documents.values() if field in v.metadata]
    if not products:
        return
    product_counts = {p: products.count(p) for p in set(products)}
    st.bar_chart(product_counts)



async def show_knowledge_base(knowledge_base_id: str):
    # st.title(knowledge_base_id)
    client = get_agent_client()
    documents = get_documents(client, knowledge_base_id)
    metadata_list = [v.metadata for v in documents.values()]
    selected = st.dataframe(
        metadata_list,
        column_config={
            "source": None,
            "name": "Name",
            "title": "Title",
            "product": "Product",
            "link": st.column_config.LinkColumn("Article URL"),
            "last_updated": st.column_config.DatetimeColumn("Updated"),
            "location": None,
            "doc_location": None,
        },
        on_select="rerun",
        selection_mode="single-row",
        # selection_mode="multi-row",
        use_container_width=True,
    )
    st.write(f"Number of documents: {len(documents)}")
    if selected:
        rows = selected["selection"]["rows"]  # type: ignore
        for row in rows:
            st.divider()
            for col in metadata_list[row]:
                st.write(f"**{col}**: {metadata_list[row][col]}")
    show_documents_bar_plot(documents, "product")


async def show_workflow_parameter_input(
    agent_client: AgentClient, workflow_metadata: WorkflowMetadata
) -> dict[str, Any]:
    input_properties = workflow_metadata.input_schema.get("properties", {})
    input_args = {}
    # st.write(input_properties)
    if "knowledgebase" in input_properties:
        available_knowledgebases = get_knowledgebases(agent_client)
        input_args["knowledgebase"] = st.selectbox(
            "Knowledgebase",
            options=list(available_knowledgebases.keys()),
        )
    if "tags_any" in input_properties and "tags_all" in input_properties:
        kb = input_args.get("knowledgebase")
        tags = get_tags(agent_client, kb)
        col1, col2 = st.columns(2)
        if kb:
            input_args["tags_any"] = col1.multiselect(
                "Tags (any of)",
                default=None,
                placeholder="All tags",
                options=tags,
            )
            input_args["tags_all"] = col2.multiselect(
                "Tags (all of)",
                default=None,
                placeholder="None",
                options=tags,
            )
        else:
            input_args["tags_any"] = col1.text_input(
                "Tags",
                placeholder="Enter tags (comma-separated)",
            )
            input_args["tags_all"] = col2.text_input(
                "Tags",
                placeholder="Enter tags (comma-separated)",
            )
    if "documents" in input_properties:
        kb = input_args.get("knowledgebase")
        if kb:
            docs = get_documents(agent_client, kb)
            input_args["documents"] = st.multiselect(
                "Documents",
                default=None,
                placeholder="All documents",
                options=list(docs.keys()),
            )
        else:
            input_args["documents"] = st.text_input(
                "Documents",
                placeholder="Enter document ID",
            )
    if "llm" in input_properties:
        llms = get_llms(agent_client)
        input_args["llm"] = st.selectbox(
            "LLM", placeholder="Default LLM", options=llms, index=None
        )
    return input_args


async def show_chat(workflow: str, thread_id: str | None):
    agent_client = get_agent_client()
    available_workflows = get_workflows(agent_client)
    input_args = {}

    # new thread created?
    if thread_id is None:
        new_thread()
        set_current_workflow(workflow)
        thread_id = get_or_create_current_thread_id()
        st.session_state.new_thread = True
        st.switch_page(
            create_thread_page(
                OldThreadInfo(
                    thread_id=thread_id,
                    name="New conversation",
                    workflow_id=workflow,
                    user=get_user(),
                ),
                available_workflows.get(workflow),
            )
        )
    # different thread selected?
    elif thread_id and get_current_thread_id() != thread_id:
        set_current_thread_id(thread_id)
        set_current_workflow(workflow)
        history = agent_client.get_history(workflow, thread_id)
        st.session_state.messages = history
        st.session_state.last_message = history[-1] if history else None
        st.session_state.new_thread = False

    if st.get_option("client.toolbarMode") != "minimal":
        st.set_option("client.toolbarMode", "minimal")
        await asyncio.sleep(0.1)
        st.rerun()

    use_streaming = True
    workflow_metadata = available_workflows.get(get_current_workflow())
    if workflow_metadata:
        st.title(f"{workflow_metadata.name}")
    else:
        st.title(get_current_workflow())

    # Draw existing messages
    if "messages" not in st.session_state:
        st.session_state.messages = []
    messages: list[ChatMessage] = st.session_state.messages

    if len(messages) == 0:
        with st.chat_message("ai", avatar=get_ai_avatar()):
            if workflow_metadata:
                st.write(workflow_metadata.description)

    # draw_messages() expects an async iterator over messages
    async def amessage_iter():
        for m in messages:
            yield m

    feedback = agent_client.get_feedback(thread_id)
    feedback.sort(key=lambda f: f.creation)
    feedback_scores = {f.message_id: f.score for f in feedback}

    await draw_messages(amessage_iter(), feedback_scores, workflow_metadata=workflow_metadata)

    # Generate new message if the user provided new input
    if "message_to_send" in st.session_state:
        input_text = st.session_state.message_to_send
        st.session_state.message_to_send = None
    else:
        if workflow_metadata:
            input_args = await show_workflow_parameter_input(
                agent_client, workflow_metadata
            )

        input_text = st.chat_input()

    if input_text:
        # a fresh new message is being sent, refresh the thread list next time
        if not messages:
            get_threads.clear()
        messages.append(ChatMessage(type="human", content=input_text))
        st.chat_message("human", avatar=get_human_avatar()).write(input_text)
        agent_client = agent_client
        if use_streaming:
            stream = agent_client.astream(
                message=input_text,
                workflow=get_current_workflow(),
                user=get_user(),
                thread_id=thread_id,
                app=APP_NAME,
                # stream_tokens=False,  # TODO: could almost work now
                workflow_args=input_args,
            )
            await draw_messages(stream, feedback_scores, is_new=True)
        else:
            response = await agent_client.ainvoke(
                message=input_text,
                workflow=get_current_workflow(),
                user=get_user(),
                thread_id=thread_id,
                app=APP_NAME,
                workflow_args=input_args,
            )
            messages.append(response)
            st.chat_message("ai", avatar=get_ai_avatar()).write(response.content)
        st.rerun()  # Clear stale containers


def selection_clicked(option):
    """User clicked on a selection option, for example picked a product.
    Store the selection in session state to send it to the agent."""
    st.session_state.message_to_send = option


def show_human_selection(artifact, container):
    """Show a list of options for the user to select from in the chat."""
    options = artifact.get("options", [])
    message = artifact.get("message", "Select from the following options:")
    if not options:
        return
    st.write(message)
    for option, col in zip(options, container.columns(len(options))):
        col.button(
            f"{option}",
            on_click=selection_clicked,
            args=(option,),
            use_container_width=True,
        )


def show_support_sources(artifact, container):
    """Show a list of support sources for the user to choose from."""
    artifact_items = artifact.get("items", [])
    if not artifact_items:
        return
    for item, column in zip(artifact_items, container.columns(len(artifact_items))):
        source_meta = item.get("metadata", {})
        link = source_meta.get("link", "")
        column.link_button(
            f"{source_meta.get('title', 'Link')}",
            link,
            use_container_width=True,
            disabled=(not link.startswith("http")),
        )


def show_knowledge_sources(artifact, container):
    """Show a list of knowledge sources for the user to choose from."""
    artifact_items = artifact.get("items", [])
    if not artifact_items:
        return
    sources = set()
    headings = {}
    container.write("**Sources:**")
    for item in artifact_items:
        source_meta = item.get("metadata", {})
        #st.write(source_meta)
        source = source_meta['source']
        sources.add(source)
        if source not in headings:
            headings[source] = []
        try:
            headings[source].append(f"Page: {source_meta['doc_items'][0]['prov'][0]['page_no']}:  {source_meta.get('headings', [])[0]}")
        except Exception:
            pass
    #for source, column in zip(sources, container.columns(len(artifact_items))):
    #    column.write(source)
    mkdown = ""
    for source in sources:
        mkdown += f"- {source}\n"
        for heading in headings.get(source, []):
            mkdown += f"  - {heading}\n"
    container.markdown(mkdown)
    container.divider()


def show_entities(artifact, container):
    """Show extracted entities from the agent."""
    entities = artifact.get("entities", {})
    if not entities:
        return
    for documents in entities:
        container.write(f"**{documents}**")
        for entity in entities[documents]:
            container.write(f"{entity}: {', '.join(entities[documents][entity])}")
        container.divider()


def show_dmh_search_results(current_artifacts, artifact):
    """Show search results from DMH."""
    items = []
    # show the results the agent told us to show
    if artifact.get("source") == "dmh_show_results":
        asset_ids = artifact.get("asset_ids", [])
        if len(asset_ids) > 0:
            items = find_dmh_items(current_artifacts, asset_ids)
    # show search results, this is only interesting for debugging the agent
    # elif artifact.get("source") == "dmh_search_results":
    #    items = artifact.get("items", [])

    if len(items) == 0:
        return
    for item, col in zip(items, st.columns(len(items))):
        titles = [
            i.get("value") for i in item.get("metaData", []) if i.get("name") == "Title"
        ]
        descriptions = [
            i.get("value")
            for i in item.get("metaData", [])
            if i.get("name") == "Description"
        ]
        col.video(item.get("url", ""))
        if titles:
            col.caption(f"{titles[0][:100]}")
        if descriptions:
            col.caption(f"{descriptions[0][:100]}")
        if assetId := item.get("assetId"):
            col.caption(
                f"[View in DMH](https://commerce.veritone.com/search/asset/{assetId})"
            )


def show_audio(artifact, container):
    """Show an audio player for the user to listen to."""
    audio_asset_id = artifact.get("audio")
    if audio_asset_id:
        audio_data = get_audio_asset(get_agent_client(), audio_asset_id)
        if audio_data:
            container.audio(audio_data, format="audio/wav")


def extract_artifact(tool_result) -> dict | None:
    """Extract artifacts from a tool result."""
    if (
        "data" in tool_result.original
        and "artifact" in tool_result.original["data"]
        and tool_result.original["data"]["artifact"]
    ):
        return tool_result.original["data"]["artifact"]
    else:
        return None


def handle_artifacts(artifacts):
    """Handle artifacts returned by the agent."""
    if artifacts:
        for artifact in artifacts:
            current_artifacts.append(artifact)
            if artifact.get("type") == "human_selection":
                show_human_selection(artifact, st)
            elif artifact.get("source") == "dmh_show_results":
                show_dmh_search_results(current_artifacts, artifact)
            elif artifact.get("source") == "veritone_support":
                show_support_sources(artifact, st)
            elif artifact.get("source") == "knowledgebase":
                show_knowledge_sources(artifact, st)
            elif artifact.get("type") == "audio":
                show_audio(artifact, st)
            elif artifact.get("source") == "extracted_entities":
                show_entities(artifact, st)


async def draw_messages(
    messages_agen: AsyncGenerator[ChatMessage | str, None],
    feedback: dict[str, float],
    is_new=False,
    workflow_metadata: WorkflowMetadata | None = None,
):
    """
    Draws a set of chat messages - either replaying existing messages
    or streaming new ones.

    This function has additional logic to handle streaming tokens and tool calls.
    - Use a placeholder container to render streaming tokens as they arrive.
    - Use a status container to render tool calls. Track the tool inputs and outputs
      and update the status container accordingly.

    The function also needs to track the last message container in session state
    since later messages can draw to the same container.

    Args:
        messages_aiter: An async iterator over messages to draw.
        feedback: A dictionary of feedback scores for some messages.
        is_new: Whether the messages are new or not.
    """

    # Keep track of the last message container
    last_message_type = None
    st.session_state.last_message = None

    # Placeholder for intermediate streaming tokens
    streaming_content = ""
    streaming_placeholder = None

    progress_bar = st.progress(0, text="Thinking...")
    progress = 0
    # Iterate over the messages and draw them
    while msg := await anext(messages_agen, None):
        if progress < 90:
            progress += 10
        progress_bar.progress(progress, text="Thinking...")
        # str message represents an intermediate token being streamed
        if isinstance(msg, str):
            # If placeholder is empty, this is the first token of a new message
            # being streamed. We need to do setup.
            if not streaming_placeholder:
                if last_message_type != "ai":
                    last_message_type = "ai"
                    st.session_state.last_message = st.chat_message(
                        "ai", avatar=get_ai_avatar()
                    )
                with st.session_state.last_message:
                    streaming_placeholder = st.empty()

            streaming_content += msg
            streaming_placeholder.write(streaming_content)
            continue
        if not isinstance(msg, ChatMessage):
            st.error(f"Unexpected message type: {type(msg)}")
            st.write(msg)
            st.stop()
        match msg.type:
            # A message from the user, the easiest case
            case "human":
                last_message_type = "human"
                st.chat_message("human", avatar=get_human_avatar()).write(msg.content)

            # A message from the agent is the most complex case, since we need to
            # handle streaming tokens and tool calls.
            case "ai":
                # If we're rendering new messages, store the message in session state
                if is_new:
                    st.session_state.messages.append(msg)

                # If the last message type was not AI, create a new chat message
                if last_message_type != "ai":
                    last_message_type = "ai"
                    st.session_state.last_message = st.chat_message(
                        "ai", avatar=get_ai_avatar()
                    )

                with st.session_state.last_message:
                    # If the message has content, write it out.
                    # Reset the streaming variables to prepare for the next message.
                    if msg.content:
                        if isinstance(msg.content, str):
                            text = msg.content
                        elif isinstance(msg.content, list):
                            text = ""
                            for t in msg.content:
                                if t.get("type", "") == "text":
                                    text += t.get("text", "")
                        # check if text is a structured output
                        entities = None
                        if workflow_metadata and "content" in workflow_metadata.output_schema.get("properties", {}):
                            json_content = json.loads(text)
                            entities = json_content.get("entities", {})
                            text = json_content.get("content", "")
                        
                        if streaming_placeholder:
                            streaming_placeholder.write(text)
                            streaming_placeholder.write(entities)
                            streaming_content = ""
                            streaming_placeholder = None
                        else:
                            # st.write(msg.content)
                            st.write(text)
                            if entities:
                                st.write(entities)
                        message_id = msg.original["data"]["id"]
                        score = feedback.get(message_id)
                        handle_feedback(message_id, score)

                    artifacts = []
                    if msg.tool_calls:
                        # Create a status container for each tool call and store the
                        # status container by ID to ensure results are mapped to the
                        # correct status container.
                        # call_results = {}
                        # for tool_call in msg.tool_calls:
                        #     status = st.status(
                        #         f"""Tool Call: {tool_call["name"]}""",
                        #         state="running" if is_new else "complete",
                        #     )
                        #     status.write("Input:")
                        #     status.write(tool_call["args"])
                        #     call_results[tool_call["id"]] = status

                        # Expect one ToolMessage for each tool call.
                        # for _ in range(len(call_results)):
                        for tool_call in msg.tool_calls:
                            tool_result: ChatMessage = await anext(messages_agen)
                            if not tool_result.type == "tool":
                                st.error(
                                    f"Unexpected ChatMessage type: {tool_result.type}"
                                )
                                st.stop()

                            # Record the message if it's new, and update the correct
                            # status container with the result
                            if is_new:
                                st.session_state.messages.append(tool_result)

                            # status = call_results[tool_result.tool_call_id]
                            # status.write("Output:")
                            # status.write(tool_result.content)
                            # status.write("Original:")
                            # status.write(tool_result.original)
                            # status.update(state="complete")

                            tool_name = tool_call["name"]
                            if tool_name == "tts_call":
                                st.write("Synthesizing text...")
                            elif tool_name == "dmh_video_search":
                                st.write(
                                    f"Searching for videos in DMH: '{tool_call['args']['query']}'..."
                                )
                            elif tool_name == "veritone_support":
                                st.write(
                                    f"Searching for support sources on '{tool_call['args']['product']}': '{tool_call['args']['query']}'..."
                                )
                            elif tool_name.startswith("kb_retrieve_"):
                                tool_args = tool_call["args"]
                                tagged = ""
                                if "tag_all_filters" in tool_args:
                                    tagged = f", in documents with tags: {', '.join(tool_args['tag_all_filters'])}"
                                elif "tag_any_filters" in tool_args:
                                    tagged = f", in documents with any of the following tags: {', '.join(tool_args['tag_any_filters'])}"
                                idx = (
                                    17
                                    if tool_name.startswith("kb_retrieve_tags")
                                    else 12
                                )
                                st.write(
                                    f"Searching in knowledgebase '{tool_name[idx:]}': '{tool_args.get('query')}' {tagged}."
                                )
                                st.divider()
                            elif tool_name == "wikipedia":
                                st.write(
                                    f"Looking up Wikipedia: '{tool_call['args']['query']}'..."
                                )
                            elif tool_name.startswith("aiware_"):
                                st.write("Querying aiWARE...")

                            # See if artifacts are available
                            if art := extract_artifact(tool_result):
                                artifacts.append(art)
                    # Artifacts from tool results
                    handle_artifacts(artifacts)
            # a tool result that didn't come with a tool call
            case "tool":
                if is_new:
                    st.session_state.messages.append(msg)
                if art := extract_artifact(msg):
                    handle_artifacts([art])
            # In case of an unexpected message type, log an error and stop
            case _:
                st.error(f"Unexpected ChatMessage type: {msg.type}")
                st.write(msg)
                st.stop()
    progress_bar.empty()


def store_feedback(message_id: str):
    """Stores feedback in the backend."""
    key = f"feedback_{message_id}"
    score = st.session_state.get(key)
    if score is None:
        return
    normalized_score = (score + 1) / 5.0
    agent_client = get_agent_client()
    agent_client.create_feedback(
        message_id=message_id,
        thread_id=get_current_thread_id() or "",
        score=normalized_score,
        kwargs=dict(
            comment="In-line human feedback",
        ),
    )
    st.toast("Feedback recorded", icon=":material/reviews:")


def handle_feedback(message_id: str, score: float):
    """Draws a feedback widget and records feedback from the user."""
    key = f"feedback_{message_id}"
    if score is not None:
        old_feedback = int(round(score * 5 - 1))
        st.session_state[key] = old_feedback
    st.feedback("stars", key=key, on_change=store_feedback, args=(message_id,))


def navigation():
    """Show the main navigation page."""
    agent_client = get_agent_client()
    st.set_page_config(
        page_title=APP_TITLE,
        # page_icon=get_ai_avatar(),  # APP_ICON,
        menu_items={},
        layout="wide",
    )

    # - Knowledge
    available_knowledgebases = get_knowledgebases(agent_client)
    knowledge_pages = []
    for kb_id, kb in available_knowledgebases.items():
        knowledge_pages.append(
            st.Page(
                page=lambda kbid=kb_id: asyncio.run(show_knowledge_base(kbid)),
                title=kb.name,
                url_path=f"knowledge_{kb_id}",
                icon=":material/library_books:",
            )
        )

    # - Workflows
    available_workflows = get_workflows(agent_client)
    if get_current_workflow() is None:
        set_current_workflow("veritone_agent")

    workflow_pages = []
    for workflow_id, workflow in available_workflows.items():
        workflow_pages.append(
            st.Page(
                page=lambda wid=workflow_id: asyncio.run(show_chat(wid, None)),
                title=workflow.name,
                url_path=f"workflow_{workflow_id}",
                icon=workflow.icon,
            )
        )

    # - Threads
    threads = get_threads(agent_client, get_user(), None)
    current_thread_id = get_current_thread_id()
    thread_pages = []

    # they opened up a new thread
    if st.session_state.get("new_thread", False):
        # Let's see if the thread meanwhile ended up in the DB and has a name then switch over
        if current_thread_id:
            current_thread = next(
                (thread for thread in threads if thread.thread_id == current_thread_id),
                None,
            )
            if current_thread:
                st.session_state.new_thread = False
                st.switch_page(
                    create_thread_page(
                        current_thread,
                        available_workflows.get(current_thread.workflow_id),
                    )
                )
        # otherwise stay in the "new thread" mode
        thread_pages.append(
            create_thread_page(
                OldThreadInfo(
                    thread_id=get_current_thread_id() or "none",
                    name="New conversation",
                    workflow_id=get_current_workflow(),
                    user=get_user(),
                ),
                available_workflows.get(get_current_workflow()),
            )
        )

    # add thread history
    for thread in threads[:30]:
        thread_pages.append(
            create_thread_page(thread, available_workflows.get(thread.workflow_id))
        )

    pg = st.navigation(
        {
            "New conversation": workflow_pages,
            "Knowledge": knowledge_pages,
            "History": thread_pages,
        },
    )
    pg.run()


if __name__ == "__main__":
    # asyncio.run(main())
    # asyncio.run(navigation())
    navigation()
