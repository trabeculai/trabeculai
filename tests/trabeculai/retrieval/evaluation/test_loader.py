from pathlib import Path

from trabeculai.retrieval.evaluation import load_evaluation_dataset

DATASET_PATH = Path("data/evaluation/retrieval")


def test_load_evaluation_dataset() -> None:
    dataset = load_evaluation_dataset(DATASET_PATH)

    assert dataset.documents
    assert dataset.queries
    assert dataset.qrels


def test_qrels_reference_existing_documents_and_queries() -> None:
    dataset = load_evaluation_dataset(DATASET_PATH)

    document_ids = {document.id for document in dataset.documents}
    query_ids = {query.id for query in dataset.queries}

    for qrel in dataset.qrels:
        assert qrel.document_id in document_ids
        assert qrel.query_id in query_ids


def test_qrels_have_non_negative_relevance() -> None:
    dataset = load_evaluation_dataset(DATASET_PATH)

    assert all(qrel.relevance >= 0 for qrel in dataset.qrels)


def test_documents_have_unique_ids() -> None:
    dataset = load_evaluation_dataset(DATASET_PATH)

    ids = [document.id for document in dataset.documents]

    assert len(ids) == len(set(ids))


def test_queries_have_unique_ids() -> None:
    dataset = load_evaluation_dataset(DATASET_PATH)

    ids = [query.id for query in dataset.queries]

    assert len(ids) == len(set(ids))
