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


WELCOME_MESSAGE = """
👋 Hi! I'm your AI financial analyst.

I can help you with:
- Stock analysis & comparisons
- Company financials & earnings
- Technical indicators & key metrics
- SEC filings research (AAPL, TSLA, MSFT, AMZN)
- Market news & analyst recommendations

Ask me anything about stocks!
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
    # Show logo/readme for 3 seconds before sending welcome message
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
    config = {"configurable": {"thread_id": thread_id}}

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

            elif kind == "on_tool_start":
                await cl.Message(
                    content=f"🔧 Using tool: **{event['name']}**",
                    author="System"
                ).send()

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
