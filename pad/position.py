from dataclasses import dataclass


@dataclass
class Position:
    y: int
    x: int

    def __repr__(self):
        return f"{self.x}{self.y}"
