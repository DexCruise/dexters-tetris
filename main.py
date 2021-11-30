from typing import Optional

Colour = Optional[tuple[int, int, int]]
black = 0, 0, 0

class Board:
    def __init__(self, rows: int, columns: int):
        self.rows = rows
        self.columns = columns
        self.spaces = [[None] * self.columns] * self.rows

    def __repr__(self):
        # out = '|' + '--' * self.columns + '|\n'
        # for row in self.board:
        #     out += '|'
        #     for pixel in row:
        #         if pixel is None:
        #             out += '  '
        #         else:
        #             out += '[]'
        #     out += '|\n'
        # out += '|' + '--' * self.columns + '|'
        # return out

        # THESE TWO ARE THE SAME

        return '\n'.join(['--' * self.columns] + ['|' + ''.join(['  ' if pixel is None else '[]' for pixel in row])
                                                  + '|' for row in self.spaces] + ['--' * self.columns])

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
        self.spaces = [[None] * self.columns] * (self.columns - len(self.spaces)) + self.spaces

    def blit(self, other):
        return [[k or l for k, l in zip(i, j)] for i, j in zip(self.spaces, other.spaces)]

    @staticmethod
    def colliding(board1, board2):
        for i, j in zip(board1.spaces, board2.spaces):
            for k, l in zip(i, j):
                if k and l:
                    return True
        return False


b = None
w = 255, 255, 255

board = Board(5, 5)

board.spaces = [
    [w, w, w, w, w],
    [w, w, b, w, w],
    [w, b, b, b, w],
    [w, w, b, w, w],
    [w, w, w, w, w],
]

print(repr(board))

# |----------|
# |[][][][][]|
# |[][]  [][]|
# |[]      []|
# |[][]  [][]|
# |[][][][][]|
# |----------|

board.row_fall()

print(repr(board))

# |----------|
# |          |
# |          |
# |[][]  [][]|
# |[]      []|
# |[][]  [][]|
# |----------|

piece = Board(5, 5)
piece.spaces = [[w, w, b, b, b], [b, b, b, b, b], [b, b, b, b, b], [b, b, b, b, b], [b, b, b, b, b]]

board.spaces = board.blit(piece)

print(repr(board))

board.row_fall()

print(repr(board))