
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
