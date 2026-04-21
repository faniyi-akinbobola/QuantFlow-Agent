# Thread ID and Memory System Explained

## Overview

The Stock Analysis Agent uses a **persistent memory system** that allows it to remember conversations across multiple interactions. This is achieved through:

1. **Thread IDs** - Unique identifiers for each conversation
2. **SQLite Checkpointer** - Persistent storage for conversation state
3. **LangGraph State Management** - Message history tracking

---

## How It Works

### 1. Thread ID System

```python
# In ui/ui.py - on_chat_start()
thread_id = cl.user_session.get("thread_id")
if not thread_id:
    import uuid
    thread_id = str(uuid.uuid4())
    cl.user_session.set("thread_id", thread_id)
```

**What happens:**

- When a user starts a chat, we check if they already have a `thread_id`
- If not, we generate a unique UUID (e.g., `"7f8a3b2c-1d4e-5f6g-7h8i-9j0k1l2m3n4o"`)
- This ID is stored in Chainlit's user session for the duration of the conversation
- The thread_id acts as a **conversation identifier** in the database

**Why it matters:**

- Each conversation is isolated - User A's chat doesn't mix with User B's
- Users can have multiple separate conversations (different threads)
- The agent can retrieve the correct conversation history using this ID

---

### 2. SQLite Checkpointer (Persistent Storage)

```python
# In memory/memory.py
from langgraph.checkpoint.sqlite import SqliteSaver

checkpointer = SqliteSaver.from_conn_string("checkpoints.db")
```

**What happens:**

- SQLite database (`checkpoints.db`) stores all conversation states
- Each message, tool call, and agent response is saved
- The checkpointer automatically manages this storage

**Database Structure:**

```
checkpoints.db
├── checkpoints table
│   ├── thread_id (the UUID)
│   ├── checkpoint_id (version of the conversation state)
│   ├── parent_id (previous checkpoint)
│   └── data (serialized state including messages)
└── writes table
    └── Intermediate agent actions
```

**Why it matters:**

- **Persistence**: Conversations survive server restarts
- **History**: Full message history is stored, not just the last few messages
- **Recovery**: Can resume conversations from any checkpoint

---

### 3. Passing thread_id to the Graph

```python
# In ui/ui.py - on_message()
config = {
    "configurable": {
        "thread_id": thread_id
    }
}

# Stream agent responses
async for event in graph.astream_events(input_data, config, version="v1"):
    # ... handle events
```

**What happens:**

1. User sends a message (e.g., "What's AAPL's price?")
2. We pass the `thread_id` in the `config` parameter
3. LangGraph uses this thread_id to:
   - Load the conversation history from SQLite
   - Add the new message to the history
   - Process with the agent
   - Save the updated state back to SQLite

**The Flow:**

```
User Message
    ↓
[thread_id] → Load from SQLite → [Previous Messages]
    ↓
Add new message → [All Messages]
    ↓
Agent processes → Calls tools → Generates response
    ↓
Save to SQLite ← [Updated State]
    ↓
Return response to user
```

---

### 4. State Management in LangGraph

```python
# In graph/state.py
from typing import Annotated
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from typing import TypedDict

class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
```

**What `add_messages` does:**

- Special reducer that **appends** messages instead of replacing them
- Maintains the full conversation history in the state
- Automatically handles different message types (Human, AI, Tool, System)

**Example conversation state:**

```python
{
    "messages": [
        SystemMessage(content="You are a financial analyst..."),
        HumanMessage(content="What's AAPL's price?"),
        AIMessage(content="", tool_calls=[{"name": "get_stock_price", "args": {"ticker": "AAPL"}}]),
        ToolMessage(content="AAPL: $178.50", tool_call_id="..."),
        AIMessage(content="Apple (AAPL) is currently trading at $178.50"),
        HumanMessage(content="What about TSLA?"),  # ← New message
        # ... agent will see full history
    ]
}
```

---

## Complete Example Flow

### First Message:

```
1. User opens chat → on_chat_start()
   - Generate thread_id: "abc-123"
   - Store in session
   - Send welcome message

2. User: "What's AAPL's price?"

3. on_message():
   - Get thread_id: "abc-123"
   - Create config: {"configurable": {"thread_id": "abc-123"}}
   - Call graph.astream_events(input, config)

4. LangGraph:
   - Check SQLite for thread "abc-123" → Empty (new conversation)
   - Create initial state: {messages: [SystemMessage, HumanMessage("What's AAPL's price?")]}
   - Agent processes → Calls get_stock_price
   - Agent responds: "AAPL is $178.50"
   - Save state to SQLite under thread "abc-123"

5. Return response to user
```

