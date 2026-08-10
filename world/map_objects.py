from OpenGL.GL import *
from OpenGL.GLU import *
import math


def draw_shop_structure(x, y):
    quad = gluNewQuadric()
    glPushMatrix()
    glTranslatef(x, y, 0.0)

    # Shop Base Platform
    glBegin(GL_QUADS)
    glColor3f(0.35, 0.25, 0.1)
    glVertex3f(-35.0, -35.0, 1.0)
    glVertex3f(35.0, -35.0, 1.0)
    glVertex3f(35.0, 35.0, 1.0)
    glVertex3f(-35.0, 35.0, 1.0)
    glEnd()

    # Cyan Glowing Interaction Border (using GL_LINES)
    glBegin(GL_LINES)
    glColor3f(0.0, 0.9, 1.0)
    glVertex3f(-35.0, -35.0, 2.0)
    glVertex3f(35.0, -35.0, 2.0)
    glVertex3f(35.0, -35.0, 2.0)
    glVertex3f(35.0, 35.0, 2.0)
    glVertex3f(35.0, 35.0, 2.0)
    glVertex3f(-35.0, 35.0, 2.0)
    glVertex3f(-35.0, 35.0, 2.0)
    glVertex3f(-35.0, -35.0, 2.0)
    glEnd()

    # Central Shop Crystal / Cylinder
    glPushMatrix()
    glTranslatef(0.0, 0.0, 1.0)
    glColor3f(0.1, 0.7, 0.9)
    gluCylinder(quad, 6.0, 6.0, 60.0, 12, 1)
    glPopMatrix()
    glPopMatrix()


def draw_obstacle_pillar(x, y):
    quad = gluNewQuadric()
    glPushMatrix()
    glTranslatef(x, y, 0.0)

    # Circular Stone Pillar using gluCylinder
    glColor3f(0.3, 0.3, 0.35)
    gluCylinder(quad, 12.0, 12.0, 90.0, 12, 1)
    glPopMatrix()


def draw_tree(x, y):
    quad = gluNewQuadric()
    glPushMatrix()
    glTranslatef(x, y, 0.0)

    # Tree Trunk (Cylinder)
    glColor3f(0.4, 0.25, 0.1)
    gluCylinder(quad, 5.0, 5.0, 60.0, 8, 1)

    # Tree Foliage Canopy (Cone / Tapered Cylinder)
    glPushMatrix()
    glTranslatef(0.0, 0.0, 50.0)
    glColor3f(0.1, 0.5, 0.2)
    gluCylinder(quad, 25.0, 0.0, 40.0, 10, 1)
    glPopMatrix()
    glPopMatrix()


def draw_rotating_magic_beam(x, y, rotation_angle):
    quad = gluNewQuadric()
    glPushMatrix()
    glTranslatef(x, y, 0.0)

    # 1. Central Pillar base/mast
    glColor3f(0.4, 0.3, 0.5)
    glPushMatrix()
    gluCylinder(quad, 4.0, 4.0, 70.0, 10, 1)
    glPopMatrix()

    # 2. Rotating horizontal sweeping beam/cone extending outward from the pillar
    glPushMatrix()
    glTranslatef(0.0, 0.0, 35.0)  # Positioned midway up the pillar height
    glRotatef(rotation_angle, 0.0, 0.0, 1.0)
    
    glColor3f(0.8, 0.2, 1.0)
    # Draw a cone/sweeping beam pointing outwards along the x-axis
    glPushMatrix()
    glTranslatef(0.0, 0.0, 0.0)
    glRotatef(90.0, 0.0, 1.0, 0.0)  # Orient cone horizontally
    gluCylinder(quad, 6.0, 2.0, 45.0, 8, 1)
    glPopMatrix()
    
    glPopMatrix()
    glPopMatrix()


def draw_spiked_floor_trap(x, y, active=True):
    glPushMatrix()
    glTranslatef(x, y, 0.5)

    # Trap Base Plate
    glColor3f(0.2, 0.2, 0.2)
    glBegin(GL_QUADS)
    glVertex3f(-15.0, -15.0, 0.0)
    glVertex3f(15.0, -15.0, 0.0)
    glVertex3f(15.0, 15.0, 0.0)
    glVertex3f(-15.0, 15.0, 0.0)
    glEnd()

    # Spikes
    if active:
        glColor3f(0.9, 0.1, 0.1)
    else:
        glColor3f(0.5, 0.5, 0.5)

    spike_offsets = [-8.0, 0.0, 8.0]
    for sx in spike_offsets:
        for sy in spike_offsets:
            glPushMatrix()
            glTranslatef(sx, sy, 0.0)
            glBegin(GL_TRIANGLES)
            # Pyramid spike
            glVertex3f(0.0, 0.0, 12.0)
            glVertex3f(-3.0, -3.0, 0.0)
            glVertex3f(3.0, -3.0, 0.0)

            glVertex3f(0.0, 0.0, 12.0)
            glVertex3f(3.0, -3.0, 0.0)
            glVertex3f(3.0, 3.0, 0.0)

            glVertex3f(0.0, 0.0, 12.0)
            glVertex3f(3.0, 3.0, 0.0)
            glVertex3f(-3.0, 3.0, 0.0)

            glVertex3f(0.0, 0.0, 12.0)
            glVertex3f(-3.0, 3.0, 0.0)
            glVertex3f(-3.0, -3.0, 0.0)
            glEnd()
            glPopMatrix()

    glPopMatrix()


def draw_rune_pickup(x, y, rune_type, float_offset=0.0):
    quad = gluNewQuadric()
    glPushMatrix()
    # Floating effect using sine/cosine offset passed in
    glTranslatef(x, y, 10.0 + float_offset)

    if rune_type == "health":
        glColor3f(0.2, 1.0, 0.3)  # Glowing Green Health Rune
    elif rune_type == "mana":
        glColor3f(0.2, 0.4, 1.0)  # Glowing Blue Mana Rune
    elif rune_type == "invincibility":
        glColor3f(1.0, 0.9, 0.1)  # Glowing Gold Invincibility Rune
    else:
        glColor3f(1.0, 1.0, 1.0)

    # Render floating glowing sphere
    gluSphere(quad, 8.0, 10, 10)

    glPopMatrix()