import React from 'react';
import './App.css';
import Square from "./Square";

export default function Board(props) {
    function renderSquare(i) {
        let color = "";
        if (props.lastHighlight === i) {
            color = "#6600EE";
        }
        if (props.winnerHighlight.includes(i)) {
            color = "#77EE00";
        }
        return (
            <Square
                key={i}
                value={props.squares[i]}
                onClick={() => props.onClick(i)}
                color={color}
            />
        );
    }

    function board() {
        let table = []
        for (let i = 0; i < 9; i += 3) {
            let rows = []
            for (let j = i; j < i + 3; j++) {
                rows.push(renderSquare(j))
            }
            table.push(<div className="board-row" key={i + 10}>{rows}</div>)
        }
        return table
    }

    return (
        <div>
            {board()}
        </div>
    );

};
