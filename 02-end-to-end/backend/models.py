from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

class LeaderboardEntry(Base):
    __tablename__ = 'leaderboard'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    score = Column(Integer, nullable=False)

class Game(Base):
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    mode = Column(String, nullable=False)
    state = Column(String, nullable=False)
