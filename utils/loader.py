import os
from dotenv import load_dotenv
from typing import List

load_dotenv()

def load_env_var(key_name: str, default: str = None) -> str:
    """
    Load environment variable with optional default value.
    
    Args:
        key_name: The name of the environment variable to load
        default: Default value if variable is not found (optional)
        
    Returns:
        The value of the environment variable
        
    Raises:
        ValueError: If the variable is not found and no default is provided
    """
    value = os.getenv(key_name, default)
    if not value:
        raise ValueError(f"{key_name} not found in environment variables.")
    return value


def validate_required_env_vars(required_vars: List[str]) -> bool:
    """
    Validate that all required environment variables are set.
    
    Args:
        required_vars: List of required environment variable names
        
    Returns:
        True if all variables are set
        
    Raises:
        ValueError: If any required variable is missing
    """
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        raise ValueError(
            f" Missing required environment variables: {', '.join(missing_vars)}\n"
            f"Please add them to your .env file."
        )
    
    return True