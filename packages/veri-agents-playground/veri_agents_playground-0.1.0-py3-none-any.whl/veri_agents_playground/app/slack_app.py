import asyncio
from functools import lru_cache
import os
import logging
import sys
from typing import Any, List, Optional, Tuple

import dotenv
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from veri_agents_playground.client import AgentClient
from veri_agents_playground.schema import ChatMessage, WorkflowMetadata, ThreadInfo


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Slack app init
dotenv.load_dotenv(dotenv.find_dotenv())
app = AsyncApp(token=os.environ.get("SLACK_BOT_TOKEN"))

workflow_name = "veritone_agent"
agent_url = os.getenv("AGENT_URL", "http://localhost")
auth_secret = os.getenv("AUTH_SECRET")
if auth_secret is None:
    raise ValueError("AUTH_SECRET environment variable is not set")
 
agent_client = AgentClient(agent_url, auth_secret, user="mtoman@veritone.com")

user_id = None
bot_id = None


async def initialize_bot():
    # any better option to do this with python asnyc?
    global user_id, bot_id
    auth_results = await app.client.auth_test()
    user_id = auth_results["user_id"]
    bot_id = auth_results["bot_id"]
    logger.info("User ID %s, Bot ID %s", user_id, bot_id)


def bot_mentioned(text: str) -> bool:
    return f"<@{user_id}>" in text


def strip_bot_mention(text: str) -> str:
    return text.replace(f"<@{user_id}>", "").strip()


@lru_cache(maxsize=5)
def get_threads(_agent_client: AgentClient, workflow: str) -> List[ThreadInfo]:
    return [t for t in _agent_client.get_threads() if t.workflow_id == workflow]


async def get_user_email(client, user):
    try:
        user_info = await client.users_info(user=user)
        email = user_info["user"]["profile"][
            "email"
        ]  # Extract email from the user profile
    except Exception:
        email = "slack_dev"
    return email


def handle_artifact(artifact):
    blocks = []
    logger.debug("Got artifact: %s", artifact)
    if artifact.get("type") == "human_selection":
        options = artifact.get("options", [])
        message = artifact.get("message", "Please select one of the following:")
        blocks.append(
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": message,
                },
            }
        )
        for option in options:
            blocks.append(
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"{option}",
                    },
                }
            )

    elif artifact.get("source") == "dmh_show_results":
        asset_ids = artifact.get("asset_ids", [])
        for asset_id in asset_ids:
            vid_link = f"https://commerce.veritone.com/search/asset/{asset_id}"
            logger.debug("Video link: %s", vid_link)
            blocks.append(
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"Video: {vid_link}",
                    },
                }
            )
    elif artifact.get("source") == "veritone_support":
        # show_support_sources(artifact, st)
        pass
    elif artifact.get("type") == "audio":
        # show_audio(artifact, st)
        pass
    return blocks


def build_answer(msg: ChatMessage) -> Optional[Tuple[List[Any], str]]:
    text = []
    blocks = []
    add_blocks = None
    if msg.type == "ai":
        if msg.content:
            text.append(msg.content)
        for tool_call in msg.tool_calls:
            tool_name = tool_call["name"]
            if tool_name == "tts_call":
                text.append("Synthesizing text...")
            elif tool_name == "dmh_video_search":
                text.append(
                    f"Searching for videos in DMH: '{tool_call["args"]["query"]}'..."
                )
            elif tool_name == "veritone_support":
                text.append(
                    f"Searching for support sources on '{tool_call['args']['product']}': '{tool_call['args']['query']}'..."
                )
            elif tool_name == "wikipedia":
                text.append(f"Looking up Wikipedia: '{tool_call['args']['query']}'...")
    elif msg.type == "tool":
        logger.debug("Got a tool message: %s", msg.content)
        if artifact := msg.get_artifact():
            add_blocks = handle_artifact(artifact)

    if len(text) > 0:
        blocks.extend(
            [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "\n".join(text),
                    },
                },
                {
                    "type": "divider",
                },
            ]
        )

    if add_blocks:
        blocks.extend(add_blocks)
    # references = [
    #    (source.title, source.reference, source.content, source.score) for source in answer.sources if source.title != "Summary"
    # ]
    # for ref in sorted(answer.sources, key=lambda x: x.score, reverse=True):
    #     blocks.append(
    #         {
    #             "type": "section",
    #             "text": {
    #                 "type": "mrkdwn",
    #                 # "text": f"*{ref[0]}* ({ref[1]})",
    #                 "text": f"*{ref.title} ({ref.score:.2f})*",
    #             },
    #             "accessory": {
    #                 "type": "button",
    #                 "text": {"type": "plain_text", "emoji": True, "text": "Link"},
    #                 "url": ref.reference,
    #                 "value": "src_link_clicked",
    #             },
    #         }
    #     )
    #     blocks.append(
    #         {
    #             "type": "section",
    #             "text": {
    #                 "type": "mrkdwn",
    #                 "text": f"{ref.content[:80]} ... {ref.content[-80:]}",
    #             },
    #         }
    #     )
    if blocks == []:
        return None

    return blocks, "/n".join(text)


async def answer(text, say, user_id, thread_ts):
    logger.info("Query: %s", text)

    stream = agent_client.astream(
        message=text,
        workflow=workflow_name,
        user=user_id,
        thread_id=thread_ts,
    )

    while msg := await anext(stream, None):
        if isinstance(msg, ChatMessage):
            answer = build_answer(msg)
            if answer:
                await say(blocks=answer[0], text=answer[1], thread_ts=thread_ts)
        elif isinstance(msg, str):
            await say(msg, thread_ts=thread_ts)


@app.event("app_mention")
async def message_mention(event, client, say):
    chat_user_id = event["user"]
    email = await get_user_email(client, chat_user_id)

    await answer(strip_bot_mention(event["text"]), say, email, event["ts"])
    # this means this is a new conversation
    # so after the answer we should refresh our threads cache
    get_threads.cache_clear()


@app.message()
async def handle_message_events(client, body, event, say, logger):
    text = event["text"]
    channel_id = event["channel"]
    threads = get_threads(agent_client, workflow_name)
    thread_dict = {t.thread_id: t.name for t in threads}
    chat_user_id = event["user"]

    # reply in a thread? check if this is a conversation we already know
    if event.get("thread_ts"):
        thread_ts = event["thread_ts"]
        # already handled by app_mention?
        if bot_mentioned(text):
            return
        if thread_ts in thread_dict:
            email = await get_user_email(client, chat_user_id)
            await answer(strip_bot_mention(text), say, email, thread_ts)
        return
    # instant message?
    elif event.get("channel_type", "") == "im":
        await answer(text, say, user_id, event["ts"])
        # this means this is a new conversation
        # so after the answer we should refresh our threads cache
        get_threads.cache_clear()


async def main():
    await initialize_bot()
    handler = AsyncSocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    await handler.start_async()


if __name__ == "__main__":
    asyncio.run(main())
