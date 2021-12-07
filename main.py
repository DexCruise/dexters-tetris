from typing import Optional, Iterable
from pieces import pieces

# pseudo-types that could be useful later
from vector2 import vector2

Colour = Optional[tuple[int, int, int]]
GameBoard = list[list[Colour]]


def represent_board(board: GameBoard):
    out = '|' + '--' * len(board) + '|\n'
    for row in board:
        out += '|'
        for pixel in row:
            if pixel is None:
                out += '  '
            else:
                out += '[]'
        out += '|\n'
    out += '|' + '--' * len(board[0]) + '|'
    return out


def make_board(rows: int, columns: int) -> GameBoard:
    return [[None] * rows] * columns


def row_fallen(board: GameBoard) -> GameBoard:
    # clear empty rows
    for i, row in enumerate(board):
        # check row for fullness
        for j, pixel in enumerate(row):  # enumerate over pixels in row
            # break if any pixel has empty spaces
            if pixel is None:
                break
        else:  # if there are no empty pixels, clear the row
            board.pop(i)

    for i, row in enumerate(board):
        # check row for fullness
        for j, pixel in enumerate(row):  # enumerate over pixels in row
            # break if any pixel has empty spaces
            if pixel is not None:
                break
        else:  # if there are no empty pixels, clear the row
            board.pop(i)

    # add enough rows to top
    board = [[None] * len(board[0])] * (len(board[0]) - len(board)) + board
    return board


def blit(base, onto):
    return [[k or l for k, l in zip(i, j)] for i, j in zip(base, onto)]


def offset(board: GameBoard, north: int, south: int, east: int, west: int):
    spaces = [[None] * len(board[0])] * north + board
    spaces += [[None] * len(board[0])] * south
    for i in range(len(spaces)):
        spaces[i] = spaces[i] + [None] * west
    for i in range(len(spaces)):
        spaces[i] += [None] * east


def rotate_clockwise_and_check(board: GameBoard, other: GameBoard) -> bool:
    rotated = rotate_matrix_clockwise(board)
    if colliding(rotated, other):
        return False
    else:
        return True


def rotate_counterclockwise_and_check(board: GameBoard, other: GameBoard) -> bool:
    rotated = rotate_matrix_counterclockwise(board)
    if colliding(rotated, other):
        return False
    else:
        return True


def falling_possible(faller, onto):
    rotated = down_shifted(faller)
    if colliding(rotated, onto):
        return False
    else:
        return True


def up_shifted(board):
    return rotate(board, -1)


def down_shifted(board):
    return rotate(board, 1)


def colliding(board1, board2):
    for i, j in zip(board1, board2):
        for k, l in zip(i, j):
            if k and l:
                return True
    return False


def rotate(data: list, n: int):
    return data[-n:] + data[:-n]


def rotate_matrix_counterclockwise(lst: Iterable[Iterable[any]]):
    return list(zip(*lst))[::-1]  # stolen from SO


def rotate_matrix_clockwise(lst: Iterable[Iterable[any]]):  # yes, this is stupid. no, i do not care
    return rotate_matrix_counterclockwise(
        rotate_matrix_counterclockwise(
            rotate_matrix_counterclockwise(lst)))


def display(boards: list[GameBoard]):
    out = boards[0]
    for i in boards:
        out = blit(out, i)
    return out


class GameState:
    def __init__(self, board: GameBoard, piece: GameBoard):
        self.board = board
        self.piece = piece

        self.piece_coords = vector2(0, 0)

    touching_ground: bool = False

    def tick(self):
        touching_ground = falling_possible(self.piece, self.board)
        if not touching_ground:
            self.piece_coords.y += 1


def new_game():
    board = make_board(10, 20)
    piece = pieces.T

    game = GameState(board, piece)

    for i in range(10):
        print(represent_board(display([game.board, game.piece])))
        game.tick()


new_game()
