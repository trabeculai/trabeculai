import pytest

from trabeculai.retrieval.evaluation import (
    EvaluationQuery,
    Qrel,
    RetrievalEvaluationDataset,
    evaluate_retriever,
)
from trabeculai.retrieval.models import EvidenceDocument, RetrievalResult


def _document(document_id: str) -> EvidenceDocument:
    return EvidenceDocument(
        id=document_id,
        title=document_id,
        text="",
        source="test",
    )


def _result(document: EvidenceDocument, rank: int) -> RetrievalResult:
    return RetrievalResult(
        document=document,
        score=1.0,
        rank=rank,
    )


class FakeRetriever:
    def __init__(
        self,
        results_by_query: dict[str, list[RetrievalResult]],
    ) -> None:
        self._results_by_query = results_by_query
        self.calls: list[tuple[str, int]] = []

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[RetrievalResult]:
        self.calls.append((query, top_k))
        return self._results_by_query[query][:top_k]


def test_evaluate_retriever() -> None:
    d1 = _document("D1")
    d2 = _document("D2")

    dataset = RetrievalEvaluationDataset(
        documents=[d1, d2],
        queries=[
            EvaluationQuery(id="Q1", text="query one"),
            EvaluationQuery(id="Q2", text="query two"),
        ],
        qrels=[
            Qrel(query_id="Q1", document_id="D1", relevance=1.0),
            Qrel(query_id="Q2", document_id="D2", relevance=1.0),
        ],
    )

    retriever = FakeRetriever(
        {
            "query one": [
                _result(d1, 1),
                _result(d2, 2),
            ],
            "query two": [
                _result(d1, 1),
                _result(d2, 2),
            ],
        }
    )

    report = evaluate_retriever(retriever, dataset, k=1)

    assert report.k == 1
    assert report.mean_recall_at_k == pytest.approx(0.5)
    assert report.mrr == pytest.approx(0.75)
    assert report.mean_ndcg_at_k == pytest.approx(0.5)

    assert len(report.queries) == 2

    q1_result = report.queries[0]
    q2_result = report.queries[1]

    assert q1_result.query_id == "Q1"
    assert q1_result.recall_at_k == pytest.approx(1.0)
    assert q1_result.reciprocal_rank == pytest.approx(1.0)
    assert q1_result.ndcg_at_k == pytest.approx(1.0)

    assert q2_result.query_id == "Q2"
    assert q2_result.recall_at_k == pytest.approx(0.0)
    assert q2_result.reciprocal_rank == pytest.approx(0.5)
    assert q2_result.ndcg_at_k == pytest.approx(0.0)

    assert retriever.calls == [
        ("query one", 2),
        ("query two", 2),
    ]


def test_evaluate_retriever_rejects_dataset_without_queries() -> None:
    dataset = RetrievalEvaluationDataset(
        documents=[],
        queries=[],
        qrels=[],
    )

    retriever = FakeRetriever({})

    with pytest.raises(ValueError, match="dataset must contain queries"):
        evaluate_retriever(retriever, dataset, k=1)


@pytest.mark.parametrize("k", [0, -1])
def test_evaluate_retriever_rejects_invalid_k(k: int) -> None:
    dataset = RetrievalEvaluationDataset(
        documents=[],
        queries=[
            EvaluationQuery(
                id="Q1",
                text="query",
            ),
        ],
        qrels=[
            Qrel(
                query_id="Q1",
                document_id="D1",
                relevance=1.0,
            ),
        ],
    )

    retriever = FakeRetriever({})

    with pytest.raises(ValueError, match="k must be greater than 0"):
        evaluate_retriever(retriever, dataset, k=k)
