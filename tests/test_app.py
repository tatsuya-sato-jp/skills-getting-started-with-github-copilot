"""Tests for the activities API used by the website."""

from fastapi.testclient import TestClient

from src.app import activities, app

client = TestClient(app)


def test_get_activities_includes_participants():
    """Each activity exposes the participants used to render the list."""
    response = client.get("/activities")
    assert response.status_code == 200

    data = response.json()
    assert data
    for details in data.values():
        assert isinstance(details["participants"], list)


def test_signup_adds_participant_to_activity():
    """Signing up adds the email so it shows up under the activity."""
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    original = list(activities[activity_name]["participants"])

    try:
        response = client.post(
            f"/activities/{activity_name}/signup", params={"email": email}
        )
        assert response.status_code == 200

        participants = client.get("/activities").json()[activity_name]["participants"]
        assert email in participants
    finally:
        activities[activity_name]["participants"] = original


def test_signup_unknown_activity_returns_404():
    response = client.post(
        "/activities/Unknown Activity/signup",
        params={"email": "student@mergington.edu"},
    )
    assert response.status_code == 404
