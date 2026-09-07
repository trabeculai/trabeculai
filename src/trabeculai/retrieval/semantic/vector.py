from collections.abc import Sequence
from math import sqrt

Vector = Sequence[float]


def dot_product(a: Vector, b: Vector) -> float:
    return sum(x * y for x, y in zip(a, b, strict=True))


def magnitude(vector: Vector) -> float:
    return sqrt(dot_product(vector, vector))


def cosine_similarity(a: Vector, b: Vector) -> float:
    magnitude_a = magnitude(a)
    magnitude_b = magnitude(b)

    if magnitude_a == 0 or magnitude_b == 0:
        raise ValueError("Cosine similarity is undefined for zero vectors.")

    return dot_product(a, b) / (magnitude_a * magnitude_b)
