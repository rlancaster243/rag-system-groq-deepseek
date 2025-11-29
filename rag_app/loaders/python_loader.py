"""
Python source code loader.
Extracts code, comments, and docstrings from .py files.
"""
from typing import List
from pathlib import Path
import ast

from langchain.schema import Document


def load_python(file_path: Path) -> List[Document]:
    """
    Load a Python source file and extract code with metadata.

    Args:
        file_path: Path to the Python file

    Returns:
        List containing a single Document object

    Raises:
        Exception: If the file cannot be loaded
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source_code = f.read()

        # Try to parse the AST to extract docstrings
        docstrings = []
        try:
            tree = ast.parse(source_code)
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Module)):
                    docstring = ast.get_docstring(node)
                    if docstring:
                        docstrings.append(docstring)
        except SyntaxError:
            # If parsing fails, just use the raw source
            pass

        # Combine source code with extracted docstrings
        content_parts = []

        if docstrings:
            content_parts.append("=== Docstrings ===\n")
            content_parts.append("\n\n".join(docstrings))
            content_parts.append("\n\n=== Source Code ===\n")

        content_parts.append(source_code)
        content = "".join(content_parts)

        document = Document(
            page_content=content,
            metadata={
                "source": str(file_path.name),
                "file_path": str(file_path),
                "file_type": "python",
                "is_code": True,
                "docstring_count": len(docstrings),
            }
        )

        return [document]

    except Exception as e:
        raise Exception(f"Failed to load Python file {file_path}: {str(e)}")
