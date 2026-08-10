import math
import core.config as config


def update_projectiles_animation(dt):
    # Scale movement to target 60 FPS standard
    time_scale = dt * 60.0

    # Loop backward through player bullets for safe removal
    for i in range(len(config.bullets) - 1, -1, -1):
        proj = config.bullets[i]

        # Translate position using velocity vector scaled by dt
        proj["x"] = proj["x"] + (proj["vx"] * time_scale)
        proj["y"] = proj["y"] + (proj["vy"] * time_scale)
        proj["z"] = proj["z"] + (proj["vz"] * time_scale)

        # Decay lifetime
        proj["life"] = proj["life"] - 1

        # Check arena boundaries
        out_of_bounds = False
        if proj["x"] > config.BOUND_LIMIT or proj["x"] < -config.BOUND_LIMIT:
            out_of_bounds = True
        if proj["y"] > config.BOUND_LIMIT or proj["y"] < -config.BOUND_LIMIT:
            out_of_bounds = True

        # Check vertical limits or expired lifetime
        if proj["z"] < 0.0 or proj["z"] > 200.0 or proj["life"] <= 0 or out_of_bounds:
            config.bullets.pop(i)

    # Loop backward through enemy arrows
    for i in range(len(config.enemy_arrows) - 1, -1, -1):
        e_proj = config.enemy_arrows[i]

        # Translate position using velocity vector scaled by dt
        e_proj["x"] = e_proj["x"] + (e_proj["vx"] * time_scale)
        e_proj["y"] = e_proj["y"] + (e_proj["vy"] * time_scale)
        e_proj["z"] = e_proj["z"] + (e_proj["vz"] * time_scale)

        e_proj["life"] = e_proj["life"] - 1

        # Boundary checks for enemy arrows
        out_of_bounds = False
        if e_proj["x"] > config.BOUND_LIMIT or e_proj["x"] < -config.BOUND_LIMIT:
            out_of_bounds = True
        if e_proj["y"] > config.BOUND_LIMIT or e_proj["y"] < -config.BOUND_LIMIT:
            out_of_bounds = True

        if e_proj["z"] < 0.0 or e_proj["z"] > 200.0 or e_proj["life"] <= 0 or out_of_bounds:
            config.enemy_arrows.pop(i)


def update_projectiles(dt):
    update_projectiles_animation(dt)