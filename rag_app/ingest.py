"""
Document ingestion orchestration.
Discovers files, routes to appropriate loaders, chunks, and indexes.
"""
from typing import List, Dict
from pathlib import Path

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

from rag_app.config import (
    DATA_DIR,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    SUPPORTED_EXTENSIONS,
)
from rag_app.loaders import (
    load_pdf,
    load_text,
    load_html,
    load_python,
    load_notebook,
)
from rag_app.vectorstore import get_vectorstore


# Mapping of file extensions to loader functions
LOADER_MAP = {
    ".pdf": load_pdf,
    ".txt": load_text,
    ".md": load_text,
    ".html": load_html,
    ".htm": load_html,
    ".py": load_python,
    ".ipynb": load_notebook,
}


def discover_files(data_dir: Path = DATA_DIR) -> List[Path]:
    """
    Recursively discover all supported files in the data directory.

    Args:
        data_dir: Directory to search for files

    Returns:
        List of file paths
    """
    files = []
    for ext in SUPPORTED_EXTENSIONS:
        files.extend(data_dir.rglob(f"*{ext}"))
    return sorted(files)


def load_document(file_path: Path) -> List[Document]:
    """
    Load a document using the appropriate loader.

    Args:
        file_path: Path to the file

    Returns:
        List of Document objects

    Raises:
        ValueError: If file type is not supported
    """
    ext = file_path.suffix.lower()
    loader = LOADER_MAP.get(ext)

    if not loader:
        raise ValueError(f"Unsupported file type: {ext}")

    return loader(file_path)


def chunk_documents(documents: List[Document]) -> List[Document]:
    """
    Split documents into chunks for embedding.

    Args:
        documents: List of Document objects

    Returns:
        List of chunked Document objects
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    chunked_docs = text_splitter.split_documents(documents)
    return chunked_docs


def ingest_documents(data_dir: Path = DATA_DIR, verbose: bool = True) -> Dict[str, int]:
    """
    Main ingestion pipeline: discover, load, chunk, and index documents.

    Args:
        data_dir: Directory containing documents to ingest
        verbose: Whether to print progress information

    Returns:
        Dictionary with ingestion statistics
    """
    if verbose:
        print(f"🔍 Discovering files in {data_dir}...")

    files = discover_files(data_dir)

    if not files:
        print(f"⚠️  No supported files found in {data_dir}")
        print(f"   Supported extensions: {', '.join(SUPPORTED_EXTENSIONS)}")
        return {"files_found": 0, "documents_loaded": 0, "chunks_created": 0, "chunks_added": 0}

    if verbose:
        print(f"📁 Found {len(files)} file(s)")

    # Load all documents
    all_documents = []
    for file_path in files:
        try:
            if verbose:
                print(f"   Loading: {file_path.name}")
            docs = load_document(file_path)
            all_documents.extend(docs)
        except Exception as e:
            print(f"   ❌ Error loading {file_path.name}: {str(e)}")

    if verbose:
        print(f"📄 Loaded {len(all_documents)} document(s)")

    # Chunk documents
    if verbose:
        print(f"✂️  Chunking documents...")
    chunked_docs = chunk_documents(all_documents)

    if verbose:
        print(f"📦 Created {len(chunked_docs)} chunk(s)")

    # Index in vector store
    if verbose:
        print(f"💾 Indexing in vector store...")

    vectorstore = get_vectorstore()
    added_count = vectorstore.add_documents(chunked_docs)

    if verbose:
        print(f"✅ Added {added_count} new chunk(s) (duplicates skipped)")
        print(f"📊 Total documents in store: {vectorstore.count()}")

    return {
        "files_found": len(files),
        "documents_loaded": len(all_documents),
        "chunks_created": len(chunked_docs),
        "chunks_added": added_count,
    }
