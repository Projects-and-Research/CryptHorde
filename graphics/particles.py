from OpenGL.GL import *
import math
import core.config as config


def create_particle(x, y, z, vx, vy, vz, color, size=2.0, life=30):
    particle = {
        "x": x,
        "y": y,
        "z": z,
        "vx": vx,
        "vy": vy,
        "vz": vz,
        "color": color,  # tuple (r, g, b)
        "size": size,
        "life": life,
        "max_life": life
    }
    config.particles.append(particle)


def spawn_aoe_ring(x, y, z, radius_max=30.0, color=(0.8, 0.2, 1.0)):
    # Create ring particles radiating outwards
    num_particles = 20
    for i in range(0, num_particles, 1):
        angle = (float(i) / float(num_particles)) * 2.0 * math.pi
        speed = radius_max / 20.0
        vx = math.cos(angle) * speed
        vy = math.sin(angle) * speed
        vz = 0.5
        create_particle(x, y, z, vx, vy, vz, color, size=3.0, life=20)


def update_and_draw_particles():
    glPointSize(3.0)

    for i in range(len(config.particles) - 1, -1, -1):
        p = config.particles[i]

        # Update position
        p["x"] = p["x"] + p["vx"]
        p["y"] = p["y"] + p["vy"]
        p["z"] = p["z"] + p["vz"]

        # Decay life
        p["life"] = p["life"] - 1

        if p["life"] <= 0:
            config.particles.pop(i)
            continue

        # Calculate alpha / brightness fade
        fade = float(p["life"]) / float(p["max_life"])
        r, g, b = p["color"]

        # Render point particle
        glColor3f(r * fade, g * fade, b * fade)
        glBegin(GL_POINTS)
        glVertex3f(p["x"], p["y"], p["z"])
        glEnd()



def update_particles():
    update_and_draw_particles()