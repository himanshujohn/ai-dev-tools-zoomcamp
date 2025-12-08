import React, { useEffect, useRef, useState } from 'react';

const GRID_SIZE = 15;
const INIT_SNAKE = [
  { x: 7, y: 7 },
];
const INIT_FOOD = { x: 3, y: 3 };
const DIRS = {
  ArrowUp: { x: 0, y: -1 },
  ArrowDown: { x: 0, y: 1 },
  ArrowLeft: { x: -1, y: 0 },
  ArrowRight: { x: 1, y: 0 },
};

export default function SnakeGame({ mode = 'walls', onGameOver, onScore }) {
  const [snake, setSnake] = useState(INIT_SNAKE);
  const [food, setFood] = useState(INIT_FOOD);
  const [dir, setDir] = useState(DIRS.ArrowRight);
  const [score, setScore] = useState(0);
  const [gameOver, setGameOver] = useState(false);
  const moveRef = useRef(dir);

  useEffect(() => { moveRef.current = dir; }, [dir]);

  useEffect(() => {
    if (gameOver) return;
    const handleKey = e => {
      if (DIRS[e.key]) setDir(DIRS[e.key]);
    };
    window.addEventListener('keydown', handleKey);
    return () => window.removeEventListener('keydown', handleKey);
  }, [gameOver]);

  useEffect(() => {
    if (gameOver) return;
    const interval = setInterval(() => {
      setSnake(prev => {
        const head = { ...prev[0] };
        head.x += moveRef.current.x;
        head.y += moveRef.current.y;
        if (mode === 'walls') {
          if (head.x < 0 || head.x >= GRID_SIZE || head.y < 0 || head.y >= GRID_SIZE) {
            setGameOver(true); onGameOver && onGameOver(score); return prev;
          }
        } else {
          head.x = (head.x + GRID_SIZE) % GRID_SIZE;
          head.y = (head.y + GRID_SIZE) % GRID_SIZE;
        }
        if (prev.some(seg => seg.x === head.x && seg.y === head.y)) {
          setGameOver(true); onGameOver && onGameOver(score); return prev;
        }
        let newSnake = [head, ...prev];
        if (head.x === food.x && head.y === food.y) {
          setScore(s => s + 1); onScore && onScore(score + 1);
          setFood({ x: Math.floor(Math.random() * GRID_SIZE), y: Math.floor(Math.random() * GRID_SIZE) });
        } else {
          newSnake.pop();
        }
        return newSnake;
      });
    }, 120);
    return () => clearInterval(interval);
  }, [food, mode, gameOver, score, onGameOver, onScore]);

  return (
    <div className="snake-game-board">
      <div className="score">Score: {score}</div>
      <div className="snake-grid">
        {[...Array(GRID_SIZE * GRID_SIZE)].map((_, i) => {
          const x = i % GRID_SIZE, y = Math.floor(i / GRID_SIZE);
          const isSnake = snake.some(seg => seg.x === x && seg.y === y);
          const isFood = food.x === x && food.y === y;
          return <div key={i} className={`snake-cell${isSnake ? ' snake' : ''}${isFood ? ' food' : ''}`} />;
        })}
      </div>
      {gameOver && <div className="game-over">Game Over</div>}
    </div>
  );
}
