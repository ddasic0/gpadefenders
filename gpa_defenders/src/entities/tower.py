
import pygame
from src.entities.entity import Entity
from src.entities.enemy import Enemy
from src.settings import TOWER_TYPES, BLACK, TILE_SIZE


class Tower(Entity):
    def __init__(self, tower_type: str, grid_x: int, grid_y: int):
        px = grid_x * TILE_SIZE + TILE_SIZE // 2
        py = grid_y * TILE_SIZE + TILE_SIZE // 2
        super().__init__(px, py)
        cfg = TOWER_TYPES[tower_type]
        self.tower_type = tower_type
        self.name = cfg["name"]
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.cost = int(cfg["cost"])
        self.damage = float(cfg["damage"])
        self.range = float(cfg["range"])
        self.fire_rate = float(cfg["fire_rate"])
        self.fire_cooldown = 0.0
        self.projectile_speed = float(cfg["projectile_speed"])
        self.color = cfg["color"]
        self.projectile_color = cfg["projectile_color"]
        self.size = TILE_SIZE // 2 - 6

    def find_target(self, enemies: list[Enemy]) -> Enemy | None:
        closest = None
        closest_dist = float("inf")
        for enemy in enemies:
            if not enemy.alive or enemy.reached_end:
                continue
            dist = self.distance_to(enemy)
            if dist <= self.range and dist < closest_dist:
                closest = enemy
                closest_dist = dist
        return closest

    def update(self, dt: float, enemies: list[Enemy]) -> dict | None:
        self.fire_cooldown -= dt
        target = self.find_target(enemies)
        if target is None or self.fire_cooldown > 0:
            return None
        self.fire_cooldown = 1.0 / self.fire_rate
        return {
            "x": self.x,
            "y": self.y,
            "target": target,
            "damage": self.damage,
            "speed": self.projectile_speed,
            "color": self.projectile_color,
        }

    def draw(self, screen: pygame.Surface) -> None:
        rect = pygame.Rect(int(self.x) - self.size, int(self.y) - self.size, self.size * 2, self.size * 2)
        pygame.draw.rect(screen, self.color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)


def create_tower(tower_type: str, grid_x: int, grid_y: int) -> Tower:
    if tower_type not in TOWER_TYPES:
        raise ValueError(f"Unknown tower type: {tower_type}")
    return Tower(tower_type, grid_x, grid_y)
