from graph.state import AgentState
from langchain_core.messages import  SystemMessage
from llm.llm import llm
from langgraph.prebuilt import ToolNode
from llm.prompt import SYSTEM_PROMPT
from tools import (
    search_sec_filings,
    fetch_latest_news,
    get_analyst_recommendations,
    get_company_info,
    get_key_metrics,
    get_financials,
    calculator,
    technical_analysis,
    get_current_price_yahoo,
    get_earnings_history,
    compare_stocks,
)

tools = [
    search_sec_filings,
    fetch_latest_news,
    get_analyst_recommendations,
    get_company_info,
    get_key_metrics,
    get_financials,
    calculator,
    technical_analysis,
    get_current_price_yahoo,
    get_earnings_history,
    compare_stocks,
]

llm_with_tools = llm.bind_tools(tools)


def agent_node(state: AgentState) -> dict:
    """
    Main agent node - LLM analyzes messages and decides next action.
    
    The LLM can either:
    1. Call one or more tools (returns AIMessage with tool_calls)
    2. Respond directly to user (returns AIMessage with content)
    
    Args:
        state: Current agent state with conversation history
        
    Returns:
        Updated state with new AIMessage appended to messages
    """
    messages = state["messages"]

    # Prepend system prompt if not already present
    if not messages or not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + list(messages)

    response = llm_with_tools.invoke(messages)

    return {"messages": [response]}
    

tool_node = ToolNode(tools=tools)   

