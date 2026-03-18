
import pygame
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, MAP_DEFINITIONS, DEFAULT_MAP_ID


def _draw_center(screen: pygame.Surface, title: str, subtitle: str = "") -> None:
    screen.fill((24, 30, 44))
    font_title = pygame.font.SysFont(None, 64, bold=True)
    font_sub = pygame.font.SysFont(None, 30)
    t = font_title.render(title, True, WHITE)
    screen.blit(t, (SCREEN_WIDTH // 2 - t.get_width() // 2, 180))
    if subtitle:
        s = font_sub.render(subtitle, True, (190, 200, 220))
        screen.blit(s, (SCREEN_WIDTH // 2 - s.get_width() // 2, 255))


def show_start_screen(screen: pygame.Surface, clock: pygame.time.Clock) -> bool:
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return True
                if event.key == pygame.K_ESCAPE:
                    return False
        _draw_center(screen, "GPA Defenders", "ENTER/SPACE om te starten, ESC om te sluiten")
        pygame.display.flip()


def show_tutorial_screen(screen: pygame.Surface, clock: pygame.time.Clock) -> bool:
    lines = [
        "Plaats torens langs het pad.",
        "SPACE start een wave.",
        "1-4 kiest torentype.",
        "Bescherm je GPA boven 5.5.",
        "ENTER om door te gaan, ESC om terug te gaan.",
    ]
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return True
                if event.key == pygame.K_ESCAPE:
                    return False
        _draw_center(screen, "Tutorial")
        font = pygame.font.SysFont(None, 30)
        for i, line in enumerate(lines):
            surf = font.render(line, True, (210, 220, 235))
            screen.blit(surf, (SCREEN_WIDTH // 2 - surf.get_width() // 2, 250 + i * 34))
        pygame.display.flip()


def show_map_select_screen(screen: pygame.Surface, clock: pygame.time.Clock, current_map_id: str = DEFAULT_MAP_ID) -> str | None:
    keys = list(MAP_DEFINITIONS.keys())
    if current_map_id not in MAP_DEFINITIONS:
        current_map_id = DEFAULT_MAP_ID
    idx = keys.index(current_map_id)

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    idx = (idx - 1) % len(keys)
                if event.key in (pygame.K_RIGHT, pygame.K_d):
                    idx = (idx + 1) % len(keys)
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return keys[idx]

        map_id = keys[idx]
        _draw_center(screen, "Kies een map", f"{MAP_DEFINITIONS[map_id]['name']} ({map_id})")
        hint = pygame.font.SysFont(None, 28).render("LEFT/RIGHT kiezen, ENTER bevestigen, ESC terug", True, (170, 185, 210))
        screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, 320))
        pygame.display.flip()


def show_mode_select_screen(screen: pygame.Surface, clock: pygame.time.Clock) -> str:
    modes = ["single", "multi"]
    idx = 0
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "back"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "back"
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    idx = (idx - 1) % len(modes)
                if event.key in (pygame.K_RIGHT, pygame.K_d):
                    idx = (idx + 1) % len(modes)
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return modes[idx]

        label = "Singleplayer" if modes[idx] == "single" else "Local Co-op"
        _draw_center(screen, "Kies modus", label)
        hint = pygame.font.SysFont(None, 28).render("LEFT/RIGHT kiezen, ENTER bevestigen, ESC terug", True, (170, 185, 210))
        screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, 320))
        pygame.display.flip()


def show_pause_menu(screen: pygame.Surface, clock: pygame.time.Clock) -> str:
    options = ["resume", "menu", "quit"]
    idx = 0
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "resume"
                if event.key in (pygame.K_UP, pygame.K_w):
                    idx = (idx - 1) % len(options)
                if event.key in (pygame.K_DOWN, pygame.K_s):
                    idx = (idx + 1) % len(options)
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return options[idx]

        _draw_center(screen, "Pauze")
        font = pygame.font.SysFont(None, 34)
        for i, option in enumerate(options):
            col = (255, 230, 120) if i == idx else (200, 210, 225)
            surf = font.render(option.upper(), True, col)
            screen.blit(surf, (SCREEN_WIDTH // 2 - surf.get_width() // 2, 280 + i * 42))
        pygame.display.flip()


def show_game_over_screen(screen: pygame.Surface, clock: pygame.time.Clock, wave: int, gpa: float) -> str:
    options = ["restart", "menu", "quit"]
    idx = 0
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    idx = (idx - 1) % len(options)
                if event.key in (pygame.K_DOWN, pygame.K_s):
                    idx = (idx + 1) % len(options)
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return options[idx]

        _draw_center(screen, "Game Over", f"Wave {wave} | GPA {gpa:.2f}")
        font = pygame.font.SysFont(None, 34)
        for i, option in enumerate(options):
            col = (255, 180, 120) if i == idx else (220, 210, 210)
            surf = font.render(option.upper(), True, col)
            screen.blit(surf, (SCREEN_WIDTH // 2 - surf.get_width() // 2, 300 + i * 42))
        pygame.display.flip()


def show_network_lobby_screen(screen: pygame.Surface, clock: pygame.time.Clock, selected_map_id: str = DEFAULT_MAP_ID):
    return None
