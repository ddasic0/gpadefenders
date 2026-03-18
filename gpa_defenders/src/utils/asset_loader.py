
from pathlib import Path
import pygame

ASSETS_DIR = Path(__file__).resolve().parents[2] / "assets"

_tower_sprites: dict[str, pygame.Surface] = {}
_enemy_icons: dict[str, pygame.Surface] = {}
_ground_tiles: dict[str, pygame.Surface] = {}


def _safe_load(path: Path) -> pygame.Surface | None:
    try:
        return pygame.image.load(str(path)).convert_alpha()
    except (pygame.error, FileNotFoundError):
        return None


def init_tower_sprites() -> None:
    _tower_sprites.clear()
    mapping = {
        "coffee": "tower_1.png",
        "study_group": "tower_2.png",
        "tutor": "tower_3.png",
        "energy_drink": "tower_4.png",
    }
    for tower_type, filename in mapping.items():
        img = _safe_load(ASSETS_DIR / "towers" / filename)
        if img is None:
            continue
        frame_w = img.get_width() // 4
        frame_h = img.get_height()
        frame = pygame.Surface((frame_w, frame_h), pygame.SRCALPHA)
        frame.blit(img, (0, 0), pygame.Rect(frame_w * 3, 0, frame_w, frame_h))
        _tower_sprites[tower_type] = frame


def get_tower_sprite(tower_type: str, size: tuple[int, int]) -> pygame.Surface | None:
    sprite = _tower_sprites.get(tower_type)
    if sprite is None:
        return None
    return pygame.transform.smoothscale(sprite, size)


def has_tower_sprites() -> bool:
    return len(_tower_sprites) > 0


def init_ground_tiles(tile_size: int) -> None:
    _ground_tiles.clear()
    grass = _safe_load(ASSETS_DIR / "tiles" / "FieldsTile_38.png")
    path = _safe_load(ASSETS_DIR / "tiles" / "FieldsTile_01.png")
    if grass is not None:
        _ground_tiles["grass"] = pygame.transform.smoothscale(grass, (tile_size, tile_size))
    if path is not None:
        _ground_tiles["path"] = pygame.transform.smoothscale(path, (tile_size, tile_size))


def get_grass_tile(tile_idx: int = 0) -> pygame.Surface | None:
    return _ground_tiles.get("grass")


def get_path_tile(tile_idx: int = 0) -> pygame.Surface | None:
    return _ground_tiles.get("path")


def has_ground_tiles() -> bool:
    return "grass" in _ground_tiles and "path" in _ground_tiles


def init_enemy_sprites() -> None:
    _enemy_icons.clear()
    mapping = {
        "quiz": "quiz.png",
        "huiswerk": "huiswerk.png",
        "midterm": "midterm.png",
        "professor": "professor_walk.png",
    }
    for enemy_type, filename in mapping.items():
        img = _safe_load(ASSETS_DIR / "enemies" / filename)
        if img is not None:
            _enemy_icons[enemy_type] = img


def get_enemy_frame(enemy_type: str, anim_time: float = 0.0) -> pygame.Surface | None:
    img = _enemy_icons.get(enemy_type)
    if img is None:
        return None
    if enemy_type == "professor":
        frame_w = img.get_width() // 4
        frame_h = img.get_height()
        idx = int(anim_time * 8) % 4
        frame = pygame.Surface((frame_w, frame_h), pygame.SRCALPHA)
        frame.blit(img, (0, 0), pygame.Rect(frame_w * idx, 0, frame_w, frame_h))
        return frame
    return img


def has_enemy_sprites() -> bool:
    return len(_enemy_icons) > 0
