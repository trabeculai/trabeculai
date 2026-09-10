from trabeculai.retrieval.models import RetrievalResult


class FakeRetriever:
    def __init__(
        self,
        results_by_query: dict[str, list[RetrievalResult]],
    ) -> None:
        self._results_by_query = results_by_query
        self.calls: list[tuple[str, int]] = []

    async def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[RetrievalResult]:
        self.calls.append((query, top_k))
        return self._results_by_query.get(query, [])[:top_k]
