from collections.abc import Sequence


def reciprocal_rank_fusion(
    rankings: Sequence[Sequence[str]], k: int = 60
) -> list[tuple[str, float]]:
    if k < 0:
        raise ValueError("k must be greater than or equal to 0")
    scores: dict[str, float] = {}

    for ranking in rankings:
        for rank, document_id in enumerate(ranking, start=1):
            score = 1 / (k + rank)

            scores[document_id] = scores.get(document_id, 0.0) + score

    return sorted(
        scores.items(),
        key=lambda item: item[1],
        reverse=True,
    )
