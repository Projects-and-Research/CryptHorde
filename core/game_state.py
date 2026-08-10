import math
import random
import core.config as config


def reset_game():
    config.player_x = 0.0
    config.player_y = 0.0
    config.player_z = 0.0
    config.player_angle = 90.0
    config.player_pitch = 0.0

    config.player_health = 100
    config.max_health = 100
    config.player_mana = 100.0
    config.max_mana = 100.0
    config.player_gold = 50
    config.player_money = 50
    config.player_arrows = 20

    config.overdrive_timer = 0
    config.invincible_timer = 0
    config.overdrive_active = False
    config.invincible_active = False

    config.current_weapon = 0
    config.weapon_levels = [1, 1, 1, 1]

    config.mb1_pressed = False
    config.charge_time = 0.0
    config.reload_timer = 0

    config.recoil_offset = 0.0
    config.weapon_y_offset = 0.0
    config.weapon_down_offset = 0.0
    config.weapon_forward_offset = 0.0
    config.view_bob = 0.0
    config.bob_step = 0.0

    config.deployable_stock = 1

    config.wave_number = 1
    # Set to 300 frames (approx 5 seconds at 60 FPS) for the very first wave start delay
    config.wave_timer = 300.0
    config.wave_active = False
    config.passive_gold_timer = 0
    config.rune_spawn_timer = 0
    config.enemies_remaining = 0
    config.game_score = 0
    config.score = 0

    # Reset entity lists (enemies start empty until the 5s timer counts down)
    config.player_projectiles = []
    config.bullets = config.player_projectiles  # Keep synced
    config.enemy_arrows = []
    config.projectiles = []
    config.enemies = []
    config.runes = []
    config.pickups = config.runes  # Keep synced
    config.traps = []
    config.hazards = config.traps  # Keep synced
    config.spiked_traps = config.traps  # Keep synced
    config.deployables = []
    config.shops = []


def get_weighted_enemy_type():
    # 0: Regular (50% chance)
    # 1: Archer  (25% chance)
    # 2: Heavy   (15% chance)
    # 3: Sage    (10% chance)
    roll = random.randint(1, 100)

    if roll <= 50:
        return 0
    elif roll <= 75:
        return 1
    elif roll <= 90:
        return 2
    else:
        return 3


def spawn_wave(wave_num):
    config.enemies = []
    enemy_count = 4 + wave_num * 2

    for i in range(0, enemy_count, 1):
        spawn_x = 0.0
        spawn_y = 0.0
        valid_spawn = False

        while not valid_spawn:
            spawn_x = float(
                random.randint(
                    -int(config.BOUND_LIMIT), int(config.BOUND_LIMIT)
                )
            )
            spawn_y = float(
                random.randint(
                    -int(config.BOUND_LIMIT), int(config.BOUND_LIMIT)
                )
            )

            dx = spawn_x - config.player_x
            dy = spawn_y - config.player_y
            dist = math.sqrt(dx * dx + dy * dy)

            if dist > 250.0:
                valid_spawn = True

        enemy_type_idx = get_weighted_enemy_type()

        # Enemy structure matching AI & Collisions: [x, y, z, type_string, hp, max_hp, cooldown, hit_flash]
        if enemy_type_idx == 0:
            # Regular Enemy (100 HP)
            config.enemies.append(
                [spawn_x, spawn_y, 0.0, "regular", 100.0, 100.0, 0, 0]
            )
        elif enemy_type_idx == 1:
            # Archer Enemy (80 HP)
            config.enemies.append(
                [spawn_x, spawn_y, 0.0, "archer", 80.0, 80.0, 0, 0]
            )
        elif enemy_type_idx == 2:
            # Heavy Enemy (150 HP)
            config.enemies.append(
                [spawn_x, spawn_y, 0.0, "heavy", 150.0, 150.0, 0, 0]
            )
        elif enemy_type_idx == 3:
            # Sage Enemy (70 HP)
            config.enemies.append(
                [spawn_x, spawn_y, 0.0, "sage", 70.0, 70.0, 0, 0]
            )

    config.enemies_remaining = len(config.enemies)
    config.wave_active = True


def update_world_spawns(dt=0.016):
    """
    Randomly spawns pickupable items (health/mana runes or invincibility) 
    roughly once every 60 seconds (3,600 frames at 60 FPS).
    """
    if not hasattr(config, "rune_spawn_timer"):
        config.rune_spawn_timer = 0

    config.rune_spawn_timer += 1

    # 3,600 frames = ~60 seconds at 60 FPS
    if config.rune_spawn_timer >= 3600:
        config.rune_spawn_timer = 0

        if not hasattr(config, "runes"):
            config.runes = []

        # Limit maximum active runes on the map to prevent clutter
        if len(config.runes) < 5:
            spawn_x = random.uniform(-400.0, 400.0)
            spawn_y = random.uniform(-400.0, 400.0)
            spawn_z = 0.0

            rune_types = ["health", "mana", "invincible"]
            chosen_type = random.choice(rune_types)

            # Format matching arena.py loop: [x, y, type, float_offset]
            config.runes.append([spawn_x, spawn_y, chosen_type, 0.0])


def update_buffs(dt=0.016):
    if config.overdrive_timer > 0:
        config.overdrive_timer -= 1
        config.overdrive_active = True
    else:
        config.overdrive_active = False

    if config.invincible_timer > 0:
        config.invincible_timer -= 1
        config.invincible_active = True
    else:
        config.invincible_active = False

    # --- Passive Income Logic ---
    if not hasattr(config, "passive_gold_timer"):
        config.passive_gold_timer = 0
        
    config.passive_gold_timer += 1
    if config.passive_gold_timer >= 180:
        if hasattr(config, "player_money"):
            config.player_money += 5
        if hasattr(config, "player_gold"):
            config.player_gold += 5
        config.passive_gold_timer = 0

    # --- Random World Item Spawns ---
    update_world_spawns(dt)

    # --- Wave Management Logic ---
    if len(config.enemies) == 0:
        config.wave_active = False
        if config.wave_timer > 0:
            config.wave_timer -= max(1.0, dt * 60.0)
            if config.wave_timer <= 0:
                config.wave_timer = 0
                spawn_wave(config.wave_number)
        else:
            # When an active wave is cleared, set a delay before the next wave
            if config.wave_number > 0 and len(config.enemies) == 0:
                config.wave_number += 1
                config.wave_timer = 1800.0
    else:
        config.wave_active = True