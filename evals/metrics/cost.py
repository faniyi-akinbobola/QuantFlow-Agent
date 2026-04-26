def calculate_cost(units_used, cost_per_unit):
    """
    Calculate the total cost based on units used and cost per unit.

    Args:
        units_used (float): The number of units used.
        cost_per_unit (float): The cost per unit.

    Returns:
        float: The total cost.
    """
    return units_used * cost_per_unit


def calculate_llm_cost(prompt_tokens, completion_tokens, model="gpt-4o-mini"):
    """
    Calculate LLM API cost based on token usage.
    
    Args:
        prompt_tokens (int): Number of input tokens
        completion_tokens (int): Number of output tokens
        model (str): Model name (default: gpt-4o-mini)
    
    Returns:
        float: Total cost in USD
    """
    # Pricing as of 2024 (per 1M tokens)
    pricing = {
        "gpt-4o-mini": {"input": 0.150, "output": 0.600},
        "gpt-4o": {"input": 2.50, "output": 10.00},
        "gpt-4-turbo": {"input": 10.00, "output": 30.00},
        "gpt-3.5-turbo": {"input": 0.50, "output": 1.50},
    }
    
    if model not in pricing:
        raise ValueError(f"Unknown model: {model}")
    
    input_cost = (prompt_tokens / 1_000_000) * pricing[model]["input"]
    output_cost = (completion_tokens / 1_000_000) * pricing[model]["output"]
    
    return input_cost + output_cost


def aggregate_costs(results):
    """
    Calculate total and average cost across multiple results.
    
    Args:
        results (list): List of dicts with 'cost' key
    
    Returns:
        dict: Total cost, average cost, and cost statistics
    """
    costs = [r.get("cost", 0) for r in results]
    
    if not costs:
        return {"total": 0, "average": 0, "min": 0, "max": 0}
    
    return {
        "total": sum(costs),
        "average": sum(costs) / len(costs),
        "min": min(costs),
        "max": max(costs),
    }