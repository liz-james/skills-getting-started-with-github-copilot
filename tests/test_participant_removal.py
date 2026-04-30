from urllib.parse import quote


def test_remove_existing_participant_success(client):
    # Arrange
    activity_name = "Art Club"
    email = "remove.success@example.edu"
    signup_path = f"/activities/{quote(activity_name)}/signup"
    remove_path = f"/activities/{quote(activity_name)}/participants"

    signup_response = client.post(signup_path, params={"email": email})
    assert signup_response.status_code == 200

    # Act
    removal_response = client.delete(remove_path, params={"email": email})

    # Assert
    assert removal_response.status_code == 200
    assert "Removed" in removal_response.json()["message"]

    activities = client.get("/activities").json()
    assert email not in activities[activity_name]["participants"]


def test_remove_non_member_returns_404(client):
    # Arrange
    activity_name = "Drama Club"
    email = "nonmember.remove@example.edu"
    remove_path = f"/activities/{quote(activity_name)}/participants"

    # Act
    response = client.delete(remove_path, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_remove_from_unknown_activity_returns_404(client):
    # Arrange
    remove_path = "/activities/Unknown%20Club/participants"

    # Act
    response = client.delete(remove_path, params={"email": "test.unknown@example.edu"})

    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]
