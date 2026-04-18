from langgraph.checkpoint.sqlite import SqliteSaver
import os

"""
SQLite-based conversation memory for QuantFlow agent.

Persists conversation history across sessions using a local SQLite database.
Each conversation thread is identified by a unique thread_id.

Usage:
    from graph import app
    from langchain_core.messages import HumanMessage
    
    # Create or resume a conversation
    config = {"configurable": {"thread_id": "user_123"}}
    
    result = app.invoke({
        "messages": [HumanMessage("What's Apple's stock price?")]
    }, config=config)
"""

# Database file location
DB_PATH = os.path.join(os.path.dirname(__file__), "checkpoints.db")

# Create checkpointer
checkpointer = SqliteSaver.from_conn_string(DB_PATH)

# Initialize database tables
checkpointer.setup()