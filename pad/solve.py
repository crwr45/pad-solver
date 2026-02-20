import multiprocessing
from typing import IO, List

from pad.board import (
    Board,
    Move
)
from pad.piece import (
    Piece,
    PIECES,
)


MONTHS = {
    'jan': 31,
    'feb': 29,
    'mar': 31,
    'apr': 30,
    'may': 31,
    'jun': 30,
    'jul': 31,
    'aug': 31,
    'sep': 30,
    'oct': 31,
    'nov': 30,
    'dec': 31,
}

PIECE_POOL = list(PIECES.keys())

def solve(moves, board: Board, piece_pool: List[Piece]):
    """ Recursively generate solutions"""
    if board.is_complete():
        yield moves
        return
    if not piece_pool:
        yield None
        return
    for i, p in enumerate(piece_pool):
        piece = PIECES[p]
        for po in piece.orientations():
            move = board.place_piece(po)
            if move is not None:
                for sol in solve(moves[:] + [move],
                                 move.board_after,
                                 piece_pool[:i] + piece_pool[i+1:]):
                    if sol:
                        yield sol

def notate_solution(solution: List[Move]):
    sol = [f"{move}" for move in solution]
    return ",".join(sol)

def generate_solutions(outfile: IO, processes: int=20):
    count = 0
    children = {}
    with multiprocessing.Pool(processes=20) as pool:
        for month, days in MONTHS.items():
            for d in range(days):
                day = str(d+1)
                if len(day) == 1:
                    day = "0" + day
                children[f"{day}{month}"] = pool.apply_async(get_solutions, (month, day))
        for d, c in children.items():
            sols = c.get(timeout=300)
            count += len(sols)
            for s in sols:
                outfile.write(s + "\n")
    return count

def get_first_solution(month, day):
    b = Board()
    b.set_target_date(month, day)
    for sol in solve([], b, PIECE_POOL):
        return notate_solution(sol)

def get_solutions(month, day):
    b = Board()
    b.set_target_date(month, day)
    solutions = list(solve([], b, PIECE_POOL))
    return [f"{day}{month},{notate_solution(sol)}" for sol in solutions]


if __name__ == "__main__":
    import time
    start = time.time()
    get_solutions("jan", "01")
    print(time.time() - start)
