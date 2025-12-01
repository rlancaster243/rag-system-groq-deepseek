# RAG System Project Summary

## Project Overview

A complete, production-ready **Retrieval Augmented Generation (RAG)** system has been successfully built and deployed to GitHub. The system leverages Groq's GPT-OSS 20B model combined with local open-source embeddings to provide accurate, document-grounded question answering.

## GitHub Repository

**Repository URL**: https://github.com/rlancaster243/rag-system-groq-deepseek

The repository is public and immediately ready for cloning, collaboration, and deployment.

## Technical Stack

### Core Technologies

The system is built with a carefully selected technology stack that balances performance, cost, and maintainability:

**LLM Provider**: Groq API provides ultra-fast inference for the GPT-OSS 20B model, a reasoning-optimized language model that excels at grounded question answering.

**Embeddings**: The BAAI/bge-base-en-v1.5 model from sentence-transformers runs completely locally, eliminating external API dependencies and costs for embedding generation. This 768-dimensional embedding model is specifically optimized for retrieval tasks.

**Vector Database**: Chroma provides persistent vector storage with efficient similarity search, automatic deduplication, and metadata filtering. The database is stored locally in the `chroma_store/` directory.

**Orchestration**: LangChain handles the RAG pipeline orchestration, including document loading, text splitting, retrieval, and prompt management.

**Web Frameworks**: FastAPI powers the HTTP API with automatic OpenAPI documentation, while Streamlit provides an interactive web interface for end users.

## System Architecture

### Document Ingestion Pipeline

The ingestion pipeline follows a systematic approach to process diverse document types. Documents are first discovered recursively in the `data/` directory, with support for PDF, text, Markdown, HTML, Python source files, and Jupyter notebooks. Each file type has a dedicated loader that extracts content while preserving important metadata such as page numbers, cell indices, and document structure.

After loading, documents are chunked using a recursive character text splitter with configurable chunk size (1000 characters) and overlap (200 characters). This chunking strategy ensures that semantic context is preserved across chunk boundaries. Each chunk is then embedded using the local BGE model, and the resulting vectors are stored in Chroma with automatic deduplication based on content hashing.

### Query Processing Pipeline

When a user submits a query, the system first embeds the question using the same BGE model to ensure semantic consistency. The embedded query is then matched against the vector store using cosine similarity to retrieve the top-k most relevant document chunks (default k=4).

The retrieved chunks are formatted into a structured context that includes source information, file types, and location metadata. This context is combined with the user's question in a carefully engineered prompt that instructs the GPT-OSS 20B model to provide answers based solely on the retrieved evidence, cite sources explicitly, and admit when information is insufficient.

## Implementation Details

### Module Structure

The codebase is organized into a clean, modular structure that promotes maintainability and extensibility:

**Configuration Module** (`rag_app/config.py`): Centralizes all environment-specific settings, including API keys, model names, chunking parameters, and file paths. This module uses python-dotenv to load secrets from a `.env` file that is excluded from version control.

**Embeddings Module** (`rag_app/embeddings.py`): Implements a LangChain-compatible embeddings interface using sentence-transformers. The module supports both batch document embedding and single query embedding with automatic normalization.

**Models Module** (`rag_app/models.py`): Provides a factory function for creating Groq LLM instances with consistent configuration. All LLM calls throughout the system go through this module to ensure uniform behavior.

**Vector Store Module** (`rag_app/vectorstore.py`): Wraps Chroma with additional functionality including deduplication, lazy initialization, and convenient retriever creation. The module uses content hashing to prevent duplicate documents from being indexed.

**Loaders Package** (`rag_app/loaders/`): Contains specialized loaders for each supported file type. Each loader returns LangChain Document objects with consistent metadata schemas, making the ingestion pipeline file-type agnostic.

**Ingestion Module** (`rag_app/ingest.py`): Orchestrates the complete ingestion pipeline from file discovery through vector indexing. The module provides detailed progress reporting and error handling for production use.

**Retrieval Module** (`rag_app/retrieval.py`): Handles document retrieval and source formatting. The module extracts relevant metadata and creates user-friendly source citations.

**RAG Chain Module** (`rag_app/rag_chain.py`): Implements the core RAG pipeline using LangChain Expression Language (LCEL). The module includes prompt engineering to ensure grounded, cited responses.

