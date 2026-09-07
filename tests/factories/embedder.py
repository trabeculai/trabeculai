from collections.abc import Callable, Sequence

import pytest

from tests.fakes.embedder import FakeEmbedder
from trabeculai.retrieval.semantic.vector import Vector


@pytest.fixture
def fake_embedder_factory() -> Callable[[dict[str, Vector]], FakeEmbedder]:
    def create_fake_embedder(embeddings: dict[str, Vector]) -> FakeEmbedder:
        return FakeEmbedder(embeddings)

    return create_fake_embedder


@pytest.fixture
def fake_embedder(request: pytest.FixtureRequest) -> FakeEmbedder:
    marker = request.node.get_closest_marker("fake_embedder")

    if marker is None:
        raise ValueError("The 'fake_embedder' marker is required for this test.")

    embeddings = marker.kwargs.get("embeddings")

    if not isinstance(embeddings, dict):
        raise ValueError(
            "The 'embeddings' argument must be provided as a dictionary "
            "for the 'fake_embedder' marker."
        )

    valid_embeddings: dict[str, Vector] = {}

    for key, vector in embeddings.items():
        if not isinstance(key, str):
            raise ValueError("Embedding keys must be strings.")

        if not isinstance(vector, Sequence) or isinstance(vector, (str, bytes)):
            raise ValueError("Embedding vectors must be lists.")

        if not all(isinstance(value, (int, float)) for value in vector):
            raise ValueError("Embedding vector values must be numbers.")

        valid_embeddings[key] = [float(value) for value in vector]

    return FakeEmbedder(valid_embeddings)
