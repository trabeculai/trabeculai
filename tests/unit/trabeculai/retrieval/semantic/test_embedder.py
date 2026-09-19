import pytest

from tests.fakes import FakeEmbedder


def test_fake_embedder() -> None:
    fake_embedder = FakeEmbedder({"renal": [1.0, 0.0]})
    assert fake_embedder.embed_document("renal") == [1.0, 0.0]
    assert fake_embedder.embed_query("renal") == [1.0, 0.0]


def test_fake_embedder_unknown_text() -> None:
    fake_embedder = FakeEmbedder({"renal": [1.0, 0.0]})
    with pytest.raises(ValueError):
        fake_embedder.embed_document("cardio")

    with pytest.raises(ValueError):
        fake_embedder.embed_query("cardio")
