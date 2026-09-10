import pytest

from trabeculai.retrieval.semantic import Vector, cosine_similarity, dot_product, magnitude


def test_dot_product() -> None:
    a = [1.0, 2.0, 3.0]
    b = [4.0, 5.0, 6.0]
    expected_result = 32.0  # 1*4 + 2*5 + 3*6
    assert dot_product(a, b) == pytest.approx(expected_result)


def test_dot_product_should_fail_when_vectors_have_different_dimensions() -> None:
    a = [1.0, 2.0]
    b = [1.0, 2.0, 3.0]

    with pytest.raises(ValueError):
        dot_product(a, b)


def test_magnitude() -> None:
    vector = [3.0, 4.0]

    assert magnitude(vector) == pytest.approx(5.0)


@pytest.mark.parametrize(
    "a, b, expected",
    [
        ([1.0, 0.0], [1.0, 0.0], 1.0),  # Same direction
        ([1.0, 0.0], [0.0, 1.0], 0.0),  # Perpendicular
        ([1.0, 0.0], [-1.0, 0.0], -1.0),  # Opposite direction
    ],
)
def test_cosine_similarity(a: Vector, b: Vector, expected: float) -> None:
    assert cosine_similarity(a, b) == pytest.approx(expected)


@pytest.mark.parametrize(
    "a, b",
    [
        ([0.0, 0.0], [1.0, 1.0]),
        ([1.0, 1.0], [0.0, 0.0]),
        ([0.0, 0.0], [0.0, 0.0]),
    ],
)
def test_cosine_similarity_arbitrary_zero_vector(a: Vector, b: Vector) -> None:
    with pytest.raises(ValueError):
        cosine_similarity(a, b)
