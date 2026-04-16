
def create_retriever(vectorstore):
    """
    Docstring for create_retriever
    
    :param vectorstore: The vector store to use for the retriever
    :type vectorstore: Any
    :return: The created retriever
    :rtype: Any
    """
    return vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 6,
            "fetch_k": 20
        }
    )