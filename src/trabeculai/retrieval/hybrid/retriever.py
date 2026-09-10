import asyncio
from collections.abc import Sequence

from ..models import RetrievalResult
from ..retriever import Retriever
from .rrf import reciprocal_rank_fusion


class HybridRetriever:
    def __init__(self, retrievers: Sequence[Retriever], k: int = 60) -> None:
        self._retrievers = retrievers
        self._k = k

    async def retrieve(self, query: str, top_k: int = 5) -> list[RetrievalResult]:
        results: list[list[RetrievalResult]] = await asyncio.gather(
            *[retriever.retrieve(query, top_k=top_k) for retriever in self._retrievers]
        )

        rankings = [
            [result.document.id for result in retriever_results] for retriever_results in results
        ]

        fused_ranking = reciprocal_rank_fusion(rankings, k=self._k)

        documents = {
            result.document.id: result.document
            for retriever_results in results
            for result in retriever_results
        }

        return [
            RetrievalResult(
                document=documents[document_id],
                score=score,
                rank=rank,
            )
            for rank, (document_id, score) in enumerate(
                fused_ranking[:top_k],
                start=1,
            )
        ]
