def calculate_cost(units, price_per_unit):
    """
    Calculate the total cost based on the number of units and price per unit.

    Args:
        units (float): The number of units consumed.
        price_per_unit (float): The cost per unit.

    Returns:
        float: The total cost.
    """
    total_cost = units * price_per_unit
    return total_cost