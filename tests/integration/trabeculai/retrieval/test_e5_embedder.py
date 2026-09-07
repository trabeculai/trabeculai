import pytest

from trabeculai.retrieval.models import EvidenceDocument
from trabeculai.retrieval.vector import (
    E5SentenceTransformerEmbedder,
    SemanticRetriever,
    cosine_similarity,
    magnitude,
)


@pytest.fixture(scope="session")
def e5_embedder() -> E5SentenceTransformerEmbedder:
    return E5SentenceTransformerEmbedder()


@pytest.mark.integration
def test_sentence_transformer_embedder(e5_embedder: E5SentenceTransformerEmbedder) -> None:
    embedding = e5_embedder.embed_query("rim parou de funcionar")

    assert len(embedding) == 384


@pytest.mark.integration
def test_sentence_transformer_embedder_returns_normalized_vector(
    e5_embedder: E5SentenceTransformerEmbedder,
) -> None:

    embedding = e5_embedder.embed_query("rim parou de funcionar")

    assert magnitude(embedding) == pytest.approx(1.0)


@pytest.mark.integration
def test_e5_semantic_similarity(e5_embedder: E5SentenceTransformerEmbedder) -> None:
    query = e5_embedder.embed_query("rim parou de funcionar")

    renal = e5_embedder.embed_document(
        "pacientes com insuficiência renal podem necessitar de diálise"
    )
    cardio = e5_embedder.embed_document("a pressão arterial deve ser monitorada regularmente")

    renal_score = cosine_similarity(query, renal)
    cardio_score = cosine_similarity(query, cardio)

    assert renal_score > cardio_score


@pytest.mark.integration
def test_semantic_retriever_with_e5_embedder(e5_embedder: E5SentenceTransformerEmbedder) -> None:
    renal_doc = EvidenceDocument(
        id="renal",
        title="Insuficiência renal",
        text="Pacientes com insuficiência renal podem necessitar de diálise.",
        source="test",
    )

    cardio_doc = EvidenceDocument(
        id="cardio",
        title="Hipertensão arterial",
        text="A pressão arterial deve ser monitorada regularmente.",
        source="test",
    )

    unrelated_doc = EvidenceDocument(
        id="bank",
        title="Banco",
        text="O banco oferece financiamento para aquisição de equipamentos.",
        source="test",
    )

    retriever = SemanticRetriever(
        [renal_doc, cardio_doc, unrelated_doc],
        e5_embedder,
    )

    results = retriever.retrieve(
        "rim parou de funcionar",
        top_k=3,
    )

    assert results[0].document.id == "renal"
    assert results[0].rank == 1

    renal_score = results[0].score
    negative_scores = [result.score for result in results[1:]]

    assert renal_score > max(negative_scores)
