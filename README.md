# RAG System with Groq and Mixtral 8x7B

A complete **Retrieval Augmented Generation (RAG)** system that uses Groq's Mixtral 8x7B model with local open-source embeddings for document-grounded question answering.

## Overview

This project implements a production-ready RAG system with the following features:

- **LLM Provider**: Groq API with Mixtral 8x7B reasoning model
- **Embeddings**: Local sentence-transformers (BAAI/bge-base-en-v1.5) - no external API required
- **Vector Store**: Chroma with persistent storage
- **Document Support**: PDF, TXT, MD, HTML, Python source files, Jupyter notebooks
- **Three Interfaces**: Python CLI, FastAPI HTTP server, Streamlit web app
- **GitHub Ready**: Clean structure, no secrets committed, proper .gitignore

## Architecture

The RAG system follows this workflow:

1. **Ingestion**: Documents are loaded from the `data/` directory, chunked, embedded, and stored in Chroma
2. **Retrieval**: User queries are embedded and matched against the vector store to find relevant documents
3. **Generation**: Retrieved context is passed to Mixtral 8x7B via Groq to generate grounded answers with citations

### Project Structure

```
rag_project/
├── rag_app/
│   ├── __init__.py
│   ├── config.py              # Configuration and environment variables
│   ├── embeddings.py          # Local BGE embeddings
│   ├── models.py              # Groq LLM integration
│   ├── vectorstore.py         # Chroma vector store with deduplication
│   ├── retrieval.py           # Document retrieval logic
│   ├── rag_chain.py           # RAG pipeline with prompt engineering
│   ├── ingest.py              # Document ingestion orchestration
│   ├── cli.py                 # Command-line interface
│   ├── api.py                 # FastAPI server
│   ├── evaluation.py          # Evaluation utilities
│   └── loaders/
│       ├── __init__.py
│       ├── pdf_loader.py      # PDF document loader
│       ├── text_loader.py     # Text and Markdown loader
│       ├── html_loader.py     # HTML loader with BeautifulSoup
│       ├── python_loader.py   # Python source code loader
│       └── notebook_loader.py # Jupyter notebook loader
├── data/                      # Place your documents here
│   └── .gitkeep
├── notebooks/
│   └── 01_manual_tests.ipynb  # Manual testing notebook
├── tests/
│   └── test_basic_pipeline.py # Basic unit tests
├── streamlit_app.py           # Streamlit web interface
├── requirements.txt           # Python dependencies
├── .env.example               # Environment variable template
├── .gitignore                 # Git ignore rules
├── LICENSE                    # MIT License
└── README.md                  # This file
```

## Setup

### Prerequisites

