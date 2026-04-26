import time
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore  # Updated import
from rag.embeddings import DIMENSIONS, get_embeddings
from utils.loader import load_env_var


INDEX_NAME = load_env_var("PINECONE_INDEX_NAME")

# Initialize client
apikey = load_env_var("PINECONE_API_KEY")
pc = Pinecone(api_key=apikey)
embeddings = get_embeddings()

def create_vectorstore(docs, embeddings):
    """
    Create and populate Pinecone vector store with retry logic.
    
    :param docs: The documents to add to the vector store
    :type docs: list
    :param embeddings: The embeddings to use for the vector store
    :type embeddings: Any
    :return: The created vector store
    :rtype: PineconeVectorStore
    """
    print(f"Creating vector store with {len(docs)} documents...")
    # Create index if it doesn't exist
    if INDEX_NAME not in [i["name"] for i in pc.list_indexes()]:
        pc.create_index(
            name=INDEX_NAME,
            dimension=DIMENSIONS,  # OpenAI embedding size
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )

    index = pc.Index(INDEX_NAME)

    vectorstore = PineconeVectorStore(
        index=index,
        embedding=embeddings,
        text_key="text"
    )

        # Process in smaller batches with retry logic
    batch_size = 100
    max_retries = 5
    
    for i in range(0, len(docs), batch_size):
        batch = docs[i:i + batch_size]
        batch_num = i // batch_size + 1
        total_batches = (len(docs) + batch_size - 1) // batch_size
        
        for attempt in range(max_retries):
            try:
                print(f"Processing batch {batch_num}/{total_batches} ({len(batch)} docs)...", end=" ")
                vectorstore.add_documents(batch)
                print("✓")
                break  # Success, move to next batch
                
            except Exception as e:
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 10  # 5s, 10s, 15s
                    print(f"⚠️  Network error, retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    print(f"❌ Failed after {max_retries} attempts")
                    raise Exception(f"Failed to process batch {batch_num}: {e}")

    print(f"✅ All {total_batches} batches processed successfully!")

    return vectorstore

def load_vectorstore(embeddings):
    """
    Docstring for load_vectorstore
    
    :param embeddings: The embeddings to use for the vector store
    :type embeddings: Any
    :return: The loaded vector store
    :rtype: PineconeVectorStore
    """
    
    index = pc.Index(INDEX_NAME)

    vectorstore = PineconeVectorStore(
        index=index,
        embedding=embeddings,
        text_key="text"
    )

    return vectorstore