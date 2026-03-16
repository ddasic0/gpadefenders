
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
)
from src.managers.grid import GridMap
from src.managers.wave_manager import WaveManager
from src.managers.game_manager import GameManager


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)

    grid_map = GridMap()
    wave_manager = WaveManager(grid_map.waypoints)
    game_manager = GameManager()

    selected_tower_type = "coffee"
    tower_types_list = list(TOWER_TYPES.keys())

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
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

        screen.fill(GRASS_COLOR)
        for row in range(GRID_ROWS):
            for col in range(GRID_COLS):
                rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if grid_map.grid[row][col] == 1:
                    pygame.draw.rect(screen, PATH_COLOR, rect)
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
            f"SPACE start wave"
        )
        screen.blit(font.render(txt, True, TEXT_COLOR), (12, GRID_ROWS * TILE_SIZE + 14))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
