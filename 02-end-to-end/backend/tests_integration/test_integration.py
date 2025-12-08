import pytest
from httpx import AsyncClient
from main import app
from db import engine, Base
import asyncio
import os
import sqlalchemy

import sys
sys.path.append("..")

@pytest.fixture(scope="session", autouse=True)
def setup_db():
    # Use a test SQLite DB
    os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///./test_integration.db"
    # Create tables
    async def init():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
    asyncio.run(init())
    yield
    # Teardown
    async def drop():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
    asyncio.run(drop())

@pytest.mark.asyncio
async def test_signup_and_login():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Signup
        r = await ac.post("/signup", json={"username": "integration", "password": "testpass"})
        assert r.status_code == 200
        assert r.json()["success"]
        # Login
        r = await ac.post("/login", json={"username": "integration", "password": "testpass"})
        assert r.status_code == 200
        data = r.json()
        assert data["success"]
        assert "token" in data
        token = data["token"]
        # Get user
        r = await ac.get("/user", headers={"Authorization": token})
        assert r.status_code == 200
        assert r.json()["username"] == "integration"
        # Logout
        r = await ac.post("/logout", headers={"Authorization": token})
        assert r.status_code == 200
        assert r.json()["success"]

@pytest.mark.asyncio
async def test_leaderboard():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Submit score
        r = await ac.post("/leaderboard", json={"username": "integration", "score": 123})
        assert r.status_code == 200
        assert r.json()["success"]
        # Get leaderboard
        r = await ac.get("/leaderboard")
        assert r.status_code == 200
        assert any(entry["username"] == "integration" for entry in r.json())

@pytest.mark.asyncio
async def test_games():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Add a game (simulate DB insert if needed)
        # Get active games
        r = await ac.get("/games")
        assert r.status_code == 200
        games = r.json()
        if games:
            game_id = games[0]["id"]
            # Get game state
            r = await ac.get(f"/games/{game_id}")
            assert r.status_code == 200
            state = r.json()
            assert state["id"] == game_id
            assert "snake" in state
            assert "food" in state
