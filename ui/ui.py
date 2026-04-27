"""
Chainlit UI for Stock Analysis Agent
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import chainlit as cl
import asyncio
from langchain_core.messages import HumanMessage
from graph.graph import workflow
from memory.memory import make_checkpointer
from utils.tracing import setup_tracing

setup_tracing()


WELCOME_MESSAGE = """
👋 Welcome to QuantFlow AI — your financial analysis assistant.

I can help you with:
- 📊 Stock analysis and company comparisons
- 💼 Financials, earnings, and key metrics
- 📈 Technical indicators and market trends
- 📄 SEC filings research (multiple companies supported)
- 📰 Latest market news and analyst insights

💡 Try asking:
- "Compare AAPL and MSFT fundamentals"
- "What are Tesla’s biggest risks from its latest 10-K?"
- "What’s the latest news on NVDA?"

Ask me anything about stocks, companies, or market trends to get started. 
"""

# Graph compiled with async checkpointer (set on first use)
_graph = None


async def get_graph():
    global _graph
    if _graph is None:
        checkpointer = await make_checkpointer()
        _graph = workflow.compile(checkpointer=checkpointer)
    return _graph


@cl.on_chat_start
async def start():
    # chainlit.md shows the logo splash instantly in the browser.
    # Sleep 3s here so the user sees it before welcome message appears.
    await asyncio.sleep(3)
    await cl.Message(content=WELCOME_MESSAGE).send()
    cl.user_session.set("thread_id", cl.user_session.get("id"))


@cl.on_message
async def main(message: cl.Message):
    thread_id = cl.user_session.get("thread_id")
    if not thread_id:
        await cl.Message(content=" Session error. Please refresh the page.").send()
        return

    graph = await get_graph()
    config = {
        "configurable": {"thread_id": thread_id},
        "recursion_limit": 25  # Prevent infinite loops
    }

    msg = cl.Message(content="")
    await msg.send()

    try:
        async for event in graph.astream_events(
            {"messages": [HumanMessage(content=message.content)]},
            config=config,
            version="v2"
        ):
            kind = event["event"]

            if kind == "on_chat_model_stream":
                content = event["data"]["chunk"].content
                if content:
                    await msg.stream_token(content)

        await msg.update()

    except Exception as e:
        msg.content = f" Error: {str(e)}\n\nPlease try rephrasing your question."
        await msg.update()
        print(f"Error: {e}")


@cl.on_chat_resume
async def resume(thread_id: str):
    cl.user_session.set("thread_id", thread_id)
    await cl.Message(
        content="�� **Conversation resumed!** I remember our previous discussion. How can I help you further?",
        author="System"
    ).send()
