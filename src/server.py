import json
import numpy as np
import copy

from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)  # initialize flask
# Set the environment to development in order to enable hot reload
Flask.env = 'development'
CORS(app)


@app.route('/getnextmove', methods=['POST'])
def getnextmove():
    data = bytes(request.data).decode('UTF_8')
    data_json = json.loads(data)
    grid = data_json['state']['current']
    grid_copy = copy.deepcopy(grid)
    gird_2d = np.reshape(grid_copy, (3, 3))

    updated_move = getBestMove(grid_copy, gird_2d)
    grid[updated_move] = 'X'
    response_value = {
        "current": grid,
        "status": 'Your Turn "O"',
        "lastHighlight": updated_move,
        "sendRequest": False,
        "moves": {}
    }
    return response_value


def getBestMove(grid, grid_2d):
    best_value = -1000
    row = -1
    col = -1
    for i in range(len(grid_2d)):
        for j in range(len(grid_2d[i])):
            if grid_2d[i][j] is None:
                grid_2d[i][j] = 'X'
                grid[i + j] = 'X'
                # Compute evaluation function for this
                move_value = miniMax(grid, grid_2d, True)
                # reset to original value
                grid_2d[i][j] = None
                grid[i + j] = None

                if move_value > best_value:
                    row = i
                    col = j
                    best_value = move_value

    return row + col


def miniMax(grid, grid_2d, isMaximizingPlayer):
    score = evaluate(grid)

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
                    grid[row + column] = 'X'
                    best = max(best, miniMax(
                        grid, grid_2d, not isMaximizingPlayer))
                    grid_2d[row][column] = None
                    grid[row + column] = None
        return best
    else:
        best = 1000
        for row in range(len(grid_2d)):
            for column in range(len(grid_2d[row])):
                if grid_2d[row][column] is None:
                    grid_2d[row][column] = 'O'
                    grid[row + column] = 'O'
                    best = min(best, miniMax(
                        grid, grid_2d, not isMaximizingPlayer))
                    grid_2d[row][column] = None
                    grid[row + column] = None
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
            return grid[a]
    return ""


def isBoardFull(grid):
    for cell in grid:
        if cell is None:
            return False
    return True


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
