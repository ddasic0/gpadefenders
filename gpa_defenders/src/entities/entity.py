
import math


class Entity:
    def __init__(self, x: float, y: float):
        self.x = float(x)
        self.y = float(y)
        self.alive = True

    def distance_to(self, other: "Entity") -> float:
        return math.dist((self.x, self.y), (other.x, other.y))
