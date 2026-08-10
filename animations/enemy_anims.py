import math
import core.config as config


def get_enemy_limb_swing(walk_step):
    rad_step = math.radians(walk_step)
    swing_angle = math.sin(rad_step) * 25.0
    return swing_angle


def update_enemy_animations(dt):
    # Iterate through each active enemy
    for i in range(0, len(config.enemies), 1):
        enemy = config.enemies[i]

        # Array layout:
        # [0]: x, [1]: y, [2]: z, [3]: type, [4]: hp, [5]: walk_step, 
        # [6]: hit_flash_ticks, [7]: arm_rot, [8]: leg_rot, [9]: prev_x, [10]: prev_y, 
        # [11]: is_initialized, [12]: rot_z

        while len(enemy) < 13:
            enemy.append(0.0)

        curr_x = enemy[0]
        curr_y = enemy[1]

        # First frame initialization check to prevent spawning jumps
        if enemy[11] == 0.0:
            enemy[9] = curr_x
            enemy[10] = curr_y
            enemy[11] = 1.0

        prev_x = enemy[9]
        prev_y = enemy[10]

        # Calculate distance moved since last frame
        dx = curr_x - prev_x
        dy = curr_y - prev_y
        dist_moved = math.sqrt(dx * dx + dy * dy)

        # Update stored previous positions for the next frame
        enemy[9] = curr_x
        enemy[10] = curr_y

        # Threshold check: enemy is moving
        if dist_moved > 0.05:
            # Advance walk step based on time
            walk_speed = 360.0  # degrees per second
            enemy[5] = enemy[5] + walk_speed * dt
            if enemy[5] >= 360.0:
                enemy[5] = enemy[5] - 360.0

            # Calculate active walking swing
            swing = get_enemy_limb_swing(enemy[5])
            enemy[7] = swing  # arm_rot
            enemy[8] = swing  # leg_rot
        else:
            # Enemy is stationary: instantly reset legs and arms to standing pose
            enemy[5] = 0.0
            enemy[7] = 0.0
            enemy[8] = 0.0

        # Hit Flash Recovery Ticks
        if enemy[6] > 0:
            enemy[6] = enemy[6] - 1