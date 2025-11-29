# Quick Start Guide

Get your RAG system up and running in 5 minutes!

## Prerequisites

- Python 3.11 or higher
- A Groq API key ([get one free here](https://console.groq.com/keys))

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/rlancaster243/rag-system-groq-deepseek.git
cd rag-system-groq-deepseek
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install all required packages including LangChain, Groq, Chroma, and more.

### 4. Configure API Key

```bash
cp .env.example .env
```

Edit `.env` and add your Groq API key:

```
GROQ_API_KEY=gsk_your_actual_api_key_here
```

## First Run

### Add Sample Documents

The repository includes a sample document. You can add your own:

```bash
# Copy your documents to the data folder
cp /path/to/your/documents/*.pdf data/
cp /path/to/your/documents/*.md data/
```

Supported formats: PDF, TXT, MD, HTML, PY, IPYNB

### Ingest Documents

Process and index your documents:

```bash
python -m rag_app.cli ingest
```

You should see output like:

```
🔍 Discovering files in /path/to/data...
📁 Found 2 file(s)
   Loading: sample_document.md
   Loading: your_document.pdf
📄 Loaded 3 document(s)
✂️  Chunking documents...
📦 Created 15 chunk(s)
💾 Indexing in vector store...
✅ Added 15 new chunk(s)
```

### Ask Your First Question

```bash
python -m rag_app.cli ask "What is this document about?"
```

You'll get an answer with source citations!

## Try the Web Interface

Launch the Streamlit app for a better experience:

```bash
streamlit run streamlit_app.py
```

Open your browser to **http://localhost:8501**

Features:
- Interactive question input
- Real-time answers
- Expandable source citations
- Index management

## Try the API

Start the FastAPI server:

```bash
python -m rag_app.cli serve
```

Access the interactive API docs at **http://localhost:8000/docs**

Test with curl:

```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the main topics?", "k": 4}'
```

## Common Commands

```bash
# Ingest documents
python -m rag_app.cli ingest

# Ask a question (CLI)
python -m rag_app.cli ask "Your question here"

# Start API server
python -m rag_app.cli serve

# Start API with auto-reload (development)
python -m rag_app.cli serve --reload

# Start Streamlit app
streamlit run streamlit_app.py

# Run tests
pytest tests/test_basic_pipeline.py -v
```

## Troubleshooting

### "GROQ_API_KEY not found"

Make sure you:
1. Created a `.env` file (copy from `.env.example`)
2. Added your actual API key (starts with `gsk_`)
3. Are in the project root directory

### "No documents in vector store"

Run ingestion first:
```bash
python -m rag_app.cli ingest
```

### Import errors

Activate your virtual environment:
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Slow performance

Embeddings run on CPU by default. To use GPU:
1. Install PyTorch with CUDA support
2. Edit `rag_app/config.py` and set `EMBEDDING_DEVICE = "cuda"`

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore the [Jupyter notebook](notebooks/01_manual_tests.ipynb) for examples
- Check out the [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) for architecture details
- Customize chunking parameters in `rag_app/config.py`
- Add new document loaders in `rag_app/loaders/`

## Need Help?

- Check the [README.md](README.md) troubleshooting section
- Review the code documentation (all modules have docstrings)
- Open an issue on GitHub

Happy RAG-ing! 🚀
