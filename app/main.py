from fastapi import FastAPI

from app.api.routes import router


app = FastAPI(
    title="WhoIsSpeaking AI",
    description=(
        "An educational open-source API for learning "
        "speaker recognition, voice embeddings, "
        "and identity-aware AI."
    ),
    version="0.1.0",
)


# Main API routes
app.include_router(
    router,
    prefix="/api",
    tags=["WhoIsSpeaking AI"],
)


@app.get("/")
def root():
    """
    Basic project information.
    """

    return {
        "project": "WhoIsSpeaking AI",
        "version": "0.1.0",
        "type": "Educational / Learning Project",
        "message": "Learn how AI recognizes who is speaking.",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    """
    Simple health check.
    """

    return {
        "status": "ok",
        "service": "WhoIsSpeaking AI",
    }