import numpy as np
import copy


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
    grid = ['X', None, None, None, 'O', None, 'O', None, None]
    gird_2d = np.reshape(grid, (3, 3))
    move = getBestMove(grid, gird_2d)
    print("The most optimal move is " + str(move))
