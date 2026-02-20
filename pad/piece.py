from typing import Generator

import numpy as np
from numpy.typing import NDArray

from pad.position import Position

class PieceRotation:
    """
    A Transformation of a piece, that can be added to a board.
    """
    def __init__(self, piece, array: NDArray, rotations: int, flipped=False):
        self._name = piece.name
        self._piece = piece
        self._array = array
        self._rotations = rotations
        self._flipped = flipped
        self._height = self._array.shape[0]
        self._width = self._array.shape[1]
        # How far left to shift the piece to ensure it covers the target square
        self.offset = 0
        while self._array[0,0 + self.offset] == 0:
            self.offset += 1

    def __repr__(self):
        name = self._name
        name += str(self._rotations)
        if self._flipped:
            name += 'f'
        return name

    def place(self, pos: Position) -> NDArray:
        """
        Generate and return an empty board matrix with this piece covering {pos}
        If this piece does not cover its own (0,0) then
        it will be shifted left until it does, to ensure the taget is covered.
        If the piece hangs off the board it is considered an invalid move.
        """
        board_mask = np.zeros((9, 9), dtype=np.int8)
        board_mask[pos.y : pos.y + self._height,
                   pos.x - self.offset : pos.x + self._width - self.offset] = self._array
        return board_mask


class Piece:
    """
    Static piece.
    """
    def __init__(self, name: str, rotations: int, can_flip: bool, array: NDArray):
        self.name = name
        self._rotations = rotations
        self._can_flip = can_flip
        self._array = array

    def __repr__(self):
        return self.name

    def orientations(self) -> Generator[PieceRotation, None, None]:
        for i in range(self._rotations):
            yield self.orientation(i, False)
        if self._can_flip:
            for i in range(self._rotations):
                yield self.orientation(i, True)

    def orientation(self, rotations: int, flipped: bool):
        if rotations > self._rotations:
            raise ValueError(f"Too many rotations ({rotations} > {self._rotations}) for piece {self}")

        a = self.flipped() if flipped else self._array.copy()
        a = np.rot90(a, rotations * -1)
        return PieceRotation(self, a, rotations, flipped)

    def flipped(self):
        return np.flip(self._array.copy(), axis=1)

    @staticmethod
    def display(piece):
        res = ""
        for i in piece._array:
            row = ""
            for j in i:
                row += chr(9608)*2 if j else "  "
            res += row + "\n"
        return res


PIECE_O = Piece("O",
                2,
                False,
                np.array([[1, 1],
                          [1, 1],
                          [1, 1]])
                )

PIECE_C = Piece("C",
                4,
                False,
                np.array([[1, 1],
                          [1, 0],
                          [1, 1]])
                )

PIECE_P = Piece("P",
                4,
                True,
                np.array([[1, 1],
                          [1, 1],
                          [1, 0]])
                )

PIECE_X = Piece("X", # No resemblance to a letter.
                4,
                True,
                np.array([[0, 1],
                          [1, 1],
                          [1, 0],
                          [1, 0]])
                )

PIECE_T = Piece("T",
                4,
                True,
                np.array([[1, 1, 1, 1],
                          [0, 1, 0, 0]])
                )

PIECE_J = Piece("J",
                4,
                True,
                np.array([[0, 1],
                          [0, 1],
                          [0, 1],
                          [1, 1]])
                )

PIECE_Z = Piece("Z",
                2,
                True,
                np.array([[1, 1, 0],
                          [0, 1, 0],
                          [0, 1, 1]])
                )

PIECE_L = Piece("L",
                4,
                False,
                np.array([[1, 0, 0],
                          [1, 0, 0],
                          [1, 1, 1]])
                )

PIECES = {
    "O": PIECE_O,
    "C": PIECE_C,
    "P": PIECE_P,
    "X": PIECE_X,
    "T": PIECE_T,
    "J": PIECE_J,
    "Z": PIECE_Z,
    "L": PIECE_L,
}
