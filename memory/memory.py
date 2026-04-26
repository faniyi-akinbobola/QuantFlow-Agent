import aiosqlite
import os
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

# Database file location
DB_PATH = os.path.join(os.path.dirname(__file__), "checkpoints.db")


async def make_checkpointer():
    """Create and return an async SQLite checkpointer."""
    conn = await aiosqlite.connect(DB_PATH)
    saver = AsyncSqliteSaver(conn)
    await saver.setup()
    return saver
