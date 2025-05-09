import os
import uuid

import requests
import streamlit as st
from veri_agents_playground.client import AgentClient
from veri_agents_playground.schema import (
    OldThreadInfo,
    WorkflowMetadata,
)
from veri_agents_knowledgebase import KnowledgebaseMetadata


@st.cache_data(show_spinner=False)
def get_threads(
    _agent_client: AgentClient, user: str, workflow: str | None = None
) -> list[OldThreadInfo]:
    return [
        t
        for t in _agent_client.get_threads(user)
        if workflow is None or t.workflow_id == workflow
    ]


def clear_chat():
    st.session_state.messages = []
    st.session_state.last_message = None
    # st.rerun()


def get_current_workflow() -> str:
    return st.session_state.get("workflow", "")


def set_current_workflow(str):
    st.session_state.workflow = str


def get_or_create_current_thread_id() -> str:
    if st.session_state.get("thread_id", None) is None:
        st.session_state.thread_id = str(uuid.uuid4())
        get_threads.clear()
    return st.session_state.thread_id


def get_current_thread_id() -> str | None:
    return st.session_state.get("thread_id", None)


def set_current_thread_id(thread_id):
    st.session_state.thread_id = thread_id


def new_thread():
    st.session_state.thread_id = None
    clear_chat()


def get_ai_avatar():
    path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(path, "images/ChatBot_Avatar_700x700_transparent.png")


def get_human_avatar():
    return ":material/face:"


def get_agent_client() -> AgentClient:
    agent_url = os.getenv("AGENT_URL", "http://localhost")
    auth_secret = os.getenv("AUTH_SECRET")
    if auth_secret is None:
        st.error("Authentication error")
        raise ValueError("AUTH_SECRET environment variable is not set")
    user = get_user()
    return AgentClient(agent_url, auth_secret=auth_secret, user=user)


@st.cache_data(show_spinner=False, hash_funcs={AgentClient: lambda ac: ac.cache_hash()})
def get_workflows(agent_client: AgentClient) -> dict[str, WorkflowMetadata]:
    return agent_client.get_workflows()


@st.cache_data(show_spinner=False, hash_funcs={AgentClient: lambda ac: ac.cache_hash()})
def get_knowledgebases(agent_client: AgentClient) -> dict[str, KnowledgebaseMetadata]:
    return agent_client.get_knowledgebases()

@st.cache_data(show_spinner=False, ttl=60)
def get_documents(_client, knowledge_base_id):
    return _client.get_documents(knowledge_base_id)

@st.cache_data(show_spinner=False, ttl=60)
def get_llms(_client):
    return _client.get_llms()

@st.cache_data(show_spinner=False, ttl=60)
def get_tags(_client, knowledge_base_id):
    return _client.get_tags(knowledge_base_id)

@st.cache_data(show_spinner=False)
def get_audio_asset(_agent_client: AgentClient, audio_asset_id: str) -> bytes | None:
    url = get_agent_client().get_asset_url(audio_asset_id)
    r = requests.get(url, timeout=30)
    if r.status_code == 200:
        return r.content
    return None


def get_user() -> str:
    user_email = st.context.headers.get("X-User-Email", "nobody@veritone.com")
    # user_id = st.context.headers.get("X-User-Id", "dummy-user-id")
    # user_name = st.context.headers.get("X-User-Name", "Dummy User")
    # user_isadmin = st.context.headers.get("X-User-Isadmin", "0")

    return user_email


# DMH related functions, those should probably be abstracted somewhere else
# perhaps this could be part of the schema?
def find_dmh_items(artifacts, asset_ids):
    items = []
    for artifact in artifacts:
        if artifact.get("source") in ("dmh_search_results", "dmh_show_results"):
            for item in artifact.get("items", []):
                if str(item.get("assetId")) in asset_ids:
                    items.append(item)
    return items
