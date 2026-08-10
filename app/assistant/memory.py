from pathlib import Path
import json
import re


MEMORY_DIR = Path("data/memory")
MEMORY_DIR.mkdir(parents=True, exist_ok=True)


def _safe_name(name: str) -> str:
    """
    Convert a speaker name into a safe filename.
    """

    safe = re.sub(
        r"[^A-Za-z0-9_-]+",
        "_",
        name.strip(),
    ).strip("_")

    return safe or "Unknown"


def _memory_path(speaker: str) -> Path:
    """
    Return the local memory file path for a speaker.
    """

    return MEMORY_DIR / f"{_safe_name(speaker)}.json"


def read_memory(speaker: str) -> dict:
    """
    Read stored memory for a speaker.
    """

    path = _memory_path(speaker)

    if not path.exists():
        return {
            "speaker": speaker,
            "notes": [],
        }

    return json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )


def add_memory(
    speaker: str,
    note: str,
) -> dict:
    """
    Add one memory note to a speaker.
    """

    if not note.strip():
        raise ValueError(
            "Memory note cannot be empty."
        )

    data = read_memory(speaker)

    data["notes"].append(
        note.strip()
    )

    _memory_path(speaker).write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    return data


def clear_memory(speaker: str) -> bool:
    """
    Delete all stored memory for a speaker.
    """

    path = _memory_path(speaker)

    if path.exists():
        path.unlink()
        return True

    return False