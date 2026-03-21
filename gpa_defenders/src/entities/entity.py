
import pygame
from abc import ABC, abstractmethod


class Entity(ABC):

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.alive = True

    @property
    def position(self) -> tuple[float, float]:
        return (self.x, self.y)

    @abstractmethod
    def update(self, dt: float) -> None:
        pass

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        pass

    def distance_to(self, other: "Entity") -> float:
        dx = self.x - other.x
        dy = self.y - other.y
        return (dx * dx + dy * dy) ** 0.5
