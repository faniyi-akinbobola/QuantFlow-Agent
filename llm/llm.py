from utils.loader import load_env_var
from langchain.chat_models import init_chat_model

# api_key = load_env_var("OPENAI_API_KEY")

llm = init_chat_model(
    model="gpt-4o",
    model_provider="openai",
    temperature=0.2,
    max_tokens=4096,
)

