import math
import core.config as config
import core.sound as sound
import entities.deployable_models as deployable_models


def init_deployables():
    """Initializes deployable storage and properties in config."""
    if not hasattr(config, "deployables"):
        config.deployables = []  # List of dicts: {'x': x, 'y': y, 'level': 1, 'shoot_timer': 0.0, 'angle': 0.0}
        
    if not hasattr(config, "max_deployables"):
        config.max_deployables = 1  # Starts at 1, can be increased to 2 via shop


def place_deployable():
    """Deploys a turret at the player's current position if within limits."""
    init_deployables()

    current_count = len(config.deployables)
    max_allowed = getattr(config, "max_deployables", 1)

    if current_count >= max_allowed:
        config.deployable_message = "Max turrets reached!"
        config.deployable_message_type = "error"
        config.deployable_message_timer = 120
        return  # Max limit reached for current deployment

    rad = math.radians(config.player_angle)
    spawn_dist = 40.0
    spawn_x = config.player_x + math.cos(rad) * spawn_dist
    spawn_y = config.player_y + math.sin(rad) * spawn_dist

    turret_level = getattr(config, "deployable_level", 1)

    new_turret = {
        "x": spawn_x,
        "y": spawn_y,
        "level": turret_level,
        "shoot_timer": 0.0,
        "angle": config.player_angle
    }

    config.deployables.append(new_turret)
    config.deployable_message = "Turret deployed successfully!"
    config.deployable_message_type = "success"
    config.deployable_message_timer = 120
    sound.play_sound("deployable_deploy.mp3")


def remove_nearest_deployable():
    """Removes the nearest turret if the player is close, otherwise attempts to place a new one."""
    init_deployables()
    
    deployables = config.deployables
    
    if len(deployables) == 0:
        place_deployable()
        return

    player_x = config.player_x
    player_y = config.player_y
    
    closest_index = -1
    min_dist = 999999.0

    for i in range(0, len(deployables), 1):
        t = deployables[i]
        dist = math.sqrt((t["x"] - player_x) ** 2 + (t["y"] - player_y) ** 2)
        
        if dist < min_dist:
            min_dist = dist
            closest_index = i


    if min_dist <= 50.0 and closest_index != -1:
        deployables.pop(closest_index)
        config.deployable_message = "Turret removed and retrieved!"
        config.deployable_message_type = "success"
        config.deployable_message_timer = 120
        sound.play_sound("deployable_deploy.mp3")
    else:
        place_deployable()


def update_deployables(dt):
    init_deployables()
    
    # Check proximity to any deployable for the HUD prompt
    config.near_deployable = False
    player_x = getattr(config, "player_x", 0.0)
    player_y = getattr(config, "player_y", 0.0)
    interaction_radius = 50.0  # Matches the removal distance threshold

    for i in range(0, len(config.deployables), 1):
        turret = config.deployables[i]
        dist = math.sqrt((turret["x"] - player_x) ** 2 + (turret["y"] - player_y) ** 2)
        if dist <= interaction_radius:
            config.near_deployable = True
            break

    if not config.deployables:
        return

    enemies = getattr(config, "enemies", [])

    for i in range(0, len(config.deployables), 1):
        turret = config.deployables[i]
        level = turret["level"]
        cooldown_max = max(1.0, 5.0 - (level - 1) * 0.6)

        turret["shoot_timer"] += dt
        
        # Reset firing visual flag each frame unless it shoots below
        turret["firing"] = False

        target = None
        min_dist = 300.0

        for j in range(0, len(enemies), 1):
            enemy = enemies[j]
            ex = enemy[0]
            ey = enemy[1]
            e_hp = enemy[4]

            if e_hp <= 0:
                continue

            dist = math.hypot(ex - turret["x"], ey - turret["y"])
            if dist < min_dist:
                min_dist = dist
                target = enemy

        if target is not None:
            ex = target[0]
            ey = target[1]
            dx = ex - turret["x"]
            dy = ey - turret["y"]
            turret["angle"] = math.degrees(math.atan2(dy, dx))

        if turret["shoot_timer"] >= cooldown_max:
            turret["shoot_timer"] = 0.0

            if target is not None:
                damage = 30.0 + (level - 1) * 10.0
                target[4] -= damage
                turret["firing"] = True  # Trigger muzzle projectile animation frame
                sound.play_sound("deployable_fire.mp3")


def render_deployables():
    init_deployables()

    for i in range(0, len(config.deployables), 1):
        turret = config.deployables[i]
        
        deployable_models.draw_deployable_turret(
            turret["x"],
            turret["y"],
            level=turret["level"],
            angle=turret.get("angle", 0.0),
            firing=turret.get("firing", False)
        )