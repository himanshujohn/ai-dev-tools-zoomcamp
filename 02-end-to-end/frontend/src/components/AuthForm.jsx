import React, { useState } from 'react';
import { mockApi } from '../api/mockApi';

export default function AuthForm({ onAuth, mode = 'login' }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const handleSubmit = async e => {
    e.preventDefault();
    setError('');
    if (mode === 'login') {
      const res = await mockApi.login(username, password);
      if (res.success) onAuth(res.token, res.username);
      else setError(res.error);
    } else {
      const res = await mockApi.signup(username, password);
      if (res.success) onAuth(null, username);
      else setError(res.error);
    }
  };
  return (
    <div className="auth-container">
      <form className="auth-form" onSubmit={handleSubmit}>
        <h2 className="auth-title">{mode === 'login' ? 'Sign in to your account' : 'Create an account'}</h2>
        <div className="auth-field">
          <label htmlFor="username">Username</label>
          <input id="username" className="auth-input" placeholder="Enter your username" value={username} onChange={e => setUsername(e.target.value)} required autoFocus />
        </div>
        <div className="auth-field">
          <label htmlFor="password">Password</label>
          <input id="password" className="auth-input" type="password" placeholder="Enter your password" value={password} onChange={e => setPassword(e.target.value)} required />
        </div>
        <button className="auth-btn" type="submit">{mode === 'login' ? 'Login' : 'Sign Up'}</button>
        {error && <div className="auth-error">{error}</div>}
      </form>
    </div>
  );
}
