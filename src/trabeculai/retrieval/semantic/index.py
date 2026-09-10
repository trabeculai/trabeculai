from collections.abc import Mapping

from .vector import Vector, cosine_similarity


def rank_vectors(
    query: Vector,
    documents: Mapping[str, Vector],
    top_k: int | None = None,
) -> list[tuple[str, float]]:
    if top_k is not None and top_k <= 0:
        raise ValueError("top_k must be greater than 0 or None.")

    similarities = {
        doc_id: cosine_similarity(query, vector) for doc_id, vector in documents.items()
    }
    sorted_similarities = sorted(similarities.items(), key=lambda item: item[1], reverse=True)

    return sorted_similarities[: top_k or len(sorted_similarities)]


class VectorIndex:
    def __init__(self) -> None:
        self._vectors: dict[str, Vector] = {}
        self._dimension: int | None = None

    @property
    def dimension(self) -> int | None:
        return self._dimension

    def add(self, document_id: str, vector: Vector) -> None:
        if document_id in self._vectors:
            raise ValueError(f"Document ID '{document_id}' already exists in the index.")

        if self._dimension is None:
            self._dimension = len(vector)

        if len(vector) != self._dimension:
            raise ValueError(
                f"Vector dimension mismatch: expected {self._dimension}, got {len(vector)}."
            )

        self._vectors[document_id] = vector

    def search(
        self,
        query: Vector,
        top_k: int | None = None,
    ) -> list[tuple[str, float]]:
        if self._dimension is None:
            raise ValueError("The index is empty. Add vectors before searching.")

        if len(query) != self._dimension:
            raise ValueError(
                f"Query vector dimension mismatch: expected {self._dimension}, got {len(query)}."
            )
        return rank_vectors(query, self._vectors, top_k)
