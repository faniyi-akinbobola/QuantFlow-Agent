from graph.state import AgentState
from langchain_core.messages import  SystemMessage
from llm.llm import llm
from langgraph.prebuilt import ToolNode
from llm.prompt import SYSTEM_PROMPT
from openai import RateLimitError
import time
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

    # Retry logic with exponential backoff for rate limits
    max_retries = 5
    base_delay = 2  # Start with 2 seconds
    
    for attempt in range(max_retries):
        try:
            response = llm_with_tools.invoke(messages)
            return {"messages": [response]}
        except RateLimitError as e:
            error_msg = str(e)
            
            # Check if it's a quota exceeded error (don't retry these)
            if "insufficient_quota" in error_msg or "exceeded your current quota" in error_msg:
                print(f"\n OpenAI quota exceeded. Please check your billing at https://platform.openai.com/account/billing")
                raise
            
            # It's a temporary rate limit - retry with backoff
            if attempt == max_retries - 1:
                # Last attempt failed, re-raise the error
                raise
            
            wait_time = base_delay * (2 ** attempt)  # Exponential backoff
            
            # Try to extract the suggested wait time from the error message
            if "Please try again in" in error_msg:
                try:
                    import re
                    match = re.search(r'Please try again in ([\d.]+)s', error_msg)
                    if match:
                        suggested_wait = float(match.group(1))
                        wait_time = max(wait_time, suggested_wait)
                except:
                    pass
            
            print(f" Rate limit hit. Waiting {wait_time:.1f}s before retry {attempt + 1}/{max_retries}...")
            time.sleep(wait_time)
    
    # This should never be reached due to the raise in the loop
    raise RuntimeError("Unexpected state in retry logic")
    

tool_node = ToolNode(tools=tools)   

