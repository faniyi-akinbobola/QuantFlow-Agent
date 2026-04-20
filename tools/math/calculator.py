from langchain.tools import tool
import numexpr


@tool
def calculator(query: str) -> str:
    """
    Evaluate mathematical expressions safely.
    
    Supports basic arithmetic: +, -, *, /, **, (), etc.
    
    Args:
        query: Mathematical expression to evaluate (e.g., "2 + 2", "10 * 5")
        
    Returns:
        The result as a string
    """

    try:
        result = numexpr.evaluate(query).item()
        return f"The result of '{query}' is: {result}"
    except Exception as e:
        return f"Error evaluating expression: {e}"