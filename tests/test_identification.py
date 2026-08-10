import numpy as np

from app.speaker.identification import cosine_similarity


def test_same_embedding_has_high_similarity():
    """
    Two identical embeddings should have
    cosine similarity close to 1.
    """

    vector = np.array(
        [0.1, 0.2, 0.3, 0.4],
        dtype=np.float32,
    )

    score = cosine_similarity(
        vector,
        vector,
    )

    assert np.isclose(
        score,
        1.0,
        atol=1e-6,
    )


def test_opposite_embeddings_have_negative_similarity():
    """
    Opposite vectors should have
    cosine similarity close to -1.
    """

    vector_a = np.array(
        [1.0, 0.0],
        dtype=np.float32,
    )

    vector_b = np.array(
        [-1.0, 0.0],
        dtype=np.float32,
    )

    score = cosine_similarity(
        vector_a,
        vector_b,
    )

    assert np.isclose(
        score,
        -1.0,
        atol=1e-6,
    )


def test_orthogonal_embeddings_have_zero_similarity():
    """
    Unrelated orthogonal vectors should have
    cosine similarity close to 0.
    """

    vector_a = np.array(
        [1.0, 0.0],
        dtype=np.float32,
    )

    vector_b = np.array(
        [0.0, 1.0],
        dtype=np.float32,
    )

    score = cosine_similarity(
        vector_a,
        vector_b,
    )

    assert np.isclose(
        score,
        0.0,
        atol=1e-6,
    )


def test_zero_vector_is_rejected_safely():
    """
    A zero vector cannot produce a meaningful
    cosine similarity.

    The function should return -1.
    """

    vector_a = np.array(
        [0.0, 0.0],
        dtype=np.float32,
    )

    vector_b = np.array(
        [1.0, 1.0],
        dtype=np.float32,
    )

    score = cosine_similarity(
        vector_a,
        vector_b,
    )

    assert score == -1.0