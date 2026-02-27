from urllib.parse import quote


def test_get_activities(client):
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_success_and_duplicate(client):
    name = "Chess Club"
    email = "teststudent@mergington.edu"

    # sign up succeeds
    resp = client.post(f"/activities/{quote(name)}/signup", params={"email": email})
    assert resp.status_code == 200
    assert email in client.get("/activities").json()[name]["participants"]

    # duplicate signup returns 400
    resp2 = client.post(f"/activities/{quote(name)}/signup", params={"email": email})
    assert resp2.status_code == 400


def test_signup_missing_activity(client):
    resp = client.post(f"/activities/{quote('Nonexistent Club')}/signup", params={"email": "a@b.com"})
    assert resp.status_code == 404


def test_unregister_success_and_missing(client):
    name = "Programming Class"
    participants = client.get("/activities").json()[name]["participants"]
    assert participants
    email = participants[0]

    # unregister succeeds
    resp = client.post(f"/activities/{quote(name)}/unregister", params={"email": email})
    assert resp.status_code == 200
    assert email not in client.get("/activities").json()[name]["participants"]

    # unregistering a non-registered email returns 404
    resp2 = client.post(f"/activities/{quote(name)}/unregister", params={"email": "noone@x.com"})
    assert resp2.status_code == 404


def test_unregister_missing_activity(client):
    resp = client.post(f"/activities/{quote('No Club')}/unregister", params={"email": "a@b.com"})
    assert resp.status_code == 404
