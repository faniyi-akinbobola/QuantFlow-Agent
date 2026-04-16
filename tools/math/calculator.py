from langchain.tools import tool
import numexpr


@tool
def calculator(query: str) -> dict:
    """
    Docstring for calculator
    
    :param query: 
    :type query: str
    :return: Description
    :rtype: dict
    """
    try:
        result = numexpr.evaluate(query).item()
        return {
            "expression": query,
            "result": result
        }
    except Exception as e:
        return {f"Error evaluating expression: {e}"}
