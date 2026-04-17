from langchain.tools import tool
from rag.vectorstore import load_vectorstore
from rag.embeddings import get_embeddings

@tool
def search_sec_filings(query: str, ticker: str = None) -> str:
    """
    Search SEC filings for relevant information based on a query and optional ticker symbol.
    Args:
        query (str): The search query to find relevant information in SEC filings.
        ticker (str, optional): The stock ticker symbol to filter results. Defaults to None.
    Returns:
        str: A formatted string containing the search results from SEC filings.
    """
    try:
        embeddings = get_embeddings()
        vector_store = load_vectorstore(embeddings)

        search_kwargs={
                "k": 5,
                "fetch_k": 20,
                "lambda_mult": 0.7
        }

        # Add Pinecone metadata filter for ticker
        if ticker:
            search_kwargs["filter"] = {"ticker": ticker.upper()}

        retriever = vector_store.as_retriever(
            search_type="mmr",
            search_kwargs=search_kwargs
        )
        
        results = retriever.invoke(query)
        
        if not results:
            ticker_msg = f" for {ticker}" if ticker else ""
            return f"No relevant information found{ticker_msg} for: {query}"
        
        # Format results
        output = f"SEC Filing Results for: {query}\n\n"
        
        for i, doc in enumerate(results, 1):
            metadata = doc.metadata
            output += f"--- Result {i} ---\n"
            output += f"Ticker: {metadata.get('ticker', 'N/A')}\n"
            output += f"Filing: {metadata.get('form', 'N/A')}\n"
            output += f"Date: {metadata.get('date', 'N/A')}\n"
            output += f"\nContent:\n{doc.page_content[:500]}...\n\n"
        
        return output
    except Exception as e:
        return f"Error searching SEC filings: {e}"
