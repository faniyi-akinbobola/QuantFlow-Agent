from langgraph.graph import StateGraph, END
from graph.state import AgentState
from graph.nodes import agent_node, tool_node


def should_continue(state: AgentState) -> str:
    messages = state["messages"]
    last_message = messages[-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return END


# Build the graph
workflow = StateGraph(AgentState)
workflow.add_node("agent", agent_node)
workflow.add_node("tools", tool_node)
workflow.set_entry_point("agent")
workflow.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
workflow.add_edge("tools", "agent")

# Compiled without checkpointer - injected at runtime via config in ui.py
# Note: recursion_limit is set in config during invoke, not compile
app = workflow.compile()
graph = app
