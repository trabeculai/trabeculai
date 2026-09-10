from typing import Protocol

from sentence_transformers import SentenceTransformer

from .vector import Vector


class Embedder(Protocol):
    def embed_document(self, text: str) -> Vector: ...
    def embed_query(self, text: str) -> Vector: ...


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
