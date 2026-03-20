
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60
TITLE = "GPA Defenders"

TILE_SIZE = 64
UI_HEIGHT = 150
GRID_COLS = SCREEN_WIDTH // TILE_SIZE
GRID_ROWS = (SCREEN_HEIGHT - UI_HEIGHT) // TILE_SIZE

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 80, 80)
GREEN = (80, 210, 100)
BLUE = (80, 120, 230)
YELLOW = (250, 210, 90)
BROWN = (145, 98, 60)

GRASS_COLOR = (100, 160, 90)
PATH_COLOR = (205, 170, 120)
GRID_LINE_COLOR = (78, 120, 74)
TEXT_COLOR = (245, 245, 245)
UI_BG = (30, 35, 46)

STARTING_GPA = 10.0
FAILING_GPA = 5.5
STARTING_ENERGY = 800
WAVE_CLEAR_ENERGY = 60

DEFAULT_MAP_ID = "campus_s"
MAP_DEFINITIONS = {
    "campus_s": {
        "name": "Campus S-Route",
        "waypoint_cells": [(-1, 2), (4, 2), (4, 5), (10, 5), (10, 2), (GRID_COLS, 2)],
    },
    "library_rush": {
        "name": "Library Rush",
        "waypoint_cells": [(-1, 4), (5, 4), (5, 2), (9, 2), (9, 4), (GRID_COLS, 4)],
    },
}

TOWER_TYPES = {
    "coffee": {
        "name": "Koffie",
        "cost": 200,
        "damage": 3.0,
        "range": 120,
        "fire_rate": 1.1,
        "projectile_speed": 320,
        "color": BROWN,
        "projectile_color": YELLOW,
    },
    "study_group": {
        "name": "Studiegroep",
        "cost": 400,
        "damage": 1.0,
        "range": 108,
        "fire_rate": 0.8,
        "projectile_speed": 230,
        "color": BLUE,
        "projectile_color": WHITE,
    },
    "tutor": {
        "name": "Tutor",
        "cost": 800,
        "damage": 12.0,
        "range": 165,
        "fire_rate": 0.35,
        "projectile_speed": 260,
        "color": GREEN,
        "projectile_color": GREEN,
    },
    "energy_drink": {
        "name": "Energy Drink",
        "cost": 600,
        "damage": 1.2,
        "range": 96,
        "fire_rate": 3.8,
        "projectile_speed": 420,
        "color": YELLOW,
        "projectile_color": YELLOW,
    },
}

TOWER_UPGRADES = {
    "coffee": {
        "espresso": {
            "name": "Espresso",
            "cost": 320,
            "damage_multiplier": 1.35,
            "fire_rate_multiplier": 1.25,
        }
    },
    "study_group": {},
    "tutor": {},
    "energy_drink": {},
}

PERK_WAVE_INTERVAL = 3
PERK_OFFER_COUNT = 3
PERKS = {
    "focus_mode": {
        "name": "Focus Mode",
        "description": "+10% damage",
        "effects": {"damage_multiplier": 1.10},
        "max_stacks": 3,
    },
    "rapid_revision": {
        "name": "Rapid Revision",
        "description": "+12% fire rate",
        "effects": {"fire_rate_multiplier": 1.12},
        "max_stacks": 3,
    },
    "bonus_budget": {
        "name": "Bonus Budget",
        "description": "+120 energy now",
        "effects": {"instant_energy": 120},
        "max_stacks": 4,
    },
}

ENEMY_TYPES = {
    "quiz": {
        "name": "Quiz",
        "hp": 16,
        "speed": 72,
        "gpa_damage": 0.08,
        "rewards": {"energy": 28},
        "color": WHITE,
        "unlock_wave": 1,
    },
    "huiswerk": {
        "name": "Huiswerk",
        "hp": 14,
        "speed": 110,
        "gpa_damage": 0.13,
        "rewards": {"energy": 24},
        "color": RED,
        "unlock_wave": 2,
    },
    "midterm": {
        "name": "Midterm",
        "hp": 70,
        "speed": 36,
        "gpa_damage": 0.55,
        "rewards": {"energy": 76},
        "color": (240, 140, 70),
        "unlock_wave": 5,
    },
    "professor": {
        "name": "Professor",
        "hp": 220,
        "speed": 24,
        "gpa_damage": 1.4,
        "rewards": {"energy": 160},
        "color": (120, 120, 120),
        "unlock_wave": 8,
    },
}
