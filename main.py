from typing import Optional, Iterable

# Colour pseudo-type that could be useful later
Colour = Optional[tuple[int, int, int]]


# a tetris board!
class Board:
    def __init__(self, rows: int, columns: int):
        self.spaces = [[None] * columns] * rows

    def __repr__(self):
        out = '|' + '--' * len(self.spaces[0]) + '|\n'
        for row in self.spaces:
            out += '|'
            for pixel in row:
                if pixel is None:
                    out += '  '
                else:
                    out += '[]'
            out += '|\n'
        out += '|' + '--' * len(self.spaces[0]) + '|'
        return out

    def row_fall(self) -> None:
        # clear empty rows
        for i, row in enumerate(self.spaces):
            # check row for fullness
            for j, pixel in enumerate(row):  # enumerate over pixels in row
                # break if any pixel has empty spaces
                if pixel is None:
                    break
            else:  # if there are no empty pixels, clear the row
                self.spaces.pop(i)

        for i, row in enumerate(self.spaces):
            # check row for fullness
            for j, pixel in enumerate(row):  # enumerate over pixels in row
                # break if any pixel has empty spaces
                if pixel is not None:
                    break
            else:  # if there are no empty pixels, clear the row
                self.spaces.pop(i)

        # add enough rows to top
        self.spaces = [[None] * len(self.spaces[0])] * (len(self.spaces[0]) - len(self.spaces)) + self.spaces

    def blit(self, other):
        return [[k or l for k, l in zip(i, j)] for i, j in zip(self.spaces, other.spaces)]

    def offset(self, north, south, east, west):
        spaces = [[None] * len(self.spaces[0])] * north + self.spaces
        spaces += [[None] * len(self.spaces[0])] * south
        for i in range(len(spaces)):
            spaces[i] = spaces[i] + [None] * west
        for i in range(len(spaces)):
            spaces[i] += [None] * east

    def rotate_clockwise_and_check(self, other):
        rotated = Board(0, 0)
        rotated.spaces = rotate_matrix_clockwise(self.spaces)
        if Board.colliding(rotated, other):
            return False
        else:
            self.spaces = rotated.spaces
            return True

    def rotate_counterclockwise_and_check(self, other):
        rotated = Board(0, 0)
        rotated.spaces = rotate_matrix_counterclockwise(self.spaces)
        if Board.colliding(rotated, other):
            return False
        else:
            self.spaces = rotated.spaces
            return True

    def fall_and_check(self, other):
        rotated = Board(0, 0)
        rotated.spaces = Board.down_shifted(self)
        if Board.colliding(rotated, other):
            return False
        else:
            self.spaces = rotated.spaces
            return True

    @staticmethod
    def up_shifted(board):
        return rotate(board.spaces, -1)

    @staticmethod
    def down_shifted(board):
        return rotate(board.spaces, 1)

    @staticmethod
    def colliding(board1, board2):
        for i, j in zip(board1.spaces, board2.spaces):
            for k, l in zip(i, j):
                if k and l:
                    return True
        return False


def rotate(data: list, n: int):
    return data[-n:] + data[:-n]


def rotate_matrix_counterclockwise(lst: Iterable[Iterable[any]]):
    return list(zip(*lst))[::-1]


def rotate_matrix_clockwise(lst: Iterable[Iterable[any]]):  # yes, this is stupid. no, i do not care
    return rotate_matrix_counterclockwise(rotate_matrix_counterclockwise(rotate_matrix_counterclockwise(lst)))


def display(boards: Iterable[Board]):
    out = boards[0]
    for i in boards:
        out.spaces = out.blit(i)
    print(repr(out))

b = None
w = 255, 255, 255

board1 = Board(4, 4)

board1.spaces = [
    [w, w, w, w],
    [b, b, b, b],
    [b, b, b, b],
    [b, b, b, b]
]

board2 = Board(4, 4)

board2.spaces = [
    [b, b, b, b],
    [b, w, w, b],
    [b, w, w, b],
    [b, b, b, b],
]

if board1.rotate_clockwise_and_check(board2):
    board1.spaces = board1.blit(board2)


display([board1, board2])