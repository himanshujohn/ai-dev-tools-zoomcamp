import React from 'react';

export default function GameMenu({ onSelectMode }) {
  return (
    <div className="menu-container">
      <h2 className="menu-title">Choose Game Mode</h2>
      <div className="menu-btns">
        <button className="menu-btn" onClick={() => onSelectMode('walls')}>Play (Walls)</button>
        <button className="menu-btn" onClick={() => onSelectMode('pass-through')}>Play (Pass-Through)</button>
      </div>
    </div>
  );
}
