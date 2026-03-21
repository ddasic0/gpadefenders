
import os
import pygame
from src.settings import TOWER_TYPES

                      
_sprite_cache: dict[str, pygame.Surface] = {}

                        
ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets")

                                                       
                                                                            
                                    
TOWER_SPRITE_MAP: dict[str, tuple[int, int]] = {
    "coffee":       (1, 3),                                
    "pen_paper":    (2, 3),                                  
    "study_group":  (3, 3),                                  
    "energy_drink": (4, 3),                                
    "motivatie":    (5, 3),                               
    "chatgpt":      (6, 3),                              
    "tutor":        (7, 3),                                  
    "hoorcolleges": (7, 1),                                 
}

                                                                
                                                                           
TOWER_TINTS: dict[str, tuple[int, int, int, int]] = {
    "coffee":       (160, 100, 50, 60),                 
    "pen_paper":    (180, 180, 200, 50),                         
    "study_group":  (60, 120, 240, 70),             
    "energy_drink": (255, 220, 50, 65),                
    "motivatie":    (255, 130, 180, 60),            
    "chatgpt":      (90, 230, 220, 65),                      
    "tutor":        (40, 130, 40, 55),                     
    "hoorcolleges": (255, 210, 90, 60),             
}


def _apply_tint(surface: pygame.Surface, tint: tuple[int, int, int, int]) -> pygame.Surface:
    r, g, b, intensity = tint
    result = surface.copy()

                                       
    overlay = pygame.Surface(result.get_size(), pygame.SRCALPHA)
    overlay.fill((r, g, b, intensity))

                                                                        
    result.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

                                                                 
    tinted = surface.copy()
    color_layer = pygame.Surface(tinted.get_size(), pygame.SRCALPHA)
    color_layer.fill((r, g, b, intensity))
    tinted.blit(color_layer, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

                                                                   
    final = surface.copy()
    tinted.set_alpha(intensity)
    final.blit(tinted, (0, 0))

    return final


def _load_row_image(file_num: int, cols: int = 4) -> list[pygame.Surface]:
    path = os.path.join(ASSETS_DIR, "towers", f"tower_{file_num}.png")
    img = pygame.image.load(path).convert_alpha()

    sprite_w = img.get_width() // cols
    sprite_h = img.get_height()

    sprites: list[pygame.Surface] = []
    for col in range(cols):
        rect = pygame.Rect(col * sprite_w, 0, sprite_w, sprite_h)
        sprites.append(img.subsurface(rect).copy())

    return sprites


def get_tower_sprite(tower_type: str, size: tuple[int, int] | None = None) -> pygame.Surface | None:
    cache_key = f"tower_{tower_type}_{size}"
    if cache_key in _sprite_cache:
        return _sprite_cache[cache_key]

    base_key = f"tower_{tower_type}_base"
    base = _sprite_cache.get(base_key)
    if base is None:
        return None

    if size:
        scaled = pygame.transform.smoothscale(base, size)
    else:
        scaled = base

    _sprite_cache[cache_key] = scaled
    return scaled


def init_tower_sprites() -> bool:
                                               
    needed_files = set(num for num, _ in TOWER_SPRITE_MAP.values())
    for num in needed_files:
        path = os.path.join(ASSETS_DIR, "towers", f"tower_{num}.png")
        if not os.path.exists(path):
            print(f"[AssetLoader] Niet gevonden: {path}")
            print("[AssetLoader] Game draait zonder sprites (fallback naar vormen).")
            return False

                                                                   
    row_cache: dict[int, list[pygame.Surface]] = {}
    for num in needed_files:
        row_cache[num] = _load_row_image(num)

                                                             
    count = 0
    for tower_type, (file_num, col) in TOWER_SPRITE_MAP.items():
        sprites = row_cache[file_num]
        if col < len(sprites):
            sprite = sprites[col]
                                                       
            tint = TOWER_TINTS.get(tower_type)
            if tint:
                sprite = _apply_tint(sprite, tint)
            _sprite_cache[f"tower_{tower_type}_base"] = sprite
            count += 1

    print(f"[AssetLoader] {count} tower sprites geladen en getint.")
    return True


def has_tower_sprites() -> bool:
    return any(k.startswith("tower_") for k in _sprite_cache)


                                              

_grass_tiles: list[pygame.Surface] = []
_path_tiles: list[pygame.Surface] = []

                                                                            
                                                                           
_GRASS_TILE_NUMS = [38]
_PATH_TILE_NUMS = list(range(1, 38))


def init_ground_tiles(tile_size: int = 64) -> bool:
    global _grass_tiles, _path_tiles
    _grass_tiles = []
    _path_tiles = []

    tiles_dir = os.path.join(ASSETS_DIR, "tiles")
    if not os.path.isdir(tiles_dir):
        print("[AssetLoader] Tiles map niet gevonden, fallback naar kleuren.")
        return False

    for num in _GRASS_TILE_NUMS:
        path = os.path.join(tiles_dir, f"FieldsTile_{num:02d}.png")
        if os.path.exists(path):
            img = pygame.image.load(path).convert()
            _grass_tiles.append(pygame.transform.smoothscale(img, (tile_size, tile_size)))

    for num in _PATH_TILE_NUMS:
        path = os.path.join(tiles_dir, f"FieldsTile_{num:02d}.png")
        if os.path.exists(path):
            img = pygame.image.load(path).convert()
            _path_tiles.append(pygame.transform.smoothscale(img, (tile_size, tile_size)))

    loaded = len(_grass_tiles) + len(_path_tiles)
    if loaded:
        print(f"[AssetLoader] {len(_grass_tiles)} gras + {len(_path_tiles)} pad tegels geladen.")
    else:
        print("[AssetLoader] Geen tegels gevonden, fallback naar kleuren.")
    return loaded > 0


def get_grass_tile(index: int) -> pygame.Surface | None:
    if not _grass_tiles:
        return None
    return _grass_tiles[index % len(_grass_tiles)]


def get_path_tile(index: int) -> pygame.Surface | None:
    if not _path_tiles:
        return None
    return _path_tiles[index % len(_path_tiles)]


def has_ground_tiles() -> bool:
    return bool(_grass_tiles) or bool(_path_tiles)


                                               

                                       
_enemy_animations: dict[str, list[pygame.Surface]] = {}

                                                
_enemy_icons: dict[str, pygame.Surface] = {}

                                                                     
ENEMY_ANIM_MAP: dict[str, tuple[str, int]] = {
    "professor": ("professor_walk.png", 12),
}

                                            
ENEMY_ICON_MAP: dict[str, str] = {
    "quiz":       "quiz.png",
    "huiswerk":   "huiswerk.png",
    "attendance": "attendance.png",
    "opdracht":   "opdracht.png",
    "midterm":    "midterm.png",
    "endterm":    "midterm.png",                         
}


def init_enemy_sprites(sprite_size: int = 36) -> bool:
    enemies_dir = os.path.join(ASSETS_DIR, "enemies")
    if not os.path.isdir(enemies_dir):
        return False

    count = 0

                                   
    for enemy_type, (filename, cols) in ENEMY_ANIM_MAP.items():
        path = os.path.join(enemies_dir, filename)
        if not os.path.exists(path):
            continue

        sheet = pygame.image.load(path).convert_alpha()
        frame_w = sheet.get_width() // cols
        frame_h = sheet.get_height()

        frames: list[pygame.Surface] = []
        for c in range(cols):
            rect = pygame.Rect(c * frame_w, 0, frame_w, frame_h)
            frame = sheet.subsurface(rect).copy()
            frame = pygame.transform.smoothscale(frame, (sprite_size, sprite_size))
            frames.append(frame)

        _enemy_animations[enemy_type] = frames
        count += 1

                          
    for enemy_type, filename in ENEMY_ICON_MAP.items():
        path = os.path.join(enemies_dir, filename)
        if not os.path.exists(path):
            continue

        img = pygame.image.load(path).convert_alpha()
        _enemy_icons[enemy_type] = pygame.transform.smoothscale(
            img, (sprite_size, sprite_size))
        count += 1

    if count:
        print(f"[AssetLoader] {count} enemy sprite(s) geladen.")
    return count > 0


def get_enemy_frame(enemy_type: str, anim_time: float,
                    fps: float = 10.0) -> pygame.Surface | None:
                            
    frames = _enemy_animations.get(enemy_type)
    if frames:
        idx = int(anim_time * fps) % len(frames)
        return frames[idx]

                          
    return _enemy_icons.get(enemy_type)


def has_enemy_sprites(enemy_type: str) -> bool:
    return enemy_type in _enemy_animations or enemy_type in _enemy_icons
