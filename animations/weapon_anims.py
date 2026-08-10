import math
import core.config as config


def update_weapon_animations():
    # Recovery for Recoil (backward, positive offset) or Thrust (forward, negative offset)
    if config.recoil_offset > 0.0:
        config.recoil_offset -= 0.5
        if config.recoil_offset < 0.0:
            config.recoil_offset = 0.0

    elif config.recoil_offset < 0.0:
        config.recoil_offset += 0.5
        if config.recoil_offset > 0.0:
            config.recoil_offset = 0.0

    # Handle Reload / Swap lowering animation
    if config.reload_timer > 0:
        config.reload_timer -= 1

        # When reload timer finally counts down to 0, make the crossbow ready to fire again
        if config.reload_timer == 0:
            config.crossbow_ready = True

        # Slightly lower weapon down vertically during reload (stays on screen)
        min_offset = -2.0  # Kept shallow so weapon remains visible on screen
        if config.weapon_y_offset > min_offset:
            config.weapon_y_offset -= 0.2
            if config.weapon_y_offset < min_offset:
                config.weapon_y_offset = min_offset
    else:
        # Smoothly return weapon back up to default view position
        if config.weapon_y_offset < 0.0:
            config.weapon_y_offset += 0.2
            if config.weapon_y_offset > 0.0:
                config.weapon_y_offset = 0.0

    # View bobbing is handled exclusively by animations/view_bob.py now - this file used to
    # have its own duplicate copy of that logic here, which ran immediately after view_bob.py
    # every frame and stomped its result back to 0.0, which was the actual cause of the bob
    # never showing up no matter what view_bob.py did.


def trigger_recoil(amount=3.0):
    # Recoil pushes weapon backward (Crossbow & Bow)
    config.recoil_offset = amount


def trigger_thrust(amount=4.0):
    # Forward thrust for magic release (Arcane Staff & Magic Hand)
    config.recoil_offset = -amount


def trigger_reload(duration_ticks=40):
    config.reload_timer = duration_ticks
    # Manually triggering reload via 'R' forces the crossbow ready state after duration
    if duration_ticks >= 180:
        config.crossbow_ready = False  # Keep unready until the 3-second reload finishes


def update_animations():
    update_weapon_animations()