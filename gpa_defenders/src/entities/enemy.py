
import math
import pygame
from src.entities.entity import Entity
from src.settings import ENEMY_TYPES, RED, GREEN


class Enemy(Entity):
    def __init__(self, enemy_type: str, waypoints: list[tuple[int, int]]):
        x, y = waypoints[0]
        super().__init__(x, y)
        cfg = ENEMY_TYPES[enemy_type]
        self.enemy_type = enemy_type
        self.name = cfg["name"]
        self.max_hp = float(cfg["hp"])
        self.hp = float(cfg["hp"])
        self.speed = float(cfg["speed"])
        self.gpa_damage = float(cfg["gpa_damage"])
        self.rewards = dict(cfg["rewards"])
        self.color = cfg["color"]
        self.radius = 12
        self.waypoints = list(waypoints)
        self.waypoint_index = 0
        self.reached_end = False

    def take_damage(self, damage: float) -> None:
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            self.alive = False

    def update(self, dt: float) -> None:
        if not self.alive or self.reached_end:
            return

        remaining = self.speed * dt
        while remaining > 0 and self.waypoint_index < len(self.waypoints):
            tx, ty = self.waypoints[self.waypoint_index]
            dx = tx - self.x
            dy = ty - self.y
            dist = math.hypot(dx, dy)
            if dist == 0:
                self.waypoint_index += 1
                continue

            step = min(remaining, dist)
            self.x += (dx / dist) * step
            self.y += (dy / dist) * step
            remaining -= step
            if step == dist:
                self.waypoint_index += 1

        if self.waypoint_index >= len(self.waypoints):
            self.reached_end = True

    def draw(self, screen: pygame.Surface) -> None:
        if not self.alive:
            return
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        bar_w = 26
        hp_ratio = self.hp / self.max_hp if self.max_hp else 0
        pygame.draw.rect(screen, RED, (int(self.x) - bar_w // 2, int(self.y) - 18, bar_w, 4))
        pygame.draw.rect(screen, GREEN, (int(self.x) - bar_w // 2, int(self.y) - 18, int(bar_w * hp_ratio), 4))


class Quiz(Enemy):
    def __init__(self, waypoints: list[tuple[int, int]]):
        super().__init__("quiz", waypoints)
