from langchain.tools import tool
import requests
from utils.loader import load_env_var

@tool
def technical_analysis(ticker: str) -> str:
    """
    Get RSI technical analysis with buy/sell signals.
    
    Args:
        ticker: Stock ticker symbol (e.g., AAPL, TSLA)
        
    Returns:
        RSI value with overbought/oversold interpretation
    """

    try:
        api_key = load_env_var("ALPHAVANTAGE_KEY")
        url = (
            f"https://www.alphavantage.co/query"
            f"?function=RSI"
            f"&symbol={ticker}"
            f"&interval=daily"
            f"&time_period=14"
            f"&series_type=close"
            f"&apikey={api_key}"
        )

        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        rsi_data = data.get("Technical Analysis: RSI", {})

        if not rsi_data:
            return {"error": "No RSI data found"}

        # get latest RSI value
        latest_date = sorted(rsi_data.keys())[-1]
        latest_rsi = float(rsi_data[latest_date]["RSI"])

        # interpret signal
        if latest_rsi > 70:
            signal = "overbought (>70 is strong sell, 50-70 is mild sell)"
        elif latest_rsi < 30:
            signal = "oversold (>30 is mild buy, <30 is strong buy)"
        else:
            signal = "neutral (50-70 is mild buy, 30-50 is mild sell)"

        # Format as readable string
        output = f"Technical Analysis for {ticker}:\n\n"
        output += f"RSI (14-day): {latest_rsi:.2f}\n"
        output += f"Signal: {signal}\n"
        output += f"Date: {latest_date}"

        return output
    except Exception as e:
        return f"Error performing technical analysis for {ticker}: {e}"