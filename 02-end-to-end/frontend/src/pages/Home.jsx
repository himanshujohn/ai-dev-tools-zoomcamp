import React, { useState } from 'react';

import AuthForm from '../components/AuthForm';
import GameMenu from '../components/GameMenu';
import SnakeGame from '../components/SnakeGame';
import Leaderboard from '../components/Leaderboard';
import WatchGame from '../components/WatchGame';
import { mockApi } from '../api/mockApi';

function TopRibbon({ onShowLeaderboard, onLogout }) {
  return (
    <div className="top-ribbon">
      <div className="ribbon-center"></div>
      <div className="ribbon-right">
        <button className="ribbon-btn" onClick={onShowLeaderboard}>Leaderboard</button>
        <button className="ribbon-btn logout" onClick={onLogout}>Logout</button>
      </div>
    </div>
  );
}

export default function Home() {
  const [token, setToken] = useState(null);
  const [username, setUsername] = useState(null);
  const [view, setView] = useState('menu');
  const [mode, setMode] = useState('walls');
  const [watchId, setWatchId] = useState(null);
  const [activeGames, setActiveGames] = useState([]);
  const [authMode, setAuthMode] = useState('login');

  const handleAuth = (token, username) => {
    setToken(token);
    setUsername(username);
    setView('menu');
  };
  const handleLogout = async () => {
    if (token) await mockApi.logout(token);
    setToken(null); setUsername(null); setView('menu');
  };
  const handleGameOver = async score => {
    if (username) await mockApi.submitScore(username, score);
    setView('menu');
  };
  const handleWatch = async () => {
    const games = await mockApi.getActiveGames();
    setActiveGames(games);
    setView('watch-list');
  };

  if (!token && view !== 'signup')
    return (
      <div className="center-viewport">
        <div>
          <AuthForm onAuth={handleAuth} mode="login" />
          <div style={{textAlign:'center', marginTop: 16}}>
            <button className="auth-btn" onClick={()=>setView('signup')}>Sign Up</button>
          </div>
        </div>
      </div>
    );
  if (!token && view === 'signup')
    return (
      <div className="center-viewport">
        <div>
          <AuthForm onAuth={handleAuth} mode="signup" />
          <div style={{textAlign:'center', marginTop: 16}}>
            <button className="auth-btn" onClick={()=>setView('menu')}>Back to Login</button>
          </div>
          <div style={{textAlign:'center', marginTop: 10}}>Welcome! You can now log in.</div>
        </div>
      </div>
    );

  // After login, always show ribbon
  if (view === 'menu')
    return (
      <>
        <TopRibbon onShowLeaderboard={()=>setView('leaderboard')} onLogout={handleLogout} />
        <div className="below-ribbon">
          <div className="welcome-player">{username && <>Welcome, <b>{username}</b></>}</div>
          <div className="center-viewport"><div className="menu-center"><GameMenu onSelectMode={m => { setMode(m); setView('game'); }} /></div></div>
        </div>
      </>
    );
  if (view === 'game')
    return (
      <>
        <TopRibbon onShowLeaderboard={()=>setView('leaderboard')} onLogout={handleLogout} />
        <div className="below-ribbon">
          <div className="welcome-player">{username && <>Welcome, <b>{username}</b></>}</div>
          <div className="center-viewport"><div className="game-center"><SnakeGame mode={mode} onGameOver={handleGameOver} onScore={()=>{}} /></div></div>
        </div>
      </>
    );
  if (view === 'leaderboard')
    return (
      <>
        <TopRibbon onShowLeaderboard={()=>setView('leaderboard')} onLogout={handleLogout} />
        <div className="below-ribbon">
          <div className="welcome-player">{username && <>Welcome, <b>{username}</b></>}</div>
          <div className="center-viewport">
            <div style={{marginBottom: 16}}><button className="auth-btn" onClick={()=>setView('menu')}>Back to Menu</button></div>
            <Leaderboard />
          </div>
        </div>
      </>
    );
  if (view === 'watch-list')
    return (
      <>
        <TopRibbon onShowLeaderboard={()=>setView('leaderboard')} onLogout={handleLogout} />
        <div className="below-ribbon">
          <div className="welcome-player">{username && <>Welcome, <b>{username}</b></>}</div>
          <div className="center-viewport"><h2>Active Games</h2><ul>{activeGames.map(g => <li key={g.id}><button className="auth-btn" onClick={()=>{setWatchId(g.id);setView('watch')}}>Watch {g.username} ({g.mode})</button></li>)}</ul><button className="auth-btn" onClick={()=>setView('menu')}>Back to Menu</button></div>
        </div>
      </>
    );
  if (view === 'watch')
    return (
      <>
        <TopRibbon onShowLeaderboard={()=>setView('leaderboard')} onLogout={handleLogout} />
        <div className="below-ribbon">
          <div className="welcome-player">{username && <>Welcome, <b>{username}</b></>}</div>
          <div className="center-viewport"><WatchGame gameId={watchId} /><div style={{marginTop: 16}}><button className="auth-btn" onClick={()=>setView('watch-list')}>Back to Games</button></div></div>
        </div>
      </>
    );
  return null;
}
