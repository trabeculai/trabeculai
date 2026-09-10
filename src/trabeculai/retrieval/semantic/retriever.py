import asyncio

from ..models import EvidenceDocument, RetrievalResult
from .embedder import Embedder
from .index import VectorIndex


class SemanticRetriever:
    def __init__(self, documents: list[EvidenceDocument], embedder: Embedder) -> None:
        self._embedder = embedder
        self._documents = {document.id: document for document in documents}
        self._index = VectorIndex()

        for document in documents:
            text = f"{document.title} {document.text}"
            vector = self._embedder.embed_document(text)
            self._index.add(document.id, vector)

    async def retrieve(self, query: str, top_k: int = 5) -> list[RetrievalResult]:
        query_vector = await asyncio.to_thread(self._embedder.embed_query, query)
        ranked_vectors = self._index.search(query_vector, top_k)

        return [
            RetrievalResult(
                document=self._documents[document_id],
                score=score,
                rank=rank,
            )
            for rank, (document_id, score) in enumerate(ranked_vectors, start=1)
        ]
