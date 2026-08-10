from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import core.config as config
import graphics.camera as camera
import graphics.particles as particles
import world.arena as arena
import world.map_objects as map_objects
import entities.enemy_models as enemy_models
import entities.weapon_models as weapon_models
import entities.projectile_models as projectile_models
import entities.player_model as player_model
import entities.pickup_models as pickup_models
import entities.hazard_models as hazard_models
import ui.hud as hud
import ui.main_menu as main_menu
import ui.pause_menu as pause_menu
import ui.shop_ui as shop_ui
import behaviors.deployable_logic as deployable_logic


def begin_frame():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()


def end_frame():
    glutSwapBuffers()


def render_entities():
    # Note: Full player model body is omitted in FPS mode to prevent view obstruction.
    # Player hands/arms can be handled directly via weapon models or first-person view passes.
    i = 0
    while (i < len(config.enemies)):
        enemy_models.draw_enemy_model(config.enemies[i])
        i += 1

    # Render Active Deployables (Turrets)
    deployable_logic.render_deployables()
    
    # Render Active Pickups
    i = 0
    while (i < len(config.pickups)):
        pickup_models.draw_pickup(config.pickups[i])
        i += 1

    # Render Active Hazards & Runes
    if hasattr(config, "spiked_traps"):
        i = 0
        while (i < len(config.spiked_traps)):
            hazard_models.draw_trap(config.spiked_traps[i])
            i += 1

    if hasattr(config, "runes"):
        i = 0
        while (i < len(config.runes)):
            hazard_models.draw_rune(config.runes[i])
            i += 1

    # Render Active Enemies
    i = 0
    while (i < len(config.enemies)):
        enemy_models.draw_enemy_model(config.enemies[i])
        i += 1

    # Render Active Projectiles
    i = 0
    while (i < len(config.player_projectiles)):
        projectile_models.draw_projectile_model(config.player_projectiles[i])
        i += 1

    i = 0
    while (i < len(config.enemy_arrows)):
        projectile_models.draw_projectile_model(config.enemy_arrows[i])
        i += 1


def render_scene():
    # Clear color and depth buffers
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    current_state = config.current_state

    # Render based on current application state
    if current_state == config.STATE_MAIN_MENU:
        main_menu.draw_main_menu()

    elif current_state == config.STATE_PLAYING:
        # 1. Setup First-Person Camera Perspective
        camera.setup_fps_camera()

        # 2. Render 3D World Environment
        arena.draw_arena()

        # 3. Render all world entities (Pickups, Hazards, Enemies, Projectiles)
        render_entities()

        # 4. Render Visual Particle Effects
        particles.update_and_draw_particles()

        # 5. Clear depth buffer so the first-person weapon/hands never clip into world geometry/walls
        glClear(GL_DEPTH_BUFFER_BIT)

        # 6. Render First-Person View Weapon Model & Player Hands
        weapon_models.draw_current_weapon()

        # 7. Render 2D Overlay HUD
        hud.draw_hud()

    elif current_state == config.STATE_PAUSED:
        # 1. Render the frozen 3D World & Gameplay in the background
        camera.setup_fps_camera()
        arena.draw_arena()
        render_entities()
        particles.update_and_draw_particles()
        glClear(GL_DEPTH_BUFFER_BIT)
        weapon_models.draw_current_weapon()
        hud.draw_hud()

        # 2. Draw Pause Menu Overlay on top
        pause_menu.draw_pause_menu()

    elif current_state == config.STATE_SHOP:
        # 1. Render the frozen 3D World & Gameplay in the background
        camera.setup_fps_camera()
        arena.draw_arena()
        render_entities()
        particles.update_and_draw_particles()
        glClear(GL_DEPTH_BUFFER_BIT)
        weapon_models.draw_current_weapon()
        hud.draw_hud()

        # 2. Draw Shop Menu Overlay on top
        shop_ui.draw_shop_ui()

    elif current_state == config.STATE_GAME_OVER:
        hud.draw_game_over_screen()

    # Flush drawing commands
    glFlush()
    glutSwapBuffers()