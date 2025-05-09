from typing import Optional, Tuple, Type

from langchain.callbacks.manager import (
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool, ToolException
from pydantic import BaseModel, Field

from veri_agents_playground.agents.providers import KnowledgebaseProvider


class VeritoneSupportQueryInput(BaseModel):
    query: str = Field(description="query to search for documents.")
    # product: Annotated[str, InjectedToolArg] = Field(
    #    description="Which product to search for."
    # )
    product: str = Field(
        description='Which Veritone product to search for.'
    )


class VeritoneSupportQuery(BaseTool):
    name: str = "veritone_support"
    description: str = (
        "Searches for Veritone product documentation. Useful when users are searching for specific information on Veritone products. "
        "Input should be a search query."
    )
    args_schema = VeritoneSupportQueryInput
    response_format: str = "content_and_artifact"  # type: ignore
    handle_tool_errors: bool = True

    num_results: int = 4

    def _run(
        self,
        query: str,
        product: str = "",
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Tuple[list[str], dict]:
        if not product:
            raise ToolException("Product not specified.")
        
        kb = KnowledgebaseProvider.get_knowledgebase("veritone_support")
        if not kb:
            raise ToolException("Knowledgebase veritone_support not found.")
        docs = kb.retrieve(query, limit=self.num_results, product=product)
        return [d.page_content for d in docs], {"items": docs, "type": "document", "source": "veritone_support"}
