
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
)
from src.managers.grid import GridMap
from src.entities.enemy import Quiz
from src.entities.tower import create_tower
from src.entities.projectile import Projectile


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)

    grid_map = GridMap()
    towers = []
    enemies = []
    projectiles = []
    spawn_timer = 0.0
    gpa = 10.0

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                gx = event.pos[0] // TILE_SIZE
                gy = event.pos[1] // TILE_SIZE
                if grid_map.can_place_tower(gx, gy):
                    towers.append(create_tower("coffee", gx, gy))
                    grid_map.place_tower(gx, gy)

        spawn_timer += dt
        if spawn_timer >= 1.2:
            spawn_timer = 0.0
            enemies.append(Quiz(grid_map.waypoints))

        for enemy in enemies:
            enemy.update(dt)
            if enemy.reached_end and enemy.alive:
                gpa -= enemy.gpa_damage
                enemy.alive = False

        for tower in towers:
            shot = tower.update(dt, enemies)
            if shot:
                projectiles.append(Projectile(**shot))

        for projectile in projectiles:
            projectile.update(dt)

        enemies = [e for e in enemies if e.alive]
        projectiles = [p for p in projectiles if p.alive]

        screen.fill(GRASS_COLOR)
        for row in range(GRID_ROWS):
            for col in range(GRID_COLS):
                rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if grid_map.grid[row][col] == 1:
                    pygame.draw.rect(screen, PATH_COLOR, rect)
                pygame.draw.rect(screen, GRID_LINE_COLOR, rect, 1)

        for tower in towers:
            tower.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)
        for projectile in projectiles:
            projectile.draw(screen)

        ui_rect = pygame.Rect(0, GRID_ROWS * TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT - GRID_ROWS * TILE_SIZE)
        pygame.draw.rect(screen, UI_BG, ui_rect)
        text = font.render(f"LMB place coffee tower | GPA {gpa:.2f}", True, TEXT_COLOR)
        screen.blit(text, (12, GRID_ROWS * TILE_SIZE + 14))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
