import asyncio
from pathlib import Path

from trabeculai.retrieval.evaluation import (
    evaluate_retriever,
    load_evaluation_dataset,
)
from trabeculai.retrieval.hybrid import HybridRetriever
from trabeculai.retrieval.lexical.bm25 import BM25Retriever
from trabeculai.retrieval.semantic import (
    E5SentenceTransformerEmbedder,
    SemanticRetriever,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATASET_PATH = PROJECT_ROOT / "data" / "evaluation" / "retrieval"


async def main() -> None:
    dataset = load_evaluation_dataset(DATASET_PATH)

    bm25 = BM25Retriever(dataset.documents)

    embedder = E5SentenceTransformerEmbedder()
    semantic = SemanticRetriever(dataset.documents, embedder)

    hybrid = HybridRetriever([bm25, semantic])

    report = await evaluate_retriever(retriever=hybrid, dataset=dataset, k=3)

    print("Hybrid Retrieval Baseline")
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
    asyncio.run(main())
