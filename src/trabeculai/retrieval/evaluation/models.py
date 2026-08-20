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


@dataclass(frozen=True)
class QueryEvaluationResult:
    query_id: str
    recall_at_k: float
    reciprocal_rank: float
    ndcg_at_k: float


@dataclass(frozen=True)
class RetrievalEvaluationReport:
    k: int
    mean_recall_at_k: float
    mrr: float
    mean_ndcg_at_k: float
    queries: list[QueryEvaluationResult]
