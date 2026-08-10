DEFAULT_CONTEXTS = {
    "Unknown": {
        "greeting": "Hello. I don't recognize this speaker yet.",
        "role": "guest",
    }
}


def get_context(speaker: str) -> dict:
    """
    Return a simple context object for the detected speaker.

    This is intentionally simple for the educational MVP.
    Later this can be connected to:
    - a database
    - user preferences
    - LLM system prompts
    - personal memory
    """

    if speaker == "Unknown":
        return DEFAULT_CONTEXTS["Unknown"]

    return {
        "greeting": f"Hello {speaker}.",
        "role": "enrolled_speaker",
    }