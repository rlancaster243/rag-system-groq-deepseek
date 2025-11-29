"""
Text and Markdown document loader.
Handles .txt and .md files.
"""
from typing import List
from pathlib import Path

from langchain.schema import Document


def load_text(file_path: Path) -> List[Document]:
    """
    Load a text or markdown file.

    Args:
        file_path: Path to the text file

    Returns:
        List containing a single Document object

    Raises:
        Exception: If the file cannot be loaded
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Determine file type
        file_type = "markdown" if file_path.suffix.lower() == ".md" else "text"

        document = Document(
            page_content=content,
            metadata={
                "source": str(file_path.name),
                "file_path": str(file_path),
                "file_type": file_type,
            }
        )

        return [document]

    except Exception as e:
        raise Exception(f"Failed to load text file {file_path}: {str(e)}")
