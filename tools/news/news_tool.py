from langchain.tools import tool
from eventregistry import *
from utils.loader import load_env_var


@tool
def fetch_latest_news(ticker: str, max_items: int = 5) -> dict:
    """
    Fetch the latest news for a given stock ticker.
    
    Args:
        ticker: Stock ticker symbol (e.g., AAPL, TSLA)
    Returns:
        List of news articles with title, url, date, summary, and source
    """
    try:
        api_key = load_env_var("NEWSAPI_KEY")
        er = EventRegistry(apiKey=api_key)

        q = QueryArticlesIter(
            keywords=ticker,
            lang="eng",
            sortBy="date",
            maxItems=max_items
        )

        news_items = []
        for article in q.execQuery(er):
            news_items.append({
                "title": article.get("title"),
                "url": article.get("url"),
                "date": article.get("date"),
                "summary": article.get("summary"),
                "source": article.get("source", {}).get("title")
            })
        
        if not news_items:
            return f"message: No recent news found for {ticker}."
        
        return {
            "ticker": ticker,
            "articles": news_items
        }

    except Exception as e:
        return {f"Error fetching news for {ticker}: {e}"}