"""
HTML document loader.
Extracts visible text from HTML files using BeautifulSoup.
"""
from typing import List
from pathlib import Path

from bs4 import BeautifulSoup
from langchain.schema import Document


def load_html(file_path: Path) -> List[Document]:
    """
    Load an HTML file and extract visible text.

    Args:
        file_path: Path to the HTML file

    Returns:
        List containing a single Document object

    Raises:
        Exception: If the file cannot be loaded
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        soup = BeautifulSoup(html_content, "html.parser")

        # Remove script and style elements
        for element in soup(["script", "style", "nav", "footer", "header"]):
            element.decompose()

        # Extract title
        title = soup.title.string if soup.title else file_path.stem

        # Get visible text
        text = soup.get_text(separator="\n", strip=True)

        # Clean up excessive whitespace
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        content = "\n".join(lines)

        document = Document(
            page_content=content,
            metadata={
                "source": str(file_path.name),
                "file_path": str(file_path),
                "file_type": "html",
                "title": title,
            }
        )

        return [document]

    except Exception as e:
        raise Exception(f"Failed to load HTML file {file_path}: {str(e)}")
