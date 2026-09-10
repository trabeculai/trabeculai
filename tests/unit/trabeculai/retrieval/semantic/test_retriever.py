from collections.abc import Callable, Sequence

from trabeculai.retrieval.models import EvidenceDocument
from trabeculai.retrieval.semantic import Embedder, SemanticRetriever


def test_semantic_retriever(
    evidence_documents: list[EvidenceDocument],
    fake_embedder_factory: Callable[[dict[str, Sequence[float]]], Embedder],
) -> None:
    renal_doc = evidence_documents[0]
    cardio_doc = evidence_documents[1]

    embedder = fake_embedder_factory(
        {
            f"{renal_doc.title} {renal_doc.text}": [1.0, 0.1],
            f"{cardio_doc.title} {cardio_doc.text}": [0.1, 1.0],
            "rim parou de funcionar": [0.9, 0.2],
        }
    )

    retriever = SemanticRetriever([renal_doc, cardio_doc], embedder)

    results = retriever.retrieve(
        "rim parou de funcionar",
        top_k=1,
    )

    assert results[0].document.id == renal_doc.id
    assert results[0].rank == 1
