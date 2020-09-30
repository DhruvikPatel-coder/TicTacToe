import React, { useState, useEffect } from 'react';
import './App.css';
import Board from './Board'
import axios from 'axios';
import Information from './Information'

export default function App() {
  let [state, setState] = useState({
    current: Array(9).fill(null),
    status: 'Your Turn "O"',
    lastHighlight: '',
    sendRequest: false,
    moves: []
  });

  // Similar to componentDidUpdate
  useEffect(() => {
    if (state.sendRequest) {
      axios.post(`https://my-third-app-dot-my-project-9894-281203.nn.r.appspot.com/getnextmove`, { state })
        .then(res => {
          let data = res.data;
          setState(data);
        });
    }
  }, [state]);

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
    if (state.status === 'Bots Turn "X"') {
      return
    }

    squares[i] = 'O';
    setState({
      current: squares,
      status: 'Bots Turn "X"',
      lastHighlight: i,
      sendRequest: true,
      moves: []
    });
  }

  function resetGame() {
    setState({
      current: Array(9).fill(null),
      status: 'Your Turn "O"',
      lastHighlight: '',
      sendRequest: false,
      moves: []
    });
  }

  return (
    <div className="container-fluid">
      <div className="row game">
        <Information status={state.status} doReset={() => resetGame()} />
      </div>
      <div className="row game">
        <Board squares={state.current}
          onClick={(i) => handleClick(i)} lastHighlight={state.lastHighlight}
          winnerHighlight={state.moves} />
      </div>
    </div>
  );
}
