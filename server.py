import json
import numpy as np
import copy

from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)  # initialize flask
# Set the environment to development in order to enable hot reload
Flask.env = 'development'
CORS(app, resources={r"/getnextmove": {"origins": "*"}})


@app.route('/getnextmove', methods=['POST'])
def getnextmove():
    data = bytes(request.data).decode('UTF_8')
    data_json = json.loads(data)
    grid = data_json['state']['current']
    grid_copy = copy.deepcopy(grid)
    gird_2d = np.reshape(grid_copy, (3, 3))
    status, moves = evaluate(grid)

    if (isBoardFull(grid_copy)):
        response_value = {
            "current": grid,
            "status": "Game tied!!",
            "lastHighlight": data_json['state']['lastHighlight'],
            "sendRequest": False,
            "moves": []
        }
    elif status:
        response_value = {
            "current": grid,
            "status": status + " Won!!",
            "lastHighlight": data_json['state']['lastHighlight'],
            "sendRequest": False,
            "moves": moves
        }
    else:
        updated_move = getBestMove(grid_copy, gird_2d)
        grid[updated_move] = 'X'
        response_value = {
            "current": grid,
            "status": 'Your Turn "O"',
            "lastHighlight": updated_move,
            "sendRequest": False,
            "moves": []
        }

    status, moves = evaluate(grid)
    if status:
        response_value = {
            "current": grid,
            "status": status + " Won!!",
            "lastHighlight": data_json['state']['lastHighlight'],
            "sendRequest": False,
            "moves": moves
        }

    return response_value


def getBestMove(grid, grid_2d):
    best_value = -500
    final_index = -1
    for i in range(len(grid_2d)):
        for j in range(len(grid_2d[i])):
            if grid_2d[i][j] is None:
                grid_2d[i][j] = 'X'
                index = ((i)*3) + j
                grid[index] = 'X'
                # Compute evaluation function for this
                move_value = miniMax(grid, grid_2d, False)
                # reset to original value
                grid_2d[i][j] = None
                grid[index] = None

                if move_value > best_value:
                    final_index = index
                    best_value = move_value

    return final_index


def miniMax(grid, grid_2d, isMaximizingPlayer):
    score, moves = evaluate(grid)

    if score == "O":
        return -10
    if score == "X":
        return 10
    if isBoardFull(grid):
        return 0

    if isMaximizingPlayer is True:
        best = -1000
        for row in range(len(grid_2d)):
            for column in range(len(grid_2d[row])):
                if grid_2d[row][column] is None:
                    grid_2d[row][column] = 'X'
                    index = ((row)*3) + column
                    grid[index] = 'X'
                    best = max(best, miniMax(
                        grid, grid_2d, not isMaximizingPlayer))
                    grid_2d[row][column] = None
                    grid[index] = None
        return best
    else:
        best = 1000
        for row in range(len(grid_2d)):
            for column in range(len(grid_2d[row])):
                if grid_2d[row][column] is None:
                    grid_2d[row][column] = 'O'
                    index = ((row)*3) + column
                    grid[index] = 'O'
                    best = min(best, miniMax(
                        grid, grid_2d, not isMaximizingPlayer))
                    grid_2d[row][column] = None
                    grid[index] = None
        return best


def evaluate(grid):
    lines = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6],
    ]
    for row in lines:
        [a, b, c] = row
        if (grid[a] and grid[a] == grid[b] and grid[b] == grid[c]):
            return grid[a], [a, b, c]
    return "", []


def isBoardFull(grid):
    for cell in grid:
        if cell is None:
            return False
    return True


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
