# from langchain.tools import tool
# import yfinance as yf


# @tool
# def get_analyst_recommendations(ticker: str) -> str:
#     """
#     Get analyst recommendations, price targets, and recent upgrades/downgrades.
    
#     Args:
#         ticker: Stock ticker symbol (e.g., 'AAPL', 'TSLA', 'MSFT')
        
#     Returns:
#         Analyst ratings, price targets, potential upside, and recent rating changes
#     """
#     try:
#         stock = yf.Ticker(ticker)
#         info = stock.info
        
#         output = f"Analyst Recommendations for {ticker}:\n\n"
        
#         # Price Targets
#         target_high = info.get('targetHighPrice', None)
#         target_low = info.get('targetLowPrice', None)
#         target_mean = info.get('targetMeanPrice', None)
#         current_price = info.get('currentPrice') or info.get('regularMarketPrice', 0)
        
#         output += "Price Targets:\n"
#         output += f"  High:    ${target_high:.2f}\n" if target_high else "  High:    N/A\n"
#         output += f"  Mean:    ${target_mean:.2f}\n" if target_mean else "  Mean:    N/A\n"
#         output += f"  Low:     ${target_low:.2f}\n" if target_low else "  Low:     N/A\n"
#         output += f"  Current: ${current_price:.2f}\n"
        
#         # Calculate upside/downside
#         if target_mean and current_price:
#             upside = ((target_mean - current_price) / current_price) * 100
#             direction = "📈 Upside" if upside > 0 else "📉 Downside"
#             output += f"\n{direction}: {abs(upside):.2f}%\n"
        
#         # Analyst Recommendation
#         recommendation = info.get('recommendationKey', 'N/A')
#         num_analysts = info.get('numberOfAnalystOpinions', 'N/A')
        
#         output += f"\nConsensus Recommendation: {recommendation.upper() if recommendation != 'N/A' else 'N/A'}\n"
#         output += f"Number of Analysts: {num_analysts}\n"
        
#         # Recent Upgrades/Downgrades
#         recommendations = stock.recommendations
        
#         if recommendations is not None and not recommendations.empty:
#             output += f"\nRecent Rating Changes (Last 5):\n"
#             output += "-" * 60 + "\n"
            
#             for idx, row in recommendations.head(5).iterrows():
#                 date = idx.strftime('%Y-%m-%d')
#                 firm = row.get('Firm', 'Unknown')
#                 to_grade = row.get('To Grade', 'N/A')
#                 from_grade = row.get('From Grade', None)
#                 action = row.get('Action', 'N/A')
                
#                 output += f"\n{date} | {firm}\n"
#                 if from_grade:
#                     output += f"  {from_grade} → {to_grade} ({action})\n"
#                 else:
#                     output += f"  Rating: {to_grade} ({action})\n"
#         else:
#             output += f"\nNo recent rating changes available\n"
        
#         return output
        
#     except Exception as e:
#         return f"Error fetching analyst recommendations for {ticker}: {str(e)}"

from langchain.tools import tool
import yfinance as yf
from datetime import datetime


@tool
def get_analyst_recommendations(ticker: str) -> str:
    """
    Get analyst recommendations and price targets for a stock.
    
    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'TSLA')
        
    Returns:
        Formatted analyst recommendations with ratings and price targets
    """
    try:
        stock = yf.Ticker(ticker)
        recommendations = stock.recommendations
        
        if recommendations is None or recommendations.empty:
            return f"No analyst recommendations available for {ticker}"
        
        # Get most recent recommendations (last 5)
        recent_recs = recommendations.tail(5)
        
        output = f"Analyst Recommendations for {ticker}:\n\n"
        output += "Recent Rating Changes:\n"
        output += "-" * 60 + "\n"
        
        for idx, row in recent_recs.iterrows():
            # Fix: Handle multiple date formats (datetime, string, int)
            try:
                if isinstance(idx, str):
                    date_str = idx
                elif isinstance(idx, (int, float)):
                    # Handle integer/timestamp index
                    date_str = str(idx)
                elif hasattr(idx, 'strftime'):
                    # Handle datetime/Timestamp objects
                    date_str = idx.strftime('%Y-%m-%d')
                else:
                    date_str = str(idx)
            except Exception:
                date_str = str(idx)
            
            firm = row.get('Firm', 'Unknown')
            to_grade = row.get('To Grade', 'N/A')
            from_grade = row.get('From Grade', '-')
            action = row.get('Action', 'init')
            
            output += f"Date: {date_str}\n"
            output += f"  Firm: {firm}\n"
            output += f"  Action: {action}\n"
            output += f"  Rating: {from_grade} → {to_grade}\n\n"
        
        # Get price targets if available
        info = stock.info
        if 'targetMeanPrice' in info and info['targetMeanPrice']:
            output += "\nPrice Targets:\n"
            output += "-" * 60 + "\n"
            output += f"  Mean Target: ${info.get('targetMeanPrice', 'N/A'):.2f}\n"
            output += f"  High Target: ${info.get('targetHighPrice', 'N/A'):.2f}\n"
            output += f"  Low Target:  ${info.get('targetLowPrice', 'N/A'):.2f}\n"
            
            current_price = info.get('currentPrice', info.get('regularMarketPrice', 0))
            if current_price and info.get('targetMeanPrice'):
                upside = ((info['targetMeanPrice'] - current_price) / current_price) * 100
                output += f"  Upside to Mean: {upside:+.2f}%\n"
        
        # Add consensus rating
        if 'recommendationKey' in info:
            output += f"\nConsensus: {info['recommendationKey'].upper()}\n"
        
        return output
        
    except Exception as e:
        return f"Error fetching analyst recommendations for {ticker}: {str(e)}"