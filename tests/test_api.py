from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root():
    """
    Root endpoint should return
    basic project information.
    """

    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["project"] == "WhoIsSpeaking AI"
    assert data["version"] == "0.1.0"
    assert data["type"] == "Educational / Learning Project"
    assert data["docs"] == "/docs"


def test_health():
    """
    Health endpoint should confirm
    that the API is running.
    """

    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"
    assert data["service"] == "WhoIsSpeaking AI"


def test_speakers_endpoint():
    """
    Speaker list endpoint should return
    a speakers array.
    """

    response = client.get("/api/speakers")

    assert response.status_code == 200

    data = response.json()

    assert "speakers" in data
    assert isinstance(
        data["speakers"],
        list,
    )


def test_unknown_memory():
    """
    A speaker without stored memory
    should receive an empty notes list.
    """

    response = client.get(
        "/api/memory/TestSpeaker"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["speaker"] == "TestSpeaker"
    assert data["notes"] == []


def test_add_and_delete_memory():
    """
    Memory can be added and deleted
    through the API.
    """

    speaker = "GitHubActionTestSpeaker"

    response = client.post(
        f"/api/memory/{speaker}",
        data={
            "note": "WhoIsSpeaking AI test memory"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["ok"] is True

    assert (
        "WhoIsSpeaking AI test memory"
        in data["memory"]["notes"]
    )

    response = client.delete(
        f"/api/memory/{speaker}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["ok"] is True