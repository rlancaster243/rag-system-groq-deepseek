"""
Retrieval module for querying the vector store.
"""
from typing import List, Dict

from langchain.schema import Document

from rag_app.config import DEFAULT_K
from rag_app.vectorstore import get_vectorstore


def retrieve_documents(query: str, k: int = DEFAULT_K) -> List[Document]:
    """
    Retrieve relevant documents for a query.

    Args:
        query: Query string
        k: Number of documents to retrieve

    Returns:
        List of relevant Document objects
    """
    vectorstore = get_vectorstore()
    retriever = vectorstore.get_retriever(k=k)
    documents = retriever.get_relevant_documents(query)
    return documents


def format_sources(documents: List[Document]) -> List[Dict]:
    """
    Format retrieved documents into a list of source dictionaries.

    Args:
        documents: List of Document objects

    Returns:
        List of dictionaries with source information
    """
    sources = []

    for doc in documents:
        metadata = doc.metadata
        source_info = {
            "filename": metadata.get("source", "Unknown"),
            "file_type": metadata.get("file_type", "Unknown"),
            "snippet": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
        }

        # Add location information based on file type
        if "page" in metadata:
            source_info["location"] = f"Page {metadata['page']}"
        elif "cell_index" in metadata:
            source_info["location"] = f"Cell {metadata['cell_index']}"
        elif "title" in metadata:
            source_info["location"] = f"Title: {metadata['title']}"
        else:
            source_info["location"] = "N/A"

        sources.append(source_info)

    return sources
