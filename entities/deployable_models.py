from OpenGL.GL import *
import math


def draw_deployable_turret(x, y, level=1, angle=0.0, firing=False):
    """
    Renders the deployable magic shooter turret at given coordinates (x, y).
    Lifted slightly off the ground to completely eliminate floor z-fighting flicker.
    """
    glPushMatrix()
    glTranslatef(x, y, 2.0)  # Lifted slightly off the floor plane

    # 1. Base Plate / Pedestal (Bottom layer at local Z = 0.0)
    glBegin(GL_TRIANGLE_FAN)
    if level >= 3:
        glColor3f(0.2, 0.5, 0.8)  # Glowing blue-ish core for higher levels
    else:
        glColor3f(0.3, 0.3, 0.3)  # Standard metal base

    glVertex3f(0.0, 0.0, 0.0)
    segments = 12
    radius = 18.0 + (level * 2.0)
    
    for i in range(0, segments + 1, 1):
        seg_angle = (float(i) / float(segments)) * (2.0 * math.pi)
        vx = math.cos(seg_angle) * radius
        vy = math.sin(seg_angle) * radius
        glVertex3f(vx, vy, 0.0)
        
    glEnd()

    # Base Rim Ring (Raised clearly above the base plate at local Z = 0.5)
    glBegin(GL_LINE_LOOP)
    glColor3f(0.8, 0.8, 0.9)
    
    for i in range(0, segments + 1, 1):
        seg_angle = (float(i) / float(segments)) * (2.0 * math.pi)
        vx = math.cos(seg_angle) * radius
        vy = math.sin(seg_angle) * radius
        glVertex3f(vx, vy, 0.5)
        
    glEnd()

    # --- Rotate the Turret Head 360 Degrees Toward Target ---
    glRotatef(angle, 0.0, 0.0, 1.0)

    # 2. Central Turret Head / Core Box (Starts cleanly above the base at Z = 1.0)
    glBegin(GL_QUADS)
    color_val = 0.4 + (level * 0.08)
    glColor3f(color_val, color_val * 0.5, color_val * 1.2)

    half_w = 7.0
    base_z = 1.0
    head_height = 24.0 + (level * 3.0)

    # Bottom of head
    glVertex3f(-half_w, -half_w, base_z)
    glVertex3f(half_w, -half_w, base_z)
    glVertex3f(half_w, half_w, base_z)
    glVertex3f(-half_w, half_w, base_z)

    # Front face
    glVertex3f(-half_w, -half_w, base_z)
    glVertex3f(half_w, -half_w, base_z)
    glVertex3f(half_w, -half_w, base_z + head_height)
    glVertex3f(-half_w, -half_w, base_z + head_height)

    # Back face
    glVertex3f(-half_w, half_w, base_z)
    glVertex3f(half_w, half_w, base_z)
    glVertex3f(half_w, half_w, base_z + head_height)
    glVertex3f(-half_w, half_w, base_z + head_height)

    # Left face
    glVertex3f(-half_w, -half_w, base_z)
    glVertex3f(-half_w, half_w, base_z)
    glVertex3f(-half_w, half_w, base_z + head_height)
    glVertex3f(-half_w, -half_w, base_z + head_height)

    # Right face
    glVertex3f(half_w, -half_w, base_z)
    glVertex3f(half_w, half_w, base_z)
    glVertex3f(half_w, half_w, base_z + head_height)
    glVertex3f(half_w, -half_w, base_z + head_height)
    glEnd()

    # 3. Horizontal Turret Barrel
    barrel_len = 18.0 + (level * 2.0)
    barrel_z = base_z + (head_height * 0.65)

    glBegin(GL_QUADS)
    glColor3f(0.9, 0.9, 1.0)

    # Top face of barrel
    glVertex3f(0.0, -2.5, barrel_z + 2.5)
    glVertex3f(barrel_len, -2.5, barrel_z + 2.5)
    glVertex3f(barrel_len, 2.5, barrel_z + 2.5)
    glVertex3f(0.0, 2.5, barrel_z + 2.5)

    # Bottom face of barrel
    glVertex3f(0.0, -2.5, barrel_z - 2.5)
    glVertex3f(barrel_len, -2.5, barrel_z - 2.5)
    glVertex3f(barrel_len, 2.5, barrel_z - 2.5)
    glVertex3f(0.0, 2.5, barrel_z - 2.5)

    # Side faces of barrel
    glVertex3f(barrel_len, -2.5, barrel_z - 2.5)
    glVertex3f(barrel_len, -2.5, barrel_z + 2.5)
    glVertex3f(barrel_len, 2.5, barrel_z + 2.5)
    glVertex3f(barrel_len, 2.5, barrel_z - 2.5)
    glEnd()

    # 4. Muzzle Projectile Effect
    if firing:
        glBegin(GL_TRIANGLE_FAN)
        glColor3f(0.0, 1.0, 1.0)
        proj_x = barrel_len + 4.0
        proj_y = 0.0
        proj_z = barrel_z
        glVertex3f(proj_x, proj_y, proj_z)

        burst_segs = 6
        burst_rad = 5.0
        
        for i in range(0, burst_segs + 1, 1):
            b_angle = (float(i) / float(burst_segs)) * (2.0 * math.pi)
            bx = proj_x + math.cos(b_angle) * burst_rad
            by = proj_y + math.sin(b_angle) * burst_rad
            bz = proj_z + math.sin(b_angle) * burst_rad
            glVertex3f(bx, by, bz)
            
        glEnd()

    # 5. Level Indicator Crystals
    if level >= 2:
        glBegin(GL_TRIANGLES)
        glColor3f(0.0, 1.0, 0.8)
        crystal_offset = 9.0
        
        for ci in range(0, level, 1):
            c_angle = (float(ci) / float(level)) * (2.0 * math.pi)
            cx = math.cos(c_angle) * crystal_offset
            cy = math.sin(c_angle) * crystal_offset

            glVertex3f(cx, cy, base_z + head_height + 5.0)
            glVertex3f(cx - 2.5, cy - 2.5, base_z + head_height)
            glVertex3f(cx + 2.5, cy - 2.5, base_z + head_height)
            
        glEnd()

    glPopMatrix()