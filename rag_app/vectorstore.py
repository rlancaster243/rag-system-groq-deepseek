"""
Vector store module using Chroma for persistent storage.
Handles document indexing, retrieval, and deduplication.
"""
from typing import List, Optional
import hashlib
from pathlib import Path

from langchain.vectorstores import Chroma
from langchain.schema import Document

from rag_app.config import CHROMA_PERSIST_DIR, CHROMA_COLLECTION_NAME
from rag_app.embeddings import get_embeddings


def _get_text_hash(text: str) -> str:
    """
    Generate a hash for text to detect duplicates.

    Args:
        text: Text to hash

    Returns:
        SHA256 hash of the text
    """
    return hashlib.sha256(text.encode()).hexdigest()


class VectorStore:
    """
    Wrapper around Chroma vector store with deduplication support.
    """

    def __init__(
        self,
        persist_directory: Optional[Path] = None,
        collection_name: str = CHROMA_COLLECTION_NAME,
    ):
        """
        Initialize the vector store.

        Args:
            persist_directory: Directory to persist the vector store
            collection_name: Name of the Chroma collection
        """
        self.persist_directory = persist_directory or CHROMA_PERSIST_DIR
        self.collection_name = collection_name
        self.embeddings = get_embeddings()
        self._vectorstore = None

    def _ensure_vectorstore(self):
        """Lazy initialization of the vector store."""
        if self._vectorstore is None:
            self.persist_directory.mkdir(parents=True, exist_ok=True)
            self._vectorstore = Chroma(
                collection_name=self.collection_name,
                embedding_function=self.embeddings,
                persist_directory=str(self.persist_directory),
            )

    def add_documents(self, documents: List[Document]) -> int:
        """
        Add documents to the vector store with deduplication.

        Args:
            documents: List of LangChain Document objects

        Returns:
            Number of documents actually added (after deduplication)
        """
        self._ensure_vectorstore()

        if not documents:
            return 0

        # Add content hash to metadata for deduplication
        for doc in documents:
            doc.metadata["content_hash"] = _get_text_hash(doc.page_content)

        # Get existing hashes
        try:
            existing_docs = self._vectorstore.get()
            existing_hashes = set()
            if existing_docs and "metadatas" in existing_docs:
                for metadata in existing_docs["metadatas"]:
                    if metadata and "content_hash" in metadata:
                        existing_hashes.add(metadata["content_hash"])
        except Exception:
            existing_hashes = set()

        # Filter out duplicates
        new_documents = [
            doc for doc in documents
            if doc.metadata["content_hash"] not in existing_hashes
        ]

        if new_documents:
            self._vectorstore.add_documents(new_documents)
            self._vectorstore.persist()

        return len(new_documents)

    def get_retriever(self, k: int = 4):
        """
        Get a retriever for querying the vector store.

        Args:
            k: Number of documents to retrieve

        Returns:
            LangChain retriever object
        """
        self._ensure_vectorstore()
        return self._vectorstore.as_retriever(search_kwargs={"k": k})

    def get_vectorstore(self) -> Chroma:
        """
        Get the underlying Chroma vector store.

        Returns:
            Chroma vector store instance
        """
        self._ensure_vectorstore()
        return self._vectorstore

    def clear(self):
        """Clear all documents from the vector store."""
        self._ensure_vectorstore()
        self._vectorstore.delete_collection()
        self._vectorstore = None

    def count(self) -> int:
        """
        Get the number of documents in the vector store.

        Returns:
            Number of documents
        """
        self._ensure_vectorstore()
        try:
            result = self._vectorstore.get()
            if result and "ids" in result:
                return len(result["ids"])
        except Exception:
            pass
        return 0


def get_vectorstore() -> VectorStore:
    """
    Factory function to get the configured vector store.

    Returns:
        VectorStore instance
    """
    return VectorStore()
