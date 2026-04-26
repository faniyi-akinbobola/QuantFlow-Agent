from langchain.tools import tool
from eventregistry import *
from utils.loader import load_env_var


@tool
def fetch_latest_news(ticker: str, max_items: int = 5) -> str:
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
            lang="eng"
        )

        news_items = []
        count = 0
        for article in q.execQuery(er):
            if count >= max_items:
                break
            
            # Try multiple fields for summary/body content
            summary = (article.get("summary") or 
                      article.get("body") or 
                      article.get("excerpt") or 
                      "No summary available")
            
            # Truncate summary to first 200 characters to avoid overwhelming the LLM
            if summary and len(summary) > 200:
                summary = summary[:200] + "..."
            
            news_items.append({
                "title": article.get("title"),
                "url": article.get("url"),
                "date": article.get("date"),
                "summary": summary,
                "source": article.get("source", {}).get("title")
            })
            count += 1
        
        if not news_items:
            return f"message: No recent news found for {ticker}."
        
        # Format as string for LLM
        output = f"Latest News for {ticker}:\n\n"
        for i, item in enumerate(news_items, 1):
            output += f"{i}. {item['title']}\n"
            output += f"   Source: {item['source']} | Date: {item['date']}\n"
            if item['summary'] and item['summary'] != "No summary available":
                output += f"   {item['summary']}\n"
            output += f"   URL: {item['url']}\n\n"
        
        return output

    except Exception as e:
        return f"Error fetching news for {ticker}: {e}"