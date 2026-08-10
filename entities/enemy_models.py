from OpenGL.GL import *
from OpenGL.GLU import *
import math
import core.config as config


def draw_sage_aura_ring():
    radius = getattr(config, "sage_heal_radius", 120.0)

    glDisable(GL_LIGHTING)
    glColor3f(0.8, 0.2, 1.0)

    glLineWidth(2.5)
    glBegin(GL_LINE_LOOP)
    for i in range(0, 36, 1):
        angle = 2.0 * math.pi * float(i) / 36.0
        rx = radius * math.cos(angle)
        ry = radius * math.sin(angle)
        glVertex3f(rx, ry, 0.5)
    glEnd()
    glLineWidth(1.0)


def draw_bow(quad):
    glPushMatrix()
    
    # Stand the bow upright vertically
    glRotatef(90.0, 1.0, 0.0, 0.0)

    # 1. BOW FRAME (3 Wood Line Segments)
    glColor3f(0.5, 0.25, 0.0)  # Brown Wood Color
    glLineWidth(3.0)

    # Y offsets control the curve depth facing away/toward the body:
    top_tip_y, top_tip_z = -3.0, 8.0
    top_joint_y, top_joint_z = 0.0, 4.0
    bot_joint_y, bot_joint_z = 0.0, -4.0
    bot_tip_y, bot_tip_z = -3.0, -8.0

    glBegin(GL_LINES)
    # Segment 1: Upper Angled Limb
    glVertex3f(0.0, top_joint_y, top_joint_z)
    glVertex3f(0.0, top_tip_y, top_tip_z)

    # Segment 2: Middle Straight Handle
    glVertex3f(0.0, top_joint_y, top_joint_z)
    glVertex3f(0.0, bot_joint_y, bot_joint_z)

    # Segment 3: Lower Angled Limb
    glVertex3f(0.0, bot_joint_y, bot_joint_z)
    glVertex3f(0.0, bot_tip_y, bot_tip_z)
    glEnd()

    # 2. BOW STRING (1 Straight White Line facing the archer)
    glColor3f(0.9, 0.9, 0.9)  # White String Color
    glLineWidth(1.5)

    glBegin(GL_LINES)
    glVertex3f(0.0, top_tip_y, top_tip_z)
    glVertex3f(0.0, bot_tip_y, bot_tip_z)
    glEnd()

    # Reset OpenGL render states
    glLineWidth(1.0)

    glPopMatrix()


def draw_limbs(quad, arm_rot, leg_rot, shoulder_x, shoulder_z, hip_x, hip_z, body_color, skin_color, is_archer=False):
    # Left Leg (Forward Swing)
    glColor3f(body_color[0] * 0.7, body_color[1] * 0.7, body_color[2] * 0.7)
    glPushMatrix()
    glTranslatef(-hip_x, 0.0, hip_z)
    glRotatef(leg_rot, 1.0, 0.0, 0.0)
    glRotatef(180.0, 1.0, 0.0, 0.0)
    gluCylinder(quad, 1.4, 1.0, 13.0, 8, 8)
    glPopMatrix()

    # Right Leg (Backward Swing)
    glPushMatrix()
    glTranslatef(hip_x, 0.0, hip_z)
    glRotatef(-leg_rot, 1.0, 0.0, 0.0)
    glRotatef(180.0, 1.0, 0.0, 0.0)
    gluCylinder(quad, 1.4, 1.0, 13.0, 8, 8)
    glPopMatrix()

    if is_archer:
        # Left Arm Holding Bow
        glColor3f(body_color[0], body_color[1], body_color[2])
        glPushMatrix()
        glTranslatef(-shoulder_x, 0.0, shoulder_z)
        glRotatef(85.0, 1.0, 0.0, 0.0)
        gluCylinder(quad, 1.1, 0.9, 12.0, 8, 8)

        glColor3f(skin_color[0], skin_color[1], skin_color[2])
        glPushMatrix()
        glTranslatef(0.0, 0.0, 12.0)
        gluSphere(quad, 1.3, 8, 8)
        draw_bow(quad)
        glPopMatrix()
        glPopMatrix()

        # Right Arm Bent Backwards
        glColor3f(body_color[0], body_color[1], body_color[2])
        glPushMatrix()
        glTranslatef(shoulder_x, 0.0, shoulder_z)
        glRotatef(45.0, 1.0, 0.0, 0.0)
        gluCylinder(quad, 1.1, 0.9, 10.0, 8, 8)

        glColor3f(skin_color[0], skin_color[1], skin_color[2])
        glPushMatrix()
        glTranslatef(0.0, 0.0, 10.0)
        gluSphere(quad, 1.3, 8, 8)
        glPopMatrix()
        glPopMatrix()

    else:
        # Left Arm
        glColor3f(body_color[0], body_color[1], body_color[2])
        glPushMatrix()
        glTranslatef(-shoulder_x, 0.0, shoulder_z)
        glRotatef(-arm_rot, 1.0, 0.0, 0.0)
        glRotatef(180.0, 1.0, 0.0, 0.0)
        gluCylinder(quad, 1.1, 0.9, 12.0, 8, 8)

        glColor3f(skin_color[0], skin_color[1], skin_color[2])
        glPushMatrix()
        glTranslatef(0.0, 0.0, 12.0)
        gluSphere(quad, 1.3, 8, 8)
        glPopMatrix()
        glPopMatrix()

        # Right Arm
        glColor3f(body_color[0], body_color[1], body_color[2])
        glPushMatrix()
        glTranslatef(shoulder_x, 0.0, shoulder_z)
        glRotatef(arm_rot, 1.0, 0.0, 0.0)
        glRotatef(180.0, 1.0, 0.0, 0.0)
        gluCylinder(quad, 1.1, 0.9, 12.0, 8, 8)

        glColor3f(skin_color[0], skin_color[1], skin_color[2])
        glPushMatrix()
        glTranslatef(0.0, 0.0, 12.0)
        gluSphere(quad, 1.3, 8, 8)
        glPopMatrix()
        glPopMatrix()


