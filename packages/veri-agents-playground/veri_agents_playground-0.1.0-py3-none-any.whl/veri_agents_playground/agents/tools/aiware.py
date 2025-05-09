import requests
import logging
from typing import Optional, Tuple, Type, cast

from langchain_core.tools import BaseTool, ToolException, InjectedToolArg
from typing_extensions import Annotated
from pydantic import BaseModel, Field
from datetime import datetime

log = logging.getLogger(__name__)


def filter_none_values(data) -> dict | list:
    if isinstance(data, dict):
        return {k: filter_none_values(v) for k, v in data.items() if v is not None}
    elif isinstance(data, list):
        return [filter_none_values(item) for item in data]
    return data


class AiWareToolInput(BaseModel):
    """Input for the aiWARE tool."""

    gql_query: str = Field(
        description="GraphQL query to execute against Veritone aiWARE."
    )
    # aiware_api_key: Annotated[Optional[str], InjectedToolArg] = Field(
    #    description="Possibly injected aiWARE API key."
    # )


class AiWareTool(BaseTool):
    """Generic aiWARE GraphQL tool."""

    name: str = "aiware_tool"
    description: str = "Performs GraphQL calls to Veritone aiWARE. Use this tool if you have no other, more specialized aiWARE tool. Before using this tool, pull the schema using the aiware_tool_schema tool. Use as few output arguments as possible."
    args_schema: Type[BaseModel] = AiWareToolInput
    response_format: str = "content_and_artifact"  # type: ignore
    handle_tool_errors: bool = True
    aiware_api_key: Optional[str] = None
    aiware_url: Optional[str] = None
    allow_mutation: bool = False
    schema_cache: dict[str, list | dict] = {}

    # TODO: use gql instead?
    def _run_query(self, gql_query: str, aiware_api_key: Optional[str]) -> dict:
        """Run the aiWARE GraphQL query."""

        # TODO: hack :)
        if not self.allow_mutation and "mutation" in gql_query:
            raise ToolException("Mutation not supported.")

        aiware_api_key = aiware_api_key or self.aiware_api_key
        if not aiware_api_key:
            raise ToolException("aiWARE API key not set.")
        if not self.aiware_url:
            raise ToolException("aiWARE URL not set.")

        headers = {
            "Authorization": f"Bearer {aiware_api_key}",
            "Content-Type": "application/json",
        }
        payload = {"query": gql_query}

        response = requests.post(
            self.aiware_url,
            json=payload,
            headers=headers,
        )
        if response.status_code != 200:
            raise ToolException(f"Error: {response.status_code} - {response.text}")

        return response.json()

    def _run(
        self,
        gql_query: str,
        # aiware_api_key: Annotated[Optional[str], InjectedToolArg]
    ) -> Tuple[str, dict]:
        """Run the aiWARE GraphQL query."""
        aiware_api_key = None
        result = self._run_query(gql_query, aiware_api_key)
        return str(result), {"items": result, "type": "json", "source": "aiware"}


class AiWareToolSchemaInput(BaseModel):
    # TODO: aiware api key, perhaps which catgory of fields to pull
    pass


class AiWareSchemaTool(AiWareTool):
    """Tool to get aiWARE schema."""

    name: str = "aiware_tool_schema"
    description: str = "Get aiWARE GraphQL schema. Use this tool to get the schema of the aiWARE GraphQL API."
    args_schema: Type[BaseModel] = AiWareToolSchemaInput

    def get_schema(self, aiware_api_key: str) -> list | dict:
        result = self._run_query(
            gql_query="""
            query IntrospectionQuery {
            __schema {
                types {
                name
                kind
                description
                fields {
                    name
                    description
                    args {
                    name
                    description
                    }
                    type {
                    name
                    description
                    kind
                    fields {
                        name
                        description
                        type {
                        name
                        description
                        }
                    }
                    }
                }
                }
            }
            }
            """,
            aiware_api_key=aiware_api_key,
        )
        types = result["data"]["__schema"]["types"]
        queries = [t for t in types if t["name"] == "Query"]
        filtered_fields = filter_none_values(queries[0]["fields"] if queries else [])
        return filtered_fields

    def _run(self) -> Tuple[str, dict]:
        result = self.get_schema(self.aiware_api_key)
        # TODO: this is too big to stream as artifact
        return str(result), {"items": "", "type": "json", "source": "aiware"}


class AiWareGetTDOsCreatedDuringInput(BaseModel):
    """Input for the aiWARE TDOsCreatedDuring tool."""

    start_time: str = Field(
        description="Start time for the query. Format: YYYY-MM-DDTHH:MM:SSZ. If the time part is not provided, it defaults to 00:00:00."
    )
    end_time: str = Field(
        description="End time for the query. Format: YYYY-MM-DDTHH:MM:SSZ. If the time part is not provided, it defaults to 00:00:00."
    )
    # aiware_api_key: Annotated[Optional[str], InjectedToolArg] = Field(
    #     description="Possibly injected aiWARE API key."
    # )


class AiWareGetTDOsCreatedDuringTool(AiWareTool):
    """Tool to get TDOs created during a specific time range."""

    name: str = "aiware_td_created_during"
    description: str = (
        "Get aiWARE TDOs (Temporal Data Objects) created during a specific time range. "
        "Input should be a start and end time."
    )
    args_schema: Type[BaseModel] = AiWareGetTDOsCreatedDuringInput

    def _run(self, start_time: str, end_time: str) -> Tuple[str, dict]:
        query = f"""
            query {{ temporalDataObjects(
                dateTimeFilter: {{
                fromDateTime: "{start_time}",
                toDateTime: "{end_time}",
                field: createdDateTime
                }} 
            ) {{
                records {{
                id
                name
                startDateTime
                stopDateTime
                organization {{
                    id
                }}
                }}
              }}
            }}
        """
        result = self._run_query(query, self.aiware_api_key)
        return str(result), {"items": result, "type": "json", "source": "aiware"}


class AiWareCreateTDOWithAssetInput(BaseModel):
    """Input for the aiWARE Create TDO with Asset tool."""

    name: str = Field(
        description="Name of the TDO to create. For example 'Sushi preparation'."
    )
    asset_uri: str = Field(
        description="URI of the asset to create a TDO for. For example an URL to a video"
    )
    # aiware_api_key: Annotated[Optional[str], InjectedToolArg] = Field(
    #     description="Possibly injected aiWARE API key."
    # )


class AiWareCreateTDOWithAssetTool(AiWareTool):
    """Tool to create a TDO with an asset."""

    name: str = "aiware_create_tdo_with_asset"
    description: str = "Create a TDO (Temporal Data Object) with an asset. This allows to ingest assets like media objects, videos etc. into aiWARE. Use this tool if the user asks you to ingest some media element like a video. Tell the user the TDO ID after you're done."
    args_schema: Type[BaseModel] = AiWareCreateTDOWithAssetInput
    allow_mutation: bool = True
    parent_folder_id: str

    def _run(self, asset_uri: str, name: str) -> Tuple[str, dict]:
        query = f"""
        mutation createTDOWithAsset {{
            createTDOWithAsset(
                input: {{
                updateStopDateTimeFromAsset: true,
                contentType: "video/mp4",
                assetType: "media",
                addToIndex: true,
                name: "{name}",
                startDateTime: "{datetime.now().isoformat()}",
                uri: "{asset_uri}",
                parentFolderId: "{self.parent_folder_id}",
                }}
            )
            {{
                id
                status
            }}
            }}
        """
        result = self._run_query(query, self.aiware_api_key)
        return str(result), {"items": result, "type": "json", "source": "aiware"}
