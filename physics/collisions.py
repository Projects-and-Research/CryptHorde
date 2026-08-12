import math
import animations.weapon_anims as weapon_anims
import behaviors.deployable_logic as deployable_logic
import core.config as config
import core.sound as sound
import graphics.particles as particles
import behaviors.pickup_logic as pickup_logic


def get_enemy_kill_reward(enemy_type):
    if enemy_type == "heavy":
        return 50
    elif enemy_type == "sage":
        return 40
    elif enemy_type == "archer":
        return 30
    else:
        return 20


def add_gold_to_player(amount):
    if hasattr(config, "player_money"):
        config.player_money += amount
    if hasattr(config, "player_gold"):
        config.player_gold += amount


def check_all_collisions(dt=0.016):
    check_player_projectile_enemy_collisions(dt)
    check_archer_proximity_damage_collisions()
    check_enemy_player_melee_collisions()
    check_player_hazard_collisions(dt)
    check_player_rune_collisions()
    check_shop_proximity()


def apply_aoe_damage(center_x, center_y, center_z, base_damage, exclude_idx=-1):
    aoe_radius = 60.0

    for i in range(0, len(config.enemies), 1):
        if i == exclude_idx:
            continue

        enemy = config.enemies[i]

        if enemy[4] <= 0.0:
            continue

        dx = enemy[0] - center_x
        dy = enemy[1] - center_y
        dist = math.sqrt(dx * dx + dy * dy)

        if dist <= aoe_radius:
            falloff = 1.0 - (dist / aoe_radius)
            actual_damage = base_damage * max(0.4, falloff)
            enemy[4] -= actual_damage

            if len(enemy) > 7:
                enemy[7] = 5
            elif len(enemy) > 6:
                enemy[6] = 5


def check_player_projectile_enemy_collisions(dt=0.016):
    for p_idx in range(len(config.player_projectiles) - 1, -1, -1):
        proj = config.player_projectiles[p_idx]

        vx = proj.get("vx", 0.0)
        vy = proj.get("vy", 0.0)
        vz = proj.get("vz", 0.0)

        move_dx = vx * dt
        move_dy = vy * dt
        move_dz = vz * dt
        frame_travel_dist = math.sqrt(
            move_dx * move_dx + move_dy * move_dy + move_dz * move_dz
        )

        curr_x = proj["x"]
        curr_y = proj["y"]
        curr_z = proj["z"]

        prev_x = curr_x - move_dx
        prev_y = curr_y - move_dy
        prev_z = curr_z - move_dz

        proj_radius = proj.get("radius", 10.0)
        hit = False

        sub_steps = max(1, int(math.ceil(frame_travel_dist / 4.0)))

        for step_i in range(1, sub_steps + 1, 1):
            if hit:
                break

            t = float(step_i) / float(sub_steps)
            sample_x = prev_x + (move_dx * t)
            sample_y = prev_y + (move_dy * t)
            sample_z = prev_z + (move_dz * t)

            for e_idx in range(0, len(config.enemies), 1):
                enemy = config.enemies[e_idx]

                if enemy[4] <= 0.0:
                    continue

                ex = enemy[0]
                ey = enemy[1]
                ez = enemy[2]

                enemy_type = enemy[3]
                if enemy_type == "heavy":
                    enemy_radius = 20.0
                    enemy_height = 46.0
                elif enemy_type == "sage":
                    enemy_radius = 16.0
                    enemy_height = 42.0
                elif enemy_type == "archer":
                    enemy_radius = 15.0
                    enemy_height = 40.0
                else:
                    enemy_radius = 15.0
                    enemy_height = 38.0

                dx = sample_x - ex
                dy = sample_y - ey
                horizontal_dist = math.sqrt(dx * dx + dy * dy)

                z_overlap = (ez - 10.0) <= sample_z <= (ez + enemy_height + 15.0)

                if horizontal_dist <= (proj_radius + enemy_radius) and z_overlap:
                    hit = True
                    damage = proj.get("damage", 10.0)

                    enemy[4] -= damage

                    if len(enemy) > 7:
                        enemy[7] = 5
                    elif len(enemy) > 6:
                        enemy[6] = 5

                    particles.create_particle(
                        sample_x,
                        sample_y,
                        sample_z,
                        0.0,
                        0.0,
                        1.0,
                        (1.0, 0.2, 0.2),
                        size=3.0,
                        life=10,
                    )

                    if proj.get("is_aoe", False):
                        apply_aoe_damage(sample_x, sample_y, sample_z, damage, exclude_idx=e_idx)
                        particles.spawn_aoe_ring(sample_x, sample_y, sample_z)

                    break

        if hit:
            config.player_projectiles.pop(p_idx)

    for i in range(len(config.enemies) - 1, -1, -1):
        if config.enemies[i][4] <= 0.0:
            enemy_type = config.enemies[i][3]
            reward = get_enemy_kill_reward(enemy_type)

            config.enemies.pop(i)
            config.score += 100
            config.game_score = config.score
            config.enemies_remaining = len(config.enemies)

            add_gold_to_player(reward)

            config.player_mana = min(
                config.max_mana, config.player_mana + 2
            )