def draw_archer_enemy(arm_rot=0.0, leg_rot=0.0):
    quad = gluNewQuadric()

    glColor3f(0.1, 0.6, 0.2)
    glPushMatrix()
    glTranslatef(0.0, 0.0, 13.0)
    gluCylinder(quad, 3.2, 2.6, 17.0, 10, 10)
    glPopMatrix()

    glColor3f(0.8, 0.7, 0.5)
    glPushMatrix()
    glTranslatef(0.0, 0.0, 32.0)
    gluSphere(quad, 3.2, 10, 10)
    glPopMatrix()

    draw_limbs(quad, arm_rot, leg_rot, 4.0, 27.0, 1.8, 13.0, (0.1, 0.6, 0.2), (0.8, 0.7, 0.5), is_archer=True)


def draw_regular_enemy(arm_rot=0.0, leg_rot=0.0):
    quad = gluNewQuadric()

    glColor3f(0.8, 0.2, 0.2)
    glPushMatrix()
    glTranslatef(0.0, 0.0, 13.0)
    gluCylinder(quad, 4.0, 3.0, 18.0, 10, 10)
    glPopMatrix()

    glColor3f(0.9, 0.7, 0.5)
    glPushMatrix()
    glTranslatef(0.0, 0.0, 33.0)
    gluSphere(quad, 3.8, 10, 10)
    glPopMatrix()

    draw_limbs(quad, arm_rot, leg_rot, 4.8, 28.0, 2.0, 13.0, (0.8, 0.2, 0.2), (0.9, 0.7, 0.5))


def draw_heavy_enemy(arm_rot=0.0, leg_rot=0.0):
    quad = gluNewQuadric()

    glColor3f(0.3, 0.3, 0.35)
    glPushMatrix()
    glTranslatef(0.0, 0.0, 14.0)
    gluCylinder(quad, 6.0, 5.0, 20.0, 12, 12)
    glPopMatrix()

    glColor3f(0.2, 0.2, 0.2)
    glPushMatrix()
    glTranslatef(0.0, 0.0, 36.0)
    gluSphere(quad, 5.0, 12, 12)
    glPopMatrix()

    draw_limbs(quad, arm_rot, leg_rot, 7.0, 31.0, 3.0, 14.0, (0.3, 0.3, 0.35), (0.2, 0.2, 0.2))


def draw_sage_enemy(arm_rot=0.0, leg_rot=0.0):
    quad = gluNewQuadric()

    glColor3f(0.5, 0.1, 0.7)
    glPushMatrix()
    glTranslatef(0.0, 0.0, 10.0)
    gluCylinder(quad, 4.8, 2.0, 19.0, 10, 10)
    glPopMatrix()

    glColor3f(0.9, 0.8, 0.2)
    glPushMatrix()
    glTranslatef(0.0, 0.0, 31.0)
    gluSphere(quad, 4.0, 10, 10)
    glPopMatrix()

    draw_limbs(quad, arm_rot, leg_rot, 5.2, 27.0, 2.2, 10.0, (0.5, 0.1, 0.7), (0.9, 0.8, 0.2))


def draw_enemy_model(enemy):
    glPushMatrix()
    glTranslatef(enemy[0], enemy[1], enemy[2])

    # Extract facing rotation calculated by AI (Index 12)
    rot_z = enemy[12] if len(enemy) > 12 else 0.0
    
    # Rotate around Z-axis (adjusted by -90 deg to face model front forward)
    glRotatef(rot_z - 90.0, 0.0, 0.0, 1.0)

    enemy_type = enemy[3]

    walk_step = enemy[5] if len(enemy) > 5 else 0.0
    computed_swing = math.sin(math.radians(walk_step)) * 25.0

    arm_rot = enemy[7] if len(enemy) > 7 and enemy[7] != 0.0 else computed_swing
    leg_rot = enemy[8] if len(enemy) > 8 and enemy[8] != 0.0 else computed_swing

    if enemy_type == "archer":
        draw_archer_enemy(arm_rot, leg_rot)

    elif enemy_type == "heavy":
        draw_heavy_enemy(arm_rot, leg_rot)

    elif enemy_type == "sage":
        draw_sage_aura_ring()
        draw_sage_enemy(arm_rot, leg_rot)

    else:
        draw_regular_enemy(arm_rot, leg_rot)

    glPopMatrix()