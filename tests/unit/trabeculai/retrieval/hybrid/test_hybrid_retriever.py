import pytest

from tests.fakes import FakeRetriever
from trabeculai.retrieval.hybrid import HybridRetriever
from trabeculai.retrieval.models import EvidenceDocument, RetrievalResult

pytestmark = pytest.mark.anyio


async def test_hybrid_retriever_fuses_rankings() -> None:
    d1 = EvidenceDocument(id="D1", title="D1", text="", source="test")
    d2 = EvidenceDocument(id="D2", title="D2", text="", source="test")
    d3 = EvidenceDocument(id="D3", title="D3", text="", source="test")

    lexical = FakeRetriever(
        {
            "query": [
                RetrievalResult(document=d1, score=1.0, rank=1),
                RetrievalResult(document=d2, score=0.8, rank=2),
                RetrievalResult(document=d3, score=0.6, rank=3),
            ]
        }
    )

    semantic = FakeRetriever(
        {
            "query": [
                RetrievalResult(document=d1, score=0.9, rank=1),
                RetrievalResult(document=d3, score=0.7, rank=2),
            ]
        }
    )

    retriever = HybridRetriever(retrievers=[lexical, semantic], k=60)

    results = await retriever.retrieve("query", top_k=3)

    assert [result.document.id for result in results] == ["D1", "D3", "D2"]
    assert [result.rank for result in results] == [1, 2, 3]


async def test_hybrid_retriever_assigns_rrf_scores() -> None:
    d1 = EvidenceDocument(id="D1", title="D1", text="", source="test")
    d2 = EvidenceDocument(id="D2", title="D2", text="", source="test")

    lexical = FakeRetriever(
        {
            "query": [
                RetrievalResult(document=d1, score=10.0, rank=1),
                RetrievalResult(document=d2, score=5.0, rank=2),
            ]
        }
    )

    semantic = FakeRetriever(
        {
            "query": [
                RetrievalResult(document=d1, score=0.01, rank=1),
            ]
        }
    )

    retriever = HybridRetriever(retrievers=[lexical, semantic], k=60)

    results = await retriever.retrieve("query", top_k=2)

    assert results[0].score == pytest.approx(1 / 61 + 1 / 61)
    assert results[1].score == pytest.approx(1 / 62)


async def test_hybrid_retriever_respects_top_k() -> None:
    d1 = EvidenceDocument(id="D1", title="D1", text="", source="test")
    d2 = EvidenceDocument(id="D2", title="D2", text="", source="test")
    d3 = EvidenceDocument(id="D3", title="D3", text="", source="test")

    lexical = FakeRetriever(
        {
            "query": [
                RetrievalResult(document=d1, score=1.0, rank=1),
                RetrievalResult(document=d2, score=0.8, rank=2),
                RetrievalResult(document=d3, score=0.6, rank=3),
            ]
        }
    )

    semantic = FakeRetriever(
        {
            "query": [
                RetrievalResult(document=d1, score=0.9, rank=1),
                RetrievalResult(document=d3, score=0.7, rank=2),
                RetrievalResult(document=d2, score=0.5, rank=3),
            ]
        }
    )

    retriever = HybridRetriever(
        retrievers=[lexical, semantic],
        k=60,
    )

    results = await retriever.retrieve("query", top_k=2)

    assert len(results) == 2


async def test_hybrid_retriever_returns_empty_without_retrievers() -> None:
    retriever = HybridRetriever(retrievers=[])

    results = await retriever.retrieve("query")

    assert results == []


async def test_hybrid_retriever_handles_empty_retriever_results() -> None:
    d1 = EvidenceDocument(id="D1", title="D1", text="", source="test")

    empty = FakeRetriever(
        {
            "query": [],
        }
    )

    semantic = FakeRetriever(
        {
            "query": [
                RetrievalResult(document=d1, score=1.0, rank=1),
            ]
        }
    )

    retriever = HybridRetriever(retrievers=[empty, semantic], k=60)

    results = await retriever.retrieve("query")

    assert [result.document.id for result in results] == ["D1"]
