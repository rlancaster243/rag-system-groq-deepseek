"""
Basic tests for the RAG pipeline.
Tests core functionality without requiring external dependencies.
"""
import pytest
from pathlib import Path
import tempfile
import shutil

from langchain.schema import Document

from rag_app.config import CHUNK_SIZE, CHUNK_OVERLAP
from rag_app.ingest import chunk_documents
from rag_app.loaders import load_text, load_html, load_python


def test_chunk_documents():
    """Test document chunking."""
    # Create a long document
    long_text = "This is a test sentence. " * 100
    doc = Document(
        page_content=long_text,
        metadata={"source": "test.txt"}
    )

    # Chunk it
    chunks = chunk_documents([doc])

    # Verify chunks were created
    assert len(chunks) > 1
    assert all(len(chunk.page_content) <= CHUNK_SIZE + CHUNK_OVERLAP for chunk in chunks)
    assert all(chunk.metadata["source"] == "test.txt" for chunk in chunks)


def test_load_text():
    """Test text file loading."""
    # Create a temporary text file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write("This is a test document.\nIt has multiple lines.")
        temp_path = Path(f.name)

    try:
        # Load the file
        docs = load_text(temp_path)

        # Verify
        assert len(docs) == 1
        assert "test document" in docs[0].page_content
        assert docs[0].metadata["file_type"] == "text"
    finally:
        temp_path.unlink()


def test_load_html():
    """Test HTML file loading."""
    html_content = """
    <html>
        <head><title>Test Page</title></head>
        <body>
            <h1>Test Heading</h1>
            <p>This is a test paragraph.</p>
            <script>console.log('should be removed');</script>
        </body>
    </html>
    """

    # Create a temporary HTML file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False) as f:
        f.write(html_content)
        temp_path = Path(f.name)

    try:
        # Load the file
        docs = load_html(temp_path)

        # Verify
        assert len(docs) == 1
        assert "Test Heading" in docs[0].page_content
        assert "test paragraph" in docs[0].page_content
        assert "should be removed" not in docs[0].page_content  # Script removed
        assert docs[0].metadata["file_type"] == "html"
        assert docs[0].metadata["title"] == "Test Page"
    finally:
        temp_path.unlink()


def test_load_python():
    """Test Python file loading."""
    python_content = '''
"""
This is a module docstring.
"""

def test_function():
    """This is a function docstring."""
    return 42

class TestClass:
    """This is a class docstring."""
    pass
'''

    # Create a temporary Python file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(python_content)
        temp_path = Path(f.name)

    try:
        # Load the file
        docs = load_python(temp_path)

        # Verify
        assert len(docs) == 1
        assert "module docstring" in docs[0].page_content
        assert "function docstring" in docs[0].page_content
        assert "class docstring" in docs[0].page_content
        assert docs[0].metadata["file_type"] == "python"
        assert docs[0].metadata["is_code"] is True
    finally:
        temp_path.unlink()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
