"""Tools package for stock market AI agent."""

from .market import (
    get_current_price_yahoo,
    get_key_metrics,
    get_company_info,
    get_earnings_history,
    get_analyst_recommendations,
    compare_stocks,
    get_financials,
    technical_analysis,
)
from .news import fetch_latest_news
from .math import calculator
from .rag import search_sec_filings

__all__ = [
    # Market tools
    "get_current_price_yahoo",
    "get_key_metrics",
    "get_company_info",
    "get_earnings_history",
    "get_analyst_recommendations",
    "compare_stocks",
    "get_financials",
    "technical_analysis",
    # News tools
    "fetch_latest_news",
    # Math tools
    "calculator",
    # RAG tools
    "search_sec_filings",
]