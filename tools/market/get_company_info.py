from langchain.tools import tool
import yfinance as yf


@tool
def get_company_info(ticker: str) -> str:
    """
    Get company information including sector, industry, and description.
    
    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'TSLA', 'MSFT')
        
    Returns:
        Company overview with name, sector, industry, employees, and business summary
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Extract company information
        company_name = info.get('longName', info.get('shortName', ticker))
        sector = info.get('sector', 'N/A')
        industry = info.get('industry', 'N/A')
        employees = info.get('fullTimeEmployees', 'N/A')
        description = info.get('longBusinessSummary', 'No description available')
        website = info.get('website', 'N/A')
        headquarters = f"{info.get('city', '')}, {info.get('state', '')} {info.get('country', '')}".strip(', ')
        
        # Format output
        output = f"Company Information for {ticker}:\n\n"
        output += f"Name: {company_name}\n"
        output += f"Sector: {sector}\n"
        output += f"Industry: {industry}\n"
        output += f"Employees: {employees:,}\n" if employees != 'N/A' else f"Employees: {employees}\n"
        output += f"Headquarters: {headquarters}\n"
        output += f"Website: {website}\n"
        output += f"\nBusiness Description:\n{description[:500]}..."  # Limit to 500 chars
        
        return output
        
    except Exception as e:
        return f"Error fetching company info for {ticker}: {str(e)}"