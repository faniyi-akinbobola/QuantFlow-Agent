import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from time import time
from rag.ingest_sec import fetch_filings
from rag.chunking import split_documents
# from rag.vectorstore import create_vectorstore
from rag.chroma_vector_store import create_vectorstore
from langchain_core.documents import Document
from rag.embeddings import get_embeddings
from pinecone import Pinecone, ServerlessSpec
from utils.loader import load_env_var

TICKERS = ["AAPL", "TSLA", "MSFT", "AMZN"]

# TICKERS = [
#     # Tech Giants
#     "AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "TSLA", "NFLX",
#     
#     # Finance
#     "JPM", "V", "MA", "BAC",
#     
#     # Healthcare
#     "JNJ", "UNH", "LLY",
#     
#     # Consumer
#     "WMT", "PG", "KO", "PEP",
# ]

def ensure_index_exists():
    """Create Pinecone index if it doesn't exist."""
    api_key = load_env_var("PINECONE_API_KEY")
    index_name = load_env_var("PINECONE_INDEX_NAME")
    
    pc = Pinecone(api_key=api_key)
    
    existing_indexes = [idx.name for idx in pc.list_indexes()]
    
    if index_name in existing_indexes:
        print(f"✅ Index '{index_name}' already exists")
        return
    
    print(f"Creating index '{index_name}'...")
    pc.create_index(
        name=index_name,
        dimension=3072,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )
    
    print("⏳ Waiting for index to be ready...")
    while True:
        status = pc.describe_index(index_name)
        if status.status['ready']:
            break
        time.sleep(1)
    
    print("✅ Index created and ready!")

def run(tickers: list[str] = TICKERS):
    """
    Ingest SEC filings for specified tickers into Pinecone vector store.
    
    Args:
        tickers: List of stock ticker symbols to process
        
    Returns:
        PineconeVectorStore instance
    """
    # ensure_index_exists()
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