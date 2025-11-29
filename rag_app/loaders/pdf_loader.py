"""
PDF document loader.
Extracts text from PDF files with page-level metadata.
"""
from typing import List
from pathlib import Path

from langchain.document_loaders import PyPDFLoader
from langchain.schema import Document


def load_pdf(file_path: Path) -> List[Document]:
    """
    Load a PDF file and return documents with page metadata.

    Args:
        file_path: Path to the PDF file

    Returns:
        List of Document objects, one per page

    Raises:
        Exception: If the PDF cannot be loaded
    """
    try:
        loader = PyPDFLoader(str(file_path))
        documents = loader.load()

        # Enhance metadata
        for i, doc in enumerate(documents):
            doc.metadata.update({
                "source": str(file_path.name),
                "file_path": str(file_path),
                "file_type": "pdf",
                "page": i + 1,
            })

        return documents

    except Exception as e:
        raise Exception(f"Failed to load PDF {file_path}: {str(e)}")
