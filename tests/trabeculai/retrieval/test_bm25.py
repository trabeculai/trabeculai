import pytest

from trabeculai.retrieval.bm25 import BM25Retriever
from trabeculai.retrieval.models import EvidenceDocument


def test_retrieves_most_relevant_document_first(evidence_documents: list[EvidenceDocument]) -> None:
    retriever = BM25Retriever(evidence_documents)

    results = retriever.retrieve(
        query="hypertension blood pressure",
        top_k=1,
    )

    assert len(results) == 1
    assert results[0].document.id == "hypertension"
    assert results[0].rank == 1


def test_returns_no_results_for_empty_query(evidence_documents: list[EvidenceDocument]) -> None:
    retriever = BM25Retriever(evidence_documents)

    assert retriever.retrieve("") == []
    assert retriever.retrieve("   ") == []


def test_returns_no_results_for_empty_corpus() -> None:
    retriever = BM25Retriever([])

    assert retriever.retrieve("hypertension") == []


def test_rejects_non_positive_top_k(evidence_documents: list[EvidenceDocument]) -> None:
    retriever = BM25Retriever(evidence_documents)

    with pytest.raises(ValueError, match="top_k must be greater than 0"):
        retriever.retrieve("hypertension", top_k=0)

    with pytest.raises(ValueError, match="top_k must be greater than 0"):
        retriever.retrieve("hypertension", top_k=-1)


def test_ignores_document_without_indexable_content() -> None:
    documents = [
        EvidenceDocument(
            id="empty",
            title="",
            text="",
            source="synthetic",
        ),
    ]

    retriever = BM25Retriever(documents)

    assert retriever.retrieve("hypertension") == []


def test_repeated_query_terms_do_not_change_score(
    evidence_documents: list[EvidenceDocument],
) -> None:
    retriever = BM25Retriever(evidence_documents)

    single = retriever.retrieve("hypertension")
    repeated = retriever.retrieve("hypertension hypertension hypertension")

    assert repeated == single
