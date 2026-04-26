from collections import Counter

def total_tools_used(results):
    """
    total number of tools used across all queries

    :param results: Describe the expected format of results, e.g., a list of dicts with "tools_used" key
    :return: The total number of tools used across all queries
    """
    return sum(len(r.get("tools_used", [])) for r in results)

def avg_tools_per_query(results):
    """
    average number of tools used per query

    :param results: Describe the expected format of results, e.g., a list of dicts with "tools_used" key
    :return: The average number of tools used per query
    """
    return (
        sum(len(r.get("tools_used", [])) for r in results) / len(results)
        if results else 0
    )

def tool_usage_distribution(results):
    """
    distribution of tool usage across all queries, e.g., how many times each tool was used

    :param results: Describe the expected format of results, e.g., a list of dicts with "tools_used" key
    :return: A dictionary mapping tool names to their usage count across all queries
    """
    counter = Counter()
    for r in results:
        counter.update(r.get("tools_used", []))
    return dict(counter)

def overuse_rate(results, threshold=3):
    """
    % of queries that used too many tools

    :param results: Describe the expected format of results, e.g., a list of dicts with "tools_used" key
    :param threshold: The number of tools above which we consider it "overuse"
    :return: The percentage of queries that used more than the threshold number of tools
    """
    overused = sum(1 for r in results if len(r.get("tools_used", [])) > threshold)
    return (overused / len(results)) * 100 if results else 0