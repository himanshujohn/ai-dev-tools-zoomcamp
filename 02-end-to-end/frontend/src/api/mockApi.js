// Centralized API for all backend calls (real backend)
// AGENTS.md: keep API logic isolated, easy to swap for mocks/tests

const BASE_URL = '/api';

export const mockApi = {
  login: async (username, password) => {
    const res = await fetch(`${BASE_URL}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    });
    return await res.json();
  },
  signup: async (username, password) => {
    const res = await fetch(`${BASE_URL}/signup`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    });
    return await res.json();
  },
  getUser: async (token) => {
    const res = await fetch(`${BASE_URL}/user`, {
      headers: { 'Authorization': token },
    });
    if (res.status === 200) return await res.json();
    return null;
  },
  logout: async (token) => {
    const res = await fetch(`${BASE_URL}/logout`, {
      method: 'POST',
      headers: { 'Authorization': token },
    });
    return await res.json();
  },
  getLeaderboard: async () => {
    const res = await fetch(`${BASE_URL}/leaderboard`);
    return await res.json();
  },
  submitScore: async (username, score) => {
    const res = await fetch(`${BASE_URL}/leaderboard`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, score }),
    });
    return await res.json();
  },
  getActiveGames: async () => {
    const res = await fetch(`${BASE_URL}/games`);
    return await res.json();
  },
  getGameState: async (gameId) => {
    const res = await fetch(`${BASE_URL}/games/${gameId}`);
    return await res.json();
  },
};