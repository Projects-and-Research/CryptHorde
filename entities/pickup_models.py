from OpenGL.GL import *
from OpenGL.GLU import *


def draw_health_rune():
    quad = gluNewQuadric()

    # Red Glowing Center Gem/Sphere
    glColor3f(0.9, 0.1, 0.2)
    glPushMatrix()
    gluSphere(quad, 3.0, 10, 10)
    glPopMatrix()

    # Outer Golden Ring
    glColor3f(0.9, 0.8, 0.2)
    glPushMatrix()
    glScalef(1.0, 1.0, 0.2)
    gluCylinder(quad, 4.5, 4.5, 2.0, 12, 1)
    glPopMatrix()


def draw_mana_rune():
    quad = gluNewQuadric()

    # Blue Glowing Center Gem/Sphere
    glColor3f(0.1, 0.4, 1.0)
    glPushMatrix()
    gluSphere(quad, 3.0, 10, 10)
    glPopMatrix()

    # Outer Silver/Cyan Ring
    glColor3f(0.5, 0.9, 1.0)
    glPushMatrix()
    glScalef(1.0, 1.0, 0.2)
    gluCylinder(quad, 4.5, 4.5, 2.0, 12, 1)
    glPopMatrix()


def draw_invincibility_rune():
    quad = gluNewQuadric()

    # Bright Gold Center Gem/Sphere
    glColor3f(1.0, 0.85, 0.0)
    glPushMatrix()
    gluSphere(quad, 3.5, 10, 10)
    glPopMatrix()

    # Outer Glowing Purple Ring
    glColor3f(0.8, 0.2, 1.0)
    glPushMatrix()
    glScalef(1.0, 1.0, 0.2)
    gluCylinder(quad, 5.0, 5.0, 2.0, 12, 1)
    glPopMatrix()


def draw_pickup_model(pickup):
    glPushMatrix()
    
    # Handle both list formats [x, y, type, offset] and dict formats {"x": ..., "y": ...}
    if isinstance(pickup, (list, tuple)):
        px = pickup[0]
        py = pickup[1]
        pz = pickup[2] if len(pickup) > 3 and isinstance(pickup[2], (int, float)) else 0.0
        
        # Determine type string from list
        pickup_type = "health"
        for item in pickup:
            if isinstance(item, str):
                pickup_type = item
                break
    else:
        px = pickup.get("x", 0.0)
        py = pickup.get("y", 0.0)
        pz = pickup.get("z", 0.0)
        pickup_type = pickup.get("type", "health")

    glTranslatef(px, py, pz)

    if pickup_type == "mana":
        draw_mana_rune()
    elif pickup_type == "invincible" or pickup_type == "invincibility":
        draw_invincibility_rune()
    else:
        draw_health_rune()

    glPopMatrix()


def draw_pickup(pickup):
    """
    Alias required by renderer.py to draw items from config.pickups / config.runes
    """
    draw_pickup_model(pickup)