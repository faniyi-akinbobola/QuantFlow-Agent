"""
LangSmith tracing setup for QuantFlow Agent.

LangGraph/LangChain automatically sends traces when these env vars are set:
  LANGCHAIN_TRACING_V2=true
  LANGCHAIN_API_KEY=...
  LANGCHAIN_PROJECT=...

This module validates the setup and logs the tracing status at startup.
"""

import os
from dotenv import load_dotenv

load_dotenv()


def setup_tracing() -> bool:
    """
    Validate and report LangSmith tracing status.

    Returns:
        True if tracing is enabled, False otherwise.
    """
    tracing_enabled = os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true"
    api_key = os.getenv("LANGCHAIN_API_KEY", "")
    project = os.getenv("LANGCHAIN_PROJECT", "default")

    if tracing_enabled and api_key:
        print(f"✅ LangSmith tracing enabled — project: '{project}'")
        print(f"   View traces at: https://smith.langchain.com/projects")
        return True
    elif tracing_enabled and not api_key:
        print("⚠️  LangSmith: LANGCHAIN_TRACING_V2=true but LANGCHAIN_API_KEY is missing.")
        return False
    else:
        print("ℹ️  LangSmith tracing disabled (set LANGCHAIN_TRACING_V2=true to enable).")
        return False
