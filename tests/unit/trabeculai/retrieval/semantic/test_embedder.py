import pytest

from trabeculai.retrieval.semantic import Embedder


@pytest.mark.fake_embedder(embeddings={"renal": [1.0, 0.0]})
def test_fake_embedder(fake_embedder: Embedder) -> None:
    assert fake_embedder.embed_document("renal") == [1.0, 0.0]
    assert fake_embedder.embed_query("renal") == [1.0, 0.0]


@pytest.mark.fake_embedder(embeddings={"renal": [1.0, 0.0]})
def test_fake_embedder_unknown_text(fake_embedder: Embedder) -> None:
    with pytest.raises(ValueError):
        fake_embedder.embed_document("cardio")

    with pytest.raises(ValueError):
        fake_embedder.embed_query("cardio")
