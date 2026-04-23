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