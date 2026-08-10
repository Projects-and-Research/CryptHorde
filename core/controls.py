from OpenGL.GL import *
from OpenGL.GLUT import *
import math
import sys
import core.config as config
import core.game_state as game_state
import core.sound as sound
import behaviors.deployable_logic as deployable_logic
import behaviors.weapons_logic as weapons_logic
import animations.weapon_anims as weapon_anims


# Key State Tracker for smooth multi-key holding
key_states = {}


def keyboard_listener(key, x, y):
    key_states[key] = True

    if config.current_state == config.STATE_MAIN_MENU:
        if key == b'\r' or key == b' ':
            config.current_state = config.STATE_PLAYING
            glutSetCursor(GLUT_CURSOR_NONE)
            game_state.reset_game()
            glutPostRedisplay()
        elif key == b'\x1b' or key == b'q' or key == b'Q':
            glutLeaveMainLoop()
        return

    if config.current_state == config.STATE_GAME_OVER:
        if key == b'r' or key == b'R':
            game_state.reset_game()
            config.current_state = config.STATE_PLAYING
            glutSetCursor(GLUT_CURSOR_NONE)
            glutPostRedisplay()
        elif key == b'\x1b' or key == b'q' or key == b'Q':
            glutLeaveMainLoop()
        return

    if config.current_state == config.STATE_PAUSED:
        if key == b'p' or key == b'P':
            config.current_state = config.STATE_PLAYING
            glutSetCursor(GLUT_CURSOR_NONE)
            glutPostRedisplay()
        return

    if config.current_state == config.STATE_SHOP:
        if key == b'p' or key == b'P' or key == b'f' or key == b'F' or key == b'b' or key == b'B' or key == b'\x1b':
            config.current_state = config.STATE_PLAYING
            config.shop_open = False
            glutSetCursor(GLUT_CURSOR_NONE)
            glutPostRedisplay()
        return

    # In-Game Single Actions
    if config.current_state == config.STATE_PLAYING:
        # Enter Shop (Keys: F or B)
        if key == b'f' or key == b'F' or key == b'b' or key == b'B':
            if getattr(config, "near_shop", False):
                if getattr(config, "wave_active", False):
                    setattr(config, "shop_warning_timer", 180)  
                else:
                    config.current_state = config.STATE_SHOP
                    config.shop_open = True
                    glutSetCursor(GLUT_CURSOR_INHERIT)
                    glutPostRedisplay()
                return

        # Dash (Spacebar) with 2-second cooldown
        if key == b' ':
            current_dodge_cooldown = getattr(config, "dodge_cooldown_timer", 0.0)

            if current_dodge_cooldown <= 0.0:
                dash_distance = 50.0
                rad = math.radians(config.player_angle)
                dir_x = math.cos(rad)
                dir_y = math.sin(rad)

                new_x = config.player_x + dir_x * dash_distance
                new_y = config.player_y + dir_y * dash_distance

                if -config.BOUND_LIMIT <= new_x <= config.BOUND_LIMIT:
                    config.player_x = new_x
                if -config.BOUND_LIMIT <= new_y <= config.BOUND_LIMIT:
                    config.player_y = new_y

                config.dodge_cooldown_timer = 2.0

        # Deployable Ability / Removal (E)
        if key == b'e' or key == b'E':
            deployable_logic.remove_nearest_deployable()

        # Reload Weapon Animation Trigger (R)
        if key == b'r' or key == b'R':
            crossbow_lvl = getattr(config, "crossbow_level", 1)
            if crossbow_lvl == 3:
                reload_duration = 100
            elif crossbow_lvl == 2:
                reload_duration = 140
            else:
                reload_duration = 180

            reload_duration = reload_duration if config.current_weapon == 2 else 40
            weapon_anims.trigger_reload(reload_duration)

        # Weapon Selection (Keys 1-4)
        if key == b'1':
            config.current_weapon = 0
            config.reload_timer = 0
        if key == b'2':
            config.current_weapon = 1
            config.reload_timer = 0
        if key == b'3':
            config.current_weapon = 2
            config.reload_timer = 0
        if key == b'4':
            config.current_weapon = 3
            config.reload_timer = 0

        # Pause Toggle
        if key == b'p' or key == b'P':
            config.current_state = config.STATE_PAUSED
            glutSetCursor(GLUT_CURSOR_INHERIT)
            glutPostRedisplay()