### Interface Implementations

**Command-Line Interface** (`rag_app/cli.py`): Provides three commands using argparse: `ingest` for document processing, `ask` for one-off questions, and `serve` for starting the FastAPI server. The CLI is designed for automation and scripting.

**FastAPI Server** (`rag_app/api.py`): Exposes HTTP endpoints with Pydantic models for request/response validation. The server includes a health check endpoint and a query endpoint with automatic OpenAPI documentation at `/docs`.

**Streamlit App** (`streamlit_app.py`): Offers an interactive web interface with sidebar controls for configuration, real-time answer generation, expandable source citations, and index management capabilities.

## Features and Capabilities

### Document Processing

The system supports six document types out of the box, each with intelligent content extraction:

**PDF Documents**: Extracted page by page using PyPDFLoader, with page numbers preserved in metadata for accurate citations.

**Text and Markdown Files**: Loaded with full content preservation, automatically detecting file type based on extension.

**HTML Files**: Processed with BeautifulSoup to extract visible text while removing scripts, styles, navigation elements, and other non-content markup. Document titles are extracted when available.

**Python Source Files**: Parsed using the AST module to extract docstrings and comments separately from code, making documentation searchable while preserving code context.

**Jupyter Notebooks**: Processed with nbformat to extract markdown cells and code comments, with cell indices preserved for precise source location.

### Retrieval and Generation

The retrieval system uses semantic search with configurable parameters. Users can adjust the number of retrieved documents (k) to balance between context richness and processing speed. The system automatically formats retrieved chunks with source information and location metadata.

The generation pipeline uses a carefully engineered prompt that enforces several critical behaviors. The model is instructed to use only the provided context, avoiding hallucination and speculation. Answers must include explicit source citations in the format `[source: filename, type, location]`. When the context lacks sufficient information, the model is required to admit this rather than generating unsupported claims.

### Evaluation Framework

The evaluation module (`rag_app/evaluation.py`) supports systematic quality assessment. Users can provide evaluation datasets in CSV or JSONL format with question-answer pairs. The system computes cosine similarity between expected and generated answers using embeddings, checks for source presence, and generates detailed reports saved to the `reports/` directory.

## GitHub-Ready Features

### Security and Privacy

The repository implements several security best practices to ensure safe public sharing:

**Environment Variables**: All secrets, including the Groq API key, are loaded from a `.env` file that is explicitly excluded from version control via `.gitignore`.

**Example Configuration**: A `.env.example` file is provided with placeholder values, making it easy for new users to configure the system without exposing actual credentials.

**No Hardcoded Secrets**: The codebase contains no hardcoded API keys, passwords, or other sensitive information.

### Artifact Management

The `.gitignore` file is configured to exclude several categories of files that should not be committed:

**Generated Artifacts**: Python bytecode, cache files, and build directories are excluded to keep the repository clean.

**Data and Indexes**: The `data/` directory (except `.gitkeep`) and `chroma_store/` are excluded to prevent committing potentially large or sensitive documents.

**Development Files**: IDE configurations, virtual environments, and OS-specific files are excluded for cross-platform compatibility.

**Reports**: Evaluation reports are excluded as they are generated artifacts specific to each deployment.

### Documentation

The repository includes comprehensive documentation at multiple levels:

**README.md**: Provides a complete guide covering overview, architecture, setup, usage, advanced features, troubleshooting, and technical details.

**Inline Documentation**: All modules include docstrings explaining purpose, parameters, return values, and exceptions.

**Code Comments**: Complex logic is annotated with explanatory comments for maintainability.

**Example Notebook**: A Jupyter notebook demonstrates manual testing and exploration of the system.

## Usage Examples

### Quick Start

After cloning the repository and installing dependencies, users can get started in three simple steps:

1. Configure the Groq API key in a `.env` file
2. Place documents in the `data/` directory
3. Run `python -m rag_app.cli ingest` to index documents

### Command-Line Usage

The CLI provides a straightforward interface for common operations:

```bash
# Ingest documents
python -m rag_app.cli ingest

# Ask a question
python -m rag_app.cli ask "What are the main topics in these documents?"

# Start the API server
python -m rag_app.cli serve --reload
```

### API Usage

