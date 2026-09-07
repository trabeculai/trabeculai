import pytest

from trabeculai.retrieval.semantic import VectorIndex, rank_vectors


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
