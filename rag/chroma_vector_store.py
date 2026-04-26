import time
from langchain_chroma import Chroma
from rag.embeddings import get_embeddings
from pathlib import Path


# Local storage path for ChromaDB
CHROMA_PATH = Path(__file__).parent.parent / "data" / "chroma_db"
CHROMA_PATH.mkdir(parents=True, exist_ok=True)


def create_vectorstore(docs, embeddings):
    """
    Create and populate ChromaDB vector store with retry logic.
    
    :param docs: The documents to add to the vector store
    :type docs: list
    :param embeddings: The embeddings to use for the vector store
    :type embeddings: Any
    :return: The created vector store
    :rtype: Chroma
    """
    print(f"Creating ChromaDB vector store with {len(docs)} documents...")
    
    vectorstore = Chroma(
        collection_name="sec_filings",
        embedding_function=embeddings,
        persist_directory=str(CHROMA_PATH)
    )
    
    # Process in batches
    batch_size = 100
    total_batches = (len(docs) + batch_size - 1) // batch_size
    
    for i in range(0, len(docs), batch_size):
        batch = docs[i:i + batch_size]
        batch_num = i // batch_size + 1
        
        print(f"Processing batch {batch_num}/{total_batches} ({len(batch)} docs)...", end=" ")
        vectorstore.add_documents(batch)
        print("✓")
    
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