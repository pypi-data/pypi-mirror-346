import json
import logging
from typing import Any, AsyncGenerator, Generator

import aiohttp
import requests

from veri_agents_api.fastapi.thread import ChatMessage
from veri_agents_knowledgebase import KnowledgebaseMetadata

from veri_agents_playground.schema import (
    DocumentMetadata,
    OldFeedback,
    OldStreamInput,
    OldThreadInfo,
    OldInvokeInput,
    WorkflowMetadata,
    WorkspaceMetadata,
)

log = logging.getLogger(__name__)


class AgentClient:
    """Client for interacting with the agent service."""

    def __init__(self, base_url, auth_secret: str, user: str | None = None):
        """
        Initialize the client.

        Args:
            base_url (str): The base URL of the agent service.
            auth_secret (str): An authentication secret to use for the agent, can be either a global secret, then a user has to be provided, or an aiWare token.
            user (str, optional): A user ID to use for the agent, only used if the auth secret is sent as well (so for example not when coming from aiWare user auth)
        """
        self.base_url = base_url
        self.auth_secret = auth_secret
        self.user = user

    def cache_hash(self) -> str:
        """Return a hash of the client configuration."""
        return f"{self.base_url}/{self.auth_secret}/{self.user}"

    def get_asset_url(self, asset_id: str) -> str:
        """Get the URL for an asset by ID."""
        return f"{self.base_url}/assets/{asset_id}"

    @property
    def _headers(self):
        headers = {}
        headers["Authorization"] = f"Bearer {self.auth_secret}"
        if self.user:
            headers["X-User-Id"] = self.user
        return headers

    async def ainvoke(
        self,
        message: str,
        workflow: str,
        user: str,
        thread_id: str,
        app: str = "",
        workflow_args={},
    ) -> ChatMessage:
        """
        Invoke the agent asynchronously. Only the final message is returned.

        Args:
            message (str): The message to send to the agent
            workflow (str): The workflow to use for the agent
            user (str): A user ID to use for the agent
            thread_id (str): Thread ID for continuing a conversation

        Returns:
            AnyMessage: The response from the agent
        """
        async with aiohttp.ClientSession() as session:
            request = OldInvokeInput(
                message=message,
                user=user,
                thread_id=thread_id,
                workflow=workflow,
                app=app,
                workflow_args=workflow_args,
            )
            async with session.post(
                f"{self.base_url}/invoke", json=request.dict(), headers=self._headers
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return ChatMessage.model_validate(result)
                else:
                    raise Exception(
                        f"Error: {response.status} - {await response.text()}"
                    )

    def invoke(
        self,
        message: str,
        workflow: str,
        user: str,
        thread_id: str,
        app: str = "",
        workflow_args: dict[str, Any] = {},
    ) -> ChatMessage:
        """
        Invoke the agent synchronously. Only the final message is returned.

        Args:
            message (str): The message to send to the agent
            workflow (str): The workflow to use for the agent
            user (str): A user ID to use for the agent
            thread_id (str): Thread ID for continuing a conversation

        Returns:
            ChatMessage: The response from the agent
        """
        request = OldInvokeInput(
            message=message,
            user=user,
            thread_id=thread_id,
            workflow=workflow,
            app=app,
            workflow_args=workflow_args,
        )
        response = requests.post(
            f"{self.base_url}/invoke",
            json=request.dict(),
            headers=self._headers,
            timeout=60,
        )
        if response.status_code == 200:
            return ChatMessage.model_validate(response.json())
        else:
            raise requests.exceptions.HTTPError(
                f"Error: {response.status_code} - {response.text}"
            )

    def _parse_stream_line(self, line: str) -> ChatMessage | str | None:
        line = line.decode("utf-8").strip()
        if line.startswith("data: "):
            data = line[6:]
            if data == "[DONE]":
                return None
            try:
                parsed = json.loads(data)
            except Exception as e:
                raise Exception(f"Error JSON parsing message from server: {e}")
            match parsed["type"]:
                case "message":
                    # Convert the JSON formatted message to an AnyMessage
                    try:
                        return ChatMessage.model_validate(parsed["content"])
                    except Exception as e:
                        raise Exception(f"Server returned invalid message: {e}")
                case "token":
                    # Yield the str token directly
                    return parsed["content"]
                case "error":
                    raise Exception(parsed["content"])
        return ""

    def stream(
        self,
        message: str,
        workflow: str,
        user: str,
        thread_id: str,
        app: str = "",
        stream_tokens: bool = True,
        workflow_args: dict[str, Any] = {},
    ) -> Generator[ChatMessage | str, None, None]:
        """
        Stream the agent's response synchronously.

        Each intermediate message of the agent process is yielded as a ChatMessage.
        If stream_tokens is True (the default value), the response will also yield
        content tokens from streaming users as they are generated.

        Args:
            message (str): The message to send to the agent
            workflow (str): The workflow to use for the agent
            user (str): A user ID to use for the agent
            thread_id (str): Thread ID for continuing a conversation
            stream_tokens (bool, optional): Stream tokens as they are generated
                Default: True

        Returns:
            Generator[ChatMessage | str, None, None]: The response from the agent
        """
        request = OldStreamInput(
            message=message,
            user=user,
            app=app,
            thread_id=thread_id,
            workflow=workflow,
            stream_tokens=stream_tokens,
            workflow_args=workflow_args,
        )
        response = requests.post(
            f"{self.base_url}/stream",
            json=request.dict(),
            headers=self._headers,
            stream=True,
            timeout=60,
        )
        if response.status_code != 200:
            raise Exception(f"Error: {response.status_code} - {response.text}")

        for line in response.iter_lines():
            if line:
                parsed = self._parse_stream_line(line)
                if parsed is None:
                    break
                yield parsed

    async def astream(
        self,
        message: str,
        workflow: str,
        user: str,
        thread_id: str,
        app: str = "",
        stream_tokens: bool = True,
        workflow_args: dict[str, Any] = {},
    ) -> AsyncGenerator[ChatMessage | str, None]:
        """
        Stream the agent's response asynchronously.

        Each intermediate message of the agent process is yielded as an AnyMessage.
        If stream_tokens is True (the default value), the response will also yield
        content tokens from streaming usersas they are generated.

        Args:
            message (str): The message to send to the agent
            workflow (str): The workflow to use for the agent
            user (str): A user ID to use for the agent
            thread_id (str): Thread ID for continuing a conversation
            stream_tokens (bool, optional): Stream tokens as they are generated
                Default: True

        Returns:
            AsyncGenerator[ChatMessage | str, None]: The response from the agent
        """
        async with aiohttp.ClientSession(
            max_field_size=600_000, max_line_size=600_000, read_bufsize=64_000_000
        ) as session:
            request = OldStreamInput(
                message=message,
                user=user,
                thread_id=thread_id,
                workflow=workflow,
                app=app,
                stream_tokens=stream_tokens,
                workflow_args=workflow_args,
            )
            async with session.post(
                f"{self.base_url}/stream", json=request.dict(), headers=self._headers
            ) as response:
                if response.status != 200:
                    raise Exception(
                        f"Error: {response.status} - {await response.text()}"
                    )
                # Parse incoming events with the SSE protocol
                async for line in response.content:
                    if line.decode("utf-8").strip():
                        parsed = self._parse_stream_line(line)
                        if parsed is None:
                            break
                        yield parsed

    def create_feedback(
        self,
        message_id: str,
        thread_id: str,
        score: float,
        kwargs: dict[str, Any] = {},
    ):
        """
        Create a feedback record for a run.
        """
        feedback = OldFeedback(
            message_id=message_id, thread_id=thread_id, score=score, kwargs=kwargs
        )
        response = requests.post(
            f"{self.base_url}/feedback",
            json=feedback.model_dump(mode="json"),
            headers=self._headers,
            timeout=60,
        )

        if response.status_code != 200:
            raise Exception(f"Error: {response.status_code} - {response.text}")

        return feedback

    def request(self, resource: str, method: str = "GET", **kwargs):
        """
        Make a request to the agent service.
        """
        response = requests.request(
            method,
            f"{self.base_url}/{resource}",
            headers=self._headers,
            timeout=90,
            **kwargs,
        )

        if response.status_code != 200:
            raise Exception(f"Error: {response.status_code} - {response.text}")
        return response

    def get_workspaces(self) -> dict[str, WorkspaceMetadata]:
        """Retrieve workspaces available from the agent service."""
        response = self.request("workspaces")
        wsdict = response.json()
        return {k: WorkspaceMetadata.model_validate(v) for k, v in wsdict.items()}

    def get_workspace_workflows(self, workspace: str) -> dict[str, WorkflowMetadata]:
        """Retrieve workflows available from a workspace."""
        response = self.request(f"workspaces/{workspace}/workflows")
        wfdict = response.json()
        return {k: WorkflowMetadata.model_validate(v) for k, v in wfdict.items()}

    def get_workspace_knowledgebases(
        self, workspace: str
    ) -> dict[str, KnowledgebaseMetadata]:
        """Retrieve knowledgebases available from a workspace."""
        response = self.request(f"workspaces/{workspace}/knowledgebases")
        kbdict = response.json()
        return {k: KnowledgebaseMetadata.model_validate(v) for k, v in kbdict.items()}

    def get_workspace_threads(self, workspace: str) -> list[OldThreadInfo]:
        """Retrieve all threads for a given workspace."""
        response = self.request(f"workspaces/{workspace}/threads")
        return [OldThreadInfo.model_validate(t) for t in response.json()]

    def get_workflows(self) -> dict[str, WorkflowMetadata]:
        """Retrieve workflows available from the agent service."""
        response = self.request("workflows")
        wfdict = response.json()
        return {k: WorkflowMetadata.model_validate(v) for k, v in wfdict.items()}

    def get_knowledgebases(self) -> dict[str, KnowledgebaseMetadata]:
        """Retrieve knowledgebases available from the agent service."""
        response = self.request("knowledgebases")
        kbdict = response.json()
        return {k: KnowledgebaseMetadata.model_validate(v) for k, v in kbdict.items()}

    def get_documents(self, kb_id: str) -> dict[str, DocumentMetadata]:
        """Retrieve all documents from the agent service."""
        response = self.request(f"knowledgebases/{kb_id}/documents")
        docdict = response.json()
        return {k: DocumentMetadata.model_validate(v) for k, v in docdict.items()}

    def get_tags(self, kb_id: str) -> dict[str, str]:
        """Retrieve all tags for a given knowledgebase from the agent service."""
        response = self.request(f"knowledgebases/{kb_id}/tags")
        tagdict = response.json()
        return tagdict

    def get_llms(self) -> list[str]:
        """Retrieve all available LLMs from the agent service."""
        response = self.request("llms")
        return response.json()

    def get_threads(self, user: str | None = None) -> list[OldThreadInfo]:
        """Retrieve all threads for a given user."""
        if user:
            url = f"threads?user={user}"
        else:
            url = "admin/threads"

        response = self.request(url)
        return [OldThreadInfo.model_validate(t) for t in response.json()]

    def get_history(self, workflow: str, thread_id: str) -> list[ChatMessage]:
        """Retrieve the history of a thread."""
        response = self.request(f"history/{workflow}/{thread_id}")
        return [ChatMessage.model_validate(m) for m in response.json()]

    def get_feedback(self, thread_id: str) -> list[OldFeedback]:
        """Retrieve feedback for a thread."""
        url = f"{self.base_url}/feedback/thread/{thread_id}"
        response = requests.get(url, headers=self._headers, timeout=60)
        if response.status_code == 200:
            return [OldFeedback.model_validate(f) for f in response.json()]
        if response.status_code == 404:
            return []
        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")
