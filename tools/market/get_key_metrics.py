from langchain.tools import tool
import yfinance as yf


@tool
def get_key_metrics(ticker: str) -> str:
    """
    Get real-time key financial metrics for a stock.
    
    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'TSLA', 'MSFT')
        
    Returns:
        Current P/E ratio, dividend yield, market cap, beta, and 52-week range
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Extract metrics
        current_price = info.get('currentPrice') or info.get('regularMarketPrice', 0)
        pe_ratio = info.get('trailingPE', 'N/A')
        forward_pe = info.get('forwardPE', 'N/A')
        market_cap = info.get('marketCap', 0)
        dividend_yield = info.get('dividendYield', 0)
        beta = info.get('beta', 'N/A')
        week_52_high = info.get('fiftyTwoWeekHigh', 0)
        week_52_low = info.get('fiftyTwoWeekLow', 0)
        eps = info.get('trailingEps', 'N/A')
        
        # Format output
        output = f"Key Metrics for {ticker}:\n\n"
        output += f"Current Price: ${current_price:.2f}\n"
        output += f"Market Cap: ${market_cap:,}\n"
        output += f"\nValuation Metrics:\n"
        output += f"  P/E Ratio (TTM): {pe_ratio if pe_ratio == 'N/A' else f'{pe_ratio:.2f}'}\n"
        output += f"  Forward P/E: {forward_pe if forward_pe == 'N/A' else f'{forward_pe:.2f}'}\n"
        output += f"  EPS (TTM): {eps if eps == 'N/A' else f'${eps:.2f}'}\n"
        output += f"\nDividend & Risk:\n"
        output += f"  Dividend Yield: {dividend_yield * 100:.2f}%\n"
        output += f"  Beta: {beta if beta == 'N/A' else f'{beta:.2f}'}\n"
        output += f"\n52-Week Range:\n"
        output += f"  High: ${week_52_high:.2f}\n"
        output += f"  Low: ${week_52_low:.2f}\n"
        output += f"  Current vs High: {((current_price - week_52_high) / week_52_high * 100):+.2f}%\n"
        output += f"  Current vs Low: {((current_price - week_52_low) / week_52_low * 100):+.2f}%\n"
        
        return output
        
    except Exception as e:
        return f"Error fetching key metrics for {ticker}: {str(e)}"