- Python 3.11+
- Groq API key ([get one here](https://console.groq.com/keys))

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd rag_project
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env and add your GROQ_API_KEY
   ```

   Your `.env` file should look like:
   ```
   GROQ_API_KEY=your_actual_groq_api_key_here
   ```

## Usage

### 1. Add Documents

Place your documents in the `data/` directory. Supported formats:
- PDF (`.pdf`)
- Text (`.txt`)
- Markdown (`.md`)
- HTML (`.html`, `.htm`)
- Python source (`.py`)
- Jupyter notebooks (`.ipynb`)

Example:
```bash
cp /path/to/your/documents/*.pdf data/
```

### 2. Ingest Documents

Run the ingestion pipeline to process and index your documents:

```bash
python -m rag_app.cli ingest
```

This will:
- Discover all supported files in `data/`
- Load and chunk documents
- Generate embeddings
- Store in Chroma vector database

### 3. Ask Questions

#### Option A: Command Line

```bash
python -m rag_app.cli ask "What is the main topic of these documents?"
```

#### Option B: FastAPI Server

Start the server:
```bash
python -m rag_app.cli serve
# Or with auto-reload:
python -m rag_app.cli serve --reload
```

Access the API:
- Interactive docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health

Example API call:
```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is this about?", "k": 4}'
```

#### Option C: Streamlit Web App

Launch the interactive web interface:
```bash
streamlit run streamlit_app.py
```

Open your browser to http://localhost:8501

Features:
- Interactive question input
- Real-time answer generation
- Source citations with expandable snippets
- Index management (rebuild, view document count)
- Configurable retrieval parameters

## Advanced Usage

### Evaluation

Evaluate the RAG system on a set of questions:

1. Create an evaluation file (`eval.csv`):
   ```csv
   question,expected_answer
   "What is RAG?","Retrieval Augmented Generation is a technique..."
   "How does it work?","It combines retrieval with generation..."
   ```

2. Run evaluation:
   ```bash
   python -m rag_app.evaluation eval.csv
   ```

Results are saved to `reports/eval_summary.json`.

### Testing

Run unit tests:
```bash
pytest tests/test_basic_pipeline.py -v
```

Use the Jupyter notebook for interactive testing:
```bash
jupyter notebook notebooks/01_manual_tests.ipynb
```

### Configuration

Edit `rag_app/config.py` to customize:

- **Chunk size and overlap**: Adjust `CHUNK_SIZE` and `CHUNK_OVERLAP`
- **Retrieval count**: Change `DEFAULT_K`
- **Model selection**: Modify `DEFAULT_MODEL` (must be a Groq-supported model)
- **Embedding model**: Switch to a different sentence-transformers model

## Extending the System

### Adding New File Types

1. Create a new loader in `rag_app/loaders/`:
   ```python
   def load_custom(file_path: Path) -> List[Document]:
       # Your loading logic
       return [Document(page_content=content, metadata={...})]
   ```

2. Register it in `rag_app/ingest.py`:
   ```python
   LOADER_MAP[".custom"] = load_custom
   ```

3. Add the extension to `SUPPORTED_EXTENSIONS` in `config.py`

### Swapping the Vector Store

Replace Chroma with another vector store by modifying `rag_app/vectorstore.py`. The interface is designed to be modular.

### Changing the Embedding Model

Update `EMBEDDING_MODEL` in `config.py` to any sentence-transformers model:
```python
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
```

## GitHub Best Practices

This repository is designed to be GitHub-ready:

- **No secrets committed**: All API keys are in `.env` (gitignored)
- **No large artifacts**: Data and vector store are gitignored
- **Clean structure**: Modular code with clear separation of concerns
- **Documentation**: Comprehensive README and inline docstrings
- **License**: MIT License for permissive use

Before pushing to GitHub:
1. Ensure `.env` is not committed
2. Verify `.gitignore` is working: `git status`
3. Remove any test data from `data/` if sensitive

## Troubleshooting

### "GROQ_API_KEY not found"
- Ensure you've created a `.env` file from `.env.example`
- Verify the API key is set correctly in `.env`

### "No documents in vector store"
- Run `python -m rag_app.cli ingest` first
- Check that documents exist in the `data/` directory

### Slow embedding generation
- Embeddings run on CPU by default
- To use GPU, change `EMBEDDING_DEVICE = "cuda"` in `config.py`

### Import errors
- Ensure you're in the project root directory
- Activate your virtual environment
- Reinstall dependencies: `pip install -r requirements.txt`

## Technical Details

### Models

- **LLM**: `mixtral-8x7b-32768` via Groq
  - Reasoning-optimized model
  - Temperature set to 0.0 for stable outputs
  
- **Embeddings**: `BAAI/bge-base-en-v1.5`
  - 768-dimensional embeddings
  - Runs locally via sentence-transformers
  - No external API calls

### Chunking Strategy

- **Chunk size**: 1000 characters (configurable)
- **Overlap**: 200 characters (configurable)
- **Splitter**: Recursive character text splitter
- **Separators**: Prioritizes paragraph and sentence boundaries

### Prompt Engineering

The RAG prompt instructs the model to:
- Use only the provided context
- Cite sources in a structured format
- Admit when information is insufficient
- Avoid hallucination

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **Groq** for fast LLM inference
- **DeepSeek** for the reasoning model
- **LangChain** for RAG orchestration
- **Chroma** for vector storage
- **Sentence Transformers** for local embeddings

---

**Built with ❤️ for production-ready RAG applications**
