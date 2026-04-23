def tools_used_metric(results):
    """Returns the number of tools used in the results."""
    return sum(len(result.get("tools_used", [])) for result in results)