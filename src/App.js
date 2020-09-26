import React, { useState, useEffect } from 'react';
import './App.css';
import Board from './Board'
import axios from 'axios';

export default function App() {
  let [state, setState] = useState({
    current: Array(9).fill(null),
    status: 'Your turn "O"',
    lastHighlight: '',
    sendRequest: false,
    moves: []
  });

  let [stateHistory, setHistory] = useState({
    history: [{
      squares: Array(9).fill(null),
    }],
    stepNumber: 0,
  })

  // Similar to componentDidUpdate
  useEffect(() => {
    if (state.sendRequest) {
      // https://my-third-app-dot-my-project-9894-281203.nn.r.appspot.com/getnextmove
      axios.post(`http://127.0.0.1:5000/getnextmove`, { state })
        .then(res => {
          let data = res.data;
          setState(data);
        });
    }
  }, [state]);

  // // Similar to componentDidUpdate
  useEffect(() => {
    let step = stateHistory.stepNumber;
    let updated_move = stateHistory.history[step].squares;
    let temp = {};
    Object.assign(temp, state, { current: updated_move });
    setState(temp);
  }, [stateHistory]);

  function handleClick(i) {
    const squares = state.current;
    if (state.status === 'Game tied!!' ||
      state.status === 'O Won!!' ||
      state.status === 'X Won!!') {
      return
    }
    if (squares[i] !== null) {
      return
    }
    if (setState.status === 'Bots Turn "X"') {
      return
    }

    squares[i] = 'O';
    const history = stateHistory.history
    setState({
      current: squares,
      status: 'Bots Turn "X"',
      lastHighlight: i,
      sendRequest: true,
      moves: []
    });

    setHistory({
      history: history.concat([{
        squares: squares
      }]),
      stepNumber: history.length,
    })
  }

  let moves = stateHistory.history.map((step, move) => {
    const desc = move ?
      'Go to move #' + move :
      'Go to game start';
    return (
      <li key={Math.random()} style={{ margin: "5px" }}>
        <button
          className="btn btn-outline-dark btn-sm"
          onClick={() => jumpTo(move, stateHistory.history)}
        >{desc}</button>
      </li>
    );
  });

  function jumpTo(step, my_history) {
    setHistory({
      history: my_history.slice(0, step + 1),
      stepNumber: step
    });
    let temp = {};
    Object.assign(temp, state, { lastHighlight: "", moves: [] });
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
