# Deployment Guide

This guide covers deploying the RAG system to various platforms.

## Streamlit Cloud Deployment

### Prerequisites

- A GitHub account with this repository
- A Groq API key ([get one free here](https://console.groq.com/keys))
- A Streamlit Cloud account ([sign up free](https://streamlit.io/cloud))

### Step-by-Step Instructions

#### 1. Fork or Clone the Repository

If you haven't already, ensure the repository is in your GitHub account.

#### 2. Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Select your repository: `rlancaster243/rag-system-groq-GPT-OSS`
4. Set the main file path: `streamlit_app.py`
5. Click "Deploy"

#### 3. Configure Secrets

The app will initially show an error because the API key is not configured. To fix this:

1. In your Streamlit Cloud dashboard, click on your app
2. Click the menu (⋮) and select "Settings"
3. Go to the "Secrets" section
4. Add the following content:

```toml
GROQ_API_KEY = "your_actual_groq_api_key_here"
```

5. Click "Save"
6. The app will automatically restart with the new configuration

#### 4. Add Sample Documents (Optional)

Since the `data/` directory is gitignored (except for the sample document), you have a few options:

**Option A: Use the included sample document**
- The repository includes `data/sample_document.md` for testing
- You can ask questions about RAG systems and the project

**Option B: Fork and add your own documents**
- Fork the repository
- Add your documents to the `data/` folder
- Force-add them: `git add -f data/your_document.pdf`
- Commit and push
- Redeploy on Streamlit Cloud

**Option C: Use the ingestion feature**
- Note: Streamlit Cloud has limited write access
- For production use, consider running ingestion locally and deploying the vector store

### Limitations on Streamlit Cloud

Be aware of these limitations when deploying to Streamlit Cloud:

**Storage**: Streamlit Cloud apps have limited persistent storage. The vector store (`chroma_store/`) will be reset on each deployment.

**Memory**: Free tier has memory limits. Large document collections may exceed available RAM.

**CPU**: Embedding generation runs on CPU, which may be slower than local deployment.

**File Upload**: The current version doesn't support file upload through the UI. Documents must be in the repository.

### Recommended Workflow

For production Streamlit Cloud deployment:

1. **Run ingestion locally**:
   ```bash
   python -m rag_app.cli ingest
   ```

2. **Commit the vector store** (not recommended for large datasets):
   ```bash
   git add -f chroma_store/
   git commit -m "Add pre-built vector store"
   git push
   ```

3. **Or use a cloud vector database**:
   - Replace Chroma with a cloud-hosted solution like Pinecone or Weaviate
   - Modify `rag_app/vectorstore.py` accordingly

## Local Deployment

### Using Python Directly

```bash
# Activate virtual environment
source venv/bin/activate

# Run Streamlit
streamlit run streamlit_app.py

# Or run FastAPI
python -m rag_app.cli serve
```

### Using Docker (Optional)

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:

```bash
docker build -t rag-system .
docker run -p 8501:8501 -e GROQ_API_KEY=your_key_here rag-system
```

## FastAPI Deployment

### Using Uvicorn

```bash
# Production server
uvicorn rag_app.api:app --host 0.0.0.0 --port 8000 --workers 4
```

### Using Gunicorn

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn rag_app.api:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Using Docker

Create a `Dockerfile.api`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

COPY . .

EXPOSE 8000

CMD ["gunicorn", "rag_app.api:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
```

## Cloud Platform Deployment

### Heroku

1. Create a `Procfile`:
   ```
   web: streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. Create `runtime.txt`:
   ```
   python-3.11.0
   ```

3. Deploy:
   ```bash
   heroku create your-app-name
   heroku config:set GROQ_API_KEY=your_key_here
   git push heroku main
   ```

### AWS EC2

1. Launch an EC2 instance (Ubuntu 22.04)
2. SSH into the instance
3. Clone the repository
4. Install dependencies
5. Configure environment variables
6. Run with systemd or supervisor

### Google Cloud Run

1. Create a `Dockerfile` (see above)
2. Build and push to Google Container Registry
3. Deploy to Cloud Run
4. Set environment variables in Cloud Run console

## Environment Variables

All deployment methods require setting the `GROQ_API_KEY` environment variable:

- **Streamlit Cloud**: Use the Secrets management UI
- **Docker**: Use `-e GROQ_API_KEY=...` flag
- **Heroku**: Use `heroku config:set`
- **AWS/GCP**: Use platform-specific secret management
- **Local**: Use `.env` file

## Performance Optimization

### For Production Deployments

1. **Use GPU for embeddings** (if available):
   - Edit `rag_app/config.py`
   - Set `EMBEDDING_DEVICE = "cuda"`
   - Install PyTorch with CUDA support

2. **Increase chunk cache**:
   - Implement Redis caching for frequently retrieved chunks
   - Cache embedding results

3. **Use a production vector database**:
   - Replace Chroma with Pinecone, Weaviate, or Qdrant
   - Better for large-scale deployments

4. **Load balancing**:
   - Run multiple API instances behind a load balancer
   - Use Nginx or cloud load balancers

## Monitoring and Logging

### Add Logging

Update `rag_app/config.py`:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Monitor API Performance

Use tools like:
- **Prometheus** + **Grafana** for metrics
- **Sentry** for error tracking
- **DataDog** for comprehensive monitoring

## Security Considerations

1. **Never commit secrets**: Always use environment variables or secret management
2. **Use HTTPS**: Deploy behind a reverse proxy with SSL
3. **Rate limiting**: Implement rate limiting on API endpoints
4. **Input validation**: The system already validates inputs via Pydantic
5. **CORS**: Configure CORS settings in FastAPI if needed

## Troubleshooting Deployment Issues

### Streamlit Cloud: "GROQ_API_KEY not configured"

- Check that secrets are properly set in Settings → Secrets
- Ensure the format is: `GROQ_API_KEY = "your_key"`
- Restart the app after changing secrets

### Memory Errors

- Reduce the number of documents
- Decrease `CHUNK_SIZE` in config
- Use a smaller embedding model
- Upgrade to a higher-tier deployment plan

### Slow Performance

- Enable GPU if available
- Reduce the number of retrieved documents (k)
- Implement caching
- Use a faster embedding model

### Import Errors

- Ensure all dependencies are in `requirements.txt`
- Check Python version compatibility
- Verify the working directory is correct

## Support

For deployment issues:
- Check the [README.md](README.md) troubleshooting section
- Review the [QUICKSTART.md](QUICKSTART.md) guide
- Open an issue on GitHub

---

**Happy Deploying! 🚀**
