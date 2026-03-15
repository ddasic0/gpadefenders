
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
    TOWER_COLOR,
    GRID_LINE_COLOR,
    TEXT_COLOR,
    UI_BG,
)
from src.managers.grid import GridMap


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)

    grid_map = GridMap()

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                gx = event.pos[0] // TILE_SIZE
                gy = event.pos[1] // TILE_SIZE
                grid_map.place_tower(gx, gy)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                gx = event.pos[0] // TILE_SIZE
                gy = event.pos[1] // TILE_SIZE
                grid_map.remove_tower(gx, gy)

        screen.fill(GRASS_COLOR)

        for row in range(GRID_ROWS):
            for col in range(GRID_COLS):
                rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                cell = grid_map.grid[row][col]
                if cell == 1:
                    pygame.draw.rect(screen, PATH_COLOR, rect)
                elif cell == 2:
                    pygame.draw.rect(screen, TOWER_COLOR, rect)
                pygame.draw.rect(screen, GRID_LINE_COLOR, rect, 1)

        ui_rect = pygame.Rect(0, GRID_ROWS * TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT - GRID_ROWS * TILE_SIZE)
        pygame.draw.rect(screen, UI_BG, ui_rect)
        msg = "LMB place marker | RMB remove marker | ESC quit"
        text = font.render(msg, True, TEXT_COLOR)
        screen.blit(text, (12, GRID_ROWS * TILE_SIZE + 14))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
