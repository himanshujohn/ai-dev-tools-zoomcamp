

from fastapi import FastAPI, HTTPException, Header, Path, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
import random
import string
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from db import SessionLocal
from models import User, LeaderboardEntry, Game
import uuid

app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session tokens (for demo; use DB/Redis for prod)
sessions = {}

def generate_token():
    return str(uuid.uuid4())

async def get_db():
    async with SessionLocal() as session:
        yield session


@app.get("/")
async def homepage():
    return {"message": "Welcome to the Snake Game API"}


@app.post("/login")
async def login(data: dict, db: AsyncSession = Depends(get_db)):
    username = data.get("username")
    password = data.get("password")
    result = await db.execute(select(User).where(User.username == username, User.password == password))
    user = result.scalar_one_or_none()
    if user:
        token = generate_token()
        sessions[token] = user.id
        return {"success": True, "token": token, "username": user.username}
    return {"success": False, "error": "Invalid credentials"}


@app.post("/signup")
async def signup(data: dict, db: AsyncSession = Depends(get_db)):
    username = data.get("username")
    password = data.get("password")
    user = User(username=username, password=password)
    db.add(user)
    try:
        await db.commit()
        return {"success": True}
    except IntegrityError:
        await db.rollback()
        return {"success": False, "error": "User exists"}


@app.get("/user")
async def get_user(Authorization: Optional[str] = Header(None), db: AsyncSession = Depends(get_db)):
    token = Authorization
    user_id = sessions.get(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user:
        return {"username": user.username}
    raise HTTPException(status_code=401, detail="Invalid token")


@app.post("/logout")
async def logout(Authorization: Optional[str] = Header(None)):
    token = Authorization
    if token in sessions:
        del sessions[token]
    return {"success": True}


@app.get("/leaderboard")
async def get_leaderboard(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(LeaderboardEntry).order_by(LeaderboardEntry.score.desc()).limit(10))
    entries = result.scalars().all()
    return [{"username": e.username, "score": e.score} for e in entries]


@app.post("/leaderboard")
async def submit_score(data: dict, db: AsyncSession = Depends(get_db)):
    username = data.get("username")
    score = data.get("score")
    entry = LeaderboardEntry(username=username, score=score)
    db.add(entry)
    await db.commit()
    return {"success": True}


@app.get("/games")
async def get_active_games(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Game))
    games = result.scalars().all()
    return [
        {"id": g.id, "username": g.username, "mode": g.mode, "state": g.state}
        for g in games
    ]


@app.get("/games/{gameId}")
async def get_game_state(gameId: int = Path(...), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Game).where(Game.id == gameId))
    game = result.scalar_one_or_none()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return {
        "id": game.id,
        "username": game.username,
        "mode": game.mode,
        "snake": [
            {"x": random.randint(0, 9), "y": random.randint(0, 9)},
            {"x": random.randint(0, 9), "y": random.randint(0, 9)},
        ],
        "food": {"x": random.randint(0, 9), "y": random.randint(0, 9)},
        "score": random.randint(0, 20),
    }
