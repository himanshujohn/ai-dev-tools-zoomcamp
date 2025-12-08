import requests

BASE_URL = "http://localhost:8000"

def check_signup_and_login():
    s = requests.Session()
    # Signup
    r = s.post(f"{BASE_URL}/signup", json={"username": "verifyuser", "password": "verifypass"})
    assert r.status_code == 200
    # Login
    r = s.post(f"{BASE_URL}/login", json={"username": "verifyuser", "password": "verifypass"})
    assert r.status_code == 200
    data = r.json()
    assert data["success"]
    token = data["token"]
    # Get user
    r = s.get(f"{BASE_URL}/user", headers={"Authorization": token})
    assert r.status_code == 200
    # Logout
    r = s.post(f"{BASE_URL}/logout", headers={"Authorization": token})
    assert r.status_code == 200

def check_leaderboard():
    s = requests.Session()
    # Submit score
    r = s.post(f"{BASE_URL}/leaderboard", json={"username": "verifyuser", "score": 99})
    assert r.status_code == 200
    # Get leaderboard
    r = s.get(f"{BASE_URL}/leaderboard")
    assert r.status_code == 200
    assert any(entry["username"] == "verifyuser" for entry in r.json())

def check_games():
    s = requests.Session()
    r = s.get(f"{BASE_URL}/games")
    assert r.status_code == 200
    games = r.json()
    if games:
        game_id = games[0]["id"]
        r = s.get(f"{BASE_URL}/games/{game_id}")
        assert r.status_code == 200
        state = r.json()
        assert state["id"] == game_id
        assert "snake" in state
        assert "food" in state

def main():
    print("Verifying /signup, /login, /user, /logout ...")
    check_signup_and_login()
    print("Verifying /leaderboard ...")
    check_leaderboard()
    print("Verifying /games and /games/{gameId} ...")
    check_games()
    print("All API endpoints verified successfully!")

if __name__ == "__main__":
    main()
