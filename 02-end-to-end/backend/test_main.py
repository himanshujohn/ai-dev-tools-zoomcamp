import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_signup_and_login():
    # Signup
    r = client.post("/signup", json={"username": "testuser", "password": "testpass"})
    assert r.status_code == 200
    assert r.json()["success"]
    # Login
    r = client.post("/login", json={"username": "testuser", "password": "testpass"})
    assert r.status_code == 200
    data = r.json()
    assert data["success"]
    assert "token" in data
    token = data["token"]
    # Get user
    r = client.get("/user", headers={"Authorization": token})
    assert r.status_code == 200
    assert r.json()["username"] == "testuser"
    # Logout
    r = client.post("/logout", headers={"Authorization": token})
    assert r.status_code == 200
    assert r.json()["success"]

def test_leaderboard():
    # Submit score
    r = client.post("/leaderboard", json={"username": "demo", "score": 42})
    assert r.status_code == 200
    assert r.json()["success"]
    # Get leaderboard
    r = client.get("/leaderboard")
    assert r.status_code == 200
    assert any(entry["score"] == 42 for entry in r.json())

def test_games():
    # Get active games
    r = client.get("/games")
    assert r.status_code == 200
    games = r.json()
    assert isinstance(games, list)
    if games:
        game_id = games[0]["id"]
        # Get game state
        r = client.get(f"/games/{game_id}")
        assert r.status_code == 200
        state = r.json()
        assert state["id"] == game_id
        assert "snake" in state
        assert "food" in state
