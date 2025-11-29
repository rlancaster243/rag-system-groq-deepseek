"""
Command-line interface for the RAG system.
Provides commands for ingestion, querying, and serving.
"""
import argparse
import sys

from rag_app.ingest import ingest_documents
from rag_app.rag_chain import answer_question


def cmd_ingest(args):
    """Run the ingestion pipeline."""
    print("🚀 Starting document ingestion...\n")
    stats = ingest_documents(verbose=True)
    print("\n✨ Ingestion complete!")
    return 0


def cmd_ask(args):
    """Ask a question and get an answer."""
    question = args.question

    if not question:
        print("❌ Error: Please provide a question")
        return 1

    print(f"❓ Question: {question}\n")
    print("🔍 Retrieving relevant documents...\n")

    try:
        result = answer_question(question, k=args.k)

        print("=" * 80)
        print("📝 ANSWER")
        print("=" * 80)
        print(result["answer"])
        print()

        if result["sources"]:
            print("=" * 80)
            print(f"📚 SOURCES ({len(result['sources'])} documents)")
            print("=" * 80)
            for i, source in enumerate(result["sources"], 1):
                print(f"\n[{i}] {source['filename']} ({source['file_type']})")
                print(f"    Location: {source['location']}")
                print(f"    Snippet: {source['snippet'][:150]}...")
        else:
            print("⚠️  No sources found")

        print("\n" + "=" * 80)
        return 0

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return 1


def cmd_serve(args):
    """Start the FastAPI server."""
    import uvicorn
    from rag_app.api import app

    print(f"🚀 Starting FastAPI server on http://localhost:{args.port}")
    print("📖 API documentation available at http://localhost:{}/docs".format(args.port))

    uvicorn.run(
        "rag_app.api:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
    )
    return 0


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="RAG System CLI - Retrieval Augmented Generation with Groq and DeepSeek",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Ingest command
    parser_ingest = subparsers.add_parser(
        "ingest",
        help="Ingest documents from the data directory"
    )
    parser_ingest.set_defaults(func=cmd_ingest)

    # Ask command
    parser_ask = subparsers.add_parser(
        "ask",
        help="Ask a question and get an answer"
    )
    parser_ask.add_argument(
        "question",
        type=str,
        help="Question to ask"
    )
    parser_ask.add_argument(
        "-k",
        type=int,
        default=4,
        help="Number of documents to retrieve (default: 4)"
    )
    parser_ask.set_defaults(func=cmd_ask)

    # Serve command
    parser_serve = subparsers.add_parser(
        "serve",
        help="Start the FastAPI server"
    )
    parser_serve.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="Host to bind to (default: 0.0.0.0)"
    )
    parser_serve.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to bind to (default: 8000)"
    )
    parser_serve.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reload"
    )
    parser_serve.set_defaults(func=cmd_serve)

    # Parse arguments
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Execute command
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
