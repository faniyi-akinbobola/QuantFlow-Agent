from langchain.tools import tool
import yfinance as yf


@tool
def compare_stocks(tickers: str) -> str:
    """
    Compare key metrics across multiple stocks side-by-side.
    
    Args:
        tickers: Comma-separated ticker symbols (e.g., "AAPL,MSFT,GOOGL")
        
    Returns:
        Side-by-side comparison table of price, P/E, market cap, dividend, and beta
    """
    try:
        ticker_list = [t.strip().upper() for t in tickers.split(',')]
        
        if len(ticker_list) > 5:
            return "Error: Maximum 5 stocks can be compared at once"
        
        if len(ticker_list) < 2:
            return "Error: Please provide at least 2 tickers to compare (e.g., 'AAPL,MSFT')"
        
        output = f"Stock Comparison: {', '.join(ticker_list)}\n\n"
        
        # Collect metrics for each ticker
        metrics = {}
        for ticker in ticker_list:
            try:
                stock = yf.Ticker(ticker)
                info = stock.info
                
                metrics[ticker] = {
                    'price': info.get('currentPrice') or info.get('regularMarketPrice', 0),
                    'pe': info.get('trailingPE', 0),
                    'forward_pe': info.get('forwardPE', 0),
                    'market_cap': info.get('marketCap', 0),
                    'dividend': info.get('dividendYield', 0) * 100 if info.get('dividendYield') else 0,
                    'beta': info.get('beta', 0),
                    'eps': info.get('trailingEps', 0)
                }
            except Exception as e:
                return f"Error fetching data for {ticker}: {str(e)}"
        
        # Format comparison table
        col_width = 12
        output += f"{'Metric':<20} " + "  ".join([f"{t:>{col_width}}" for t in ticker_list]) + "\n"
        output += "=" * (20 + (col_width + 2) * len(ticker_list)) + "\n"
        
        # Price
        output += f"{'Price':<20} " + "  ".join([f"${metrics[t]['price']:>{col_width-1}.2f}" for t in ticker_list]) + "\n"
        
        # P/E Ratio
        output += f"{'P/E Ratio (TTM)':<20} " + "  ".join([
            f"{metrics[t]['pe']:>{col_width}.2f}" if metrics[t]['pe'] else f"{'N/A':>{col_width}}" 
            for t in ticker_list
        ]) + "\n"
        
        # Forward P/E
        output += f"{'Forward P/E':<20} " + "  ".join([
            f"{metrics[t]['forward_pe']:>{col_width}.2f}" if metrics[t]['forward_pe'] else f"{'N/A':>{col_width}}" 
            for t in ticker_list
        ]) + "\n"
        
        # EPS
        output += f"{'EPS (TTM)':<20} " + "  ".join([
            f"${metrics[t]['eps']:>{col_width-1}.2f}" if metrics[t]['eps'] else f"{'N/A':>{col_width}}" 
            for t in ticker_list
        ]) + "\n"
        
        # Market Cap
        output += f"{'Market Cap':<20} " + "  ".join([
            f"${metrics[t]['market_cap']/1e9:>{col_width-2}.1f}B" if metrics[t]['market_cap'] else f"{'N/A':>{col_width}}" 
            for t in ticker_list
        ]) + "\n"
        
        # Dividend Yield
        output += f"{'Dividend Yield':<20} " + "  ".join([
            f"{metrics[t]['dividend']:>{col_width-1}.2f}%" if metrics[t]['dividend'] else f"{'0.00%':>{col_width}}" 
            for t in ticker_list
        ]) + "\n"
        
        # Beta
        output += f"{'Beta':<20} " + "  ".join([
            f"{metrics[t]['beta']:>{col_width}.2f}" if metrics[t]['beta'] else f"{'N/A':>{col_width}}" 
            for t in ticker_list
        ]) + "\n"
        
        # Add interpretation
        output += "\n" + "=" * (20 + (col_width + 2) * len(ticker_list)) + "\n"
        output += "\nKey Insights:\n"
        
        # Find lowest P/E (best value if profitable)
        valid_pes = {t: metrics[t]['pe'] for t in ticker_list if metrics[t]['pe'] and metrics[t]['pe'] > 0}
        if valid_pes:
            lowest_pe_ticker = min(valid_pes, key=valid_pes.get)
            output += f"• Lowest P/E: {lowest_pe_ticker} ({valid_pes[lowest_pe_ticker]:.2f}) - Potentially undervalued\n"
        
        # Find highest dividend yield
        highest_div_ticker = max(ticker_list, key=lambda t: metrics[t]['dividend'])
        if metrics[highest_div_ticker]['dividend'] > 0:
            output += f"• Highest Dividend: {highest_div_ticker} ({metrics[highest_div_ticker]['dividend']:.2f}%) - Best for income\n"
        
        # Find largest market cap
        largest_cap_ticker = max(ticker_list, key=lambda t: metrics[t]['market_cap'])
        output += f"• Largest Company: {largest_cap_ticker} (${metrics[largest_cap_ticker]['market_cap']/1e9:.1f}B market cap)\n"
        
        return output
        
    except Exception as e:
        return f"Error comparing stocks: {str(e)}"