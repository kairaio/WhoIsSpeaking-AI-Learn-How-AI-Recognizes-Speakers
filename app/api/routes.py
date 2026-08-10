from pathlib import Path
from tempfile import NamedTemporaryFile
import shutil

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.assistant.context import get_context
from app.assistant.memory import add_memory, clear_memory, read_memory
from app.speaker.enrollment import (
    delete_speaker,
    enroll_speaker,
    list_speakers,
)
from app.speaker.identification import identify_speaker


router = APIRouter()

ALLOWED_SUFFIXES = {".wav", ".flac"}
MAX_FILES = 10


def _save_upload(upload: UploadFile) -> str:
    """
    Save an uploaded audio file temporarily.
    """

    suffix = Path(
        upload.filename or ""
    ).suffix.lower()

    if suffix not in ALLOWED_SUFFIXES:
        raise HTTPException(
            status_code=400,
            detail=(
                "Use WAV or FLAC audio "
                "for this educational MVP."
            ),
        )

    temp = NamedTemporaryFile(
        delete=False,
        suffix=suffix,
    )

    temp.close()

    with open(
        temp.name,
        "wb",
    ) as output:
        shutil.copyfileobj(
            upload.file,
            output,
        )

    return temp.name


def _cleanup(paths: list[str]) -> None:
    """
    Delete temporary uploaded audio files.
    """

    for path in paths:
        try:
            Path(path).unlink(
                missing_ok=True
            )
        except OSError:
            pass


@router.get("/speakers")
def speakers():
    """
    List all enrolled speakers.
    """

    return {
        "speakers": list_speakers(),
    }


@router.post("/enroll")
def enroll(
    name: str = Form(...),
    files: list[UploadFile] = File(...),
):
    """
    Enroll a speaker using one or more
    voice samples.
    """

    if len(files) > MAX_FILES:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Maximum {MAX_FILES} "
                "samples per enrollment."
            ),
        )

    paths: list[str] = []

    try:
        paths = [
            _save_upload(file)
            for file in files
        ]

        result = enroll_speaker(
            name,
            paths,
        )

        return {
            "ok": True,
            **result,
            "privacy_note": (
                "Raw uploads were temporary. "
                "Only the derived speaker "
                "profile is retained."
            ),
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    finally:
        _cleanup(paths)


@router.post("/identify")
def identify(
    file: UploadFile = File(...),
    threshold: float = Form(0.65),
):
    """
    Identify a speaker from a new audio sample.
    """

    paths: list[str] = []

    try:
        path = _save_upload(file)
        paths.append(path)

        result = identify_speaker(
            path,
            threshold=threshold,
        )

        speaker = result["speaker"]

        return {
            "ok": True,
            "identification": result,
            "context": get_context(
                speaker
            ),
            "memory": read_memory(
                speaker
            ),
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    finally:
        _cleanup(paths)


@router.delete("/speakers/{name}")
def remove_speaker(name: str):
    """
    Delete a speaker profile and its memory.
    """

    deleted = delete_speaker(name)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Speaker not found.",
        )

    clear_memory(name)

    return {
        "ok": True,
        "speaker": name,
        "deleted": True,
    }


@router.get("/memory/{speaker}")
def get_memory(speaker: str):
    """
    Read memory for one speaker.
    """

    return read_memory(
        speaker
    )


@router.post("/memory/{speaker}")
def remember(
    speaker: str,
    note: str = Form(...),
):
    """
    Add one memory note for a speaker.
    """

    try:
        return {
            "ok": True,
            "memory": add_memory(
                speaker,
                note,
            ),
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc


@router.delete("/memory/{speaker}")
def forget(speaker: str):
    """
    Delete all memory for a speaker.
    """

    return {
        "ok": True,
        "speaker": speaker,
        "deleted": clear_memory(
            speaker
        ),
    }