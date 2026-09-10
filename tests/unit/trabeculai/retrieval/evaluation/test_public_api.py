import trabeculai.retrieval.evaluation as evaluation


def test_public_api_exports_are_available() -> None:
    for name in evaluation.__all__:
        assert hasattr(evaluation, name)
