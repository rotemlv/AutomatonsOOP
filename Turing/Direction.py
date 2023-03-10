from enum import Enum


class Direction(Enum):
    STAY = 0
    LEFT = -1
    RIGHT = 1

    def __str__(self):
        return self.name
