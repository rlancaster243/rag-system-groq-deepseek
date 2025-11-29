# Sample Document for RAG System

## Introduction

This is a sample document to demonstrate the RAG (Retrieval Augmented Generation) system capabilities. The system uses Groq's DeepSeek R1 model combined with local embeddings to provide accurate, source-grounded answers.

## Key Features

### 1. Document Processing

The RAG system can process multiple document types:
- **PDF files**: Extracted page by page with metadata
- **Markdown files**: Like this one, with full formatting support
- **Text files**: Simple plain text documents
- **HTML files**: Web pages with cleaned content
- **Python source code**: Including docstrings and comments
- **Jupyter notebooks**: Extracting markdown and code cells

### 2. Intelligent Retrieval

The system uses semantic search to find relevant information:
- Documents are chunked into manageable pieces
- Each chunk is embedded using the BGE model
- Queries are matched against embeddings using cosine similarity
- Top-k most relevant chunks are retrieved

### 3. Grounded Generation

The DeepSeek R1 model generates answers that:
- Are based solely on retrieved context
- Include source citations
- Admit when information is insufficient
- Avoid hallucination

## Technical Architecture

### Embedding Model

The system uses **BAAI/bge-base-en-v1.5**, which is:
- A state-of-the-art embedding model
- Runs completely locally
- Produces 768-dimensional vectors
- Optimized for retrieval tasks

### Vector Store

**Chroma** is used for vector storage with:
- Persistent storage on disk
- Efficient similarity search
- Automatic deduplication
- Metadata filtering capabilities

### LLM Integration

**Groq** provides fast inference for:
- DeepSeek R1 Distill Llama 70B model
- Low-latency responses
- Reasoning capabilities
- Cost-effective API access

## Use Cases

This RAG system is ideal for:

1. **Knowledge Base QA**: Answer questions about internal documentation
2. **Research Assistant**: Query academic papers and reports
3. **Code Documentation**: Search through codebases and technical docs
4. **Customer Support**: Provide accurate answers from support materials
5. **Educational Tools**: Help students learn from course materials

## Example Queries

Here are some example questions you can ask:

- "What document types does the system support?"
- "How does the retrieval process work?"
- "What embedding model is used?"
- "Explain the technical architecture"
- "What are the main use cases?"

## Conclusion

This RAG system provides a powerful, production-ready solution for document-grounded question answering. It combines the best of retrieval and generation to deliver accurate, cited responses.
