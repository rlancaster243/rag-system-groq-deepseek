"""
Jupyter Notebook loader.
Extracts markdown cells and code comments from .ipynb files.
"""
from typing import List
from pathlib import Path
import json

import nbformat
from langchain.schema import Document


def load_notebook(file_path: Path) -> List[Document]:
    """
    Load a Jupyter notebook and extract content from cells.

    Args:
        file_path: Path to the .ipynb file

    Returns:
        List of Document objects, one per cell with content

    Raises:
        Exception: If the notebook cannot be loaded
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            notebook = nbformat.read(f, as_version=4)

        documents = []

        for cell_index, cell in enumerate(notebook.cells):
            content = None
            cell_type = cell.cell_type

            if cell_type == "markdown":
                # Include all markdown cells
                content = cell.source

            elif cell_type == "code":
                # Extract comments and docstrings from code cells
                lines = cell.source.split("\n")
                comments = []

                for line in lines:
                    stripped = line.strip()
                    # Extract comment lines
                    if stripped.startswith("#"):
                        comments.append(stripped)
                    # Extract docstrings (simplified)
                    elif '"""' in stripped or "'''" in stripped:
                        comments.append(stripped)

                if comments:
                    content = "\n".join(comments)

            # Create document if we have content
            if content and content.strip():
                document = Document(
                    page_content=content,
                    metadata={
                        "source": str(file_path.name),
                        "file_path": str(file_path),
                        "file_type": "notebook",
                        "cell_index": cell_index,
                        "cell_type": cell_type,
                    }
                )
                documents.append(document)

        # If no cells had content, create a single document with notebook name
        if not documents:
            document = Document(
                page_content=f"Jupyter Notebook: {file_path.name}",
                metadata={
                    "source": str(file_path.name),
                    "file_path": str(file_path),
                    "file_type": "notebook",
                    "cell_count": len(notebook.cells),
                }
            )
            documents.append(document)

        return documents

    except Exception as e:
        raise Exception(f"Failed to load notebook {file_path}: {str(e)}")
