from urllib.parse import quote


def test_signup_for_activity_success(client):
    # Arrange
    activity_name = "Basketball Team"
    email = "john.signup@example.edu"
    path = f"/activities/{quote(activity_name)}/signup"

    # Act
    response = client.post(path, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert email in response.json()["message"]

    activities = client.get("/activities").json()
    assert email in activities[activity_name]["participants"]


def test_signup_duplicate_participant_returns_400(client):
    # Arrange
    activity_name = "Soccer Club"
    email = "duplicate.signup@example.edu"
    path = f"/activities/{quote(activity_name)}/signup"

    # Act
    first_response = client.post(path, params={"email": email})
    second_response = client.post(path, params={"email": email})

    # Assert
    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert "already signed up" in second_response.json()["detail"]


def test_signup_for_unknown_activity_returns_404(client):
    # Arrange
    path = "/activities/Unknown%20Club/signup"

    # Act
    response = client.post(path, params={"email": "test.unknown@example.edu"})

    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]
