from langchain.tools import tool
import yfinance as yf


@tool
def get_analyst_recommendations(ticker: str) -> str:
    """
    Get analyst recommendations, price targets, and recent upgrades/downgrades.
    
    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'TSLA', 'MSFT')
        
    Returns:
        Analyst ratings, price targets, potential upside, and recent rating changes
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        output = f"Analyst Recommendations for {ticker}:\n\n"
        
        # Price Targets
        target_high = info.get('targetHighPrice', None)
        target_low = info.get('targetLowPrice', None)
        target_mean = info.get('targetMeanPrice', None)
        current_price = info.get('currentPrice') or info.get('regularMarketPrice', 0)
        
        output += "Price Targets:\n"
        output += f"  High:    ${target_high:.2f}\n" if target_high else "  High:    N/A\n"
        output += f"  Mean:    ${target_mean:.2f}\n" if target_mean else "  Mean:    N/A\n"
        output += f"  Low:     ${target_low:.2f}\n" if target_low else "  Low:     N/A\n"
        output += f"  Current: ${current_price:.2f}\n"
        
        # Calculate upside/downside
        if target_mean and current_price:
            upside = ((target_mean - current_price) / current_price) * 100
            direction = "📈 Upside" if upside > 0 else "📉 Downside"
            output += f"\n{direction}: {abs(upside):.2f}%\n"
        
        # Analyst Recommendation
        recommendation = info.get('recommendationKey', 'N/A')
        num_analysts = info.get('numberOfAnalystOpinions', 'N/A')
        
        output += f"\nConsensus Recommendation: {recommendation.upper() if recommendation != 'N/A' else 'N/A'}\n"
        output += f"Number of Analysts: {num_analysts}\n"
        
        # Recent Upgrades/Downgrades
        recommendations = stock.recommendations
        
        if recommendations is not None and not recommendations.empty:
            output += f"\nRecent Rating Changes (Last 5):\n"
            output += "-" * 60 + "\n"
            
            for idx, row in recommendations.head(5).iterrows():
                date = idx.strftime('%Y-%m-%d')
                firm = row.get('Firm', 'Unknown')
                to_grade = row.get('To Grade', 'N/A')
                from_grade = row.get('From Grade', None)
                action = row.get('Action', 'N/A')
                
                output += f"\n{date} | {firm}\n"
                if from_grade:
                    output += f"  {from_grade} → {to_grade} ({action})\n"
                else:
                    output += f"  Rating: {to_grade} ({action})\n"
        else:
            output += f"\nNo recent rating changes available\n"
        
        return output
        
    except Exception as e:
        return f"Error fetching analyst recommendations for {ticker}: {str(e)}"