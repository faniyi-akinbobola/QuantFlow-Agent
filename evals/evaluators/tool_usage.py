def tool_usage_evaluator(results, dataset):
    """
    Evaluates whether the correct tools were used.
    
    Supports two modes:
    - exact match: used tools must exactly match expected tools
    - contains: used tools must contain all expected tools (can have more)
    
    Args:
        results (list): List of dicts with 'tools_used' key
        dataset (list): List of dicts with 'expected_tools' key and optional 'mode' key
    
    Returns:
        float: Percentage of correct tool usage (0-100)
    """

    correct = 0

    for result, example in zip(results, dataset):
        used = set(result.get("tools_used", []))
        expected = set(example.get("expected_tools", []))
        mode = example.get("mode", "exact")  # "exact" or "contains"
        
        if mode == "contains":
            # Check if all expected tools are present (can have extras)
            if expected.issubset(used):
                correct += 1
        else:
            # Exact match required
            if used == expected:
                correct += 1

    return correct / len(dataset) * 100 if dataset else 0