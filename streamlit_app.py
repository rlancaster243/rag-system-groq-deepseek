"""
Streamlit web application for the RAG system.
Provides an interactive interface for querying the knowledge base.
"""
import streamlit as st
from pathlib import Path

from rag_app.rag_chain import answer_question
from rag_app.ingest import ingest_documents
from rag_app.config import DEFAULT_MODEL, DEFAULT_K
from rag_app.vectorstore import get_vectorstore


# Page configuration
st.set_page_config(
    page_title="RAG System",
    page_icon="🤖",
    layout="wide",
)


def main():
    """Main Streamlit application."""

    # Title and description
    st.title("🤖 RAG System")
    st.markdown(
        "**Retrieval Augmented Generation** powered by Groq, DeepSeek R1, and local embeddings"
    )
    st.divider()

    # Check for API key
    from rag_app.config import GROQ_API_KEY
    if not GROQ_API_KEY:
        st.error(
            "⚠️ **GROQ_API_KEY not configured!**\n\n"
            "To use this app, you need to set your Groq API key:\n\n"
            "**For Local Deployment:**\n"
            "1. Copy `.env.example` to `.env`\n"
            "2. Add your API key: `GROQ_API_KEY=your_key_here`\n\n"
            "**For Streamlit Cloud:**\n"
            "1. Go to App Settings → Secrets\n"
            "2. Add: `GROQ_API_KEY = \"your_key_here\"`\n\n"
            "Get a free API key at: https://console.groq.com/keys"
        )
        st.stop()

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")

        # Model information
        st.subheader("Model")
        st.info(f"**LLM:** {DEFAULT_MODEL}\n\n**Provider:** Groq")

        # Retrieval settings
        st.subheader("Retrieval Settings")
        k = st.slider(
            "Number of documents (k)",
            min_value=1,
            max_value=10,
            value=DEFAULT_K,
            help="Number of relevant documents to retrieve"
        )

        st.divider()

        # Index management
        st.subheader("📚 Index Management")

        # Show document count
        try:
            vectorstore = get_vectorstore()
            doc_count = vectorstore.count()
            st.metric("Documents in index", doc_count)
        except Exception as e:
            st.warning("Could not load vector store")
            doc_count = 0

        # Ingestion button
        if st.button("🔄 Rebuild Index", use_container_width=True):
            with st.spinner("Ingesting documents..."):
                try:
                    stats = ingest_documents(verbose=False)
                    st.success(
                        f"✅ Ingestion complete!\n\n"
                        f"- Files found: {stats['files_found']}\n"
                        f"- Documents loaded: {stats['documents_loaded']}\n"
                        f"- Chunks created: {stats['chunks_created']}\n"
                        f"- Chunks added: {stats['chunks_added']}"
                    )
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error during ingestion: {str(e)}")

        st.divider()

        # Instructions
        st.subheader("📖 Instructions")
        st.markdown(
            """
            1. Place documents in the `data/` folder
            2. Click **Rebuild Index** to ingest
            3. Ask questions in the main panel
            4. View answers with source citations
            """
        )

    # Main panel
    col1, col2 = st.columns([2, 1])

    with col1:
        st.header("💬 Ask a Question")

    with col2:
        if doc_count == 0:
            st.warning("⚠️ No documents indexed yet")

    # Question input
    question = st.text_input(
        "Enter your question:",
        placeholder="What would you like to know?",
        help="Ask a question about the documents in your knowledge base"
    )

    # Submit button
    if st.button("🔍 Submit", type="primary", use_container_width=True):
        if not question:
            st.warning("Please enter a question")
        elif doc_count == 0:
            st.error("No documents in the index. Please add documents and rebuild the index.")
        else:
            with st.spinner("Searching and generating answer..."):
                try:
                    from rag_app.config import GROQ_API_KEY
                    if not GROQ_API_KEY:
                        st.error("GROQ_API_KEY is not configured. Please check your environment variables or Streamlit secrets.")
                        st.stop()
                    
                    result = answer_question(question, k=k)

                    # Display answer
                    st.subheader("📝 Answer")
                    st.markdown(
                        f"""
                        <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #4CAF50;">
                        {result['answer']}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    # Display sources
                    if result["sources"]:
                        st.subheader(f"📚 Sources ({len(result['sources'])} documents)")

                        for i, source in enumerate(result["sources"], 1):
                            with st.expander(
                                f"📄 {source['filename']} ({source['file_type']}) - {source['location']}"
                            ):
                                st.markdown(f"**Snippet:**")
                                st.text(source['snippet'])
                    else:
                        st.info("No sources found")

                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")


if __name__ == "__main__":
    main()
