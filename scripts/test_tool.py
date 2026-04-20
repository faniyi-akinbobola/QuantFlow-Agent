import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tools.rag.retrieval_tool import search_sec_filings

print("=" * 60)
print("TESTING RAG TOOL - SEC FILINGS SEARCH")
print("=" * 60)

# Test 1: Risk Factors for Apple
print("\n1. Test: Apple Risk Factors")
print("-" * 60)
result = search_sec_filings.invoke({
    "query": "What are the main risk factors?",
    "ticker": "AAPL"
})
print(result)

# Test 2: Tesla Business Strategy
print("\n2. Test: Tesla Business Strategy")
print("-" * 60)
result = search_sec_filings.invoke({
    "query": "What is the company's business strategy and competitive advantages?",
    "ticker": "TSLA"
})
print(result)

# Test 3: Microsoft Revenue Streams
print("\n3. Test: Microsoft Revenue Streams")
print("-" * 60)
result = search_sec_filings.invoke({
    "query": "What are the main revenue sources?",
    "ticker": "MSFT"
})
print(result)

# Test 4: Amazon Growth Plans
print("\n4. Test: Amazon Growth Initiatives")
print("-" * 60)
result = search_sec_filings.invoke({
    "query": "What are the key growth initiatives and investments?",
    "ticker": "AMZN"
})
print(result)

# Test 5: Ticker Not in Database
print("\n5. Test: Ticker Not in Database (NVDA)")
print("-" * 60)
result = search_sec_filings.invoke({
    "query": "What are the risk factors?",
    "ticker": "NVDA"
})
print(result)

print("\n" + "=" * 60)
print("✅ RAG TOOL TESTING COMPLETE")
print("=" * 60)