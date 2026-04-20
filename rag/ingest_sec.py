from edgar import Company, set_identity
from utils.loader import load_env_var
from typing import List, Dict
    
def fetch_filings(ticker: str, num_10k: int = 3, num_10q: int = 2) -> List[Dict]:
    """
    Fetch SEC filings for a given ticker using edgar library.
    
    Args:
        ticker: Stock ticker symbol
        num_10k: Number of 10-K filings to fetch
        num_10q: Number of 10-Q filings to fetch
        
    Returns:
        List of documents with text and metadata
        
    Raises:
        ValueError: If filings cannot be fetched
    """

    name = load_env_var("NAME", default="Stock Agent")
    email = load_env_var("EMAIL")
    set_identity(f"{name} {email}")
    
    try:
        company = Company(ticker)

        ten_ks = company.get_filings(form="10-K").head(num_10k)
        ten_qs = company.get_filings(form="10-Q").head(num_10q)

        docs = []

        for filing in list(ten_ks) + list(ten_qs):
            try:
                print(f" {ticker} | {filing.form} | {filing.filing_date}")
                
                # Get the filing text using the correct API
                filing_obj = filing.obj()
                
                # Try different methods to extract text
                if hasattr(filing_obj, 'text'):
                    text = filing_obj.text
                elif hasattr(filing_obj, 'get_text'):
                    text = filing_obj.get_text()
                else:
                    # Fallback: get the raw HTML and extract text
                    text = filing.html()
                
                if not text or len(text.strip()) < 100:
                    print(f"  ⚠️  Skipping empty/invalid filing")
                    continue
                
                docs.append({
                    "text": text,
                    "metadata": {
                        "ticker": ticker.upper(),
                        "form": filing.form,
                        "date": str(filing.filing_date),
                        "year": str(filing.filing_date)[:4],
                        "accession_number": filing.accession_number,
                    }
                })
                
            except Exception as e:
                print(f"  Failed to process filing: {e}")
                continue
        
        if not docs:
            raise ValueError(f"No valid filings found for {ticker}")
        
        print(f"✓ Fetched {len(docs)} filings for {ticker}")
        return docs

    except Exception as e:
        raise ValueError(f"Error fetching filings for {ticker}: {e}")