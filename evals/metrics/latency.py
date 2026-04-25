import statistics


def calculate_latency(start_time, end_time):
    """
    Calculate latency in seconds.

    Args:
        start_time (float): The start time in seconds.
        end_time (float): The end time in seconds.

    Returns:
        float: The latency in seconds.
    """
    latency = end_time - start_time
    return latency


def aggregate_latencies(results):
    """
    Calculate latency statistics across multiple results.
    
    Args:
        results (list): List of dicts with 'latency' key (in seconds)
    
    Returns:
        dict: Latency statistics including mean, median, p50, p95, p99
    """
    latencies = [r.get("latency", 0) for r in results]
    
    if not latencies:
        return {
            "mean": 0,
            "median": 0,
            "min": 0,
            "max": 0,
            "p50": 0,
            "p95": 0,
            "p99": 0,
        }
    
    sorted_latencies = sorted(latencies)
    
    return {
        "mean": statistics.mean(latencies),
        "median": statistics.median(latencies),
        "min": min(latencies),
        "max": max(latencies),
        "p50": percentile(sorted_latencies, 50),
        "p95": percentile(sorted_latencies, 95),
        "p99": percentile(sorted_latencies, 99),
    }


def percentile(sorted_data, percent):
    """
    Calculate percentile from sorted data.
    
    Args:
        sorted_data (list): Sorted list of numbers
        percent (float): Percentile to calculate (0-100)
    
    Returns:
        float: Value at the given percentile
    """
    if not sorted_data:
        return 0
    
    k = (len(sorted_data) - 1) * (percent / 100)
    f = int(k)
    c = f + 1
    
    if c >= len(sorted_data):
        return sorted_data[-1]
    
    d0 = sorted_data[f] * (c - k)
    d1 = sorted_data[c] * (k - f)
    
    return d0 + d1