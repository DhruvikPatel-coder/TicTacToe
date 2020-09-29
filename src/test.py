import numpy as np


def evaluate(grid_2d, grid):
    size = len(grid_2d)
    row_result = True
    column_result = True
    diagonal_result = True
    reverse_diagonal_result = True

    who = ""
    # Check for rows
    for row in range(size):
        for column in range(len(grid_2d[row])):
            if grid_2d[row][column] is not None:
                if grid_2d[row][0] != grid_2d[row][column]:
                    row_result = False
                    who = ""
        who = grid_2d[row][0]

    # Check for columns
    for row in range(size):
        index_1d = 0
        while index_1d in range(len(grid)):
            if grid[row] is not None:
                who = grid[row]
                if grid(row) != grid[index_1d]:
                    column_result = False
                    who = ""
                index_1d += size
            else:
                break

    # Check for diagonals
    for row in range(size):
        for column in range(len(grid_2d[row])):
            if grid_2d[0][0] is not None:
                who = grid_2d[0][0]
                if row == column and grid_2d[0][0] != grid_2d[row][column]:
                    diagonal_result = False
                    who = ""

    # check for reverse diagonals
    i = size - 1
    while i >= 0:
        j = size - 1
        while j >= 0:
            if grid_2d[size-1][size-1] is not None:
                who = grid_2d[size-1][size-1]
                if i == j and grid_2d[size-1][size-1] != grid_2d[i][j]:
                    reverse_diagonal_result = False
                    who = ""

    return (row_result or column_result or diagonal_result or reverse_diagonal_result), who


if __name__ == '__main__':
    array = ["O", "X", "0", "O", "X", "", "0", "", "X"]
    array_2d = np.reshape(array, (3, 3))
    result, who = evaluate(array_2d, array)
    print("Coming here")
    print(result)
    print(who)
