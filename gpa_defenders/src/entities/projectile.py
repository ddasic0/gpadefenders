
import math
import pygame


class Projectile:
    def __init__(self, x: float, y: float, target, damage: float, speed: float, color: tuple[int, int, int]):
        self.x = float(x)
        self.y = float(y)
        self.target = target
        self.damage = float(damage)
        self.speed = float(speed)
        self.color = color
        self.radius = 4
        self.alive = True

    def update(self, dt: float) -> None:
        if not self.alive:
            return
        if not self.target.alive:
            self.alive = False
            return

        dx = self.target.x - self.x
        dy = self.target.y - self.y
        dist = math.hypot(dx, dy)
        if dist <= self.radius + self.target.radius:
            self.target.take_damage(self.damage)
            self.alive = False
            return

        step = self.speed * dt
        if step >= dist:
            self.target.take_damage(self.damage)
            self.alive = False
            return

        self.x += (dx / dist) * step
        self.y += (dy / dist) * step

    def draw(self, screen: pygame.Surface) -> None:
        if self.alive:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
