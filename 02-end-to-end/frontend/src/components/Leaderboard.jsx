import React, { useEffect, useState } from 'react';
import { mockApi } from '../api/mockApi';

export default function Leaderboard() {
  const [scores, setScores] = useState([]);
  useEffect(() => {
    mockApi.getLeaderboard().then(setScores);
  }, []);
  return (
    <div>
      <h2>Leaderboard</h2>
      <ol>
        {scores.map((s, i) => (
          <li key={i}>{s.username}: {s.score}</li>
        ))}
      </ol>
    </div>
  );
}
