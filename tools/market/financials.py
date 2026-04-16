from langchain.tools import tool
import yfinance as yf

@tool
def get_financials(ticker: str) -> dict:
    """
    Fetches the financial statements for a given stock ticker using yfinance.
    
    :param ticker: The stock ticker symbol (e.g., 'AAPL' for Apple Inc.)
    :type ticker: str
    :return: A dictionary containing the financial statements (income statement, balance sheet, cash flow)
    :rtype: dict
    """
    try:
        stock = yf.Ticker(ticker)
        financials = {
            "income_statement": stock.financials.to_dict(),
            "balance_sheet": stock.balance_sheet.to_dict(),
            "cash_flow": stock.cashflow.to_dict()
        }
        return financials
    except Exception as e:
        return {"error": f"Error fetching financials for {ticker}: {e}"}