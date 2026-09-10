import pytest

from trabeculai.retrieval.lexical.bm25 import BM25Retriever
from trabeculai.retrieval.models import EvidenceDocument

pytestmark = pytest.mark.anyio


async def test_retrieves_most_relevant_document_first(
    evidence_documents: list[EvidenceDocument],
) -> None:
    retriever = BM25Retriever(evidence_documents)

    results = await retriever.retrieve(query="hypertension blood pressure", top_k=1)

    assert len(results) == 1
    assert results[0].document.id == "hypertension"
    assert results[0].rank == 1


async def test_returns_no_results_for_empty_query(
    evidence_documents: list[EvidenceDocument],
) -> None:
    retriever = BM25Retriever(evidence_documents)

    assert await retriever.retrieve("") == []
    assert await retriever.retrieve("   ") == []


async def test_returns_no_results_for_empty_corpus() -> None:
    retriever = BM25Retriever([])

    assert await retriever.retrieve("hypertension") == []


async def test_rejects_non_positive_top_k(evidence_documents: list[EvidenceDocument]) -> None:
    retriever = BM25Retriever(evidence_documents)

    with pytest.raises(ValueError, match="top_k must be greater than 0"):
        await retriever.retrieve("hypertension", top_k=0)

    with pytest.raises(ValueError, match="top_k must be greater than 0"):
        await retriever.retrieve("hypertension", top_k=-1)


async def test_ignores_document_without_indexable_content() -> None:
    documents = [
        EvidenceDocument(
            id="empty",
            title="",
            text="",
            source="synthetic",
        ),
    ]

    retriever = BM25Retriever(documents)

    assert await retriever.retrieve("hypertension") == []


async def test_repeated_query_terms_do_not_change_score(
    evidence_documents: list[EvidenceDocument],
) -> None:
    retriever = BM25Retriever(evidence_documents)

    single = await retriever.retrieve("hypertension")
    repeated = await retriever.retrieve("hypertension hypertension hypertension")

    assert repeated == single


async def test_corpus_is_not_affected_by_external_mutation(
    evidence_documents: list[EvidenceDocument],
) -> None:
    documents = list(evidence_documents)

    retriever = BM25Retriever(documents)

    documents.append(
        EvidenceDocument(
            id="new",
            title="New document",
            text="new content",
            source="test",
        )
    )

    results = await retriever.retrieve(
        query="new content",
        top_k=len(documents),
    )

    assert all(result.document.id != "new" for result in results)


async def test_corpus_is_snapshotted_at_initialization() -> None:
    documents = [
        EvidenceDocument(
            id="D1",
            title="Hypertension",
            text="blood pressure",
            source="test",
        ),
    ]

    retriever = BM25Retriever(documents)

    documents.append(
        EvidenceDocument(
            id="D2",
            title="Diabetes",
            text="blood glucose",
            source="test",
        )
    )

    results = await retriever.retrieve("diabetes")

    assert results == []
