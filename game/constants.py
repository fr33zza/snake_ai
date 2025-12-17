from enum import Enum
from collections import namedtuple

Point = namedtuple("Point", "x y")

class Direction(Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3