def keyboard_up_listener(key, x, y):
    key_states[key] = False


def update_player_movement(dt):
    if config.current_state != config.STATE_PLAYING:
        return

    dodge_timer = getattr(config, "dodge_cooldown_timer", 0.0)
    if dodge_timer > 0.0:
        config.dodge_cooldown_timer = max(0.0, dodge_timer - dt)

    warning_timer = getattr(config, "shop_warning_timer", 0)
    if warning_timer > 0:
        setattr(config, "shop_warning_timer", warning_timer - 1)

    move_speed = 120.0  

    rad = math.radians(config.player_angle)
    forward_x = math.cos(rad)
    forward_y = math.sin(rad)

    strafe_rad = math.radians(config.player_angle + 90.0)
    strafe_x = math.cos(strafe_rad)
    strafe_y = math.sin(strafe_rad)

    dir_x = 0.0
    dir_y = 0.0

    if key_states.get(b'w', False) or key_states.get(b'W', False):
        dir_x += forward_x
        dir_y += forward_y

    if key_states.get(b's', False) or key_states.get(b'S', False):
        dir_x -= forward_x
        dir_y -= forward_y

    if key_states.get(b'a', False) or key_states.get(b'A', False):
        dir_x += strafe_x
        dir_y += strafe_y

    if key_states.get(b'd', False) or key_states.get(b'D', False):
        dir_x -= strafe_x
        dir_y -= strafe_y

    length = math.sqrt(dir_x * dir_x + dir_y * dir_y)

    if length > 0.0:
        dir_x = dir_x / length
        dir_y = dir_y / length

        new_x = config.player_x + dir_x * move_speed * dt
        new_y = config.player_y + dir_y * move_speed * dt

        if -config.BOUND_LIMIT <= new_x <= config.BOUND_LIMIT:
            config.player_x = new_x

        if -config.BOUND_LIMIT <= new_y <= config.BOUND_LIMIT:
            config.player_y = new_y

        config.bob_step += 5.0 * dt


