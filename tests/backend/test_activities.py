"""Tests for retrieving extracurricular activities."""


def test_get_activities_returns_expected_structure(client):
    # Arrange
    expected_activity_names = {"Chess Club", "Programming Class", "Gym Class"}
    expected_fields = {
        "description",
        "schedule",
        "max_participants",
        "participants",
    }

    # Act
    response = client.get("/activities")
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert expected_activity_names <= data.keys()

    for details in data.values():
        assert set(details) == expected_fields
        assert isinstance(details["description"], str)
        assert isinstance(details["schedule"], str)
        assert isinstance(details["max_participants"], int)
        assert isinstance(details["participants"], list)