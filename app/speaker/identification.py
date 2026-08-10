from pathlib import Path

import numpy as np

from app.speaker.embedding import extract_embedding


SPEAKER_DIR = Path("data/speakers")

# Nilai awal untuk pembelajaran.
# Threshold sebenarnya perlu dikalibrasi dari sampel nyata.
DEFAULT_THRESHOLD = 0.65


def cosine_similarity(
    vector_a: np.ndarray,
    vector_b: np.ndarray,
) -> float:
    """
    Calculate cosine similarity between two embeddings.
    """

    denominator = (
        np.linalg.norm(vector_a)
        * np.linalg.norm(vector_b)
    )

    if denominator == 0:
        return -1.0

    score = np.dot(
        vector_a,
        vector_b,
    ) / denominator

    return float(score)


def identify_speaker(
    audio_path: str,
    threshold: float = DEFAULT_THRESHOLD,
) -> dict:
    """
    Compare a new voice recording against all
    enrolled speaker profiles.

    Returns:
    - matched speaker
    - best candidate
    - similarity score
    - threshold
    """

    if not 0.0 <= threshold <= 1.0:
        raise ValueError(
            "Threshold must be between 0 and 1."
        )

    profiles = list(
        SPEAKER_DIR.glob("*.npy")
    )

    if not profiles:
        return {
            "speaker": "Unknown",
            "best_candidate": None,
            "score": 0.0,
            "threshold": threshold,
            "matched": False,
            "reason": "No enrolled speakers.",
        }

    candidate_embedding = extract_embedding(
        audio_path
    )

    best_name = None
    best_score = -1.0

    for profile_path in profiles:
        enrolled_embedding = np.load(
            profile_path
        )

        score = cosine_similarity(
            candidate_embedding,
            enrolled_embedding,
        )

        if score > best_score:
            best_score = score
            best_name = profile_path.stem

    matched = best_score >= threshold

    return {
        "speaker": (
            best_name
            if matched
            else "Unknown"
        ),
        "best_candidate": best_name,
        "score": round(
            best_score,
            4,
        ),
        "threshold": threshold,
        "matched": matched,
    }