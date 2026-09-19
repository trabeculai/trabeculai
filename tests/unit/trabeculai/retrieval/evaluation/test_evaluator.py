import pytest

from tests.fakes import FakeRetriever
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


def _result(
    document: EvidenceDocument,
    rank: int,
) -> RetrievalResult:
    return RetrievalResult(
        document=document,
        score=1.0,
        rank=rank,
    )


@pytest.mark.anyio
async def test_evaluate_retriever() -> None:
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

    report = await evaluate_retriever(retriever, dataset, k=1)

    assert report.k == 1
    assert report.mean_recall_at_k == pytest.approx(0.5)
    assert report.mrr == pytest.approx(0.75)
    assert report.mean_ndcg_at_k == pytest.approx(0.5)

    assert retriever.calls == [
        ("query one", 2),
        ("query two", 2),
    ]