def mouse_listener(button, state, x, y):
    if config.current_state == config.STATE_MAIN_MENU:
        if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
            cart_y = 720 - y
            if 460 <= x <= 820 and 260 <= cart_y <= 330:
                config.current_state = config.STATE_PLAYING
                glutSetCursor(GLUT_CURSOR_NONE)
                game_state.reset_game()
                glutPostRedisplay()
            elif 500 <= x <= 780 and 150 <= cart_y <= 210:
                glutLeaveMainLoop()
        return

    if config.current_state == config.STATE_PAUSED:
        if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
            cart_y = 720 - y
            if 490 <= x <= 790 and 260 <= cart_y <= 320:
                config.current_state = config.STATE_PLAYING
                glutSetCursor(GLUT_CURSOR_NONE)
                glutPostRedisplay()
            elif 490 <= x <= 790 and 175 <= cart_y <= 235:
                config.current_state = config.STATE_MAIN_MENU
                glutSetCursor(GLUT_CURSOR_INHERIT)
                glutPostRedisplay()
        return

    if config.current_state == config.STATE_SHOP:
        if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
            cart_y = 720 - y
            current_gold = getattr(config, "player_money", getattr(config, "player_gold", 0))

            # --- Row 3: Consumables ---
            if 130 <= cart_y <= 260:
                if 130 <= x <= 370:  # Health Elixir (Cost: 50)
                    if current_gold >= 50:
                        if hasattr(config, "player_money"): config.player_money -= 50
                        if hasattr(config, "player_gold"): config.player_gold -= 50
                        config.player_health = min(config.max_health, config.player_health + 50.0)
                        config.shop_message = "Health Elixir purchased!"
                        config.shop_message_type = "success"
                        sound.play_sound("buy.mp3")
                    else:
                        config.shop_message = "Insufficient gold for Health Elixir!"
                        config.shop_message_type = "error"
                    config.shop_message_timer = 120
                    glutPostRedisplay()

                elif 395 <= x <= 635:  # Mana Potion (Cost: 50)
                    if current_gold >= 50:
                        if hasattr(config, "player_money"): config.player_money -= 50
                        if hasattr(config, "player_gold"): config.player_gold -= 50
                        config.player_mana = min(config.max_mana, config.player_mana + 50.0)
                        config.shop_message = "Mana Potion purchased!"
                        config.shop_message_type = "success"
                        sound.play_sound("buy.mp3")
                    else:
                        config.shop_message = "Insufficient gold for Mana Potion!"
                        config.shop_message_type = "error"
                    config.shop_message_timer = 120
                    glutPostRedisplay()

                elif 660 <= x <= 900:  # Invincibility (Cost: 150)
                    if current_gold >= 150:
                        if hasattr(config, "player_money"): config.player_money -= 150
                        if hasattr(config, "player_gold"): config.player_gold -= 150
                        config.invincible_active = True
                        config.invincible_timer = 7200
                        config.shop_message = "Invincibility Shield activated!"
                        config.shop_message_type = "success"
                        sound.play_sound("buy.mp3")
                    else:
                        config.shop_message = "Insufficient gold for Invincibility!"
                        config.shop_message_type = "error"
                    config.shop_message_timer = 120
                    glutPostRedisplay()

                elif 925 <= x <= 1165:  # Ammo Pack (Cost: 30)
                    if current_gold >= 30:
                        if hasattr(config, "player_money"): config.player_money -= 30
                        if hasattr(config, "player_gold"): config.player_gold -= 30
                        config.player_arrows = getattr(config, "player_arrows", 0) + 20
                        config.shop_message = "Ammo Pack purchased (+20 Arrows)!"
                        config.shop_message_type = "success"
                        sound.play_sound("buy.mp3")
                    else:
                        config.shop_message = "Insufficient gold for Ammo Pack!"
                        config.shop_message_type = "error"
                    config.shop_message_timer = 120
                    glutPostRedisplay()

            # --- Row 2: Weapon Upgrades ---
            elif 285 <= cart_y <= 455:
                if 130 <= x <= 370:  # Arcane Staff
                    staff_lvl = getattr(config, "staff_level", 1)
                    if staff_lvl < 2:
                        cost = 5000
                        if current_gold >= cost:
                            if hasattr(config, "player_money"): config.player_money -= cost
                            if hasattr(config, "player_gold"): config.player_gold -= cost
                            config.staff_level = staff_lvl + 1
                            config.shop_message = "Arcane Staff upgraded to Lvl 2!"
                            config.shop_message_type = "success"
                            sound.play_sound("buy.mp3")
                        else:
                            config.shop_message = "Insufficient gold for Arcane Staff upgrade!"
                            config.shop_message_type = "error"
                    else:
                        config.shop_message = "Arcane Staff is already MAX level!"
                        config.shop_message_type = "error"
                    config.shop_message_timer = 120
                    glutPostRedisplay()

                elif 395 <= x <= 635:  # Crossbow
                    cb_lvl = getattr(config, "crossbow_level", 1)
                    if cb_lvl < 3:
                        cost = 2000 if cb_lvl == 1 else 4000
                        if current_gold >= cost:
                            if hasattr(config, "player_money"): config.player_money -= cost
                            if hasattr(config, "player_gold"): config.player_gold -= cost
                            config.crossbow_level = cb_lvl + 1
                            config.shop_message = f"Crossbow upgraded to Lvl {config.crossbow_level}!"
                            config.shop_message_type = "success"
                            sound.play_sound("buy.mp3")
                        else:
                            config.shop_message = "Insufficient gold for Crossbow upgrade!"
                            config.shop_message_type = "error"
                    else:
                        config.shop_message = "Crossbow is already MAX level!"
                        config.shop_message_type = "error"
                    config.shop_message_timer = 120
                    glutPostRedisplay()

                elif 660 <= x <= 900:  # Hand Magic
                    hand_lvl = getattr(config, "hand_level", 1)
                    if hand_lvl < 3:
                        cost = 1500 if hand_lvl == 1 else 3000
                        if current_gold >= cost:
                            if hasattr(config, "player_money"): config.player_money -= cost
                            if hasattr(config, "player_gold"): config.player_gold -= cost
                            config.hand_level = hand_lvl + 1
                            config.shop_message = f"Hand Magic upgraded to Lvl {config.hand_level}!"
                            config.shop_message_type = "success"
                            sound.play_sound("buy.mp3")
                        else:
                            config.shop_message = "Insufficient gold for Hand Magic upgrade!"
                            config.shop_message_type = "error"
                    else:
                        config.shop_message = "Hand Magic is already MAX level!"
                        config.shop_message_type = "error"
                    config.shop_message_timer = 120
                    glutPostRedisplay()

                elif 925 <= x <= 1165:  # Bow
                    bow_lvl = getattr(config, "bow_level", 1)
                    if bow_lvl < 3:
                        cost = 1000 if bow_lvl == 1 else 2000
                        if current_gold >= cost:
                            if hasattr(config, "player_money"): config.player_money -= cost
                            if hasattr(config, "player_gold"): config.player_gold -= cost
                            config.bow_level = bow_lvl + 1
                            config.shop_message = f"Bow upgraded to Lvl {config.bow_level}!"
                            config.shop_message_type = "success"
                            sound.play_sound("buy.mp3")
                        else:
                            config.shop_message = "Insufficient gold for Bow upgrade!"
                            config.shop_message_type = "error"
                    else:
                        config.shop_message = "Bow is already MAX level!"
                        config.shop_message_type = "error"
                    config.shop_message_timer = 120
                    glutPostRedisplay()

            # --- Row 1: Turret Upgrades & Capacity ---
            elif 480 <= cart_y <= 610:
                if 130 <= x <= 370:  # Turret Level Upgrade (Lvl 2=500, 3=1500, 4=3500, 5=8000)
                    turret_lvl = getattr(config, "deployable_level", 1)
                    if turret_lvl < 5:
                        if turret_lvl == 1:
                            cost = 500
                        elif turret_lvl == 2:
                            cost = 1500
                        elif turret_lvl == 3:
                            cost = 3500
                        else:
                            cost = 8000

                        if current_gold >= cost:
                            if hasattr(config, "player_money"): config.player_money -= cost
                            if hasattr(config, "player_gold"): config.player_gold -= cost
                            config.deployable_level = turret_lvl + 1
                            config.shop_message = f"Turret upgraded to Lvl {config.deployable_level}!"
                            config.shop_message_type = "success"
                            sound.play_sound("buy.mp3")
                        else:
                            config.shop_message = "Insufficient gold for Turret upgrade!"
                            config.shop_message_type = "error"
                    else:
                        config.shop_message = "Turrets are at MAX level!"
                        config.shop_message_type = "error"
                    config.shop_message_timer = 120
                    glutPostRedisplay()

                elif 395 <= x <= 635:  # Max Turret Slots (2nd slot=5000, 3rd slot=15000)
                    max_turrets = getattr(config, "max_deployables", 1)
                    if max_turrets < 3:
                        cost = 5000 if max_turrets == 1 else 15000
                        if current_gold >= cost:
                            if hasattr(config, "player_money"): config.player_money -= cost
                            if hasattr(config, "player_gold"): config.player_gold -= cost
                            config.max_deployables = max_turrets + 1
                            config.shop_message = f"Max Turret Slots increased to {config.max_deployables}!"
                            config.shop_message_type = "success"
                            sound.play_sound("buy.mp3")
                        else:
                            config.shop_message = "Insufficient gold for Turret Slot upgrade!"
                            config.shop_message_type = "error"
                    else:
                        config.shop_message = "Max Turret Slots are already at MAX limit!"
                        config.shop_message_type = "error"
                    config.shop_message_timer = 120
                    glutPostRedisplay()
        return

    if config.current_state != config.STATE_PLAYING:
        return

    # Left Mouse Button (MB1) - Fire / Charge Attack
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            weapons_logic.handle_weapon_input(mouse_pressed=True)
        elif state == GLUT_UP:
            weapons_logic.handle_weapon_input(mouse_pressed=False)


def handle_mouse_look(x, y):
    if config.current_state != config.STATE_PLAYING:
        return

    center_x = 640
    center_y = 360

    delta_x = x - center_x
    delta_y = y - center_y

    if delta_x != 0 or delta_y != 0:
        sensitivity = 0.1

        if getattr(config, "mb1_pressed", False) and config.current_weapon in [0, 1, 3]:
            sensitivity = 0.02

        config.player_angle = (config.player_angle - delta_x * sensitivity) % 360.0
        config.player_pitch -= delta_y * sensitivity

        if config.player_pitch > 89.0:
            config.player_pitch = 89.0
        if config.player_pitch < -89.0:
            config.player_pitch = -89.0

        glutSetCursor(GLUT_CURSOR_NONE)
        glutWarpPointer(center_x, center_y)


def handle_passive_motion(x, y):
    handle_mouse_look(x, y)


def handle_active_motion(x, y):
    handle_mouse_look(x, y)