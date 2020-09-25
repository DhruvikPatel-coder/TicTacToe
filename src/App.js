import React, { useState, useEffect } from 'react';
import './App.css';
import Board from './Board'
import axios from 'axios';

function App() {
  let [state, setState] = useState({
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
          console.log(data);
          setState(data);
        });
    }
  }, [state]);

  function handleClick(i) {
    const squares = state.current;
    if (state.status === 'Game tied!!') {
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
      </div>
    </div>
  );
}

export default App;
