from typing import Optional, Tuple, Type

from langchain.callbacks.manager import CallbackManagerForToolRun
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool, InjectedToolArg, ToolException
from langchain_core.messages import ToolMessage

class HumanSelectionInput(BaseModel):
    options: list[str] = Field(
        description="List of options to present to the human for selection."
    )


class HumanSelection(BaseTool):
    name: str = "human_selection"
    description: str = "Ask the human to select from a list of options. Useful when the agent needs the human to make a choice."
    args_schema = HumanSelectionInput
    response_format: str = "content_and_artifact"  # type: ignore
    handle_tool_errors: bool = True
    message: str = "Please select an option."

    def _run(
        self,
        options: list[str],
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Tuple[str, dict]:
        return f"Showing options: {options}", {
            "type": "human_selection",
            "message": self.message,
            "options": options,
        }


class HumanSelectionFixedOptions(BaseTool):
    name: str = "human_selection_f"
    description: str = "Ask the human to select from a list of options. Useful when the agent needs the human to make a choice."
    response_format: str = "content_and_artifact"  # type: ignore
    handle_tool_errors: bool = True
    options: list[str] = []
    message: str = "Please select an option."

    def _run(
        self,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Tuple[str, dict]:
        return "Showing options.", {
            "type": "human_selection",
            "message": self.message,
            "options": self.options,
        }


def shall_wait_for_human(self, state):
    messages = state["messages"]
    last_message = messages[-1]
    if (
        isinstance(last_message, ToolMessage)
        and last_message.name is not None
        and last_message.name.startswith("human_")
    ):
        return "end"
    else:
        return "continue"

