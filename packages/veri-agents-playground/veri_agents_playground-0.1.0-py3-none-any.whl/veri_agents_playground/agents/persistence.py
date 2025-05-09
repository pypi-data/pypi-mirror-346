import uuid
from os import PathLike
from pathlib import Path
from typing import Optional

from hydra.utils import instantiate
from omegaconf import DictConfig

AssetId = str

class AssetsStorage:
    def save_binary(self, user: str, data: bytes) -> AssetId:
        raise NotImplementedError

    def load_binary(self, user: str, asset_id: AssetId) -> bytes:
        raise NotImplementedError


class AssetsFileStorage(AssetsStorage):
    def __init__(self, location: PathLike | str) -> None:
        self.location = Path(location)

    @classmethod
    def from_config(cls, config: DictConfig) -> "AssetsFileStorage":
        return cls(config.assets_manager.location)

    def generate_uuid(self) -> AssetId:
        return str(uuid.uuid4())

    def save_binary(self, user: str, data: bytes) -> AssetId:
        asset_id = self.generate_uuid()
        asset_dir = self.location / user
        asset_dir.mkdir(parents=True, exist_ok=True)
        asset_path = asset_dir / asset_id
        with asset_path.open("wb") as f:
            f.write(data)
        return asset_id

    def load_binary(self, user: str, asset_id: AssetId) -> bytes:
        asset_path = self.location / user / asset_id
        with asset_path.open("rb") as f:
            return f.read()


# TODO: remove this once we use the toolkit
import aiosqlite
from langgraph.checkpoint.base import SerializerProtocol
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from contextlib import asynccontextmanager
from typing import Any, AsyncIterator, Dict, Optional
from veri_agents_playground.schema import OldFeedback, OldThreadInfo
import json
from langgraph.checkpoint.sqlite.utils import search_where
class AsyncSqliteSaverPlus(AsyncSqliteSaver):
    """Additional functions to also store additional information (e.g workflow ID) for each thread."""

    def __init__(
        self, conn: aiosqlite.Connection, *, serde: SerializerProtocol | None = None
    ):
        super().__init__(conn, serde=serde)

    @classmethod
    @asynccontextmanager
    async def from_conn_string(
        cls, conn_string: str
    ) -> AsyncIterator["AsyncSqliteSaverPlus"]:
        """Create a new AsyncSqliteSaver instance from a connection string.

        Args:
            conn_string (str): The SQLite connection string.

        Yields:
            AsyncSqliteSaver: A new AsyncSqliteSaver instance.
        """
        async with aiosqlite.connect(conn_string) as conn:
            yield AsyncSqliteSaverPlus(conn)

    async def setup(self):
        async with self.lock:
            if self.is_setup:
                return
            if not self.conn.is_alive():
                await self.conn

            async with self.conn.executescript(
                """
                PRAGMA journal_mode=WAL;
                CREATE TABLE IF NOT EXISTS threads (
                    thread_id TEXT NOT NULL PRIMARY KEY,
                    workflow_id TEXT NOT NULL,
                    user TEXT NOT NULL,
                    name TEXT NOT NULL,
                    metadata TEXT NOT NULL DEFAULT '',
                    creation DATE NOT NULL DEFAULT CURRENT_TIMESTAMP
                );
                CREATE TABLE IF NOT EXISTS feedback (
                    feedback_id INTEGER PRIMARY KEY,
                    message_id TEXT NOT NULL,
                    thread_id TEXT NOT NULL,
                    score TEXT NOT NULL,
                    creation DATE NOT NULL DEFAULT CURRENT_TIMESTAMP
                );
            """
            ):
                await self.conn.commit()

        await super().setup()

    async def aput_thread(self, thread_info: OldThreadInfo):
        """Store additional information for each thread."""
        async with self.lock:
            await self.conn.execute(
                "INSERT OR REPLACE INTO threads (thread_id, workflow_id, user, name, metadata, creation) VALUES (?, ?, ?, ?, ?, ?)",
                (
                    thread_info.thread_id,
                    thread_info.workflow_id,
                    thread_info.user,
                    thread_info.name,
                    json.dumps(thread_info.metadata),
                    thread_info.creation,
                ),
            )
            await self.conn.commit()

    async def alist_threads(
        self,
        filters: Optional[Dict[str, Any]] = None,
        limit: Optional[int] = None,
    ) -> AsyncIterator[OldThreadInfo]:
        """List all threads with additional information."""
        await self.setup()
        where, param_values = search_where(None, filters, None)
        query = f"SELECT thread_id, workflow_id, user, name, metadata, creation FROM threads {where} ORDER BY creation DESC"
        if limit:
            query += f" LIMIT {limit}"
        async with self.lock:
            cursor = await self.conn.execute(query, param_values)
            results = await cursor.fetchall()
            for result in results:
                yield OldThreadInfo(
                    thread_id=result[0],
                    workflow_id=result[1],
                    user=result[2],
                    name=result[3],
                    metadata=json.loads(result[4]),
                    creation=result[5],
                )

    async def aput_feedback(self, feedback: OldFeedback):
        """Store user feedback."""
        async with self.lock:
            await self.conn.execute(
                "INSERT OR REPLACE INTO feedback (message_id, thread_id, score, creation) VALUES (?, ?, ?, ?)",
                (
                    feedback.message_id,
                    feedback.thread_id,
                    feedback.score,
                    feedback.creation,
                ),
            )
            await self.conn.commit()

    async def alist_feedback(
        self, thread_id: Optional[str] = None, limit: Optional[int] = None
    ) -> AsyncIterator[OldFeedback]:
        """Get user feedbacks."""
        await self.setup()
        if thread_id is not None:
            where = "WHERE thread_id = ?"
            params = (thread_id,)
        else:
            where = ""
            params = ()
        query = f"SELECT message_id, thread_id, score, creation FROM feedback {where} ORDER BY creation DESC"
        if limit:
            query += f" LIMIT {limit}"
        async with self.lock:
            cursor = await self.conn.execute(query, params)
            results = await cursor.fetchall()
            for result in results:
                yield OldFeedback(
                    message_id=result[0],
                    thread_id=result[1],
                    score=result[2],
                    creation=result[3],
                )
