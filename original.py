# Not very well documented, because there is a better documented, explained and implemented version in bitboard.py

def print_board(board):
    for row in board:
        print(" ".join(str(cell) for cell in row))
    print("\n")


def get_neighbours(board, i, j):
    neighbours = []
    for x in range(i - 1, i + 2):
        for y in range(j - 1, j + 2):
            if (
                x >= 0
                and x < len(board)
                and y >= 0
                and y < len(board[i])
                and (x != i or y != j)
            ):
                neighbours.append(board[x][y])
    return neighbours


def get_live_indices(board):
    indices = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 1:
                indices.append((i, j))
    return indices


def get_dead_indices(board):
    indices = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                indices.append((i, j))
    return indices


def rule_one(board):
    live_indices = get_live_indices(board)
    dead_indices = []

    for i, j in live_indices:
        if get_neighbours(board, i, j).count(1) < 2:
            dead_indices.append((i, j))

    return dead_indices


def rule_two(board):
    live_indices = get_live_indices(board)
    dead_indices = []

    for i, j in live_indices:
        if get_neighbours(board, i, j).count(1) > 3:
            dead_indices.append((i, j))

    return dead_indices


def rule_three(board):
    dead_indices = get_dead_indices(board)
    live_indices = []

    for i, j in dead_indices:
        if get_neighbours(board, i, j).count(1) == 3:
            live_indices.append((i, j))

    return live_indices


def apply_rules(board):
    counter = 0
    while counter < 10:
        dead_indices = rule_one(board)
        dead_indices.extend(rule_two(board))
        live_indices = rule_three(board)
        for i, j in dead_indices:
            board[i][j] = 0
        for i, j in live_indices:
            board[i][j] = 1
        counter += 1


if __name__ == "__main__":
    board = [[0] * 10 for _ in range(10)]

    board[0][1] = 1
    board[1][2] = 1
    board[2][0] = 1
    board[2][1] = 1
    board[2][2] = 1
