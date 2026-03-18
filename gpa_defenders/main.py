
import pygame
from src.settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    TITLE,
    TILE_SIZE,
    GRID_COLS,
    GRID_ROWS,
    GRASS_COLOR,
    PATH_COLOR,
    GRID_LINE_COLOR,
    UI_BG,
    TEXT_COLOR,
    TOWER_TYPES,
    DEFAULT_MAP_ID,
)
from src.managers.grid import GridMap
from src.managers.wave_manager import WaveManager
from src.managers.game_manager import GameManager
from src.ui.screens import (
    show_start_screen,
    show_pause_menu,
    show_tutorial_screen,
    show_game_over_screen,
    show_mode_select_screen,
    show_map_select_screen,
)
from src.utils.asset_loader import (
    init_tower_sprites,
    init_ground_tiles,
    init_enemy_sprites,
    get_grass_tile,
    get_path_tile,
)


def run_game(screen: pygame.Surface, clock: pygame.time.Clock, map_id: str, multiplayer: bool = False) -> str:
    font = pygame.font.SysFont(None, 24)

    grid_map = GridMap(map_id=map_id)
    wave_manager = WaveManager(grid_map.waypoints)
    game_manager = GameManager()

    init_tower_sprites()
    init_ground_tiles(TILE_SIZE)
    init_enemy_sprites()

    selected_tower_type = "coffee"
    tower_types_list = list(TOWER_TYPES.keys())

    while True:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    result = show_pause_menu(screen, clock)
                    if result == "quit":
                        return "quit"
                    if result == "menu":
                        return "menu"
                if event.key == pygame.K_SPACE and not wave_manager.wave_active:
                    game_manager.add_enemies(wave_manager.spawn_wave())
                for i, tower_type in enumerate(tower_types_list):
                    if event.key == pygame.K_1 + i:
                        selected_tower_type = tower_type
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                gx = event.pos[0] // TILE_SIZE
                gy = event.pos[1] // TILE_SIZE
                if grid_map.can_place_tower(gx, gy):
                    if game_manager.place_tower(selected_tower_type, gx, gy):
                        grid_map.place_tower(gx, gy)

        game_manager.update(dt, wave_manager)

        if game_manager.game_over:
            return show_game_over_screen(screen, clock, wave_manager.wave, game_manager.gpa)

        screen.fill(GRASS_COLOR)
        for row in range(GRID_ROWS):
            for col in range(GRID_COLS):
                rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                tile_idx = row * GRID_COLS + col
                if grid_map.grid[row][col] == 1:
                    path_tile = get_path_tile(tile_idx)
                    if path_tile:
                        screen.blit(path_tile, rect)
                    else:
                        pygame.draw.rect(screen, PATH_COLOR, rect)
                else:
                    grass_tile = get_grass_tile(tile_idx)
                    if grass_tile:
                        screen.blit(grass_tile, rect)
                pygame.draw.rect(screen, GRID_LINE_COLOR, rect, 1)

        for tower in game_manager.towers:
            tower.draw(screen)
        for enemy in game_manager.enemies:
            enemy.draw(screen)
        for projectile in game_manager.projectiles:
            projectile.draw(screen)

        ui_rect = pygame.Rect(0, GRID_ROWS * TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT - GRID_ROWS * TILE_SIZE)
        pygame.draw.rect(screen, UI_BG, ui_rect)

        txt = (
            f"GPA {game_manager.gpa:.2f} | Energy {game_manager.energy} | "
            f"Wave {wave_manager.wave} | Selected {TOWER_TYPES[selected_tower_type]['name']} | "
            f"SPACE start wave | ESC pause"
        )
        screen.blit(font.render(txt, True, TEXT_COLOR), (12, GRID_ROWS * TILE_SIZE + 14))
        pygame.display.flip()


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()
    selected_map_id = DEFAULT_MAP_ID

    while show_start_screen(screen, clock):
        if not show_tutorial_screen(screen, clock):
            continue

        map_choice = show_map_select_screen(screen, clock, selected_map_id)
        if map_choice is None:
            continue
        selected_map_id = map_choice

        mode = show_mode_select_screen(screen, clock)
        if mode == "back":
            continue

        multiplayer = mode == "multi"

        while True:
            result = run_game(screen, clock, selected_map_id, multiplayer=multiplayer)
            if result == "quit":
                pygame.quit()
                return
            if result == "menu":
                break
            if result == "restart":
                continue
            break

    pygame.quit()


if __name__ == "__main__":
    main()
