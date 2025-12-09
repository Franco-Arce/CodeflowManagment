from app.auth import get_password_hash
from app.models import User

def test_login(client, session):
    # Create user
    user = User(username="testuser", password_hash=get_password_hash("testpass"))
    session.add(user)
    session.commit()

    # Test success
    response = client.post("/token", data={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    assert "access_token" in response.json()

    # Test fail
    response = client.post("/token", data={"username": "testuser", "password": "wrongpass"})
    assert response.status_code == 401

def test_read_users_me(client, session):
    user = User(username="testuser", password_hash=get_password_hash("testpass"))
    session.add(user)
    session.commit()

    token = client.post("/token", data={"username": "testuser", "password": "testpass"}).json()["access_token"]
    
    response = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
