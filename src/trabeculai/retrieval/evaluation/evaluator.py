from statistics import fmean
from typing import Literal

from ..metrics import ndcg_at_k, recall_at_k, rr
from ..retriever import Retriever
from .models import QueryEvaluationResult, RetrievalEvaluationDataset, RetrievalEvaluationReport


def evaluate_retriever(
    retriever: Retriever,
    dataset: RetrievalEvaluationDataset,
    k: int,
    gain: Literal["linear", "exponential"] = "exponential",
) -> RetrievalEvaluationReport:
    if not dataset.queries:
        raise ValueError("dataset must contain queries")

    if k <= 0:
        raise ValueError("k must be greater than 0")

    query_results: list[QueryEvaluationResult] = []

    for query in dataset.queries:
        query_relevance = {
            qrel.document_id: qrel.relevance for qrel in dataset.qrels if qrel.query_id == query.id
        }

        relevant_document_ids = {
            document_id for document_id, relevance in query_relevance.items() if relevance > 0
        }

        results = retriever.retrieve(query.text, top_k=len(dataset.documents))

        query_results.append(
            QueryEvaluationResult(
                query_id=query.id,
                recall_at_k=recall_at_k(results, relevant_document_ids, k),
                reciprocal_rank=rr(results, relevant_document_ids),
                ndcg_at_k=ndcg_at_k(results, query_relevance, k, gain=gain),
            )
        )

    return RetrievalEvaluationReport(
        k=k,
        mean_recall_at_k=fmean(result.recall_at_k for result in query_results),
        mrr=fmean(result.reciprocal_rank for result in query_results),
        mean_ndcg_at_k=fmean(result.ndcg_at_k for result in query_results),
        queries=query_results,
    )
