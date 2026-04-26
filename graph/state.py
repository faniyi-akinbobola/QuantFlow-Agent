from typing import Annotated, Sequence
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage


class AgentState(TypedDict):
    """State for the QuantFlow financial agent."""
    
    messages: Annotated[Sequence[BaseMessage], add_messages]
    """Full conversation history with automatic message deduplication."""

