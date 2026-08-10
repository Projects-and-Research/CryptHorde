from OpenGL.GL import *
from OpenGL.GLU import *
import math
import core.config as config


def setup_fps_camera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    # Dynamic aspect ratio based on your 1280x720 window resolution (16:9 ratio)
    aspect_ratio = 1280.0 / 720.0
    gluPerspective(90.0, aspect_ratio, 0.1, 2500.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Convert angles from degrees to radians
    rad_yaw = math.radians(config.player_angle)
    rad_pitch = math.radians(config.player_pitch)

    # Calculate 3D facing direction vector using spherical coordinates
    dir_x = math.cos(rad_yaw) * math.cos(rad_pitch)
    dir_y = math.sin(rad_yaw) * math.cos(rad_pitch)
    dir_z = math.sin(rad_pitch)

    # Eye position including view bobbing height offset
    eye_x = config.player_x
    eye_y = config.player_y
    eye_z = config.eye_z + config.view_bob

    # Target look-at point projected 100 units ahead along the facing vector
    target_x = eye_x + dir_x * 100.0
    target_y = eye_y + dir_y * 100.0
    target_z = eye_z + dir_z * 100.0

    # Store looking directional vector for projectile mechanics
    config.dir_x = dir_x
    config.dir_y = dir_y
    config.dir_z = dir_z

    # Apply First-Person view matrix
    gluLookAt(
        eye_x, eye_y, eye_z,
        target_x, target_y, target_z,
        0.0, 0.0, 1.0
    )