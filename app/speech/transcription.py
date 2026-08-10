def transcribe_audio(audio_path: str) -> dict:
    """
    Educational placeholder for Speech-to-Text.

    Speaker recognition and speech transcription
    are two different tasks.

    This base MVP keeps transcription optional
    so the project can run without a paid API.

    Later this function can be replaced with:
    - Whisper
    - faster-whisper
    - SpeechBrain ASR
    - another speech-to-text engine
    """

    return {
        "enabled": False,
        "text": None,
        "audio_path": audio_path,
        "message": (
            "Speech-to-text is not enabled "
            "in the base educational MVP."
        ),
    }