The FastAPI server exposes a simple HTTP interface:

```bash
# Health check
curl http://localhost:8000/health

# Query endpoint
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Explain the system architecture", "k": 4}'
```

### Web Interface Usage

The Streamlit app provides the most user-friendly experience. Users can launch it with `streamlit run streamlit_app.py` and access an interactive interface with question input, real-time answer generation, expandable source citations, and index management controls.

## Testing and Quality Assurance

### Unit Tests

The `tests/test_basic_pipeline.py` file includes unit tests for core functionality including document chunking, text loading, HTML loading, and Python file loading. Tests use temporary files to avoid dependencies on external data.

### Manual Testing

The Jupyter notebook `notebooks/01_manual_tests.ipynb` provides interactive cells for testing configuration, ingestion, retrieval, question answering, and embeddings. This notebook is valuable for debugging and exploration.

### Evaluation

The evaluation module supports systematic quality assessment with metrics including average embedding similarity and source coverage percentage. Results are saved as JSON reports for tracking performance over time.

## Extensibility

### Adding New File Types

The system is designed for easy extension to new document types. Developers can create a new loader function in `rag_app/loaders/`, register it in the `LOADER_MAP` in `ingest.py`, and add the file extension to `SUPPORTED_EXTENSIONS` in `config.py`.

### Customizing Chunking

Chunking parameters can be adjusted in `config.py` to optimize for different document types or use cases. Larger chunks provide more context but may reduce retrieval precision, while smaller chunks enable more precise retrieval but may lose context.

### Swapping Components

The modular architecture makes it straightforward to swap components:

**Vector Store**: Replace Chroma by implementing a new class with the same interface in `vectorstore.py`

**Embeddings**: Change the `EMBEDDING_MODEL` in `config.py` to any sentence-transformers model

**LLM**: Modify `models.py` to use a different Groq model or even a different provider

## Performance Considerations

### Embedding Generation

Embeddings are generated locally on CPU by default. For faster processing, users with NVIDIA GPUs can set `EMBEDDING_DEVICE = "cuda"` in `config.py`. The BGE model is relatively lightweight and performs well even on CPU for moderate document volumes.

### Vector Search

Chroma provides efficient similarity search with performance scaling roughly logarithmically with collection size. For very large document collections (millions of chunks), consider using approximate nearest neighbor search or a distributed vector database.

### LLM Inference

Groq provides exceptionally fast inference, typically returning responses in under a second. The GPT-OSS 20B model balances reasoning capability with speed, making it suitable for interactive applications.

## Deployment Considerations

### Local Deployment

The system runs entirely on a single machine with minimal resource requirements. A modern laptop with 8GB RAM is sufficient for moderate document collections (thousands of documents).

### Server Deployment

For production deployment, the FastAPI server can be run behind a reverse proxy like Nginx. The Streamlit app can be deployed using Streamlit Cloud or containerized with Docker.

### Scaling

For high-volume deployments, consider:

**Horizontal Scaling**: Run multiple FastAPI instances behind a load balancer

**Caching**: Implement response caching for frequently asked questions

**Async Processing**: Use background workers for document ingestion

**Distributed Vector Store**: Replace Chroma with a distributed solution like Weaviate or Qdrant

## License and Attribution

The project is released under the MIT License, allowing free use, modification, and distribution. The system builds on several open-source projects including LangChain, Chroma, sentence-transformers, FastAPI, and Streamlit.

## Next Steps

Users can immediately start using the system by:

1. Cloning the repository from GitHub
2. Following the setup instructions in README.md
3. Adding their own documents to the `data/` directory
4. Running ingestion and asking questions

For advanced use cases, users can explore the evaluation framework, customize the prompt engineering, or extend the system with new loaders and capabilities.

## Conclusion

This RAG system represents a complete, production-ready solution for document-grounded question answering. The combination of Groq's fast inference, local embeddings, and modular architecture creates a system that is both powerful and practical. The GitHub-ready structure ensures that the project can be easily shared, collaborated on, and deployed in various environments.

The system successfully meets all requirements specified in the original mission, including Groq integration with GPT-OSS 20B, local embeddings, Chroma vector storage, support for multiple file types, three distinct interfaces (CLI, API, web), and a clean GitHub-ready structure with no committed secrets or large artifacts.
