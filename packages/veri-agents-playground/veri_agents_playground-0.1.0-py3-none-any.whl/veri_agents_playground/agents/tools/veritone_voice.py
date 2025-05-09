import logging
from typing import Optional, Tuple, Type

import requests
from langchain.callbacks.manager import CallbackManagerForToolRun
from langchain_core.tools import BaseTool, ToolException
from pydantic import BaseModel, Field

from veri_agents_playground.agents.providers.persistence import AssetsManager

log = logging.getLogger(__name__)

class TTSCallInput(BaseModel):
    text: str = Field(
        description="The text to synthesize."
    )


class TTSCall(BaseTool):
    name: str = "tts_call"
    description: str = "Synthesize text to speech. Useful if the user wants to generate speech output given some text."
    args_schema = TTSCallInput
    response_format: str = "content_and_artifact"  # type: ignore
    handle_tool_errors: bool = True
    veritone_voice_url: str
    veritone_voice_token: str
    #veritone_voice_speaker_id: str = "0d8c979c-3da5-43ad-a2b1-16b99dbdff74"  # TODO: this should be controlled by... the user?
    #veritone_voice_speaker_id: str = "2ab84d7a-23db-4947-b751-946ecda1ac70" # claire
    veritone_voice_speaker_id: str = "27096814-c8ba-4816-bb70-cb84cc6ad38d" # malik
    veritone_voice_timeout: int = 30

    def _run(
        self,
        text: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Tuple[str, dict]:
        response = requests.post(
            url=f"{self.veritone_voice_url}",
            headers={
                "Authorization": f"Bearer {self.veritone_voice_token}",
                "Content-Type": "application/json",
            },
            json={
                "ssml": f"<speak version=\"3.0\" xmlns=\"https://voice2.veritone.com/api/ssml/base\" xml:lang=\"en-US\" xmlns:veritone=\"https://voice2.veritone.com/api/ssml/extensions\"><voice id=\"{self.veritone_voice_speaker_id}\" title=\"Einstein\" version=\"\" lang=\"en-US\">{text}</voice></speak>",
                "audioOutput": "riff-48khz-16bit-mono-pcm",
            },
            timeout=self.veritone_voice_timeout
        )
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            log.error("Failed to synthesize text to speech. Response: %s", response.text)
            raise ToolException("Unable to synthesize")

        # store results in with assetsmanager and only return the asset id
        # TODO: user ID should be passed in, how can we provide this to all tools?
        asset_id = AssetsManager.get_storage().save_binary("veritone_voice", response.content)

        return "Synthesized text", { 
            "type": "audio",
            "source": self.name,
            "audio": asset_id # base64.b64encode(response.content).decode('utf-8'),
        }

