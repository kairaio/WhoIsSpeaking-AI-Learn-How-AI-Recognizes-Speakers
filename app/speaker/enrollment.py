from pathlib import Path
import re

import numpy as np

from app.speaker.embedding import extract_embedding


SPEAKER_DIR = Path("data/speakers")
SPEAKER_DIR.mkdir(parents=True, exist_ok=True)


def normalize_speaker_name(name: str) -> str:
    """
    Convert a speaker name into a safe filename.
    """

    name = name.strip()

    if not name:
        raise ValueError("Speaker name cannot be empty.")

    if len(name) > 60:
        raise ValueError("Speaker name is too long.")

    safe_name = re.sub(
        r"[^A-Za-z0-9_-]+",
        "_",
        name,
    ).strip("_")

    if not safe_name:
        raise ValueError(
            "Speaker name contains no usable characters."
        )

    return safe_name


def profile_path(name: str) -> Path:
    """
    Return the local embedding profile path
    for a speaker.
    """

    safe_name = normalize_speaker_name(name)

    return SPEAKER_DIR / f"{safe_name}.npy"


def enroll_speaker(
    name: str,
    audio_paths: list[str],
) -> dict:
    """
    Create one speaker profile from one or more
    voice recordings.

    Multiple samples are averaged to create
    a more stable speaker embedding.
    """

    if not audio_paths:
        raise ValueError(
            "At least one voice sample is required."
        )

    embeddings = []

    for audio_path in audio_paths:
        embedding = extract_embedding(audio_path)
        embeddings.append(embedding)

    combined = np.stack(embeddings)

    mean_embedding = np.mean(
        combined,
        axis=0,
    )

    norm = np.linalg.norm(mean_embedding)

    if norm == 0:
        raise ValueError(
            "Could not create a valid speaker profile."
        )

    mean_embedding = (
        mean_embedding / norm
    ).astype(np.float32)

    output_path = profile_path(name)

    np.save(
        output_path,
        mean_embedding,
    )

    return {
        "speaker": name.strip(),
        "samples": len(audio_paths),
        "profile_created": True,
        "profile_file": output_path.name,
    }


def list_speakers() -> list[str]:
    """
    Return all currently enrolled speakers.
    """

    speakers = []

    for path in sorted(
        SPEAKER_DIR.glob("*.npy")
    ):
        speakers.append(path.stem)

    return speakers


def delete_speaker(name: str) -> bool:
    """
    Delete an enrolled speaker profile.
    """

    path = profile_path(name)

    if path.exists():
        path.unlink()
        return True

    return False