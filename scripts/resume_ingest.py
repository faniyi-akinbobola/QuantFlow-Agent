import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from rag.ingest_sec import fetch_filings
from rag.chunking import split_documents
from rag.vectorstore import create_vectorstore
from langchain_core.documents import Document
from rag.embeddings import get_embeddings
from utils.loader import load_env_var

TICKERS = ["AAPL", "TSLA", "MSFT", "AMZN"]
START_BATCH = 40  # Resume from batch 40
BATCH_SIZE = 100

def resume_ingestion():
    """Resume ingestion from a specific batch."""
    
    # Re-fetch and chunk documents
    all_docs = []
    for ticker in TICKERS:
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
            print(f"Skipping {ticker}: {e}")
            continue
    
    chunked_docs = split_documents(all_docs)
    
    # Calculate which documents to process
    start_idx = (START_BATCH - 1) * BATCH_SIZE
    remaining_docs = chunked_docs[start_idx:]
    
    print(f"\n📊 Total chunks: {len(chunked_docs)}")
    print(f"✅ Already processed: batches 1-{START_BATCH-1} ({start_idx} docs)")
    print(f"⏳ Remaining: {len(remaining_docs)} docs")
    print(f"Starting from batch {START_BATCH}...\n")
    
    # Process remaining documents
    embeddings = get_embeddings()
    vectorstore = create_vectorstore(remaining_docs, embeddings)
    
    print("\n✅ Resume complete!")
    return vectorstore


if __name__ == "__main__":
    resume_ingestion()