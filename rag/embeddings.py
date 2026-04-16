from langchain_openai import OpenAIEmbeddings
from utils.loader import load_env_var

MODEL = "text-embedding-3-large"
DIMENSIONS = 3072


def get_embeddings(model: str = MODEL, dimensions: int = DIMENSIONS) -> OpenAIEmbeddings:
    """
    Get OpenAI embeddings instance.
    
    Args:
        model: The OpenAI embedding model to use
        dimensions: The dimensionality of the embeddings
        
    Returns:
        OpenAIEmbeddings instance
    """
    api_key = load_env_var("OPENAI_API_KEY")
    return OpenAIEmbeddings(model=model, dimensions=dimensions, api_key=api_key)