### Follow-up Message:

```
1. User: "Compare it with TSLA"

2. on_message():
   - Get thread_id: "abc-123" (same as before)
   - Create config: {"configurable": {"thread_id": "abc-123"}}
   - Call graph.astream_events(input, config)

3. LangGraph:
   - Check SQLite for thread "abc-123" → Found!
   - Load previous state:
     {
       messages: [
         SystemMessage("..."),
         HumanMessage("What's AAPL's price?"),
         AIMessage("..."),
         ToolMessage("AAPL: $178.50"),
         AIMessage("AAPL is $178.50")
       ]
     }
   - Add new message: HumanMessage("Compare it with TSLA")
   - Agent sees FULL history → Knows "it" refers to AAPL
   - Agent calls compare_stocks("AAPL", "TSLA")
   - Agent responds with comparison
   - Save updated state to SQLite

4. Return response to user
```

---

## Key Benefits

### 1. **Context Awareness**

```python
User: "What's AAPL's PE ratio?"
Agent: "AAPL has a P/E ratio of 28.5"

User: "How does that compare to the tech sector average?"
# Agent remembers we're talking about AAPL ✓
```

### 2. **Multi-turn Conversations**

```python
User: "Analyze TSLA's financials"
Agent: [Provides detailed analysis]

User: "What about their debt levels?"
# Agent knows "their" = TSLA's ✓

User: "Show me their last 3 earnings reports"
# Still remembers the context ✓
```

### 3. **Persistence Across Sessions**

- User closes browser → Conversation saved
- User returns later → Can continue where they left off (if same thread_id)
- Server restarts → All conversations preserved in SQLite

### 4. **Isolated Conversations**

- Each thread_id is independent
- User A's conversations don't affect User B's
- Multiple tabs = multiple thread_ids = separate conversations

---

## Memory Configuration

### In graph/graph.py:

```python
from memory.memory import checkpointer

# Create the graph
workflow = StateGraph(AgentState)
# ... add nodes and edges

# Compile with checkpointer
graph = workflow.compile(checkpointer=checkpointer)
```

### In memory/memory.py:

```python
from langgraph.checkpoint.sqlite import SqliteSaver

# Create SQLite checkpointer
checkpointer = SqliteSaver.from_conn_string("checkpoints.db")

# Alternative: In-memory (testing only, not persistent)
# checkpointer = MemorySaver()
```

---

## Testing Memory

You can test the memory system directly:

```python
from graph.graph import graph
from langchain_core.messages import HumanMessage

# First conversation
config1 = {"configurable": {"thread_id": "test-123"}}

result1 = graph.invoke({
    "messages": [HumanMessage(content="What's AAPL's price?")]
}, config1)

print(result1["messages"][-1].content)

# Follow-up (same thread)
result2 = graph.invoke({
    "messages": [HumanMessage(content="What about TSLA?")]
}, config1)

print(result2["messages"][-1].content)
# Agent will remember we just discussed AAPL

# Different conversation (different thread)
config2 = {"configurable": {"thread_id": "test-456"}}

result3 = graph.invoke({
    "messages": [HumanMessage(content="What about TSLA?")]
}, config2)

print(result3["messages"][-1].content)
# Agent won't know about previous AAPL discussion (different thread)
```

---

## Troubleshooting

### Issue: Agent doesn't remember context

```python
# ❌ Wrong - Missing thread_id
config = {}

# ✓ Correct
config = {"configurable": {"thread_id": "unique-id"}}
```

### Issue: Multiple users see each other's conversations

```python
# ❌ Wrong - Using same thread_id for all users
thread_id = "global-thread"

# ✓ Correct - Unique thread_id per user/session
import uuid
thread_id = str(uuid.uuid4())
```

### Issue: Conversations don't persist

```python
# ❌ Wrong - Using MemorySaver (in-memory only)
from langgraph.checkpoint.memory import MemorySaver
checkpointer = MemorySaver()

# ✓ Correct - Using SqliteSaver (persistent)
from langgraph.checkpoint.sqlite import SqliteSaver
checkpointer = SqliteSaver.from_conn_string("checkpoints.db")
```

---

## Summary

1. **thread_id** = Unique conversation identifier (UUID)
2. **SQLite** = Persistent storage (`checkpoints.db`)
3. **Config** = Pass thread_id to graph: `{"configurable": {"thread_id": "..."}}`
4. **add_messages** = Reducer that maintains full message history
5. **Checkpointer** = Automatically saves/loads state on each interaction

This architecture enables natural, context-aware conversations that feel like talking to a human analyst who remembers everything you've discussed! 🧠
