from app.auth import get_password_hash
from app.models import User, Incident, IncidentStatus

def get_auth_token(client, session):
    user = User(username="testuser", password_hash=get_password_hash("testpass"))
    session.add(user)
    session.commit()
    return client.post("/token", data={"username": "testuser", "password": "testpass"}).json()["access_token"]

def test_create_incident(client, session):
    token = get_auth_token(client, session)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.post("/incidents/", json={"title": "Test Incident", "description": "Something broke", "severity": "high"}, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Incident"
    assert data["status"] == "open"

def test_list_incidents(client, session):
    token = get_auth_token(client, session)
    headers = {"Authorization": f"Bearer {token}"}
    
    client.post("/incidents/", json={"title": "Incident 1", "description": "Desc 1"}, headers=headers)
    client.post("/incidents/", json={"title": "Incident 2", "description": "Desc 2"}, headers=headers)
    
    response = client.get("/incidents/", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_resolve_incident(client, session):
    token = get_auth_token(client, session)
    headers = {"Authorization": f"Bearer {token}"}
    
    incident = client.post("/incidents/", json={"title": "To Resolve", "description": "Fix me"}, headers=headers).json()
    incident_id = incident["id"]
    
    response = client.put(f"/incidents/{incident_id}", json={"status": "resolved"}, headers=headers)
    assert response.status_code == 200
    assert response.json()["status"] == "resolved"
