# from langchain.tools import tool
# from rag.vectorstore import load_vectorstore
# from rag.embeddings import get_embeddings
# import re
# from bs4 import BeautifulSoup

# def clean_html(html_text: str) -> str:
#     """Remove HTML tags and clean text."""
#     try:
#         soup = BeautifulSoup(html_text, 'html.parser')
#         for script in soup(["script", "style"]):
#             script.decompose()
#         text = soup.get_text()
#         lines = (line.strip() for line in text.splitlines())
#         chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
#         text = '\n'.join(chunk for chunk in chunks if chunk)
#         return text
#     except:
#         text = re.sub(r'<[^>]+>', ' ', html_text)
#         text = re.sub(r'\s+', ' ', text)
#         return text.strip()

# @tool
# def search_sec_filings(query: str, ticker: str = None) -> str:
#     """
#     Search SEC filings for relevant information based on a query and optional ticker symbol.
#     Args:
#         query (str): The search query to find relevant information in SEC filings.
#         ticker (str, optional): The stock ticker symbol to filter results. Defaults to None.
#     Returns:
#         str: A formatted string containing the search results from SEC filings.
#     """
#     try:
#         embeddings = get_embeddings()
#         vector_store = load_vectorstore(embeddings)

#         search_kwargs={
#                 "k": 5,
#                 "fetch_k": 20,
#                 "lambda_mult": 0.7
#         }

#         # Add Pinecone metadata filter for ticker
#         if ticker:
#             search_kwargs["filter"] = {"ticker": ticker.upper()}

#         retriever = vector_store.as_retriever(
#             search_type="mmr",
#             search_kwargs=search_kwargs
#         )
        
#         results = retriever.invoke(query)
        
#         if not results:
#             ticker_msg = f" for {ticker}" if ticker else ""
#             return f"No relevant information found{ticker_msg} for: {query}"
        
#         # Format results
#         output = f"SEC Filing Results for: {query}\n\n"
        
#         for i, doc in enumerate(results, 1):
#             # Clean HTML from content
#             content = clean_html(doc.page_content)
            
#             # Truncate to reasonable length
#             content = content[:500] + "..." if len(content) > 500 else content

#             metadata = doc.metadata
#             output += f"--- Result {i} ---\n"
#             output += f"Ticker: {metadata.get('ticker', 'N/A')}\n"
#             output += f"Filing: {metadata.get('form', 'N/A')}\n"
#             output += f"Date: {metadata.get('date', 'N/A')}\n"
#             output += f"\nContent:\n{doc.page_content[:500]}...\n\n"
        
#         return output
#     except Exception as e:
#         return f"Error searching SEC filings: {e}"

from langchain.tools import tool
from rag.vectorstore import load_vectorstore
from rag.embeddings import get_embeddings
import re


def clean_html(text: str) -> str:
    """Remove HTML tags and clean text."""
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', ' ', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove common HTML entities
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&amp;', '&')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    return text.strip()


@tool
def search_sec_filings(query: str, ticker: str, top_k: int = 5) -> str:
    """
    Search SEC filings (10-K and 10-Q) for a given stock ticker.
    
    Args:
        query: The search query (e.g., "risk factors", "revenue breakdown")
        ticker: Stock ticker symbol (e.g., 'AAPL', 'TSLA')
        top_k: Number of results to return (default: 5)
        
    Returns:
        Relevant excerpts from SEC filings
    """
    try:
        embeddings = get_embeddings()
        vectorstore = load_vectorstore(embeddings)
        
        # Search with metadata filter
        results = vectorstore.similarity_search(
            query,
            k=top_k,
            filter={"ticker": ticker.upper()}
        )
        
        if not results:
            return f"No relevant SEC filings found for {ticker.upper()}"
        
        # Format results with HTML cleaning
        output = f"SEC Filing Results for {ticker.upper()}: {query}\n\n"
        
        for i, doc in enumerate(results, 1):
            # Clean HTML from content
            content = clean_html(doc.page_content)
            
            # Truncate to reasonable length
            if len(content) > 800:
                content = content[:800] + "..."
            
            metadata = doc.metadata
            output += f"--- Excerpt {i} ---\n"
            output += f"Source: {metadata.get('form', 'N/A')} filed on {metadata.get('date', 'N/A')}\n\n"
            output += f"{content}\n\n"
        
        return output
        
    except Exception as e:
        return f"Error searching SEC filings for {ticker}: {str(e)}"