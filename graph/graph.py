from langgraph.graph import StateGraph, END
from graph.state import AgentState
from graph.nodes import agent_node, tool_node
from memory.memory import checkpointer


def should_continue(state: AgentState) -> str:
    """
    Determine if the agent should continue to tools or end.
    
    Args:
        state: Current agent state
        
    Returns:
        "tools" if the agent called tools, END otherwise
    """
    messages = state["messages"]
    last_message = messages[-1]
    
    # If LLM called tools, route to tool node
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    
    # Otherwise, end the conversation
    return END


# Build the graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("agent", agent_node)
workflow.add_node("tools", tool_node)

# Add edges
workflow.set_entry_point("agent")

workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        END: END,
    }
)

workflow.add_edge("tools", "agent")

# Compile the graph
app = workflow.compile(checkpointer=checkpointer)