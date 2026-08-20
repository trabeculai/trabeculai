from pathlib import Path

from trabeculai.retrieval.bm25 import BM25Retriever
from trabeculai.retrieval.evaluation import (
    evaluate_retriever,
    load_evaluation_dataset,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATASET_PATH = PROJECT_ROOT / "data" / "evaluation" / "retrieval"


def main() -> None:
    dataset = load_evaluation_dataset(DATASET_PATH)

    retriever = BM25Retriever(dataset.documents)

    report = evaluate_retriever(retriever=retriever, dataset=dataset, k=3)

    print("BM25 Retrieval Baseline")
    print(f"Recall@{report.k}: {report.mean_recall_at_k:.4f}")
    print(f"MRR: {report.mrr:.4f}")
    print(f"NDCG@{report.k}: {report.mean_ndcg_at_k:.4f}")

    print("\nPer-query results:")

    for result in report.queries:
        print(
            f"{result.query_id}: "
            f"Recall@{report.k}={result.recall_at_k:.4f}, "
            f"RR={result.reciprocal_rank:.4f}, "
            f"NDCG@{report.k}={result.ndcg_at_k:.4f}"
        )


if __name__ == "__main__":
    main()
