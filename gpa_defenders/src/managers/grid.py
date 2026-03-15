
from src.settings import TILE_SIZE, GRID_COLS, GRID_ROWS, MAP_DEFINITIONS, DEFAULT_MAP_ID


class GridMap:

    def __init__(self, map_id: str = DEFAULT_MAP_ID):
        if map_id not in MAP_DEFINITIONS:
            map_id = DEFAULT_MAP_ID
        self.map_id = map_id
        self.grid = [[0 for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
        self.waypoint_cells = list(MAP_DEFINITIONS[map_id]["waypoint_cells"])
        self.waypoints = self._to_pixel_waypoints(self.waypoint_cells)
        self._mark_path_cells()

    def _to_pixel_waypoints(self, waypoint_cells: list[tuple[int, int]]) -> list[tuple[int, int]]:
        result = []
        for gx, gy in waypoint_cells:
            px = gx * TILE_SIZE + TILE_SIZE // 2
            py = gy * TILE_SIZE + TILE_SIZE // 2
            result.append((px, py))
        return result

    def _mark_path_cells(self) -> None:
        for i in range(len(self.waypoint_cells) - 1):
            x1, y1 = self.waypoint_cells[i]
            x2, y2 = self.waypoint_cells[i + 1]
            if y1 == y2:
                start = min(x1, x2)
                end = max(x1, x2)
                for gx in range(start, end + 1):
                    if 0 <= gx < GRID_COLS and 0 <= y1 < GRID_ROWS:
                        self.grid[y1][gx] = 1
            elif x1 == x2:
                start = min(y1, y2)
                end = max(y1, y2)
                for gy in range(start, end + 1):
                    if 0 <= x1 < GRID_COLS and 0 <= gy < GRID_ROWS:
                        self.grid[gy][x1] = 1

    def is_within_bounds(self, gx: int, gy: int) -> bool:
        return 0 <= gx < GRID_COLS and 0 <= gy < GRID_ROWS

    def can_place_tower(self, gx: int, gy: int) -> bool:
        return self.is_within_bounds(gx, gy) and self.grid[gy][gx] == 0

    def place_tower(self, gx: int, gy: int) -> bool:
        if not self.can_place_tower(gx, gy):
            return False
        self.grid[gy][gx] = 2
        return True

    def remove_tower(self, gx: int, gy: int) -> bool:
        if not self.is_within_bounds(gx, gy):
            return False
        if self.grid[gy][gx] != 2:
            return False
        self.grid[gy][gx] = 0
        return True
