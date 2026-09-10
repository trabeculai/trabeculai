import pytest

from trabeculai.retrieval.hybrid import reciprocal_rank_fusion


def test_reciprocal_rank_fusion_prioritizes_documents_across_rankings() -> None:
    rankings = [
        ["D1", "D2", "D3"],
        ["D1", "D3", "D2"],
    ]

    result = reciprocal_rank_fusion(rankings, k=60)

    assert result[0][0] == "D1"


def test_reciprocal_rank_fusion_includes_documents_from_single_ranking() -> None:
    rankings = [
        ["D1", "D2"],
        ["D1", "D3"],
    ]

    result = reciprocal_rank_fusion(rankings, k=60)

    document_ids = [document_id for document_id, _ in result]

    assert document_ids == ["D1", "D2", "D3"]


def test_reciprocal_rank_fusion_prioritizes_higher_ranked_documents() -> None:
    rankings = [
        ["D1", "D2", "D3"],
        ["D2", "D3", "D1"],
    ]

    result = reciprocal_rank_fusion(rankings, k=60)

    assert result[0][0] == "D2"


def test_reciprocal_rank_fusion_returns_empty_for_empty_rankings() -> None:
    result = reciprocal_rank_fusion([])

    assert result == []


@pytest.mark.parametrize("k", [-1, -10])
def test_reciprocal_rank_fusion_rejects_negative_k(k: int) -> None:
    with pytest.raises(ValueError, match="k must be greater than or equal to 0"):
        reciprocal_rank_fusion(rankings=[["D1", "D2"]], k=k)


def test_reciprocal_rank_fusion_ignores_empty_rankings() -> None:
    rankings = [
        [],
        ["D1", "D2"],
    ]

    result = reciprocal_rank_fusion(rankings)

    assert [document_id for document_id, _ in result] == ["D1", "D2"]


def test_reciprocal_rank_fusion_accumulates_scores_across_rankings() -> None:
    rankings = [
        ["D1", "D2", "D3"],
        ["D1", "D3", "D2"],
    ]

    result = reciprocal_rank_fusion(rankings, k=60)

    scores = dict(result)

    assert scores["D1"] == pytest.approx(1 / 61 + 1 / 61)
    assert scores["D2"] == pytest.approx(1 / 62 + 1 / 63)
    assert scores["D3"] == pytest.approx(1 / 63 + 1 / 62)
