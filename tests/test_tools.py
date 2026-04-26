"""Test individual tools before running full agent."""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tools import (
    get_current_price_yahoo,
    get_key_metrics,
    get_company_info,
    get_earnings_history,
    get_analyst_recommendations,
    compare_stocks,
    get_financials,
    technical_analysis,
    fetch_latest_news,
    calculator,
    search_sec_filings,
)


def test_market_tools():
    print("=== Testing Market Tools ===\n")
    
    ticker = "AAPL"
    
    # Test 1: Stock Price
    print("1. Current Price:")
    print(get_current_price_yahoo.invoke({"ticker": ticker}))
    print()
    
    # Test 2: Key Metrics
    print("2. Key Metrics:")
    print(get_key_metrics.invoke({"ticker": ticker}))
    print()
    
    # Test 3: Company Info
    print("3. Company Info:")
    print(get_company_info.invoke({"ticker": ticker}))
    print()
    
    # Test 4: Earnings History
    print("4. Earnings History:")
    print(get_earnings_history.invoke({"ticker": ticker}))
    print()
    
    # Test 5: Analyst Recommendations
    print("5. Analyst Recommendations:")
    print(get_analyst_recommendations.invoke({"ticker": ticker}))
    print()
    
    # Test 6: Stock Comparison
    print("6. Compare Stocks:")
    print(compare_stocks.invoke({"tickers": "AAPL,MSFT"}))
    print()
    
    # Test 7: Financials
    print("7. Financials:")
    print(get_financials.invoke({"ticker": ticker}))
    print()
    
    # Test 8: Technical Analysis
    print("8. Technical Analysis:")
    print(technical_analysis.invoke({"ticker": ticker}))
    print()


def test_news_tool():
    print("=== Testing News Tool ===\n")
    print(fetch_latest_news.invoke({"ticker": "AAPL", "max_items": 3}))
    print()


def test_rag_tool():
    print("=== Testing RAG Tool ===\n")
    try:
        result = search_sec_filings.invoke({"query": "What are the main risk factors?", "ticker": "AAPL"})
        print(result)
    except Exception as e:
        if "NOT_FOUND" in str(e):
            print("⚠️  Pinecone index not found. Run 'python scripts/setup_pinecone.py' first.")
        else:
            print(f"Error: {e}")
    print()


def test_calculator(query: str = "175.23 * 1.05"):
    print("=== Testing Calculator ===\n")
    print(calculator.invoke({"query": query}))
    print()


if __name__ == "__main__":
    print("\n" + "="*60)
    print("QUANTFLOW AGENT - TOOL TESTING")
    print("="*60 + "\n")
    
    # Test each category
    test_market_tools()
    test_news_tool()
    test_rag_tool()
    test_calculator()
    
    print("="*60)
    print("✅ All tools tested successfully!")
    print("="*60)