def check_archer_proximity_damage_collisions():
    for i in range(0, len(config.enemies), 1):
        enemy = config.enemies[i]
        
        if enemy[4] <= 0.0:
            continue
        
        enemy_type = enemy[3]
        if enemy_type != "archer":
            continue

        dx = config.player_x - enemy[0]
        dy = config.player_y - enemy[1]
        dist = math.sqrt(dx * dx + dy * dy)

        if dist <= 150.0:
            while len(enemy) <= 6:
                enemy.append(0)

            if enemy[6] <= 0:
                if not config.invincible_active:
                    config.player_health -= 15.0
                    sound.play_hit_sound()

                    if config.player_health <= 0.0:
                        config.player_health = 0.0
                        config.current_state = config.STATE_GAME_OVER

                enemy[6] = 180

        if len(enemy) > 6 and enemy[6] > 0:
            enemy[6] -= 1


def check_enemy_player_melee_collisions():
    for i in range(0, len(config.enemies), 1):
        enemy = config.enemies[i]
        if enemy[4] <= 0.0:
            continue

        if enemy[3] == "archer":
            continue

        dx = config.player_x - enemy[0]
        dy = config.player_y - enemy[1]
        dist = math.sqrt(dx * dx + dy * dy)

        if dist < 25.0:
            if not config.invincible_active:
                while len(enemy) <= 6:
                    enemy.append(0)

                if enemy[6] <= 0:
                    config.player_health -= 5.0
                    sound.play_hit_sound()
                    enemy[6] = 60

                    if config.player_health <= 0.0:
                        config.player_health = 0.0
                        config.current_state = config.STATE_GAME_OVER
            
            if len(enemy) > 6 and enemy[6] > 0:
                enemy[6] -= 1


def check_player_hazard_collisions(dt=0.016):
    # 1. Spiked Floor Trap Collisions
    hazards_list = getattr(config, "hazards", [])
    if not hazards_list:
        hazards_list = [
            {"x": 150.0, "y": 150.0},
            {"x": -150.0, "y": 150.0},
            {"x": 150.0, "y": -150.0},
            {"x": -150.0, "y": -150.0},
            {"x": 0.0, "y": 350.0},
            {"x": 0.0, "y": -350.0}
        ]
        config.hazards = hazards_list

    spikes_active = getattr(config, "hazard_spikes_active", True)

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

        if dist < 30.0 and spikes_active:
            if not config.invincible_active:
                if config.trap_cooldowns.get(i, 0.0) <= 0.0:
                    config.player_health -= 15.0
                    config.player_mana = max(0.0, config.player_mana - 10.0)
                    sound.play_hit_sound()
                    config.trap_cooldowns[i] = 1.0

                    if config.player_health <= 0.0:
                        config.player_health = 0.0
                        config.current_state = config.STATE_GAME_OVER

        i += 1

    # 2. Rotating Magic Beam Collisions (Fixed: Only damage when aligned with the beam's angle)
    beams_list = getattr(config, "beams", [])
    if not beams_list:
        beams_list = [
            {"x": 300.0, "y": 100.0},
            {"x": -300.0, "y": -100.0},
            {"x": 100.0, "y": 300.0},
            {"x": -100.0, "y": -300.0}
        ]
        config.beams = beams_list

    current_beam_angle = getattr(config, "beam_rotation_angle", 0.0)

    b_idx = 0
    while b_idx < len(beams_list):
        beam = beams_list[b_idx]
        bx = beam["x"]
        by = beam["y"]

        dx = config.player_x - bx
        dy = config.player_y - by
        dist_from_pillar = math.sqrt(dx * dx + dy * dy)

        # Beam extends outward between radius 10.0 and 55.0 from the pillar center
        if 10.0 <= dist_from_pillar <= 55.0:
            player_angle = math.degrees(math.atan2(dy, dx)) % 360.0
            normalized_beam_angle = current_beam_angle % 360.0

            angle_diff = abs((player_angle - normalized_beam_angle + 180.0) % 360.0 - 180.0)

            # Only hit if the player's angle precisely matches the beam sweep line (within 8 degrees)
            if angle_diff <= 8.0:
                if not config.invincible_active:
                    config.player_health -= 20.0 * dt
                    config.player_mana = max(0.0, config.player_mana - 15.0 * dt)
                    
                    if config.player_health <= 0.0:
                        config.player_health = 0.0
                        config.current_state = config.STATE_GAME_OVER

        b_idx += 1


def check_player_rune_collisions():
    """
    Checks distance between player and active runes/pickups.
    If collected, applies the appropriate buff/stat and removes the rune.
    """
    if not hasattr(config, "runes") or not config.runes:
        return

    player_x = getattr(config, "player_x", 0.0)
    player_y = getattr(config, "player_y", 0.0)
    
    # Interaction radius for picking up items
    pickup_radius = 25.0 

    remaining_runes = []
    for rune in config.runes:
        rx, ry = rune[0], rune[1]
        rtype = rune[2]

        dx = rx - player_x
        dy = ry - player_y
        dist = math.sqrt(dx * dx + dy * dy)

        if dist < pickup_radius:
            # Player collected this rune! Apply effect:
            pickup_logic.apply_pickup_effect(rune)  
            
            # Skip adding it back to remaining_runes (effectively removing it)
            continue
        
        remaining_runes.append(rune)

    config.runes = remaining_runes
    config.pickups = config.runes  # Keep synced if other systems look at pickups


def check_shop_proximity():
    shop_zones = [
        {"x": 200.0, "y": 200.0, "radius": 45.0},
        {"x": -200.0, "y": -200.0, "radius": 45.0},
    ]

    config.near_shop = False

    for i in range(0, len(shop_zones), 1):
        shop = shop_zones[i]
        dx = config.player_x - shop["x"]
        dy = config.player_y - shop["y"]
        dist = math.sqrt(dx * dx + dy * dy)

        if dist <= shop["radius"]:
            config.near_shop = True
            break