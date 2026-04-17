from langchain.tools import tool
import yfinance as yf
from datetime import datetime


@tool
def get_earnings_history(ticker: str) -> str:
    """
    Get earnings history with estimates vs actuals and next earnings date.
    
    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'TSLA', 'MSFT')
        
    Returns:
        Recent earnings data with beat/miss percentages and upcoming earnings date
    """
    try:
        stock = yf.Ticker(ticker)
        
        # Get earnings history
        earnings_history = stock.earnings_dates
        
        if earnings_history is None or earnings_history.empty:
            return f"No earnings data available for {ticker}"
        
        output = f"Earnings History for {ticker}:\n\n"
        
        # Get past earnings (already reported)
        past_earnings = earnings_history[earnings_history['Reported EPS'].notna()].head(4)
        
        if not past_earnings.empty:
            output += "Recent Earnings (Last 4 Quarters):\n"
            output += "-" * 60 + "\n"
            
            for date, row in past_earnings.iterrows():
                eps_estimate = row.get('EPS Estimate', None)
                eps_actual = row.get('Reported EPS', None)
                
                if eps_estimate and eps_actual:
                    surprise = eps_actual - eps_estimate
                    surprise_pct = (surprise / abs(eps_estimate) * 100) if eps_estimate != 0 else 0
                    
                    beat_miss = " BEAT" if surprise > 0 else " MISS" if surprise < 0 else " MET"
                    
                    output += f"\nDate: {date.strftime('%Y-%m-%d')}\n"
                    output += f"  EPS Estimate: ${eps_estimate:.2f}\n"
                    output += f"  EPS Actual:   ${eps_actual:.2f}\n"
                    output += f"  Surprise:     ${surprise:+.2f} ({surprise_pct:+.1f}%) {beat_miss}\n"
                else:
                    output += f"\nDate: {date.strftime('%Y-%m-%d')}\n"
                    output += f"  EPS Actual: ${eps_actual:.2f}\n"
        
        # Get next earnings date
        future_earnings = earnings_history[earnings_history['Reported EPS'].isna()]
        
        if not future_earnings.empty:
            next_earnings_date = future_earnings.index[0]
            output += f"\n{'='*60}\n"
            output += f"\n Next Earnings Date: {next_earnings_date.strftime('%Y-%m-%d')}\n"
            
            # Check if estimate is available
            next_estimate = future_earnings.iloc[0].get('EPS Estimate', None)
            if next_estimate:
                output += f"   Expected EPS: ${next_estimate:.2f}\n"
        else:
            output += f"\n{'='*60}\n"
            output += f"\n Next Earnings Date: Not available\n"
        
        return output
        
    except Exception as e:
        return f"Error fetching earnings history for {ticker}: {str(e)}"