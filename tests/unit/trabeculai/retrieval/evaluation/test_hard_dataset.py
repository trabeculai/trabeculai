from pathlib import Path

from trabeculai.retrieval.evaluation import load_evaluation_dataset

DATASET_PATH = Path("data/evaluation/retrieval_hard")


def test_hard_dataset_has_valid_unique_references_and_one_target_per_query() -> None:
    dataset = load_evaluation_dataset(DATASET_PATH)

    document_ids = [document.id for document in dataset.documents]
    query_ids = [query.id for query in dataset.queries]

    assert len(document_ids) == len(set(document_ids)) == 100
    assert len(query_ids) == len(set(query_ids)) == 60
    assert len(dataset.qrels) == 60
    assert all(document.source == "synthetic" for document in dataset.documents)

    targets = {query_id: [] for query_id in query_ids}
    for qrel in dataset.qrels:
        assert qrel.query_id in targets
        assert qrel.document_id in document_ids
        assert qrel.relevance == 3
        targets[qrel.query_id].append(qrel.document_id)

    assert all(len(documents) == 1 for documents in targets.values())
