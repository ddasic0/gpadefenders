
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60
TITLE = "GPA Defenders"

TILE_SIZE = 64
UI_HEIGHT = 150
GRID_COLS = SCREEN_WIDTH // TILE_SIZE
GRID_ROWS = (SCREEN_HEIGHT - UI_HEIGHT) // TILE_SIZE

GRASS_COLOR = (100, 160, 90)
PATH_COLOR = (205, 170, 120)
TOWER_COLOR = (70, 85, 110)
GRID_LINE_COLOR = (78, 120, 74)
TEXT_COLOR = (245, 245, 245)
UI_BG = (30, 35, 46)
ENEMY_COLOR = (220, 80, 80)
PROJECTILE_COLOR = (255, 220, 120)
BLACK = (0, 0, 0)
RED = (220, 80, 80)
GREEN = (80, 210, 100)

STARTING_GPA = 10.0
FAILING_GPA = 5.5
STARTING_ENERGY = 500

DEFAULT_MAP_ID = "campus_s"
MAP_DEFINITIONS = {
    "campus_s": {
        "name": "Campus S-Route",
        "waypoint_cells": [(-1, 2), (4, 2), (4, 5), (10, 5), (10, 2), (GRID_COLS, 2)],
    }
}

TOWER_TYPES = {
    "coffee": {
        "name": "Koffie",
        "cost": 150,
        "damage": 3.0,
        "range": 120,
        "fire_rate": 1.0,
        "projectile_speed": 320,
        "color": TOWER_COLOR,
        "projectile_color": PROJECTILE_COLOR,
    }
}

ENEMY_TYPES = {
    "quiz": {
        "name": "Quiz",
        "hp": 16,
        "speed": 70,
        "gpa_damage": 0.1,
        "rewards": {"energy": 25},
        "color": ENEMY_COLOR,
    }
}
