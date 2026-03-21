
from src.settings import (
    TILE_SIZE,
    GRID_COLS,
    GRID_ROWS,
    DEFAULT_MAP_ID,
    MAP_DEFINITIONS,
)


class GridMap:

    def __init__(self, map_id: str = DEFAULT_MAP_ID):
        self.grid: list[list[int]] = []
        self.waypoints: list[tuple[int, int]] = []
        self.map_id = map_id
        self.map_name = ""
        self.wave_pressure_multiplier = 1.0
        self.available_map_ids = tuple(MAP_DEFINITIONS.keys())
        self._setup_grid()

    def _cell_to_pixel(self, grid_x: int, grid_y: int) -> tuple[int, int]:
        return (
            grid_x * TILE_SIZE + TILE_SIZE // 2,
            grid_y * TILE_SIZE + TILE_SIZE // 2,
        )

    def _setup_grid(self) -> None:
        self.grid = [[0 for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
        if self.map_id not in MAP_DEFINITIONS:
            raise ValueError(f"Onbekende map id: {self.map_id}")

        map_config = MAP_DEFINITIONS[self.map_id]
        self.map_name = map_config["name"]
        self.wave_pressure_multiplier = float(
            map_config.get("wave_pressure_multiplier", 1.0)
        )

        waypoint_cells: list[tuple[int, int]] = map_config["waypoint_cells"]
        self.waypoints = [
            self._cell_to_pixel(grid_x, grid_y) for grid_x, grid_y in waypoint_cells
        ]

                                        
        for i in range(len(waypoint_cells) - 1):
            gx1, gy1 = waypoint_cells[i]
            gx2, gy2 = waypoint_cells[i + 1]

            if gy1 == gy2:               
                for gx in range(min(gx1, gx2), max(gx1, gx2) + 1):
                    if 0 <= gx < GRID_COLS and 0 <= gy1 < GRID_ROWS:
                        self.grid[gy1][gx] = 1
            elif gx1 == gx2:             
                for gy in range(min(gy1, gy2), max(gy1, gy2) + 1):
                    if 0 <= gx1 < GRID_COLS and 0 <= gy < GRID_ROWS:
                        self.grid[gy][gx1] = 1

    def is_within_bounds(self, grid_x: int, grid_y: int) -> bool:
        return 0 <= grid_x < GRID_COLS and 0 <= grid_y < GRID_ROWS

    def can_place_tower(self, grid_x: int, grid_y: int) -> bool:
        if not self.is_within_bounds(grid_x, grid_y):
            return False
        return self.grid[grid_y][grid_x] == 0

    def place_tower(self, grid_x: int, grid_y: int) -> bool:
        if not self.can_place_tower(grid_x, grid_y):
            return False
        self.grid[grid_y][grid_x] = 2
        return True

    def remove_tower(self, grid_x: int, grid_y: int) -> bool:
        if not self.is_within_bounds(grid_x, grid_y):
            return False
        if self.grid[grid_y][grid_x] != 2:
            return False
        self.grid[grid_y][grid_x] = 0
        return True
