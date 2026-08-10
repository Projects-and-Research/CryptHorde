from OpenGL.GL import *
from OpenGL.GLU import *

import world.map_objects as map_objects

def draw_rune(rune_data):
    """
    Renders a rune from config.runes / config.pickups.
    Expected structure: [x, y, type_string, float_offset_val]
    """
    if not rune_data or len(rune_data) < 3:
        return

    rx = rune_data[0]
    ry = rune_data[1]
    rtype = rune_data[2]
    roffset = rune_data[3] if len(rune_data) > 3 else 0.0

    map_objects.draw_rune_pickup(rx, ry, rtype, float_offset=roffset)

def draw_spiked_trap(hazard):
    glPushMatrix()
    glTranslatef(hazard["x"], hazard["y"], hazard["z"])

    # Base Plate (Dark Gray Metal)
    glColor3f(0.2, 0.2, 0.2)
    glPushMatrix()
    glScalef(12.0, 12.0, 1.0)
    
    # 3D Box Base
    glBegin(GL_QUADS)
    # Front
    glVertex3f(-0.5, -0.5, 0.5)
    glVertex3f(0.5, -0.5, 0.5)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    # Back
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(-0.5, 0.5, -0.5)
    glVertex3f(0.5, 0.5, -0.5)
    glVertex3f(0.5, -0.5, -0.5)
    # Top
    glVertex3f(-0.5, 0.5, -0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(0.5, 0.5, -0.5)
    # Bottom
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(0.5, -0.5, 0.5)
    glVertex3f(-0.5, -0.5, 0.5)
    glEnd()
    glPopMatrix()

    # Spikes Array (Iron Cones)
    glColor3f(0.6, 0.6, 0.65)
    quad = gluNewQuadric()

    spike_offsets = [-3.5, 0.0, 3.5]
    for ox in spike_offsets:
        for oy in spike_offsets:
            glPushMatrix()
            glTranslatef(ox, oy, 0.5)
            gluCylinder(quad, 0.8, 0.0, 5.0, 6, 1)
            glPopMatrix()

    glPopMatrix()


def draw_hazard_model(hazard):
    if hazard.get("type") == "spikes":
        draw_spiked_trap(hazard)