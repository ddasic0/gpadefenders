
from src.entities.projectile import Projectile
from src.entities.tower import create_tower
from src.settings import STARTING_GPA, STARTING_ENERGY, FAILING_GPA, TOWER_TYPES, WAVE_CLEAR_ENERGY


class GameManager:
    def __init__(self):
        self.gpa = STARTING_GPA
        self.energy = STARTING_ENERGY
        self.game_over = False
        self.towers = []
        self.enemies = []
        self.projectiles = []

    def can_afford_tower(self, tower_type: str) -> bool:
        return self.energy >= int(TOWER_TYPES[tower_type]["cost"])

    def place_tower(self, tower_type: str, grid_x: int, grid_y: int) -> bool:
        if not self.can_afford_tower(tower_type):
            return False
        tower = create_tower(tower_type, grid_x, grid_y)
        self.energy -= tower.cost
        self.towers.append(tower)
        return True

    def add_enemies(self, enemies: list) -> None:
        self.enemies.extend(enemies)

    def get_tower_at(self, grid_x: int, grid_y: int):
        for tower in self.towers:
            if tower.grid_x == grid_x and tower.grid_y == grid_y:
                return tower
        return None

    def update(self, dt: float, wave_manager) -> None:
        if self.game_over:
            return

        for enemy in self.enemies:
            enemy.update(dt)
            if enemy.reached_end and enemy.alive:
                self.gpa -= enemy.gpa_damage
                enemy.alive = False

        for tower in self.towers:
            shot = tower.update(dt, self.enemies)
            if shot:
                self.projectiles.append(Projectile(**shot))

        for projectile in self.projectiles:
            projectile.update(dt)

        for enemy in self.enemies:
            if not enemy.alive and not enemy.reached_end:
                self.energy += int(enemy.rewards.get("energy", 0))

        self.enemies = [e for e in self.enemies if e.alive]
        self.projectiles = [p for p in self.projectiles if p.alive]

        was_active = wave_manager.wave_active
        wave_manager.update_wave_state(self.enemies)
        if was_active and not wave_manager.wave_active:
            self.energy += WAVE_CLEAR_ENERGY

        if self.gpa <= FAILING_GPA:
            self.game_over = True
