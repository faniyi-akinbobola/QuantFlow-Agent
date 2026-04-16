from utils.loader import validate_required_env_vars


REQUIRED_ENV_VARS = [
    "OPENAI_API_KEY",
    "PINECONE_API_KEY",
    "PINECONE_INDEX_NAME",
    "NAME",
    "EMAIL"
]

def main():
    validate_required_env_vars(REQUIRED_ENV_VARS)
    print("Hello from stock-agent!")


if __name__ == "__main__":
    main()
