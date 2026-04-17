from langchain.tools import tool
import yfinance as yf


@tool
def get_current_price_yahoo(ticker: str) -> str:
    """
    Get current stock price using Yahoo Finance (free, near real-time).
    
    Args:
        ticker: Stock ticker symbol
        
    Returns:
        Current price and basic stats
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        current_price = info.get('currentPrice') or info.get('regularMarketPrice')
        prev_close = info.get('previousClose')
        
        if not current_price:
            return f"Error: Unable to fetch price for {ticker}"
        
        change = current_price - prev_close if prev_close else 0
        change_pct = (change / prev_close * 100) if prev_close else 0
        
        output = f"{ticker} Current Price: ${current_price:.2f}\n"
        output += f"Change: ${change:.2f} ({change_pct:+.2f}%)\n"
        output += f"Previous Close: ${prev_close:.2f}"
        
        return output
    except Exception as e:
        return f"Error fetching price for {ticker}: {str(e)}"