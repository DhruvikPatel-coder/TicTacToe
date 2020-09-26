import * as React from "react";
import './style.css';

export default function Square(props) {
    let my_style = {
        backgroundColor: props.color,
        "fontFamily": 'TicTacToe',
        "fontWeight": "bold",
        "fontSize": "50px"
    }
    return (
        <button
            className="square"
            onClick={props.onClick}
            style={my_style}
        > {props.value}
        </button>
    );
}
