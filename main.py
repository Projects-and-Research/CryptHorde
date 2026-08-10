import sys
import os
import time
import random

# Force Python to look in the root directory first so local OpenGL is found globally
root_path = os.path.dirname(os.path.abspath(__file__))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

from OpenGL.GL import *
from OpenGL.GLUT import *
import core.sound as sound
import core.config as config
import core.controls as controls
import core.game_state as game_state
import physics.collisions as collisions
import behaviors.enemy_ai as enemy_ai
import behaviors.pickup_logic as pickup_logic
import behaviors.hazard_logic as hazard_logic
import behaviors.deployable_logic as deployable_logic
import behaviors.weapons_logic as weapons_logic
import animations.view_bob as view_bob
import animations.weapon_anims as weapon_anims
import animations.projectile_anims as projectile_anims
import animations.enemy_anims as enemy_anims
import animations.hazard_anims as hazard_anims
import graphics.renderer as renderer
import graphics.particles as particles

last_frame_time = time.time()
TARGET_FPS = 60
FRAME_TIME = 1.0 / TARGET_FPS  # ~0.01666 seconds per frame

def idle():
    global last_frame_time
    current_time = time.time()
    dt = current_time - last_frame_time

    # Frame-rate limiter: enforce ~60 FPS cap
    if dt < FRAME_TIME:
        time.sleep(FRAME_TIME - dt)
        current_time = time.time()
        dt = current_time - last_frame_time

    last_frame_time = current_time

    current_state = config.current_state

    if current_state == config.STATE_PLAYING:
        
        game_state.update_buffs(dt)
        controls.update_player_movement(dt)
        enemy_ai.update_enemies(dt)
        pickup_logic.update_pickups()
        hazard_logic.update_hazards(dt)
        deployable_logic.update_deployables(dt)
        weapons_logic.update_weapons()

        view_bob.update_view_bob(dt)
        weapon_anims.update_animations()
        enemy_anims.update_enemy_animations(dt)
        projectile_anims.update_projectiles(dt)
        hazard_anims.update_hazard_animations(dt)

        collisions.check_all_collisions()
        particles.update_particles()

    glutPostRedisplay()


def showScreen():
    # Delegate everything to the centralized renderer pipeline
    renderer.render_scene()


def main():
    print("1: starting main")
    glutInit()
    print("2: glutInit done")
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1280, 720)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"CryptHorde")

    glEnable(GL_DEPTH_TEST)
    game_state.reset_game()
    sound.preload_sounds()


    glutDisplayFunc(showScreen)
    glutKeyboardFunc(controls.keyboard_listener)
    glutKeyboardUpFunc(controls.keyboard_up_listener)
    glutMouseFunc(controls.mouse_listener)
    glutPassiveMotionFunc(controls.handle_passive_motion)
    glutMotionFunc(controls.handle_active_motion)
    glutIdleFunc(idle)
    glutMainLoop()


if __name__ == "__main__":
    main()