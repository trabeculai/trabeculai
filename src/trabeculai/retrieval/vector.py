from collections.abc import Mapping, Sequence
from math import sqrt
from typing import Protocol

from sentence_transformers import SentenceTransformer

from .models import EvidenceDocument, RetrievalResult

Vector = Sequence[float]


def dot_product(a: Vector, b: Vector) -> float:
    return sum(x * y for x, y in zip(a, b, strict=True))


def magnitude(vector: Vector) -> float:
    return sqrt(dot_product(vector, vector))


def cosine_similarity(a: Vector, b: Vector) -> float:
    magnitude_a = magnitude(a)
    magnitude_b = magnitude(b)

    if magnitude_a == 0 or magnitude_b == 0:
        raise ValueError("Cosine similarity is undefined for zero vectors.")

    return dot_product(a, b) / (magnitude_a * magnitude_b)


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


class Embedder(Protocol):
    def embed_document(self, text: str) -> Vector: ...
    def embed_query(self, text: str) -> Vector: ...


class FakeEmbedder:
    def __init__(self, embeddings: dict[str, Vector]) -> None:
        self._embeddings = embeddings

    def embed_document(self, text: str) -> Vector:
        return self._embed(text)

    def embed_query(self, text: str) -> Vector:
        return self._embed(text)

    def _embed(self, text: str) -> Vector:
        if text not in self._embeddings:
            raise ValueError(f"No fake embedding configured for text: {text!r}")

        return self._embeddings[text]


class SemanticRetriever:
    def __init__(self, documents: list[EvidenceDocument], embedder: Embedder) -> None:
        self._embedder = embedder
        self._documents = {document.id: document for document in documents}
        self._index = VectorIndex()

        for document in documents:
            text = f"{document.title} {document.text}"
            vector = self._embedder.embed_document(text)
            self._index.add(document.id, vector)

    def retrieve(self, query: str, top_k: int = 5) -> list[RetrievalResult]:
        query_vector = self._embedder.embed_query(query)
        ranked_vectors = self._index.search(query_vector, top_k)

        return [
            RetrievalResult(
                document=self._documents[document_id],
                score=score,
                rank=rank,
            )
            for rank, (document_id, score) in enumerate(ranked_vectors, start=1)
        ]


class SentenceTransformerEmbedder:
    def __init__(self, model_name: str) -> None:
        self._model = SentenceTransformer(model_name)

    def embed_query(self, text: str) -> Vector:
        embedding = self._model.encode_query(self._prepare_query(text), normalize_embeddings=True)
        return [float(value) for value in embedding]

    def embed_document(self, text: str) -> Vector:
        embedding = self._model.encode_document(
            self._prepare_document(text), normalize_embeddings=True
        )
        return [float(value) for value in embedding]

    def _prepare_query(self, text: str) -> str:
        return text

    def _prepare_document(self, text: str) -> str:
        return text


class E5SentenceTransformerEmbedder(SentenceTransformerEmbedder):
    def __init__(self, model_name: str = "intfloat/multilingual-e5-small") -> None:
        super().__init__(model_name)

    def _prepare_query(self, text: str) -> str:
        return f"query: {text}"

    def _prepare_document(self, text: str) -> str:
        return f"passage: {text}"
