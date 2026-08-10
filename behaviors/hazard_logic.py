import math
import core.config as config
import core.sound as sound


def update_hazards(dt=0.016):
    # --- 1. Spiked Floor Trap Logic ---
    spikes_active = getattr(config, "hazard_spikes_active", False)
    
    # Safely retrieve hazards list from config if defined dynamically
    hazards_list = getattr(config, "hazards", [])

    if not hasattr(config, "trap_cooldowns"):
        config.trap_cooldowns = {}

    i = 0
    while i < len(hazards_list):
        trap = hazards_list[i]
        tx = trap["x"]
        ty = trap["y"]

        dx = config.player_x - tx
        dy = config.player_y - ty
        dist = math.sqrt(dx * dx + dy * dy)

        current_cooldown = config.trap_cooldowns.get(i, 0.0)
        if current_cooldown > 0.0:
            config.trap_cooldowns[i] = current_cooldown - dt

        if dist < 15.0 and config.player_z <= 5.0 and spikes_active:
            if not getattr(config, "invincible_active", False) and getattr(config, "invincible_timer", 0.0) <= 0.0:
                if config.trap_cooldowns.get(i, 0.0) <= 0.0:
                    config.player_health -= 15.0
                    config.player_mana = max(0.0, config.player_mana - 10.0)
                    sound.play_hit_sound()
                    config.trap_cooldowns[i] = 1.0

                    if config.player_health <= 0.0:
                        config.player_health = 0.0
                        config.current_state = config.STATE_GAME_OVER

        i += 1

    # --- 2. Rotating Magic Beam Logic ---
    beams_list = getattr(config, "beams", [])
    current_beam_angle = getattr(config, "beam_rotation_angle", 0.0)

    b_idx = 0
    while b_idx < len(beams_list):
        beam = beams_list[b_idx]
        bx = beam["x"]
        by = beam["y"]

        dx = config.player_x - bx
        dy = config.player_y - by
        dist_from_pillar = math.sqrt(dx * dx + dy * dy)

        if 4.0 <= dist_from_pillar <= 45.0 and config.player_z <= 70.0:
            player_angle = math.degrees(math.atan2(dy, dx)) % 360.0
            normalized_beam_angle = current_beam_angle % 360.0

            angle_diff = abs((player_angle - normalized_beam_angle + 180.0) % 360.0 - 180.0)

            if angle_diff <= 15.0:
                if not getattr(config, "invincible_active", False) and getattr(config, "invincible_timer", 0.0) <= 0.0:
                    config.player_health -= 20.0 * dt
                    config.player_mana = max(0.0, config.player_mana - 15.0 * dt)

                    if config.player_health <= 0.0:
                        config.player_health = 0.0
                        config.current_state = config.STATE_GAME_OVER

        b_idx += 1

    # --- 3. Enemy Collision with Spiked Floor Traps ---
    enemies_list = getattr(config, "enemies", [])
    e_idx = 0
    while e_idx < len(enemies_list):
        enemy = enemies_list[e_idx]

        if enemy[4] <= 0.0:
            e_idx += 1
            continue

        h_idx = 0
        while h_idx < len(hazards_list):
            trap = hazards_list[h_idx]

            dx = enemy[0] - trap["x"]
            dy = enemy[1] - trap["y"]
            dist = math.sqrt(dx * dx + dy * dy)

            if dist < 8.0 and spikes_active:
                enemy[4] -= 0.5  # Constant ticking damage to enemies walking on traps

            h_idx += 1

        e_idx += 1