import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))

from graph.graph import graph

# Configuration for conversation memory
config = {"configurable": {"thread_id": "test_session_1"}}

# Test 1: Apple Risk Factors
print("\n" + "=" * 80)
print("TEST 1: Apple's Risk Factors")
print("=" * 80)
result = graph.invoke({
    'messages': [('user', "What are Apple's main risk factors according to their SEC filings?")]
}, config=config)
print(result['messages'][-1].content)

# Test 2: Compare companies
print("\n" + "=" * 80)
print("TEST 2: Compare Apple vs Tesla Risk Factors")
print("=" * 80)
result = graph.invoke({
    'messages': [('user', 'Compare the risk factors between Apple and Tesla')]
}, config=config)
print(result['messages'][-1].content)

# Test 3: Specific section
print("\n" + "=" * 80)
print("TEST 3: Microsoft AI Strategy")
print("=" * 80)
result = graph.invoke({
    'messages': [('user', 'What does Microsoft say about AI in their latest 10-K?')]
}, config=config)
print(result['messages'][-1].content)

# Test 4: Financial metrics
print("\n" + "=" * 80)
print("TEST 4: Tesla Revenue Streams")
print("=" * 80)
result = graph.invoke({
    'messages': [('user', "Analyze Tesla's revenue streams based on their SEC filings")]
}, config=config)
print(result['messages'][-1].content)

# Test 5: Multi-step analysis
print("\n" + "=" * 80)
print("TEST 5: Investment Analysis - AAPL")
print("=" * 80)
result = graph.invoke({
    'messages': [('user', 'Should I invest in AAPL? Consider their fundamentals from SEC filings and current market conditions')]
}, config=config)
print(result['messages'][-1].content)

# Test 6: Non-RAG Ticker (NVDA - not in database)
print("\n" + "=" * 80)
print("TEST 6: Non-RAG Ticker Analysis - NVDA")
print("=" * 80)
result = graph.invoke({
    'messages': [('user', "Analyze NVIDIA's fundamentals and recent performance. What are the key metrics?")]
}, config=config)
print(result['messages'][-1].content)

# Test 7: Multi-tool combination (price + metrics + news)
print("\n" + "=" * 80)
print("TEST 7: Multi-Tool Combination - TSLA")
print("=" * 80)
result = graph.invoke({
    'messages': [('user', "What's Tesla's current price, P/E ratio, and what does recent news say about the company?")]
}, config=config)
print(result['messages'][-1].content)

# Test 8: Calculation query
print("\n" + "=" * 80)
print("TEST 8: Calculation - Valuation")
print("=" * 80)
result = graph.invoke({
    'messages': [('user', "If Apple's stock is $175 and I want to buy 50 shares, how much would that cost? Also calculate a 15% gain.")]
}, config=config)
print(result['messages'][-1].content)

# Test 9: Technical Analysis
print("\n" + "=" * 80)
print("TEST 9: Technical Analysis - RSI")
print("=" * 80)
result = graph.invoke({
    'messages': [('user', "What's the RSI for Microsoft? Is it overbought or oversold?")]
}, config=config)
print(result['messages'][-1].content)

# Test 10: Comparison (RAG + Non-RAG)
print("\n" + "=" * 80)
print("TEST 10: Compare RAG vs Non-RAG Tickers")
print("=" * 80)
result = graph.invoke({
    'messages': [('user', "Compare Apple (AAPL) and NVIDIA (NVDA) - which is a better investment right now?")]
}, config=config)
print(result['messages'][-1].content)

# Test 11: Analyst Recommendations
print("\n" + "=" * 80)
print("TEST 11: Analyst Recommendations")
print("=" * 80)
result = graph.invoke({
    'messages': [('user', "What are analysts saying about Amazon? Show me recent ratings and price targets.")]
}, config=config)
print(result['messages'][-1].content)

# Test 12: Earnings History
print("\n" + "=" * 80)
print("TEST 12: Earnings Performance")
print("=" * 80)
result = graph.invoke({
    'messages': [('user', "How has Tesla performed in their recent earnings? Did they beat or miss estimates?")]
}, config=config)
print(result['messages'][-1].content)

# Test 13: Edge Case - Invalid Ticker
print("\n" + "=" * 80)
print("TEST 13: Edge Case - Invalid Ticker")
print("=" * 80)
result = graph.invoke({
    'messages': [('user', "What's the stock price for XYZ123?")]
}, config=config)
print(result['messages'][-1].content)

# Test 14: Complex Multi-Step Analysis
print("\n" + "=" * 80)
print("TEST 14: Complex Multi-Step Analysis")
print("=" * 80)
result = graph.invoke({
    'messages': [('user', "I have $10,000 to invest. Should I buy Microsoft or Google? Consider their SEC filings, current metrics, news, and analyst recommendations.")]
}, config=config)
print(result['messages'][-1].content)

# Test 15: Company Comparison (same sector, different RAG status)
print("\n" + "=" * 80)
print("TEST 15: Sector Comparison")
print("=" * 80)
result = graph.invoke({
    'messages': [('user', "Compare the cloud businesses of Microsoft (from SEC filings) and Google. Which has better growth prospects?")]
}, config=config)
print(result['messages'][-1].content)

print("\n" + "=" * 80)
print("✅ ALL 15 TESTS COMPLETE")
print("=" * 80)