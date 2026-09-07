import pytest

from trabeculai.retrieval.models import EvidenceDocument
from trabeculai.retrieval.vector import (
    FakeEmbedder,
    SemanticRetriever,
    Vector,
    VectorIndex,
    cosine_similarity,
    dot_product,
    magnitude,
    rank_vectors,
)


def test_dot_product() -> None:
    a = [1.0, 2.0, 3.0]
    b = [4.0, 5.0, 6.0]
    expected_result = 32.0  # 1*4 + 2*5 + 3*6
    assert dot_product(a, b) == pytest.approx(expected_result)


def test_dot_product_should_fail_when_vectors_have_different_dimensions() -> None:
    a = [1.0, 2.0]
    b = [1.0, 2.0, 3.0]

    with pytest.raises(ValueError):
        dot_product(a, b)


def test_magnitude() -> None:
    vector = [3.0, 4.0]

    assert magnitude(vector) == pytest.approx(5.0)


@pytest.mark.parametrize(
    "a, b, expected",
    [
        ([1.0, 0.0], [1.0, 0.0], 1.0),  # Same direction
        ([1.0, 0.0], [0.0, 1.0], 0.0),  # Perpendicular
        ([1.0, 0.0], [-1.0, 0.0], -1.0),  # Opposite direction
    ],
)
def test_cosine_similarity(a: Vector, b: Vector, expected: float) -> None:
    assert cosine_similarity(a, b) == pytest.approx(expected)


@pytest.mark.parametrize(
    "a, b",
    [
        ([0.0, 0.0], [1.0, 1.0]),
        ([1.0, 1.0], [0.0, 0.0]),
        ([0.0, 0.0], [0.0, 0.0]),
    ],
)
def test_cosine_similarity_arbitrary_zero_vector(a: Vector, b: Vector) -> None:
    with pytest.raises(ValueError):
        cosine_similarity(a, b)


def test_rank_vectors() -> None:
    documents = {
        "renal": [1.0, 0.1],
        "cardio": [0.1, 1.0],
        "mixed": [0.7, 0.7],
    }

    query = [0.9, 0.2]

    results = rank_vectors(query, documents)

    assert results[0][0] == "renal"
    assert results[1][0] == "mixed"
    assert results[2][0] == "cardio"


@pytest.mark.parametrize(
    "top_k, count_expected",
    [(1, 1), (2, 2), (3, 3), (None, 3), (100, 3)],
)
def test_rank_vectors_with_top_k(top_k: int | None, count_expected: int) -> None:
    documents = {
        "renal": [1.0, 0.1],
        "cardio": [0.1, 1.0],
        "mixed": [0.7, 0.7],
    }

    query = [0.9, 0.2]

    results = rank_vectors(query, documents, top_k=top_k)

    assert len(results) == count_expected


def test_rank_vectors_should_fail_when_top_k_is_zero_or_negative() -> None:
    documents = {
        "renal": [1.0, 0.1],
        "cardio": [0.1, 1.0],
        "mixed": [0.7, 0.7],
    }

    query = [0.9, 0.2]

    with pytest.raises(ValueError):
        rank_vectors(query, documents, top_k=0)

    with pytest.raises(ValueError):
        rank_vectors(query, documents, top_k=-1)


def test_vector_index_search() -> None:
    index = VectorIndex()

    index.add("renal", [1.0, 0.1])
    index.add("cardio", [0.1, 1.0])
    index.add("mixed", [0.7, 0.7])

    results = index.search([0.9, 0.2], top_k=2)

    assert results[0][0] == "renal"
    assert results[1][0] == "mixed"


def test_fake_embedder() -> None:
    embedder = FakeEmbedder({"renal": [1.0, 0.0]})

    assert embedder.embed_document("renal") == [1.0, 0.0]
    assert embedder.embed_query("renal") == [1.0, 0.0]


def test_fake_embedder_unknown_text() -> None:
    embedder = FakeEmbedder({"renal": [1.0, 0.0]})

    with pytest.raises(ValueError):
        embedder.embed_document("cardio")

    with pytest.raises(ValueError):
        embedder.embed_query("cardio")


def test_semantic_retriever(evidence_documents: list[EvidenceDocument]) -> None:
    renal_doc = evidence_documents[0]
    cardio_doc = evidence_documents[1]

    embedder = FakeEmbedder(
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
