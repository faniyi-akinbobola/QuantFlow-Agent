# from edgar import Company, set_identity
# from utils.loader import load_env_var
# from typing import List, Dict
    
# def fetch_filings(ticker: str, num_10k: int = 3, num_10q: int = 2) -> List[Dict]:
#     """
#     Fetch SEC filings for a given ticker using edgar library.
    
#     Args:
#         ticker: Stock ticker symbol
#         num_10k: Number of 10-K filings to fetch
#         num_10q: Number of 10-Q filings to fetch
        
#     Returns:
#         List of documents with text and metadata
        
#     Raises:
#         ValueError: If filings cannot be fetched
#     """

#     name = load_env_var("NAME", default="Stock Agent")
#     email = load_env_var("EMAIL")
#     set_identity(f"{name} {email}")
    
#     try:
#         company = Company(ticker)

#         ten_ks = company.get_filings(form="10-K").head(num_10k)
#         ten_qs = company.get_filings(form="10-Q").head(num_10q)

#         docs = []

#         for filing in list(ten_ks) + list(ten_qs):
#             try:
#                 print(f" {ticker} | {filing.form} | {filing.filing_date}")
                
#                 # Get the filing text using the correct API
#                 filing_obj = filing.obj()
                
#                 # Try different methods to extract text
#                 if hasattr(filing_obj, 'text'):
#                     text = filing_obj.text
#                 elif hasattr(filing_obj, 'get_text'):
#                     text = filing_obj.get_text()
#                 else:
#                     # Fallback: get the raw HTML and extract text
#                     text = filing.html()
                
#                 if not text or len(text.strip()) < 100:
#                     print(f"  ⚠️  Skipping empty/invalid filing")
#                     continue
                
#                 docs.append({
#                     "text": text,
#                     "metadata": {
#                         "ticker": ticker.upper(),
#                         "form": filing.form,
#                         "date": str(filing.filing_date),
#                         "year": str(filing.filing_date)[:4],
#                         "accession_number": filing.accession_number,
#                     }
#                 })
                
#             except Exception as e:
#                 print(f"  Failed to process filing: {e}")
#                 continue
        
#         if not docs:
#             raise ValueError(f"No valid filings found for {ticker}")
        
#         print(f"✓ Fetched {len(docs)} filings for {ticker}")
#         return docs

#     except Exception as e:
#         raise ValueError(f"Error fetching filings for {ticker}: {e}")

from edgar import Company, set_identity
from utils.loader import load_env_var
from typing import List, Dict
import re
from bs4 import BeautifulSoup


def clean_html(html_text: str) -> str:
    """Remove HTML tags and clean text using BeautifulSoup."""
    try:
        # Parse HTML with lxml parser (faster and more robust)
        soup = BeautifulSoup(html_text, 'lxml')
        
        # Remove script, style, and other non-content tags
        for element in soup(['script', 'style', 'meta', 'link', 'noscript']):
            element.decompose()
        
        # Get text
        text = soup.get_text(separator=' ', strip=True)
        
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove common artifacts
        text = text.replace('&nbsp;', ' ')
        text = text.replace('&amp;', '&')
        text = text.replace('&lt;', '<')
        text = text.replace('&gt;', '>')
        text = text.replace('\xa0', ' ')
        
        return text.strip()
    except Exception as e:
        print(f"    ⚠️  HTML cleaning failed ({e}), using fallback")
        # Fallback: simple regex
        text = re.sub(r'<[^>]+>', ' ', html_text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()


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
                
                # Get HTML and clean it
                try:
                    html = filing.html()
                    text = clean_html(html)
                except Exception as e:
                    print(f"  ⚠️  Could not extract text: {e}")
                    continue
                
                # Validate text quality
                if not text or len(text.strip()) < 500:
                    print(f"  ⚠️  Skipping - text too short ({len(text)} chars)")
                    continue
                
                # Check if cleaning worked (should have very few < or > symbols)
                html_symbols = text.count('<') + text.count('>')
                if html_symbols > 10:
                    print(f"  ⚠️  Warning: Still contains {html_symbols} HTML symbols")
                
                # Limit length to avoid massive documents
                if len(text) > 1_000_000:  # 1MB limit
                    print(f"  ⚠️  Truncating from {len(text):,} to 1,000,000 chars")
                    text = text[:1_000_000]
                
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
                print(f"  ✓ Extracted {len(text):,} clean characters")
                
            except Exception as e:
                print(f"  ⚠️  Failed to process filing: {e}")
                continue
        
        if not docs:
            raise ValueError(f"No valid filings found for {ticker}")
        
        print(f"✅ Fetched {len(docs)} filings for {ticker}\n")
        return docs

    except Exception as e:
        raise ValueError(f"Error fetching filings for {ticker}: {e}")