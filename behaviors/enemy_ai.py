import math
import core.config as config
import entities.projectile_models as projectile_models


def update_enemy_ai(dt):
    i = 0
    while i < len(config.enemies):
        enemy = config.enemies[i]

        # Array layout check to ensure rotation index [12] exists
        while len(enemy) < 13:
            enemy.append(0.0)

        dx = config.player_x - enemy[0]
        dy = config.player_y - enemy[1]
        dist_to_player = math.sqrt(dx * dx + dy * dy)

        e_type = enemy[3]

        # Base Movement Speeds (Units per Second) & Stopping Distances
        if e_type == "archer":
            speed = 60.0
            stop_dist = 120.0  # Keeps distance to shoot arrows
        elif e_type == "heavy":
            speed = 35.0
            stop_dist = 5.0
        elif e_type == "sage":
            speed = 50.0
            stop_dist = 150.0  # Keeps range to support/heal allies
        else:  # Regular enemy
            speed = 85.0
            stop_dist = 5.0

        # Face towards player angle (in degrees)
        angle_to_player = math.degrees(math.atan2(dy, dx))

        # Move towards player if outside minimum stopping distance
        if dist_to_player > stop_dist:
            dir_x = dx / dist_to_player
            dir_y = dy / dist_to_player

            enemy[0] += dir_x * speed * dt
            enemy[1] += dir_y * speed * dt

            # Update orientation while moving
            enemy[12] = angle_to_player
        else:
            # Always face the player when stopped (especially archers shooting)
            enemy[12] = angle_to_player

        # Handle Enemy Actions & Cooldowns
        cooldown_idx = 5
        if len(enemy) > cooldown_idx:
            if enemy[cooldown_idx] > 0:
                enemy[cooldown_idx] -= 1.0 * (dt * 60.0)  # Scale frame cooldown drops by dt
            else:
                # 1. Archer Attack: Fires arrows into enemy_arrows
                if e_type == "archer" and dist_to_player <= 180.0:
                    attack_angle = math.degrees(math.atan2(dy, dx))
                    
                    # Calculate velocity components for the arrow
                    rad_angle = math.radians(attack_angle)
                    arrow_speed = 350.0  # Units per second
                    vx = math.cos(rad_angle) * arrow_speed
                    vy = math.sin(rad_angle) * arrow_speed
                    vz = 0.0

                    arrow = {
                        "x": enemy[0],
                        "y": enemy[1],
                        "z": enemy[2] + 10.0,
                        "vx": vx,
                        "vy": vy,
                        "vz": vz,
                        "damage": 10.0,
                        "life": 120.0
                    }
                    config.enemy_arrows.append(arrow)
                    enemy[cooldown_idx] = 90.0  # Reload cooldown frames

                # 2. Sage Ability: Heals and buffs surrounding enemies in an aura radius
                elif e_type == "sage":
                    j = 0
                    while j < len(config.enemies):
                        ally = config.enemies[j]
                        if i != j:
                            adx = ally[0] - enemy[0]
                            ady = ally[1] - enemy[1]
                            adist = math.sqrt(adx * adx + ady * ady)

                            # If ally is within Sage heal/buff aura radius
                            if adist <= config.sage_heal_radius:
                                # Heal ally HP up to a cap (assuming HP is at index 4)
                                if len(ally) > 4:
                                    ally[4] = min(100.0, ally[4] + 5.0)
                        j += 1

                    enemy[cooldown_idx] = 120.0  # Aura pulse cooldown frames

        # Simple Separation Logic (prevent enemies from stacking on each other)
        j = 0
        while j < len(config.enemies):
            if i != j:
                other = config.enemies[j]
                sep_dx = enemy[0] - other[0]
                sep_dy = enemy[1] - other[1]
                sep_dist = math.sqrt(sep_dx * sep_dx + sep_dy * sep_dy)

                if sep_dist < 10.0 and sep_dist > 0.0:
                    enemy[0] += (sep_dx / sep_dist) * 25.0 * dt
                    enemy[1] += (sep_dy / sep_dist) * 25.0 * dt
            j += 1

        i += 1


# Alias to support both function name conventions if called elsewhere
def update_enemies(dt):
    update_enemy_ai(dt)