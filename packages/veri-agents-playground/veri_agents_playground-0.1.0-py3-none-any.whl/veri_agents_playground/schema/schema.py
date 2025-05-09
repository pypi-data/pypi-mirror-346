from datetime import datetime
from os import PathLike
from typing import Dict, Any, Optional

from pydantic import BaseModel, Field


class DocumentMetadata(BaseModel):
    """Metadata for a document."""

    id: str
    metadata: dict = Field(default={})


class DataSource(BaseModel):
    """Data source for a knowledge base."""

    location: PathLike | str = Field(
        description="Location of the data source, e.g. a file path or URL."
    )
    name: str = Field(
        description="Name of the data source. Can be used for filtering in the knowledgebase and important that document names are unique"
    )
    tags: list[str] = Field(
        default=[],
        description="Tags applied to all documents and chunks of the source, e.g. 'finance'.",
    )
    incremental: bool = Field(
        default=False,
        description="Whether to do incremental indexing of the data source.",
    )


#class KnowledgebaseMetadata(BaseModel):
#     """Metadata for a knowledge base."""

#     name: str
#     description: str
#     workspace: str
#     tags: dict[str, str] = {}
#     llm: str
#     embedding_model: str
#     collection: str
#     doc_summarize: bool = False
#     doc_autotag: bool = False
#     data_sources: list[Dict] = []

#     class Config:
#         extra = "ignore"


class WorkspaceMetadata(BaseModel):
    """Metadata for a workspace."""

    name: str
    description: str


class WorkflowMetadata(BaseModel):
    """Workflow for the agent."""

    name: str
    description: str
    icon: str
    workspace: str
    input_schema: Dict[str, Any] = Field(
        default={}, description="JSON Schema for input arguments to the workflow."
    )
    output_schema: Dict[str, Any] = Field(
        default={},
        description="JSON Schema for output arguments from the workflow. If not given, output is just a string.",
    )


class OldThreadInfo(BaseModel):
    """Information about a single thread."""

    thread_id: str
    workflow_id: str
    name: str
    user: str
    metadata: dict = Field(default={})
    creation: datetime = Field(default_factory=datetime.now)


class OldInvokeInput(BaseModel):
    """Basic user input for the agent."""

    message: str = Field(
        description="User input to the agent.",
        examples=["What is the weather in Tokyo?"],
    )
    app: str = Field(
        description="Application this input is coming from. Can be used to filter threads by application.",
        examples=["veritone_support", "dmh"],
        default="",
    )
    workflow: str = Field(
        description="Workflow to run.",
        examples=["poem_composer"],
    )
    workflow_args: Dict[str, Any] = Field(
        description="Arguments to pass to the workflow.",
        default={},
        examples=[{"kb": "veritone_support"}],
    )
    user: Optional[str] = Field(
        description="A user identifier to validate the user in knowledge bases and other tools.",
        default=None,
        examples=["jjohnson", "ccarlson"],
    )
    thread_id: str = Field(
        description="Thread ID to persist and continue a multi-turn conversation.",
        examples=["847c6285-8fc9-4560-a83f-4e6285809254"],
    )

class OldStreamInput(OldInvokeInput):
    """User input for streaming the agent's response."""

    stream_tokens: bool = Field(
        description="Whether to stream LLM tokens to the client.",
        default=True,
    )


class OldFeedback(BaseModel):
    """Feedback for a run."""

    message_id: str = Field(
        description="Message ID to record feedback for.",
        examples=["847c6285-8fc9-4560-a83f-4e6285809254"],
    )
    thread_id: str = Field(
        description="Thread ID to record feedback for.",
        examples=["847c6285-8fc9-4560-a83f-4e6285809254"],
    )
    score: float = Field(
        description="Feedback score.",
        examples=[0.8],
    )
    kwargs: Dict[str, Any] = Field(
        description="Additional feedback kwargs, passed to LangSmith.",
        default={},
        examples=[{"comment": "In-line human feedback"}],
    )
    creation: datetime = Field(default_factory=datetime.now)
