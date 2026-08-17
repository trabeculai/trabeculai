from dataclasses import dataclass

from pydantic import BaseModel

from ..models import EvidenceDocument


class EvaluationQuery(BaseModel):
    id: str
    text: str


class Qrel(BaseModel):
    query_id: str
    document_id: str
    relevance: float


@dataclass(frozen=True)
class RetrievalEvaluationDataset:
    documents: list[EvidenceDocument]
    queries: list[EvaluationQuery]
    qrels: list[Qrel]
