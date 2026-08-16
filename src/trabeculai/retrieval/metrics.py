import math
from collections.abc import Sequence
from typing import Literal

from .models import RetrievalResult


def recall_at_k(
    results: Sequence[RetrievalResult],
    relevant_document_ids: set[str],
    k: int,
) -> float:
    if k <= 0:
        raise ValueError("k must be greater than 0")

    if not relevant_document_ids:
        raise ValueError("relevant_document_ids must not be empty")

    retrieved_ids = {result.document.id for result in results[:k]}

    retrieved_relevant = retrieved_ids & relevant_document_ids

    return len(retrieved_relevant) / len(relevant_document_ids)


def rr(results: Sequence[RetrievalResult], relevant_document_ids: set[str]) -> float:
    if not relevant_document_ids:
        raise ValueError("relevant_document_ids must not be empty")

    for rank, result in enumerate(results, start=1):
        if result.document.id in relevant_document_ids:
            return 1.0 / rank

    return 0.0


def mrr(rankings: Sequence[tuple[Sequence[RetrievalResult], set[str]]]) -> float:
    if not rankings:
        raise ValueError("rankings must not be empty")

    reciprocal_ranks = [
        rr(results, relevant_document_ids) for results, relevant_document_ids in rankings
    ]

    return sum(reciprocal_ranks) / len(reciprocal_ranks)


def _ndcg_at_k_gain(
    relevance: float,
    method: Literal["linear", "exponential"],
) -> float:
    match method:
        case "linear":
            return relevance
        case "exponential":
            return 2**relevance - 1
        case _:
            raise ValueError("Invalid method. Must be 'linear' or 'exponential'.")


def ndcg_at_k(
    results: Sequence[RetrievalResult],
    relevance: dict[str, float],
    k: int,
    gain: Literal["linear", "exponential"] = "exponential",
) -> float:
    if k <= 0:
        raise ValueError("k must be greater than 0")

    if not relevance:
        raise ValueError("relevance must not be empty")

    dcg = sum(
        _ndcg_at_k_gain(relevance.get(result.document.id, 0.0), gain) / math.log2(rank + 1)
        for rank, result in enumerate(results[:k], start=1)
    )

    ideal_relevances = sorted(relevance.values(), reverse=True)[:k]

    idcg = sum(
        _ndcg_at_k_gain(relevance_score, gain) / math.log2(rank + 1)
        for rank, relevance_score in enumerate(
            ideal_relevances,
            start=1,
        )
    )

    return dcg / idcg if idcg > 0 else 0.0
