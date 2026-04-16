import os
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
    Docstring for create_vectorstore
    
    :param docs: The documents to add to the vector store
    :type docs: list
    :param embeddings: The embeddings to use for the vector store
    :type embeddings: Any
    :return: The created vector store
    :rtype: PineconeVectorStore
    """
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

    vectorstore.add_documents(docs)

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