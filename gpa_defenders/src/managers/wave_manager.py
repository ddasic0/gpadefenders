
from src.entities.enemy import Enemy
from src.settings import ENEMY_TYPES


class WaveManager:
    def __init__(self, waypoints: list[tuple[int, int]]):
        self.waypoints = waypoints
        self.wave = 0
        self.wave_active = False

    def _available_types(self) -> list[str]:
        available = []
        for enemy_type, cfg in ENEMY_TYPES.items():
            if self.wave >= int(cfg.get("unlock_wave", 1)):
                available.append(enemy_type)
        return available

    def spawn_wave(self) -> list[Enemy]:
        self.wave += 1
        self.wave_active = True

        count = 5 + self.wave * 2
        available = self._available_types() or ["quiz"]
        result: list[Enemy] = []
        for i in range(count):
            enemy_type = available[i % len(available)]
            enemy = Enemy(enemy_type, self.waypoints)
            enemy.x -= i * 42
            result.append(enemy)
        return result

    def update_wave_state(self, enemies: list[Enemy]) -> None:
        self.wave_active = any(e.alive for e in enemies)
