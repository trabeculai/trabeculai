# Synthetic hard retrieval benchmark

This dataset contains **100 passages, 60 Portuguese queries, and 60 graded judgments**. It is separate from the original 12-document baseline in `../retrieval/`. Each of 20 topics has five passages: three closely related targets and two plausible near misses. Queries distinguish, for example, acute from chronic, high from low, one organ from another, and an established finding from a symptom alone. They use patient-like phrasing as well as explicit evidence questions.

All passages are original synthetic examples, not clinical sources. They are intended to test retrieval and ranking behavior; they are **not** suitable as medical evidence or for training clinical decision systems.

## Files and labels

The three JSONL files use the existing `load_evaluation_dataset` schema. IDs have the form `H01D1` for a document and `H01Q1` for a query. Each query has one specifically targeted document with relevance **3**. Every other document is currently **unjudged**, and the evaluator treats it as zero relevance. In particular, a related passage might still be useful to a human. A later, independently reviewed annotation pass should add graded secondary judgments before using this as an authoritative benchmark.

Run the comparison without changing the original baseline:

```bash
uv run python experiments/retrieval/compare_baselines.py --dataset data/evaluation/retrieval_hard --k 3
uv run python experiments/retrieval/compare_baselines.py --dataset data/evaluation/retrieval_hard --k 10
```

Locally measured with the repository's BM25 implementation: Recall@3 **0.9333**, MRR **0.8888**, NDCG@3 **0.8903**; Recall@10 **1.0000**. Thus four of 60 exact targets fall below rank three, while all targets are within the first ten BM25 candidates. This makes the corpus useful for comparing reranking of top ten candidates against an imperfect initial ordering. These numbers describe BM25 only; no improvement from E5, Hybrid, or a future reranker is assumed.

The corpus is deliberately small for a production benchmark. Its topics and wording were authored together and may contain stylistic shortcuts. Compare per-query results, candidate recall, and ranking metrics; do not treat the aggregate score alone as proof of clinical retrieval quality.
