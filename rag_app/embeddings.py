"""
Embeddings module using local sentence-transformers.
Provides BGE embeddings without relying on external APIs.
"""
from typing import List
from sentence_transformers import SentenceTransformer
from langchain.embeddings.base import Embeddings
from rag_app.config import EMBEDDING_MODEL, EMBEDDING_DEVICE


class LocalEmbeddings(Embeddings):
    """
    Local embeddings using sentence-transformers BGE model.
    Implements LangChain's Embeddings interface for compatibility.
    """

    def __init__(self, model_name: str = EMBEDDING_MODEL, device: str = EMBEDDING_DEVICE):
        """
        Initialize the local embedding model.

        Args:
            model_name: Name of the sentence-transformers model
            device: Device to run the model on ('cpu' or 'cuda')
        """
        self.model = SentenceTransformer(model_name, device=device)
        self.model_name = model_name

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Embed a list of documents.

        Args:
            texts: List of text strings to embed

        Returns:
            List of embedding vectors
        """
        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=False,
        )
        return embeddings.tolist()

    def embed_query(self, text: str) -> List[float]:
        """
        Embed a single query string.

        Args:
            text: Query text to embed

        Returns:
            Embedding vector
        """
        embedding = self.model.encode(
            text,
            normalize_embeddings=True,
            show_progress_bar=False,
        )
        return embedding.tolist()


def get_embeddings() -> LocalEmbeddings:
    """
    Factory function to get the configured embeddings model.

    Returns:
        LocalEmbeddings instance
    """
    return LocalEmbeddings()
