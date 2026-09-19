from typing import Protocol

from trabeculai.retrieval.models import RetrievalResult


class Retriever(Protocol):
    async def retrieve(self, query: str, top_k: int = 5) -> list[RetrievalResult]: ...
