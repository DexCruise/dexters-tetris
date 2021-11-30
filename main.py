from typing import Optional

Colour = Optional[tuple[int, int, int]]

black = 1, 1, 1


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

        # add enough rows to top
        self.spaces = [[None] * self.columns] * (self.columns - len(self.spaces)) + self.spaces

    def blit(self, other):
        return [[k if l is None else l for k, l in zip(i, j)] for i, j in zip(self.spaces, other.spaces)]


b = None
w = 1, 1, 1

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
