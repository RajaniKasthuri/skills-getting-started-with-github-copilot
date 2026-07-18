from uuid import uuid4

from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_unregister_participant():
    # Arrange
    activity_name = "Chess Club"
    email = f"{uuid4()}@mergington.edu"

    # Act
    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    unregister_response = client.delete(f"/activities/{activity_name}/signup?email={email}")
    activities_response = client.get("/activities")

    # Assert
    assert signup_response.status_code == 200
    assert unregister_response.status_code == 200
    assert unregister_response.json()["message"] == f"Removed {email} from {activity_name}"

    activities = activities_response.json()
    assert email not in activities[activity_name]["participants"]


def test_duplicate_signup_is_rejected():
    # Arrange
    activity_name = "Chess Club"
    email = f"{uuid4()}@mergington.edu"

    # Act
    first_signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    second_signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert first_signup_response.status_code == 200
    assert second_signup_response.status_code == 400
    assert second_signup_response.json()["detail"] == "Student is already signed up for this activity"
