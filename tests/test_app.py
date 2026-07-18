from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_unregister_participant():
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    signup_response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    assert signup_response.status_code == 200

    unregister_response = client.delete(
        f"/activities/{activity_name}/signup?email={email}"
    )
    assert unregister_response.status_code == 200
    assert unregister_response.json()["message"] == f"Removed {email} from {activity_name}"

    activities = client.get("/activities").json()
    assert email not in activities[activity_name]["participants"]
