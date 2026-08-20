from dataclasses import dataclass


@dataclass(frozen=True)
class EvidenceDocument:
    id: str
    title: str
    text: str
    source: str


@dataclass(frozen=True)
class RetrievalResult:
    document: EvidenceDocument
    score: float
    rank: int
