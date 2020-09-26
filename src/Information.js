import React from 'react';
import './status.css';

export default function Information({ status, doReset }) {
    let bots_turn = "";
    let your_turn = "";
    let game_status = "Classic";

    let div_style = {
        "display": "flex",
        "justify-content": "center",
        "align-items": "center"
    }

    if (status === 'Bots Turn "X"') {
        bots_turn = "infoBox content yellow orangeBorder";
        your_turn = "infoBox content";
    } else if (status === 'Your Turn "O"') {
        your_turn = "infoBox content yellow orangeBorder";
        bots_turn = "infoBox content";
    } else {
        your_turn = "infoBox content";
        bots_turn = "infoBox content";
        game_status = status;
    }

    return (
        <div>
            <div className="text-center">
                <b className="title">Tic - Tac - Toe</b>
            </div>
            <div className="text-center status-div">
                <b className="content">{game_status}</b>
            </div>
            <div className="intro-div">
                <b className="content">You are player "O" and player "X" is a bot, enjoy playing.</b>
            </div>
            <section id="gameInfo" className="infoContainer">
                <div id="yourTurn" style={div_style}
                    className={your_turn}>
                    Your turn</div>
                <button id="resetButton" className="infoBox content" onClick={doReset}>
                    Reset Game</button>
                <div id="compTurn"
                    className={bots_turn}>
                    Computer's turn</div>
            </section>
        </div>
    );
}