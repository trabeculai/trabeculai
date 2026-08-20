import json
from pathlib import Path

from pydantic import BaseModel

from ..models import EvidenceDocument
from .models import EvaluationQuery, Qrel, RetrievalEvaluationDataset

_DOCUMENTS_FILE_NAME = "documents.jsonl"
_QUERIES_FILE_NAME = "queries.jsonl"
_QRELS_FILE_NAME = "qrels.jsonl"


def _load_jsonl[T_JsonModel: BaseModel](path: Path, model: type[T_JsonModel]) -> list[T_JsonModel]:
    with path.open(encoding="utf-8") as file:
        return [model.model_validate_json(line) for line in file if line.strip()]


def _load_documents(path: Path) -> list[EvidenceDocument]:
    documents = []

    with path.open(encoding="utf-8") as file:
        for line in file:
            if not line.strip():
                continue

            data = json.loads(line)

            documents.append(EvidenceDocument(**data))

    return documents


def load_evaluation_dataset(path: Path) -> RetrievalEvaluationDataset:
    return RetrievalEvaluationDataset(
        documents=_load_documents(path / _DOCUMENTS_FILE_NAME),
        queries=_load_jsonl(path / _QUERIES_FILE_NAME, EvaluationQuery),
        qrels=_load_jsonl(path / _QRELS_FILE_NAME, Qrel),
    )
