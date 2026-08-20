import pytest

from trabeculai.retrieval.metrics import ndcg_at_k, recall_at_k, rr
from trabeculai.retrieval.models import EvidenceDocument, RetrievalResult


def _result(document_id: str, rank: int) -> RetrievalResult:
    document = EvidenceDocument(
        id=document_id,
        title=document_id,
        text="",
        source="test",
    )

    return RetrievalResult(
        document=document,
        score=1.0,
        rank=rank,
    )


def test_recall_at_k() -> None:
    results = [
        _result("D1", 1),
        _result("D5", 2),
        _result("D3", 3),
        _result("D8", 4),
        _result("D2", 5),
    ]

    relevant = {"D1", "D3", "D7", "D9"}

    assert recall_at_k(results, relevant, k=5) == 0.5


def test_recall_at_k_respects_k() -> None:
    results = [
        _result("D1", 1),
        _result("D5", 2),
        _result("D3", 3),
    ]

    relevant = {"D1", "D3"}

    assert recall_at_k(results, relevant, k=1) == 0.5
    assert recall_at_k(results, relevant, k=3) == 1.0


@pytest.mark.parametrize("k", [0, -1])
def test_recall_at_k_invalid_k(k: int) -> None:
    results = [
        _result("D1", 1),
        _result("D5", 2),
        _result("D3", 3),
    ]

    relevant = {"D1", "D3"}

    with pytest.raises(ValueError, match="k must be greater than 0"):
        recall_at_k(results, relevant, k=k)


def test_recall_at_k_empty_relevant_documents() -> None:
    with pytest.raises(
        ValueError,
        match="relevant_document_ids must not be empty",
    ):
        recall_at_k([], set(), k=1)


def test_rr() -> None:
    results = [
        _result("D5", 1),
        _result("D8", 2),
        _result("D3", 3),
    ]

    assert rr(results, relevant_document_ids={"D3"}) == 1 / 3


def test_rr_no_relevant_documents() -> None:
    results = [
        _result("D5", 1),
        _result("D8", 2),
        _result("D3", 3),
    ]

    assert rr(results, relevant_document_ids={"D1"}) == 0.0


def test_rr_empty_relevant_documents() -> None:
    results = [
        _result("D5", 1),
        _result("D8", 2),
        _result("D3", 3),
    ]

    with pytest.raises(ValueError, match="relevant_document_ids must not be empty"):
        rr(results, relevant_document_ids=set())


def test_ndcg_at_k() -> None:
    results = [
        _result("D1", 1),
        _result("D2", 2),
        _result("D3", 3),
    ]

    relevance = {
        "D1": 3.0,
        "D2": 2.0,
        "D3": 1.0,
    }

    assert ndcg_at_k(results, relevance, k=3, gain="linear") == pytest.approx(1.0)
    assert ndcg_at_k(results, relevance, k=3, gain="exponential") == pytest.approx(1.0)


def test_ndcg_at_k_penalizes_non_ideal_ranking() -> None:
    results = [
        _result("D3", 1),
        _result("D2", 2),
        _result("D1", 3),
    ]

    relevance = {
        "D1": 3.0,
        "D2": 2.0,
        "D3": 1.0,
    }

    score = ndcg_at_k(
        results,
        relevance,
        k=3,
        gain="linear",
    )

    assert 0.0 < score < 1.0


def test_ndcg_gain_methods_weight_relevance_differently() -> None:
    results = [
        _result("D3", 1),
        _result("D2", 2),
        _result("D1", 3),
    ]

    relevance = {
        "D1": 3.0,
        "D2": 2.0,
        "D3": 1.0,
    }

    linear = ndcg_at_k(
        results,
        relevance,
        k=3,
        gain="linear",
    )

    exponential = ndcg_at_k(
        results,
        relevance,
        k=3,
        gain="exponential",
    )

    assert exponential < linear


def test_ndcg_at_k_respects_k() -> None:
    results = [
        _result("D1", 1),
        _result("D3", 2),
        _result("D2", 3),
    ]

    relevance = {
        "D1": 3.0,
        "D2": 2.0,
        "D3": 1.0,
    }

    assert ndcg_at_k(results, relevance, k=1) == pytest.approx(1.0)
    assert ndcg_at_k(results, relevance, k=3) < 1.0


@pytest.mark.parametrize("k", [0, -1])
def test_ndcg_at_k_invalid_k(k: int) -> None:
    results = [
        _result("D1", 1),
        _result("D2", 2),
        _result("D3", 3),
    ]

    relevance = {
        "D1": 3.0,
        "D2": 2.0,
        "D3": 1.0,
    }

    with pytest.raises(ValueError, match="k must be greater than 0"):
        ndcg_at_k(results, relevance, k=k)


def test_ndcg_at_k_empty_relevance() -> None:
    results = [
        _result("D1", 1),
        _result("D2", 2),
        _result("D3", 3),
    ]

    with pytest.raises(ValueError, match="relevance must not be empty"):
        ndcg_at_k(results, {}, k=3)
