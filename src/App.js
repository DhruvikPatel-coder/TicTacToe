import React, { useState, useEffect } from 'react';
import './App.css';
import Board from './Board'
import axios from 'axios';

function App() {
  let [state, setState] = useState({
    history: [{
      squares: Array(9).fill(null),
    }],
    stepNumber: 0,
    current: Array(9).fill(null),
    status: 'Your turn "O"',
    lastHighlight: '',
    sendRequest: false,
    moves: []
  });

  // Similar to componentDidUpdate
  useEffect(() => {
    if (state.sendRequest) {
      axios.post(`http://127.0.0.1:5000/getnextmove`, { state })
        .then(res => {
          let data = res.data;
          setState(data);
        });
    }
  }, [state]);

  function handleClick(i) {
    const squares = state.current;
    if (state.status === 'Game tied!!' || state.status === 'O Won!!' || state.status === 'X Won!!') {
      return
    }
    squares[i] = 'O';
    const history = state.history
    setState({
      history: history.concat([{
        squares: squares
      }]),
      stepNumber: history.length,
      current: squares,
      status: 'Bots Turn "X"',
      lastHighlight: i,
      sendRequest: true,
      moves: []
    });
  }

  let moves = state.history.map((step, move) => {
    const desc = move ?
      'Go to move #' + move :
      'Go to game start';
    return (
      <li key={Math.random()} style={{ margin: "5px" }}>
        <button className="btn btn-outline-dark btn-sm" onClick={() => jumpTo(move, state.history)}>{desc}</button>
      </li>
    );
  });

  function jumpTo(step, history) {
    let temp = {};
    Object.assign(temp, state, { stepNumber: step, history: history.slice(0, step + 1) });
    setState(temp);
  }

  return (
    <div className="game">
      <div className="col-lg-2">
        <Board squares={state.current}
          onClick={(i) => handleClick(i)} lastHighlight={state.lastHighlight}
          winnerHighlight={state.moves} />
      </div>
      <div className="col-lg-10">
        <div><b>You are player "X" and player "O" is a bot, enjoy playing.
        Click the button below in order to retive the game back to specific move!!</b></div>
        <div style={{ marginBottom: "10px" }}>{state.status}</div>
        <ol>{moves}</ol>
      </div>
    </div>
  );
}

export default App;
