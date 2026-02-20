"""CLI entry point for the ``pad`` application.

This file provides a small, extendable Click-based scaffold with example
commands and a `stats` command that uses `numpy` when available.
"""
from __future__ import annotations
import datetime

import click

from pad.solve import (
    generate_solutions,
    get_solutions,
    get_first_solution
)

from pad.piece import(
    PIECES,
    Piece
)


@click.group()
@click.version_option(prog_name="pad")
def main() -> None:
    pass


@main.command()
@click.argument('piece', type=str)
def piece(piece) -> None:
    """Generate all solutions"""
    click.echo(Piece.display(PIECES[piece]))


@main.command()
@click.argument('filename', type=click.Path(dir_okay=False))
@click.option("--processes", default=20, type=click.IntRange(min=1, max=128))
def generate(filename, processes) -> None:
    """Generate all solutions"""
    start = datetime.datetime.now()
    with open(filename, "w") as f:
        count = generate_solutions(f, processes)
    end = datetime.datetime.now()
    click.echo(f"Done. {count} solutions in {end - start} seconds.")


@main.command()
@click.argument("month", nargs=1)
@click.argument("day", nargs=1)
def solve(month: str, day: str) -> None:
    """Find a single solution for given day"""
    if len(day) == 1:
        day = "0" + day
    click.echo(f"Found a solution for {day} {month}")
    click.echo(f"{get_first_solution(month, day)}")

@main.command()
@click.argument("month", nargs=1)
@click.argument("day", nargs=1)
def solutions(month: str, day: str) -> None:
    """Generate all solutions for given day"""
    if len(day) == 1:
        day = "0" + day
    solutions = get_solutions(month, day)
    click.echo(f"{len(solutions)} solutions found for {day} {month}")
    for sol in solutions:
        click.echo(sol)

if __name__ == "__main__":
    main()
