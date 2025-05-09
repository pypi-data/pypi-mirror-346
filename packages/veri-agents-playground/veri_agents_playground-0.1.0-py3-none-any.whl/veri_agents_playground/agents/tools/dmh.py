import logging
import os
import traceback
from typing import Optional, Tuple, Type

import requests
from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.tools import BaseTool, ToolException
from pydantic import BaseModel, Field

log = logging.getLogger(__name__)


class DMHVideoSearchInput(BaseModel):
    """Input for the DMHSearch tool."""

    query: str = Field(
        description="query to search for videos in Veritone Digital Media Hub (DMH)"
    )

    num_results: int = Field(
        description="Number of results to return",
        default=3,
    )


class DMHVideoSearch(BaseTool):
    """Tool that searches the Veritone DMH."""

    name: str = "dmh_video_search"
    description: str = (
        "Searches for Videos in the Veritone Digital Media Hub (DMH). "
        "Useful when users are searching for videos on a specific topic that are managed by Veritone. "
        "Input should be a search query."
    )
    args_schema = DMHVideoSearchInput
    response_format: str = "content_and_artifact"  # type: ignore
    handle_tool_errors: bool = True
    dmh_api_key: str
    dmh_api_base_url: str
    dmh_api_num_results: int = 3
    dmh_search_filter: str = ""
    max_videos: int = 10 

    def get_rendition_url(
        self, asset_id: str, use_type: str = "clipPreview", timeout: int = 30
    ) -> Optional[str]:
        r = requests.get(
            url=f"{self.dmh_api_base_url}/renditionType/{asset_id}/?useType={use_type}&api_key={self.dmh_api_key}",
            headers={"accept": "application/json"},
            timeout=timeout,
        )
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            log.error(
                "Fetching rendition URLs for asset id %s resulted in an error:\n%s",
                asset_id,
                traceback.format_exc(),
            )
            return None
        url = r.json().get("url", None)
        if url is None:
            return None
        return "https:" + url

    def search(self, query: str, num_results: int = 1) -> Optional[dict]:
        url = f"{self.dmh_api_base_url}/search"
        r = requests.get(
            url,
            params={
                "api_key": self.dmh_api_key,
                "q": f"{query} {self.dmh_search_filter}",
                "n": min(num_results, self.max_videos) * 5,  # TODO: hack, get more than needed, need filter to get videos with rendition url
                "i": 0,
            },
            timeout=30,
        )
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            log.error(
                "Search resulted in an error:\n%s\n\nThe request data was:\n%s",
                traceback.format_exc(),
                query,
            )
            return None
        return r.json()

    def _run(
        self,
        query: str,
        num_results: int = 1,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Tuple[str, dict]:
        """Search for DMH videos."""
        try:
            search_results = self.search(query, num_results)
            if search_results is None:
                raise ToolException("Could not find any videos for the query: " + query)
            if "items" not in search_results or len(search_results["items"]) == 0:
                return f"No videos found for query: {query}", search_results
            search_results["type"] = "video"
            search_results["source"] = "dmh_search_results"
            llm_results = []
            for item in search_results["items"]:
                title, description = "", ""
                assetId = item["assetId"]
                url = self.get_rendition_url(assetId)
                if url is None:
                    #  TODO: do we want to remove this from the search results?
                    continue
                item["url"] = url
                item["type"] = "video"
                for mdata in item["metaData"]:
                    if mdata["name"] == "Title":
                        title = mdata["value"]
                    if mdata["name"] == "Description":
                        description = mdata["value"]
                llm_results.append(
                    f"Asset ID: {assetId} | Title: {title} | Description: {description}"
                )
                if len(llm_results) >= num_results:
                    break
            if len(llm_results) == 0:
                return f"No videos found for query: {query}", search_results
            # filter all items that don't have an url
            search_results["items"] = [
                item for item in search_results["items"] if "url" in item
            ]
            return "\n".join(llm_results), search_results
        except Exception as e:
            log.error("Error in DMHVideoSearch: %s", e)
            raise ToolException("Could not find any videos for the query: " + query)


class DMHVideoSearchShowResultsInput(BaseModel):
    """Input for the DMHVideoSearchShowResults tool."""

    asset_ids: list[str] = Field(
        description="List of Asset IDs of videos in the Veritone Digital Media Hub (DMH). Only use Asset IDs you previously retrieved with the video search tool."
    )


class DMHVideoSearchShowResults(BaseTool):
    name: str = "dmh_show_results"
    description: str = (
        "Shows a list of videos found in the Veritone Digital Media Hub (DMH) to the user."
        "Input should be a list of asset IDs previously retrieved with the video search tool."
    )
    args_schema = DMHVideoSearchShowResultsInput
    response_format: str = "content_and_artifact"  # type: ignore

    def _run(
        self,
        asset_ids: list[str],
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Tuple[str, dict]:
        return f"Showing videos with asset IDs: {asset_ids}", {
            "type": "video",
            "source": "dmh_show_results",
            "asset_ids": asset_ids,
        }


if __name__ == "__main__":
    # test the tool
    tool = DMHVideoSearch(
        dmh_api_base_url="https://crxextapi.pd.dmh.veritone.com/assets-api/v1",
        dmh_api_key=os.environ["DMH_API_KEY"],
    )
    ret = tool.invoke(
        {
            "name": "dmh_video_search",
            "args": {"query": "serena williams"},
            "id": "123",
            "type": "tool_call",
        }
    )
    print(ret)

    ret2 = tool.invoke({"query": "serena williams"})
    print("------")
    print(ret2)
