from pathlib import Path

from trabeculai.retrieval.evaluation import (
    RetrievalEvaluationReport,
    evaluate_retriever,
    load_evaluation_dataset,
)
from trabeculai.retrieval.lexical.bm25 import BM25Retriever
from trabeculai.retrieval.semantic import E5SentenceTransformerEmbedder, SemanticRetriever

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATASET_PATH = PROJECT_ROOT / "data" / "evaluation" / "retrieval"


def print_summary(name: str, report: RetrievalEvaluationReport) -> None:
    print(name)
    print(f"Recall@{report.k}: {report.mean_recall_at_k:.4f}")
    print(f"MRR: {report.mrr:.4f}")
    print(f"NDCG@{report.k}: {report.mean_ndcg_at_k:.4f}")
    print()


def main() -> None:
    dataset = load_evaluation_dataset(DATASET_PATH)

    bm25 = BM25Retriever(dataset.documents)

    embedder = E5SentenceTransformerEmbedder()
    semantic = SemanticRetriever(dataset.documents, embedder)

    bm25_report = evaluate_retriever(retriever=bm25, dataset=dataset, k=3)
    semantic_report = evaluate_retriever(retriever=semantic, dataset=dataset, k=3)

    print("Retrieval Baseline Comparison\n")

    print_summary("BM25", bm25_report)
    print_summary("Semantic E5", semantic_report)

    print("Per-query comparison:")

    for bm25_result, semantic_result in zip(
        bm25_report.queries,
        semantic_report.queries,
        strict=True,
    ):
        print(
            f"{bm25_result.query_id}: "
            f"BM25 RR={bm25_result.reciprocal_rank:.4f}, "
            f"NDCG@{bm25_report.k}={bm25_result.ndcg_at_k:.4f} | "
            f"Semantic RR={semantic_result.reciprocal_rank:.4f}, "
            f"NDCG@{semantic_report.k}={semantic_result.ndcg_at_k:.4f}"
        )


if __name__ == "__main__":
    main()
