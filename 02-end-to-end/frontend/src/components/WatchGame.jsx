import React, { useEffect, useState } from 'react';
import { mockApi } from '../api/mockApi';

export default function WatchGame({ gameId }) {
  const [game, setGame] = useState(null);
  useEffect(() => {
    let running = true;
    const fetchState = async () => {
      if (!running) return;
      const state = await mockApi.getGameState(gameId);
      setGame(state);
      setTimeout(fetchState, 400);
    };
    fetchState();
    return () => { running = false; };
  }, [gameId]);
  if (!game) return <div>Loading...</div>;
  return (
    <div>
      <div>Watching: {game.username} ({game.mode})</div>
      <div>Score: {game.score}</div>
      <div style={{
        display: 'grid',
        gridTemplateRows: `repeat(15, 20px)`,
        gridTemplateColumns: `repeat(15, 20px)`
      }}>
        {[...Array(15 * 15)].map((_, i) => {
          const x = i % 15, y = Math.floor(i / 15);
          const isSnake = game.snake.some(seg => seg.x === x && seg.y === y);
          const isFood = game.food.x === x && game.food.y === y;
          return <div key={i} style={{ width: 20, height: 20, background: isSnake ? '#2d6' : isFood ? '#e33' : '#fff', border: '1px solid #ccc' }} />;
        })}
      </div>
    </div>
  );
}
