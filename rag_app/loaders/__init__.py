"""
Document loaders for various file types.
Each loader returns LangChain Document objects with consistent metadata.
"""

from .pdf_loader import load_pdf
from .text_loader import load_text
from .html_loader import load_html
from .python_loader import load_python
from .notebook_loader import load_notebook

__all__ = [
    "load_pdf",
    "load_text",
    "load_html",
    "load_python",
    "load_notebook",
]
