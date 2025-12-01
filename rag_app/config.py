"""
Configuration module for RAG system.
All environment-specific settings are centralized here.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
CHROMA_PERSIST_DIR = PROJECT_ROOT / "chroma_store"
REPORTS_DIR = PROJECT_ROOT / "reports"

# Groq API configuration
# Try to get from Streamlit secrets first (for cloud deployment), then environment variables
try:
    import streamlit as st
    GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))
except (ImportError, FileNotFoundError, AttributeError):
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Note: We don't raise an error here anymore to allow imports to succeed
# Individual modules will check for the key when needed

# LLM configuration
DEFAULT_MODEL = "mixtral-8x7b-32768"
LLM_TEMPERATURE = 0.0

# Embedding configuration
EMBEDDING_MODEL = "BAAI/bge-base-en-v1.5"
EMBEDDING_DEVICE = "cpu"  # Change to "cuda" if GPU is available

# Chunking configuration
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Retrieval configuration
DEFAULT_K = 4  # Number of documents to retrieve

# Chroma configuration
CHROMA_COLLECTION_NAME = "rag_documents"

# Supported file extensions
SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".txt",
    ".md",
    ".html",
    ".htm",
    ".py",
    ".ipynb",
}
