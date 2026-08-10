import core.config as config


def apply_pickup_effect(pickup):
    """
    Applies the effect of a collected rune.
    Expected rune list format: [x, y, type_string, float_offset_val]
    """
    if not pickup or len(pickup) < 3:
        return

    # Index 2 holds the type string ("health", "mana", "invincible")
    p_type = pickup[2]

    if p_type == "health":
        config.player_health = min(config.max_health, config.player_health + 30.0)

    elif p_type == "mana":
        config.player_mana = min(config.max_mana, config.player_mana + 40.0)

    elif p_type in ["invincible", "invincibility"]:
        # 30 seconds at 60 FPS = 1800 frames
        config.invincible_timer = 1800
        config.invincible_active = True


def update_pickups():
    # Update active invincibility timer
    if config.invincible_timer > 0:
        config.invincible_timer -= 1
        if config.invincible_timer <= 0:
            config.invincible_active = False