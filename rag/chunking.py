import uuid
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_documents(documents: list[Document], chunk_size: int = 1500, chunk_overlap: int = 300) -> list[Document]:
    """
    Splits the input text into chunks of specified size with optional overlap.

    Args:
        documents (list[Document]): The input documents to be chunked.
        chunk_size (int): The maximum size of each chunk. Default is 1000 characters.
        chunk_overlap (int): The number of characters to overlap between chunks. Default is 200 characters.

    Returns:
        list[Document]: A list of chunked documents.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
        )  
    
    chunks = text_splitter.split_documents(documents)

    # Add unique chunk IDs to metadata
    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = str(uuid.uuid4())
        chunk.metadata["chunk_index"] = i
    
    return chunks
