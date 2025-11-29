"""
FastAPI server for the RAG system.
Provides HTTP endpoints for querying the knowledge base.
"""
from typing import List, Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from rag_app.rag_chain import answer_question
from rag_app.config import DEFAULT_K


# Pydantic models for request/response
class QueryRequest(BaseModel):
    """Request model for query endpoint."""
    question: str = Field(..., description="Question to ask", min_length=1)
    k: int = Field(DEFAULT_K, description="Number of documents to retrieve", ge=1, le=20)


class SourceInfo(BaseModel):
    """Model for source information."""
    filename: str
    file_type: str
    location: str
    snippet: str


class QueryResponse(BaseModel):
    """Response model for query endpoint."""
    answer: str
    sources: List[SourceInfo]
    retrieved_docs: int


class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str
    message: str


# Create FastAPI app
app = FastAPI(
    title="RAG System API",
    description="Retrieval Augmented Generation API using Groq and DeepSeek R1",
    version="1.0.0",
)


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.

    Returns:
        Health status
    """
    return {
        "status": "healthy",
        "message": "RAG system is operational"
    }


@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """
    Query the RAG system with a question.

    Args:
        request: Query request with question and optional k parameter

    Returns:
        Answer with sources

    Raises:
        HTTPException: If query processing fails
    """
    try:
        result = answer_question(request.question, k=request.k)

        return QueryResponse(
            answer=result["answer"],
            sources=[SourceInfo(**source) for source in result["sources"]],
            retrieved_docs=result["retrieved_docs"]
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "RAG System API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "query": "/query (POST)",
            "docs": "/docs",
        }
    }
