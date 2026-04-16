from rag.ingest_sec import fetch_filings
from rag.chunking import split_documents
from rag.vectorstore import create_vectorstore
from langchain_core.documents import Document
from rag.embeddings import get_embeddings

TICKERS = ["AAPL", "TSLA", "MSFT", "AMZN"]

def run(tickers: list[str] = TICKERS):
    """
    Ingest SEC filings for specified tickers into Pinecone vector store.
    
    Args:
        tickers: List of stock ticker symbols to process
        
    Returns:
        PineconeVectorStore instance
    """
    all_docs = []
    failed_tickers = []

    print(f"Fetching filings for {len(tickers)} tickers...")

    for i, ticker in enumerate(tickers, 1) :
        print(f"Processing {ticker} ({i}/{len(tickers)})")

        try:    
            raw_docs = fetch_filings(ticker)

            for d in raw_docs:
                all_docs.append(
                    Document(
                        page_content=d["text"],
                        metadata=d["metadata"]
                    )
                )
        except Exception as e:
            print(f"Failed to fetch filings for {ticker}: {e}")
            failed_tickers.append(ticker)
            continue
        
    if not all_docs:
        raise ValueError("No documents were fetched. Please check the tickers and try again.")
    
    print(f"Fetched {len(all_docs)} documents. Now chunking...")
    chunked_docs = split_documents(all_docs)

    
    print(f"Chunked into {len(chunked_docs)} chunks. Now creating vector store...")

    print("creating vector store...")
    embeddings = get_embeddings()
    vectorstore = create_vectorstore(chunked_docs, embeddings)
    print("Vector store created successfully.")

    print(f"\n✅ Ingestion complete!")
    print(f"   - Successfully processed: {len(tickers) - len(failed_tickers)} tickers")
    if failed_tickers:
        print(f"   - Failed: {failed_tickers}")
    
    return vectorstore

if __name__ == "__main__":
    run()