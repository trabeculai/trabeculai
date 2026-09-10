from trabeculai.retrieval.semantic.vector import Vector


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
