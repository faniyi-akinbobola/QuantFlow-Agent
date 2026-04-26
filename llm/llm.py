from utils.loader import load_env_var
from langchain.chat_models import init_chat_model
from langchain_ollama import ChatOllama
# api_key = load_env_var("OPENAI_API_KEY")

llm = init_chat_model(
    model="gpt-4o",
    model_provider="openai",
    temperature=0.2,
    max_tokens=4096,
)

###ollama local setup example
# llm = ChatOllama(
#     model="qwen2.5:7b",  # Name of your local Ollama model
#     temperature=0.2,
#     num_ctx=8192,
# )