from langchain.tools import tool
import requests

from utils.loader import load_env_var

@tool
def technical_analysis(ticker: str) -> dict:
    """
    Docstring for technical_analysis
    
    :param ticker: Stock ticker symbol (e.g., AAPL, TSLA)
    :type ticker: str
    :return: A dictionary containing technical analysis results (e.g., RSI, signal, date)
    :rtype: dict
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
        data = response.json()

        rsi_data = data.get("Technical Analysis: RSI", {})

        if not rsi_data:
            return {"error": "No RSI data found"}

        # get latest RSI value
        latest_date = sorted(rsi_data.keys())[-1]
        latest_rsi = float(rsi_data[latest_date]["RSI"])

        # interpret signal
        if latest_rsi > 70:
            signal = "overbought"
        elif latest_rsi < 30:
            signal = "oversold"
        else:
            signal = "neutral"

        return {
            "ticker": ticker,
            "rsi": latest_rsi,
            "signal": signal,
            "date": latest_date
        }
    except Exception as e:
        return {"error": f"Error performing technical analysis for {ticker}: {e}"}