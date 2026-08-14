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
