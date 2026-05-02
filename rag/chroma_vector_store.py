import time
from langchain_chroma import Chroma
from rag.embeddings import get_embeddings
from pathlib import Path


# Local storage path for ChromaDB
CHROMA_PATH = Path(__file__).parent.parent / "data" / "chroma_db"
CHROMA_PATH.mkdir(parents=True, exist_ok=True)


def _add_batch_with_retry(vectorstore, batch, batch_num, total_batches, max_retries=5):
    """Add a batch with exponential backoff on rate limit errors."""
    for attempt in range(max_retries):
        try:
            print(f"Processing batch {batch_num}/{total_batches} ({len(batch)} docs)...", end=" ")
            vectorstore.add_documents(batch)
            print("✓")
            return
        except Exception as e:
            if "rate_limit_exceeded" in str(e) or "429" in str(e):
                wait = 2 ** attempt  # 1s, 2s, 4s, 8s, 16s
                print(f"⏳ Rate limit hit, retrying in {wait}s... (attempt {attempt + 1}/{max_retries})")
                time.sleep(wait)
            else:
                raise
    raise RuntimeError(f"Batch {batch_num} failed after {max_retries} retries")


def create_vectorstore(docs, embeddings):
    """
    Create and populate ChromaDB vector store with retry logic.
    """
    print(f"Creating ChromaDB vector store with {len(docs)} documents...")

    vectorstore = Chroma(
        collection_name="sec_filings",
        embedding_function=embeddings,
        persist_directory=str(CHROMA_PATH)
    )

    batch_size = 100
    total_batches = (len(docs) + batch_size - 1) // batch_size

    for i in range(0, len(docs), batch_size):
        batch = docs[i:i + batch_size]
        batch_num = i // batch_size + 1
        _add_batch_with_retry(vectorstore, batch, batch_num, total_batches)
        # Small delay between batches to stay under TPM limits
        time.sleep(0.5)

    print(f"✅ All {total_batches} batches processed successfully!")
    print(f"📁 Data stored at: {CHROMA_PATH}")

    return vectorstore


def load_vectorstore(embeddings):
    """
    Load existing ChromaDB vector store.
    
    :param embeddings: The embeddings to use for the vector store
    :type embeddings: Any
    :return: The loaded vector store
    :rtype: Chroma
    """
    
    vectorstore = Chroma(
        collection_name="sec_filings",
        embedding_function=embeddings,
        persist_directory=str(CHROMA_PATH)
    )
    
    return vectorstore