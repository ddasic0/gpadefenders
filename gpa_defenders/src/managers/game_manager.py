
import random
from src.entities.projectile import Projectile
from src.entities.tower import create_tower
from src.settings import (
    STARTING_GPA,
    STARTING_ENERGY,
    FAILING_GPA,
    TOWER_TYPES,
    TOWER_UPGRADES,
    WAVE_CLEAR_ENERGY,
    PERKS,
    PERK_WAVE_INTERVAL,
    PERK_OFFER_COUNT,
)


class GameManager:
    def __init__(self):
        self.gpa = STARTING_GPA
        self.energy = STARTING_ENERGY
        self.game_over = False
        self.towers = []
        self.enemies = []
        self.projectiles = []

        self.allowed_speeds = (1.0, 2.0, 4.0)
        self.speed_multiplier = 1.0

        self.pending_perk_choices: list[dict] = []
        self.perk_stacks: dict[str, int] = {}
        self.global_damage_multiplier = 1.0
        self.global_fire_rate_multiplier = 1.0

    def cycle_speed(self) -> float:
        idx = self.allowed_speeds.index(self.speed_multiplier)
        self.speed_multiplier = self.allowed_speeds[(idx + 1) % len(self.allowed_speeds)]
        return self.speed_multiplier

    def can_afford_tower(self, tower_type: str) -> bool:
        return self.energy >= int(TOWER_TYPES[tower_type]["cost"])

    def place_tower(self, tower_type: str, grid_x: int, grid_y: int) -> bool:
        if not self.can_afford_tower(tower_type):
            return False
        tower = create_tower(tower_type, grid_x, grid_y)
        self.energy -= tower.cost
        self.towers.append(tower)
        return True

    def get_tower_at(self, grid_x: int, grid_y: int):
        for tower in self.towers:
            if tower.grid_x == grid_x and tower.grid_y == grid_y:
                return tower
        return None

    def get_tower_upgrades(self, tower_type: str) -> dict[str, dict]:
        return TOWER_UPGRADES.get(tower_type, {})

    def can_upgrade_tower(self, tower, upgrade_id: str) -> bool:
        cfg = self.get_tower_upgrades(tower.tower_type).get(upgrade_id)
        if cfg is None:
            return False
        if tower.has_upgrade(upgrade_id):
            return False
        return self.energy >= int(cfg["cost"])

    def upgrade_tower_at(self, grid_x: int, grid_y: int, upgrade_id: str) -> bool:
        tower = self.get_tower_at(grid_x, grid_y)
        if tower is None:
            return False
        if not self.can_upgrade_tower(tower, upgrade_id):
            return False
        cfg = self.get_tower_upgrades(tower.tower_type)[upgrade_id]
        self.energy -= int(cfg["cost"])
        return tower.apply_upgrade(upgrade_id, cfg)

    def has_pending_perk_choice(self) -> bool:
        return len(self.pending_perk_choices) > 0

    def get_pending_perk_choices(self) -> list[dict]:
        return [dict(choice) for choice in self.pending_perk_choices]

    def offer_perks(self, wave: int) -> list[dict]:
        if wave <= 0 or wave % PERK_WAVE_INTERVAL != 0:
            return []
        if self.has_pending_perk_choice():
            return self.get_pending_perk_choices()

        available = []
        for perk_id, cfg in PERKS.items():
            if self.perk_stacks.get(perk_id, 0) < int(cfg.get("max_stacks", 1)):
                available.append(perk_id)
        if not available:
            return []

        k = min(PERK_OFFER_COUNT, len(available))
        chosen = random.sample(available, k)
        self.pending_perk_choices = [
            {
                "id": perk_id,
                "name": PERKS[perk_id]["name"],
                "description": PERKS[perk_id]["description"],
            }
            for perk_id in chosen
        ]
        return self.get_pending_perk_choices()

    def apply_perk(self, perk_id: str) -> bool:
        if perk_id not in PERKS:
            return False
        if self.has_pending_perk_choice() and perk_id not in {x["id"] for x in self.pending_perk_choices}:
            return False

        current = self.perk_stacks.get(perk_id, 0)
        max_stacks = int(PERKS[perk_id].get("max_stacks", 1))
        if current >= max_stacks:
            return False

        effects = PERKS[perk_id].get("effects", {})
        if "damage_multiplier" in effects:
            self.global_damage_multiplier *= float(effects["damage_multiplier"])
        if "fire_rate_multiplier" in effects:
            self.global_fire_rate_multiplier *= float(effects["fire_rate_multiplier"])
        if "instant_energy" in effects:
            self.energy += int(effects["instant_energy"])

        self.perk_stacks[perk_id] = current + 1
        self.pending_perk_choices = []
        return True

    def add_enemies(self, enemies: list) -> None:
        self.enemies.extend(enemies)

    def update(self, dt: float, wave_manager) -> None:
        if self.game_over:
            return

        scaled_dt = dt * self.speed_multiplier

        for enemy in self.enemies:
            enemy.update(scaled_dt)
            if enemy.reached_end and enemy.alive:
                self.gpa -= enemy.gpa_damage
                enemy.alive = False

        for tower in self.towers:
            shot = tower.update(scaled_dt * self.global_fire_rate_multiplier, self.enemies)
            if shot:
                shot["damage"] *= self.global_damage_multiplier
                self.projectiles.append(Projectile(**shot))

        for projectile in self.projectiles:
            projectile.update(scaled_dt)

        for enemy in self.enemies:
            if not enemy.alive and not enemy.reached_end:
                self.energy += int(enemy.rewards.get("energy", 0))

        self.enemies = [e for e in self.enemies if e.alive]
        self.projectiles = [p for p in self.projectiles if p.alive]

        was_active = wave_manager.wave_active
        wave_manager.update_wave_state(self.enemies)
        if was_active and not wave_manager.wave_active:
            self.energy += WAVE_CLEAR_ENERGY
            self.offer_perks(wave_manager.wave)

        if self.gpa <= FAILING_GPA:
            self.game_over = True
