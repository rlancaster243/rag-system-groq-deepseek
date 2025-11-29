"""
Evaluation module for RAG system.
Evaluates answer quality using embedding similarity and source validation.
"""
import json
import csv
from typing import List, Dict
from pathlib import Path
import numpy as np

from rag_app.rag_chain import answer_question
from rag_app.embeddings import get_embeddings
from rag_app.config import REPORTS_DIR


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Calculate cosine similarity between two vectors.

    Args:
        vec1: First vector
        vec2: Second vector

    Returns:
        Cosine similarity score (0 to 1)
    """
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)

    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return float(dot_product / (norm1 * norm2))


def evaluate_rag(
    eval_file: Path,
    k: int = 4,
    output_file: Path = None
) -> Dict:
    """
    Evaluate RAG system on a set of questions.

    Args:
        eval_file: Path to evaluation file (CSV or JSONL)
        k: Number of documents to retrieve
        output_file: Path to save evaluation report (optional)

    Returns:
        Dictionary with evaluation results

    Expected CSV format:
        question,expected_answer

    Expected JSONL format:
        {"question": "...", "expected_answer": "..."}
    """
    # Load evaluation data
    eval_data = []

    if eval_file.suffix == ".csv":
        with open(eval_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            eval_data = list(reader)
    elif eval_file.suffix == ".jsonl":
        with open(eval_file, "r", encoding="utf-8") as f:
            for line in f:
                eval_data.append(json.loads(line))
    else:
        raise ValueError(f"Unsupported file format: {eval_file.suffix}")

    if not eval_data:
        raise ValueError("No evaluation data found")

    print(f"📊 Evaluating {len(eval_data)} questions...")

    # Get embeddings model
    embeddings = get_embeddings()

    # Evaluate each question
    results = []
    total_similarity = 0.0
    total_with_sources = 0

    for i, item in enumerate(eval_data, 1):
        question = item.get("question")
        expected_answer = item.get("expected_answer")

        if not question or not expected_answer:
            print(f"⚠️  Skipping item {i}: missing question or expected_answer")
            continue

        print(f"[{i}/{len(eval_data)}] Evaluating: {question[:60]}...")

        try:
            # Get RAG answer
            result = answer_question(question, k=k)
            generated_answer = result["answer"]
            sources = result["sources"]

            # Calculate similarity
            expected_emb = embeddings.embed_query(expected_answer)
            generated_emb = embeddings.embed_query(generated_answer)
            similarity = cosine_similarity(expected_emb, generated_emb)

            # Check if sources are present
            has_sources = len(sources) > 0

            # Store result
            eval_result = {
                "question": question,
                "expected_answer": expected_answer,
                "generated_answer": generated_answer,
                "similarity_score": similarity,
                "has_sources": has_sources,
                "num_sources": len(sources),
            }
            results.append(eval_result)

            total_similarity += similarity
            if has_sources:
                total_with_sources += 1

        except Exception as e:
            print(f"❌ Error evaluating question {i}: {str(e)}")
            results.append({
                "question": question,
                "expected_answer": expected_answer,
                "generated_answer": f"ERROR: {str(e)}",
                "similarity_score": 0.0,
                "has_sources": False,
                "num_sources": 0,
            })

    # Calculate summary statistics
    avg_similarity = total_similarity / len(results) if results else 0.0
    source_coverage = total_with_sources / len(results) if results else 0.0

    summary = {
        "total_questions": len(results),
        "average_similarity": avg_similarity,
        "source_coverage": source_coverage,
        "questions_with_sources": total_with_sources,
    }

    # Print summary
    print("\n" + "=" * 80)
    print("📊 EVALUATION SUMMARY")
    print("=" * 80)
    print(f"Total questions: {summary['total_questions']}")
    print(f"Average similarity: {summary['average_similarity']:.3f}")
    print(f"Source coverage: {summary['source_coverage']:.1%}")
    print(f"Questions with sources: {summary['questions_with_sources']}")
    print("=" * 80)

    # Save report
    report = {
        "summary": summary,
        "results": results,
    }

    if output_file is None:
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        output_file = REPORTS_DIR / "eval_summary.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(f"\n💾 Report saved to: {output_file}")

    return report


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python -m rag_app.evaluation <eval_file.csv|eval_file.jsonl>")
        sys.exit(1)

    eval_file = Path(sys.argv[1])
    if not eval_file.exists():
        print(f"Error: File not found: {eval_file}")
        sys.exit(1)

    evaluate_rag(eval_file)
