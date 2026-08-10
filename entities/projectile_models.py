from OpenGL.GL import *
from OpenGL.GLU import *
import math
import core.config as config


def create_projectile(x, y, z, angle, pitch, speed, damage, p_type, radius=3.0, is_aoe=False):
    rad_angle = math.radians(angle)
    rad_pitch = math.radians(pitch)

    # Direction vectors derived from player camera angles
    vx = math.cos(rad_angle) * math.cos(rad_pitch) * speed
    vy = math.sin(rad_angle) * math.cos(rad_pitch) * speed
    vz = math.sin(rad_pitch) * speed

    proj = {
        "x": x,
        "y": y,
        "z": z,
        "vx": vx,
        "vy": vy,
        "vz": vz,
        "damage": damage,
        "type": p_type,
        "radius": radius,
        "is_aoe": is_aoe,
        "life": 120  # Max frames before auto-despawn
    }

    # Register to global player projectile container
    config.player_projectiles.append(proj)
    if config.bullets != config.player_projectiles:
        config.bullets = config.player_projectiles


def draw_projectile_model(proj):
    glPushMatrix()
    glTranslatef(proj["x"], proj["y"], proj["z"])

    # Align rotation with the projectile's movement trajectory vectors (vx, vy, vz)
    speed_xy = math.sqrt(proj["vx"]**2 + proj["vy"]**2)
    yaw_deg = math.degrees(math.atan2(proj["vy"], proj["vx"]))
    pitch_deg = math.degrees(math.atan2(proj["vz"], speed_xy if speed_xy != 0 else 0.001))

    glRotatef(yaw_deg, 0.0, 0.0, 1.0)
    glRotatef(pitch_deg, 0.0, 1.0, 0.0)

    # Safely retrieve projectile type, defaulting to "arrow" for enemy arrows or untyped dicts
    proj_type = proj.get("type", "arrow")

    # 1. Arcane Staff Ball / Magic Hand Energy
    if proj_type == "magic_ball" or proj_type == "magic_hand":
        if proj_type == "magic_ball":
            glColor3f(0.6, 0.2, 1.0)  # Purple
        else:
            glColor3f(0.2, 0.8, 1.0)  # Cyan/Blue

        radius = proj.get("radius", 4.0)
        quad = gluNewQuadric()
        gluSphere(quad, radius, 10, 10)

    # 2. Crossbow Bolt / Generic Bolt
    elif proj_type == "bolt":
        glColor3f(0.7, 0.7, 0.7)  # Metallic Gray

        # Scale into an elongated bolt/rod shape
        glPushMatrix()
        glScalef(1.5, 0.3, 0.3)

        # Simple 3D Box for bolt body
        glBegin(GL_QUADS)
        # Front
        glVertex3f(-2.0, -1.0, 1.0)
        glVertex3f(2.0, -1.0, 1.0)
        glVertex3f(2.0, 1.0, 1.0)
        glVertex3f(-2.0, 1.0, 1.0)
        # Back
        glVertex3f(-2.0, -1.0, -1.0)
        glVertex3f(-2.0, 1.0, -1.0)
        glVertex3f(2.0, 1.0, -1.0)
        glVertex3f(2.0, -1.0, -1.0)
        # Top
        glVertex3f(-2.0, 1.0, -1.0)
        glVertex3f(-2.0, 1.0, 1.0)
        glVertex3f(2.0, 1.0, 1.0)
        glVertex3f(2.0, 1.0, -1.0)
        # Bottom
        glVertex3f(-2.0, -1.0, -1.0)
        glVertex3f(2.0, -1.0, -1.0)
        glVertex3f(2.0, -1.0, 1.0)
        glVertex3f(-2.0, -1.0, 1.0)
        glEnd()
        glPopMatrix()

    # 3. Bow Arrow / Enemy Arrow
    elif proj_type == "arrow":
        glColor3f(0.5, 0.35, 0.05)  # Wooden Shaft

        # Arrow shaft
        quad = gluNewQuadric()
        gluCylinder(quad, 0.5, 0.5, 6.0, 8, 1)

        # Arrow tip
        glColor3f(0.8, 0.8, 0.8)
        glPushMatrix()
        glTranslatef(0.0, 0.0, 6.0)
        gluCylinder(quad, 1.0, 0.0, 2.0, 8, 1)
        glPopMatrix()

    glPopMatrix()