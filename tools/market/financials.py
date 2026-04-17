from langchain.tools import tool
import yfinance as yf

@tool
def get_financials(ticker: str) -> str:
    """
    Get financial statements for a stock ticker.
    
    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'TSLA')
        
    Returns:
        Formatted financial statement data (income statement, balance sheet, cash flow)
    """
    try:
        stock = yf.Ticker(ticker)
    
        financials = f"Income Statement:\n{stock.financials}\n\nBalance Sheet:\n{stock.balance_sheet}\n\nCash Flow:\n{stock.cashflow}"
        
        return financials
    except Exception as e:
        return f"Error fetching financials for {ticker}: {e}"
    