from dataclasses import dataclass
from typing import Any
import numpy as np
from numpy.typing import NDArray
from collections import deque

from pad.piece import PieceRotation
from pad.position import Position

NAMES = np.array([[1, 1, 1, 1, 1, 1, 1, 1, 1],
                  [1, "jan", "feb", "mar", "apr", "may", "jun", 1, 1],
                  [1, "jul", "aug", "sep", "oct", "nov", "dec", 1, 1],
                  [1, "01", "02", "03", "04", "05", "06", "07", 1],
                  [1, "08", "09", "10", "11", "12", "13", "14", 1],
                  [1, "15", "16", "17", "18", "19", "20", "21", 1],
                  [1, "22", "23", "24", "25", "26", "27", "28", 1],
                  [1, "29", "30", "31", 1, 1, 1, 1, 1],
                  [1, 1, 1, 1, 1, 1, 1, 1, 1]])

EMPTY = np.array([[1, 1, 1, 1, 1, 1, 1, 1, 1],
                  [1, 0, 0, 0, 0, 0, 0, 1, 1],
                  [1, 0, 0, 0, 0, 0, 0, 1, 1],
                  [1, 0, 0, 0, 0, 0, 0, 0, 1],
                  [1, 0, 0, 0, 0, 0, 0, 0, 1],
                  [1, 0, 0, 0, 0, 0, 0, 0, 1],
                  [1, 0, 0, 0, 0, 0, 0, 0, 1],
                  [1, 0, 0, 0, 1, 1, 1, 1, 1],
                  [1, 1, 1, 1, 1, 1, 1, 1, 1]], dtype=np.int8)



@dataclass
class Move:
    board_after: Any
    piece: PieceRotation
    position: Position

    def notate(self):
        return f"{str(self.position)}{str(self.piece)}"

    def __repr__(self):
        return self.notate()


class Board:
    def __init__(self, state=None):
        self.state = EMPTY.copy() if state is None else state

    def __repr__(self):
        return "Board: " + str(np.count_nonzero(self.state))

    def set_target_date(self, month: str, day: str):
        month = month.lower()
        day = day.lower()
        self.target = [month, day]
        self.state[np.where(NAMES == month)] = 1
        self.state[np.where(NAMES == day)] = 1

    def next_gap(self):
        for y, r in enumerate(self.state):
            for x, v in enumerate(r):
                if v == 0:
                    return Position(y, x)
        raise Exception("complete!")

    def place_piece(self, piece: PieceRotation) -> Move:
        pos = self.next_gap()
        try:
            overlay = piece.place(pos)
            move_result = self.state + overlay
            b = Board(move_result)
            if b.is_valid():
                return Move(b, piece, pos)
        except ValueError as e:
            return

    def is_valid(self) -> bool:
        if np.any(self.state > 1):
            return False
        if self.has_unfillable_hole():
            return False
        return True

    def has_unfillable_hole(self) -> bool:
        """
        Detect if a board is unsolvable.
        A board in unsolvable if it contains an area
        of 1, 2, 3 or 4 `0`s that is completely
        surrounded by `1`s.
        """
        h, w = self.state.shape
        # Track which cells we've already visited while scanning components
        visited = np.zeros(self.state.shape, dtype=bool)

        # Iterate over every cell looking for unvisited zero cells
        for y in range(h):
            for x in range(w):
                # Skip non-zero cells and cells already accounted for
                if self.state[y, x] != 0 or visited[y, x]:
                    continue

                # Found a new zero: measure connected region size
                q = deque()
                q.append((y, x))
                visited[y, x] = True
                size = 0
                while q:
                    cy, cx = q.popleft()
                    size += 1
                    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        ny, nx = cy + dy, cx + dx
                        # Ignore out-of-bounds coordinates and already visited cells
                        if ny < 0 or ny >= h or nx < 0 or nx >= w or visited[ny, nx]:
                            continue
                        # If neighbor is also zero, include it in this component
                        if self.state[ny, nx] == 0:
                            visited[ny, nx] = True
                            q.append((ny, nx))
                if size in (1, 2, 3, 4):
                    return True
        return False

    def is_complete(self) -> bool:
        if np.any(self.state == 0):
            return False
        return True
