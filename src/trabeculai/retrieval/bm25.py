import math
import re
from collections import Counter
from collections.abc import Callable
from functools import cached_property

from .models import EvidenceDocument, RetrievalResult


def _document_indexer(
    documents: list[EvidenceDocument],
    tokenizer: Callable[[str], list[str]],
) -> tuple[list[Counter[str]], Counter[str], list[int]]:
    term_frequencies: list[Counter[str]] = []
    document_frequencies: Counter[str] = Counter()
    document_lengths: list[int] = []

    for document in documents:
        text = f"{document.title} {document.text}"
        tokens = tokenizer(text)

        term_frequency = Counter(tokens)

        term_frequencies.append(term_frequency)
        document_lengths.append(len(tokens))

        document_frequencies.update(set(tokens))
    return term_frequencies, document_frequencies, document_lengths


class BM25Retriever:
    @staticmethod
    def tokenize(text: str) -> list[str]:
        return re.findall(r"\b\w+\b", text.lower())

    def __init__(self, documents: list[EvidenceDocument], k1: float = 1.5, b: float = 0.75) -> None:
        self._documents = documents
        self._k1 = k1
        self._b = b

        self._term_frequencies, self._document_frequencies, self._document_lengths = (
            _document_indexer(self._documents, self.tokenize)
        )

    @cached_property
    def _average_document_length(self) -> float:
        return (
            sum(self._document_lengths) / len(self._document_lengths)
            if self._document_lengths
            else 0.0
        )

    def _idf(self, term: str) -> float:
        document_frequency = self._document_frequencies.get(term, 0)
        number_of_documents = len(self._documents)

        return math.log(
            1 + (number_of_documents - document_frequency + 0.5) / (document_frequency + 0.5)
        )

    def _score(self, query_tokens: list[str], document_index: int) -> float:
        term_frequency = self._term_frequencies[document_index]
        document_length = self._document_lengths[document_index]

        score = 0.0

        for term in query_tokens:
            frequency = term_frequency.get(term, 0)

            if frequency == 0:
                continue

            idf = self._idf(term)

            numerator = frequency * (self._k1 + 1)

            denominator = frequency + self._k1 * (
                1 - self._b + self._b * document_length / self._average_document_length
            )

            score += idf * numerator / denominator

        return score

    def retrieve(self, query: str, top_k: int = 5) -> list[RetrievalResult]:
        if top_k <= 0:
            raise ValueError("top_k must be greater than 0")

        query_tokens = list(dict.fromkeys(self.tokenize(query)))

        scored_documents = [
            (document, self._score(query_tokens, index))
            for index, document in enumerate(self._documents)
        ]

        ranked_documents = sorted(scored_documents, key=lambda x: x[1], reverse=True)
        return [
            RetrievalResult(document=doc, score=score, rank=rank)
            for rank, (doc, score) in enumerate(ranked_documents[:top_k], start=1)
            if score > 0
        ]
