import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))

from graph.graph import graph

# Configuration for conversation memory
config = {"configurable": {"thread_id": "quick_test"}}

# Test 1: Simple RAG query
print("\n" + "=" * 80)
print("TEST 1: Apple Risk Factors (RAG)")
print("=" * 80)
result = graph.invoke({
    'messages': [('user', "What are Apple's main risk factors?")]
}, config=config)
print(result['messages'][-1].content)

# Test 2: Non-RAG ticker
print("\n" + "=" * 80)
print("TEST 2: NVIDIA Price (No RAG)")
print("=" * 80)
result = graph.invoke({
    'messages': [('user', "What's NVIDIA's current stock price?")]
}, config=config)
print(result['messages'][-1].content)

# Test 3: Calculator
print("\n" + "=" * 80)
print("TEST 3: Calculator")
print("=" * 80)
result = graph.invoke({
    'messages': [('user', "Calculate 175.50 * 100")]
}, config=config)
print(result['messages'][-1].content)

print("\n" + "=" * 80)
print("✅ QUICK TESTS COMPLETE")
print("=" * 80)
