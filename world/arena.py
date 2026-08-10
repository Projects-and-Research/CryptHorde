from OpenGL.GL import *
import core.config as config
import world.map_objects as map_objects
import math


def draw_arena():

    # 1. Draw Floor Arena Base
    glBegin(GL_QUADS)
    glColor3f(0.15, 0.15, 0.18)
    glVertex3f(-config.GRID_LENGTH, -config.GRID_LENGTH, 0.0)
    glVertex3f(config.GRID_LENGTH, -config.GRID_LENGTH, 0.0)
    glVertex3f(config.GRID_LENGTH, config.GRID_LENGTH, 0.0)
    glVertex3f(-config.GRID_LENGTH, config.GRID_LENGTH, 0.0)
    glEnd()

    # 2. Draw Floor Grid Lines
    glBegin(GL_LINES)
    glColor3f(0.25, 0.25, 0.3)
    step = 100.0
    val = -config.GRID_LENGTH
    while (val <= config.GRID_LENGTH):
        glVertex3f(val, -config.GRID_LENGTH, 0.5)
        glVertex3f(val, config.GRID_LENGTH, 0.5)
        glVertex3f(-config.GRID_LENGTH, val, 0.5)
        glVertex3f(config.GRID_LENGTH, val, 0.5)
        val += step
    glEnd()

    # 3. Draw Perimeter Walls
    wall_height = 120.0
    glBegin(GL_QUADS)
   
    # North Wall
    glColor3f(0.3, 0.3, 0.35)
    glVertex3f(-config.GRID_LENGTH, config.GRID_LENGTH, 0.0)
    glVertex3f(config.GRID_LENGTH, config.GRID_LENGTH, 0.0)
    glVertex3f(config.GRID_LENGTH, config.GRID_LENGTH, wall_height)
    glVertex3f(-config.GRID_LENGTH, config.GRID_LENGTH, wall_height)

    # South Wall
    glColor3f(0.25, 0.25, 0.3)
    glVertex3f(-config.GRID_LENGTH, -config.GRID_LENGTH, 0.0)
    glVertex3f(-config.GRID_LENGTH, -config.GRID_LENGTH, wall_height)
    glVertex3f(config.GRID_LENGTH, -config.GRID_LENGTH, wall_height)
    glVertex3f(config.GRID_LENGTH, -config.GRID_LENGTH, 0.0)

    # East Wall
    glColor3f(0.32, 0.32, 0.38)
    glVertex3f(config.GRID_LENGTH, -config.GRID_LENGTH, 0.0)
    glVertex3f(config.GRID_LENGTH, -config.GRID_LENGTH, wall_height)
    glVertex3f(config.GRID_LENGTH, config.GRID_LENGTH, wall_height)
    glVertex3f(config.GRID_LENGTH, config.GRID_LENGTH, 0.0)

    # West Wall
    glColor3f(0.28, 0.28, 0.33)
    glVertex3f(-config.GRID_LENGTH, -config.GRID_LENGTH, 0.0)
    glVertex3f(-config.GRID_LENGTH, config.GRID_LENGTH, 0.0)
    glVertex3f(-config.GRID_LENGTH, config.GRID_LENGTH, wall_height)
    glVertex3f(-config.GRID_LENGTH, -config.GRID_LENGTH, wall_height)
    glEnd()

    # 4. Place Map Objects using map_objects blueprints
   
    # Shops
    map_objects.draw_shop_structure(200.0, 200.0)
    map_objects.draw_shop_structure(-200.0, -200.0)

    # Obstacle Pillars
    map_objects.draw_obstacle_pillar(0.0, 250.0)
    map_objects.draw_obstacle_pillar(0.0, -250.0)
    map_objects.draw_obstacle_pillar(250.0, 0.0)
    map_objects.draw_obstacle_pillar(-250.0, 0.0)

    # Trees
    map_objects.draw_tree(400.0, 400.0)
    map_objects.draw_tree(-400.0, 400.0)
    map_objects.draw_tree(400.0, -400.0)
    map_objects.draw_tree(-400.0, -400.0) 

    # 5. Place Spiked Floor Traps
    trap_positions = [
        (150.0, 150.0),
        (-150.0, 150.0),
        (150.0, -150.0),
        (-150.0, -150.0),
        (0.0, 350.0),
        (0.0, -350.0)
    ]
    
    # Check global frame/hazard animation state if available
    hazard_active_state = getattr(config, "hazard_spikes_active", True)
    for (tx, ty) in trap_positions:
        map_objects.draw_spiked_floor_trap(tx, ty, active=hazard_active_state)

    # 6. Place Rotating Magic Beams
    beam_positions = [
        (300.0, 100.0),
        (-300.0, -100.0),
        (100.0, 300.0),
        (-100.0, -300.0)
    ]
    
    # Use global beam rotation counter or tick from config for animation
    beam_angle = getattr(config, "beam_rotation_angle", 0.0)
    for (bx, by) in beam_positions:
        map_objects.draw_rotating_magic_beam(bx, by, beam_angle)

    # 7. Render World Pickups / Runes (Dynamic from config + Test Runes)
    runes_list = getattr(config, "runes", [])
    
    combined_runes = list(runes_list)

    for rune in combined_runes:
        # Expected structure: [x, y, type_string, float_offset_val]
        rx = rune[0]
        ry = rune[1]
        rtype = rune[2]
        roffset = rune[3] if len(rune) > 3 else 0.0
        map_objects.draw_rune_pickup(rx, ry, rtype, float_offset=roffset)

