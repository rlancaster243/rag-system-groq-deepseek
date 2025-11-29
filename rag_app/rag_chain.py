"""
RAG chain implementation using LangChain.
Combines retrieval with LLM generation for grounded answering.
"""
from typing import Dict, List

from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser

from rag_app.models import get_llm
from rag_app.retrieval import retrieve_documents, format_sources
from rag_app.config import DEFAULT_K


# RAG prompt template
RAG_PROMPT_TEMPLATE = """You are a helpful assistant that answers questions based solely on the provided context.

IMPORTANT INSTRUCTIONS:
1. Use ONLY the information from the context below to answer the question
2. If the context does not contain enough information to answer the question, say "I don't have enough information in the provided documents to answer this question."
3. Always cite your sources using the format: [source: filename, type, location]
4. Be specific and accurate in your answers
5. Do not make up information or use external knowledge

CONTEXT:
{context}

QUESTION: {question}

ANSWER:"""


def format_documents(docs: List) -> str:
    """
    Format documents into a context string.

    Args:
        docs: List of Document objects

    Returns:
        Formatted context string
    """
    formatted = []
    for i, doc in enumerate(docs, 1):
        metadata = doc.metadata
        source = metadata.get("source", "Unknown")
        file_type = metadata.get("file_type", "Unknown")

        # Determine location
        location = "N/A"
        if "page" in metadata:
            location = f"Page {metadata['page']}"
        elif "cell_index" in metadata:
            location = f"Cell {metadata['cell_index']}"

        formatted.append(
            f"[Document {i}]\n"
            f"Source: {source} ({file_type}, {location})\n"
            f"Content: {doc.page_content}\n"
        )

    return "\n---\n".join(formatted)


def answer_question(question: str, k: int = DEFAULT_K) -> Dict[str, any]:
    """
    Answer a question using RAG.

    Args:
        question: Question to answer
        k: Number of documents to retrieve

    Returns:
        Dictionary containing:
            - answer: The generated answer
            - sources: List of source documents with metadata
            - retrieved_docs: Number of documents retrieved
    """
    # Retrieve relevant documents
    documents = retrieve_documents(question, k=k)

    if not documents:
        return {
            "answer": "No relevant documents found in the knowledge base.",
            "sources": [],
            "retrieved_docs": 0,
        }

    # Format context
    context = format_documents(documents)

    # Create prompt
    prompt = ChatPromptTemplate.from_template(RAG_PROMPT_TEMPLATE)

    # Get LLM
    llm = get_llm()

    # Create chain
    chain = (
        {
            "context": lambda x: context,
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    # Generate answer
    answer = chain.invoke(question)

    # Format sources
    sources = format_sources(documents)

    return {
        "answer": answer,
        "sources": sources,
        "retrieved_docs": len(documents),
    }
