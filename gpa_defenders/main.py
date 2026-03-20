
import pygame
from src.network.client import NetworkClient
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
    show_network_lobby_screen,
)
from src.utils.asset_loader import (
    init_tower_sprites,
    init_ground_tiles,
    init_enemy_sprites,
    get_grass_tile,
    get_path_tile,
)


def _draw_speed_btn(screen: pygame.Surface, rect: pygame.Rect, speed: float) -> None:
    pygame.draw.rect(screen, (42, 50, 70), rect, border_radius=6)
    pygame.draw.rect(screen, (110, 130, 170), rect, 2, border_radius=6)
    font = pygame.font.SysFont(None, 24, bold=True)
    txt = font.render(f"{speed:.0f}x", True, (235, 235, 245))
    screen.blit(txt, (rect.centerx - txt.get_width() // 2, rect.centery - txt.get_height() // 2))


def run_game(
    screen: pygame.Surface,
    clock: pygame.time.Clock,
    map_id: str,
    multiplayer: bool = False,
    network_client: "NetworkClient | None" = None,
    is_host: bool = False,
) -> str:
    font = pygame.font.SysFont(None, 24)

    grid_map = GridMap(map_id=map_id)
    wave_manager = WaveManager(grid_map.waypoints)
    game_manager = GameManager()

    init_tower_sprites()
    init_ground_tiles(TILE_SIZE)
    init_enemy_sprites()

    net = network_client
    selected_tower_type = "coffee"
    tower_types_list = list(TOWER_TYPES.keys())
    selected_tower = None
    speed_btn = pygame.Rect(SCREEN_WIDTH - 88, 8, 76, 34)
    sync_timer = 0.0

    def poll_network() -> None:
        nonlocal net
        if net is None:
            return
        while True:
            msg = net.poll()
            if msg is None:
                break
            t = msg.get("type")
            if t == "PLACE_TOWER":
                gx, gy = msg["gx"], msg["gy"]
                tt = msg["tower_type"]
                if grid_map.can_place_tower(gx, gy):
                    if game_manager.place_tower(tt, gx, gy):
                        grid_map.place_tower(gx, gy)
            elif t == "START_WAVE" and not wave_manager.wave_active:
                game_manager.add_enemies(wave_manager.spawn_wave())
            elif t == "STATE_SYNC":
                if not is_host:
                    game_manager.gpa = msg.get("gpa", game_manager.gpa)
                    game_manager.energy = msg.get("energy", game_manager.energy)
            elif t == "PLAYER_LEFT":
                net.disconnect()
                net = None

    while True:
        dt = clock.tick(FPS) / 1000.0

        if net:
            poll_network()
            if is_host:
                sync_timer += dt
                if sync_timer >= 1.0:
                    sync_timer = 0.0
                    net.send({"type": "STATE_SYNC", "gpa": game_manager.gpa, "energy": game_manager.energy})

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    result = show_pause_menu(screen, clock)
                    if result == "quit":
                        return "quit"
                    if result == "menu":
                        return "menu"

                if game_manager.has_pending_perk_choice():
                    if event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                        idx = event.key - pygame.K_1
                        choices = game_manager.get_pending_perk_choices()
                        if 0 <= idx < len(choices):
                            game_manager.apply_perk(choices[idx]["id"])
                    continue

                if event.key == pygame.K_SPACE and not wave_manager.wave_active:
                    game_manager.add_enemies(wave_manager.spawn_wave())
                    if net:
                        net.send({"type": "START_WAVE"})

                if event.key == pygame.K_u and selected_tower:
                    upgrades = list(game_manager.get_tower_upgrades(selected_tower.tower_type).keys())
                    if upgrades:
                        game_manager.upgrade_tower_at(selected_tower.grid_x, selected_tower.grid_y, upgrades[0])

                for i, tower_type in enumerate(tower_types_list):
                    if event.key == pygame.K_1 + i:
                        selected_tower_type = tower_type

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if speed_btn.collidepoint(event.pos):
                    game_manager.cycle_speed()
                    continue

                gx = event.pos[0] // TILE_SIZE
                gy = event.pos[1] // TILE_SIZE
                if not grid_map.is_within_bounds(gx, gy):
                    selected_tower = None
                    continue

                tower = game_manager.get_tower_at(gx, gy)
                if tower:
                    selected_tower = tower
                    continue

                selected_tower = None
                if grid_map.can_place_tower(gx, gy):
                    if game_manager.place_tower(selected_tower_type, gx, gy):
                        grid_map.place_tower(gx, gy)
                        if net:
                            net.send({
                                "type": "PLACE_TOWER",
                                "tower_type": selected_tower_type,
                                "gx": gx,
                                "gy": gy,
                            })

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
            if tower == selected_tower:
                pygame.draw.circle(screen, (255, 255, 255), (int(tower.x), int(tower.y)), int(tower.range), 1)
        for enemy in game_manager.enemies:
            enemy.draw(screen)
        for projectile in game_manager.projectiles:
            projectile.draw(screen)

        ui_rect = pygame.Rect(0, GRID_ROWS * TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT - GRID_ROWS * TILE_SIZE)
        pygame.draw.rect(screen, UI_BG, ui_rect)

        txt = (
            f"GPA {game_manager.gpa:.2f} | Energy {game_manager.energy} | "
            f"Wave {wave_manager.wave} | Selected {TOWER_TYPES[selected_tower_type]['name']} | "
            f"SPACE wave | U upgrade"
        )
        screen.blit(font.render(txt, True, TEXT_COLOR), (12, GRID_ROWS * TILE_SIZE + 14))

        if net:
            nline = f"Online {'Host' if is_host else 'Client'}"
            screen.blit(font.render(nline, True, (180, 220, 180)), (12, 10))

        _draw_speed_btn(screen, speed_btn, game_manager.speed_multiplier)

        if game_manager.has_pending_perk_choice():
            choices = game_manager.get_pending_perk_choices()
            panel = pygame.Rect(140, 120, SCREEN_WIDTH - 280, 220)
            pygame.draw.rect(screen, (22, 22, 30), panel, border_radius=8)
            pygame.draw.rect(screen, (120, 130, 160), panel, 2, border_radius=8)
            title = pygame.font.SysFont(None, 34, bold=True).render("Kies een perk (1-3)", True, (245, 245, 255))
            screen.blit(title, (panel.centerx - title.get_width() // 2, panel.y + 16))
            for i, choice in enumerate(choices):
                line = f"{i + 1}. {choice['name']} - {choice['description']}"
                surf = pygame.font.SysFont(None, 28).render(line, True, (220, 225, 240))
                screen.blit(surf, (panel.x + 24, panel.y + 74 + i * 40))

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

        game_map_id = selected_map_id
        if mode == "online":
            lobby = show_network_lobby_screen(screen, clock, selected_map_id)
            if lobby is None:
                continue
            net_client, is_host, game_map_id = lobby
            selected_map_id = game_map_id
        else:
            net_client, is_host = None, False

        multiplayer = mode == "multi"

        while True:
            result = run_game(
                screen,
                clock,
                game_map_id,
                multiplayer=multiplayer,
                network_client=net_client,
                is_host=is_host,
            )
            if net_client:
                net_client.disconnect()
            if result == "quit":
                pygame.quit()
                return
            if result == "menu":
                break
            if result == "restart" and mode != "online":
                continue
            break

    pygame.quit()


if __name__ == "__main__":
    main()
