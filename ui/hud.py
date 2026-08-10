from OpenGL.GL import *
from OpenGL.GLUT import *
import core.config as config


def draw_game_over_screen():
    # Switch to 2D orthogonal projection for Game Over screen overlay (1280x720)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, 1280, 0, 720, -1, 1)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glDisable(GL_DEPTH_TEST)

    # Dark red/black tint overlay spanning 1280x720
    glColor3f(0.1, 0.02, 0.02)
    glBegin(GL_QUADS)
    glVertex2f(0, 0)
    glVertex2f(1280, 0)
    glVertex2f(1280, 720)
    glVertex2f(0, 720)
    glEnd()

    # Game Over Box (Centered for 1280x720)
    glColor3f(0.2, 0.05, 0.05)
    glBegin(GL_QUADS)
    glVertex2f(440, 240)
    glVertex2f(840, 240)
    glVertex2f(840, 480)
    glVertex2f(440, 480)
    glEnd()

    # Border Accent
    glColor3f(0.8, 0.2, 0.2)
    glLineWidth(2.0)
    glBegin(GL_LINES)
    glVertex2f(440, 240)
    glVertex2f(840, 240)
    glVertex2f(440, 480)
    glVertex2f(840, 480)
    glVertex2f(440, 240)
    glVertex2f(440, 480)
    glVertex2f(840, 240)
    glVertex2f(840, 480)
    glEnd()

    # Reset line width
    glLineWidth(1.0)

    # Game Over Text & Final Stats
    glColor3f(1.0, 0.2, 0.2)
    title_text = "YOU DIED"
    raster_x = 640 - (len(title_text) * 4.5)
    glRasterPos2f(575, 435)
    
    for i in range(0, len(title_text), 1):
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(title_text[i]))

    glColor3f(1.0, 1.0, 1.0)
    final_score = getattr(config, "score", 0)
    final_wave = getattr(config, "wave_number", 1)

    wave_text = "Final Wave Reached: " + str(final_wave)
    glRasterPos2f(500, 375)
    
    for i in range(0, len(wave_text), 1):
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(wave_text[i]))

    score_text = "Final Score: " + str(final_score)
    glRasterPos2f(500, 335)
    
    for i in range(0, len(score_text), 1):
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(score_text[i]))

    # Restart Instruction Box
    glColor3f(0.2, 0.4, 0.3)
    glBegin(GL_QUADS)
    glVertex2f(500, 270)
    glVertex2f(780, 270)
    glVertex2f(780, 320)
    glVertex2f(500, 320)
    glEnd()

    glColor3f(1.0, 1.0, 1.0)
    restart_text = "Press R to Restart"
    glRasterPos2f(560, 288)
    
    for i in range(0, len(restart_text), 1):
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(restart_text[i]))

    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()


def draw_hud():
    # Switch to 2D orthogonal projection for HUD overlay using glOrtho (1280x720)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, 1280, 0, 720, -1, 1)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glDisable(GL_DEPTH_TEST)

    # 1. Crosshair in center of 1280x720 screen (640, 360)
    glColor3f(1.0, 1.0, 1.0)
    glLineWidth(2.0)
    glBegin(GL_LINES)
    glVertex2f(635, 360)
    glVertex2f(645, 360)
    glVertex2f(640, 355)
    glVertex2f(640, 365)
    glEnd()

    # Reset line width
    glLineWidth(1.0)

    # 2. Health Bar Background (Top Left)
    glColor3f(0.3, 0.3, 0.3)
    glBegin(GL_QUADS)
    glVertex2f(30, 670)
    glVertex2f(250, 670)
    glVertex2f(250, 695)
    glVertex2f(30, 695)
    glEnd()

    # Health Bar Fill
    max_hp = getattr(config, "max_health", 100.0)
    cur_hp = getattr(config, "player_health", 100.0)
    health_width = max(0.0, (cur_hp / max_hp) * 220.0)
    
    glColor3f(0.2, 0.9, 0.2)
    glBegin(GL_QUADS)
    glVertex2f(30, 670)
    glVertex2f(30 + health_width, 670)
    glVertex2f(30 + health_width, 695)
    glVertex2f(30, 695)
    glEnd()

    # 3. Mana Bar Background (Top Left below Health)
    glColor3f(0.3, 0.3, 0.3)
    glBegin(GL_QUADS)
    glVertex2f(30, 635)
    glVertex2f(250, 635)
    glVertex2f(250, 660)
    glVertex2f(30, 660)
    glEnd()

    # Mana Bar Fill
    max_mn = getattr(config, "max_mana", 100.0)
    cur_mn = getattr(config, "player_mana", 100.0)
    mana_width = max(0.0, (cur_mn / max_mn) * 220.0)
    
    glColor3f(0.2, 0.5, 1.0)
    glBegin(GL_QUADS)
    glVertex2f(30, 635)
    glVertex2f(30 + mana_width, 635)
    glVertex2f(30 + mana_width, 660)
    glVertex2f(30, 660)
    glEnd()

    # 4. Gold Display
    glColor3f(1.0, 0.84, 0.0)
    money_val = getattr(config, "player_money", 0)
    money_str = "Gold: " + str(money_val)

    glRasterPos2f(30, 600)
    
    for i in range(0, len(money_str), 1):
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(money_str[i]))

    # 5. Arrows Display
    glColor3f(0.8, 0.8, 0.8)
    arrow_val = getattr(config, "player_arrows", 20)
    arrow_str = "Arrows: " + str(arrow_val)

    glRasterPos2f(30, 570)
    
    for i in range(0, len(arrow_str), 1):
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(arrow_str[i]))

    # 6. Current Weapon & Level Display
    glColor3f(1.0, 1.0, 0.2)
    weapon_names_list = getattr(config, "weapon_names", ["Arcane Staff", "Magic Hand", "Crossbow", "Bow"])
    curr_wep_idx = getattr(config, "current_weapon", 0)
    wep_name = weapon_names_list[curr_wep_idx] if curr_wep_idx < len(weapon_names_list) else "Unknown"

    if curr_wep_idx == 0:
        wep_lvl = getattr(config, "staff_level", 1)
    elif curr_wep_idx == 1:
        wep_lvl = getattr(config, "hand_level", 1)
    elif curr_wep_idx == 2:
        wep_lvl = getattr(config, "crossbow_level", 1)
    elif curr_wep_idx == 3:
        wep_lvl = getattr(config, "bow_level", 1)
    else:
        wep_lvl = 1

    weapon_str = f"Weapon: {wep_name} (Lvl {wep_lvl})"
    glRasterPos2f(30, 535)
    
    for i in range(0, len(weapon_str), 1):
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(weapon_str[i]))

    # 7. Wave Count & Next Wave Timer Display
    glColor3f(1.0, 0.5, 0.0)
    current_wave_val = getattr(config, "wave_number", 1)
    wave_str = "Wave: " + str(current_wave_val)

    glRasterPos2f(30, 500)
    
    for i in range(0, len(wave_str), 1):
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(wave_str[i]))

    wave_timer_val = getattr(config, "wave_timer", 0.0)
    
    if wave_timer_val > 0.0:
        seconds_left = int(wave_timer_val / 60.0) + 1
        timer_str = f"Next Wave in: {seconds_left}s"
        glColor3f(1.0, 1.0, 0.0)
    else:
        timer_str = "Wave In Progress"
        glColor3f(0.2, 1.0, 0.2)

    glRasterPos2f(30, 470)
    
    for i in range(0, len(timer_str), 1):
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(timer_str[i]))

    # 8. Enemies Remaining Display
    glColor3f(1.0, 0.3, 0.3)
    enemies_left = len(getattr(config, "enemies", []))
    enemies_str = "Enemies Left: " + str(enemies_left)

    glRasterPos2f(30, 440)
    
    for i in range(0, len(enemies_str), 1):
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(enemies_str[i]))

    # 9. Deployables Remaining / Status Display
    glColor3f(0.2, 0.8, 1.0)
    active_deployables = len(getattr(config, "deployables", []))
    max_deployables = getattr(config, "max_deployables", 1)
    deployable_level = getattr(config, "deployable_level", 1)
    deployable_str = f"Turrets: {active_deployables}/{max_deployables} (Lvl {deployable_level})"

    glRasterPos2f(30, 410)
    
    for i in range(0, len(deployable_str), 1):
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(deployable_str[i]))

    # 10. Invincibility Timer Display (Shows only if active)
    if getattr(config, "invincible_active", False):
        invincible_frames = getattr(config, "invincible_timer", 0)
        invincible_seconds = max(1, int(invincible_frames / 60.0))
        
        glColor3f(0.0, 1.0, 1.0)
        invincible_str = f"Invincible: {invincible_seconds}s"
        
        glRasterPos2f(30, 380)
        
        for i in range(0, len(invincible_str), 1):
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(invincible_str[i]))

    # 11. Deployable Proximity Prompt ("Press E to remove turret")
    if getattr(config, "near_deployable", False):
        glColor3f(1.0, 0.6, 0.2)
        remove_str = "Press E to remove turret"
        raster_x = 640 - (len(remove_str) * 4.5)
        
        glRasterPos2f(raster_x, 220)
        
        for i in range(0, len(remove_str), 1):
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(remove_str[i]))

    # 12. Deployable Feedback Message Popup (Bottom Center / above shop prompt)
    message_timer = getattr(config, "deployable_message_timer", 0)
    
    if message_timer > 0:
        msg_text = getattr(config, "deployable_message", "")
        msg_type = getattr(config, "deployable_message_type", "info")
        
        if msg_type == "error":
            glColor3f(1.0, 0.3, 0.3)
        else:
            glColor3f(0.2, 1.0, 0.4)
            
        raster_x = 640 - (len(msg_text) * 4.5)
        glRasterPos2f(raster_x, 190)
        
        for i in range(0, len(msg_text), 1):
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(msg_text[i]))
            
        config.deployable_message_timer = message_timer - 1

    # 13. Shop Proximity Prompts & Wave Warning HUD Overlays (Bottom/Center Screen)
    if getattr(config, "near_shop", False):
        if getattr(config, "wave_active", False):
            warning_timer = getattr(config, "shop_warning_timer", 0)
            
            if warning_timer > 0:
                glColor3f(1.0, 0.2, 0.2)
                warning_str = "Shop not available during wave attack!"
                raster_x = 640 - (len(warning_str) * 4.5)
                glRasterPos2f(raster_x, 150)
                
                for i in range(0, len(warning_str), 1):
                    glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(warning_str[i]))
        else:
            glColor3f(1.0, 1.0, 0.0)
            prompt_str = "Press F or B to access Shop"
            raster_x = 640 - (len(prompt_str) * 4.5)
            glRasterPos2f(raster_x, 150)
            
            for i in range(0, len(prompt_str), 1):
                glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(prompt_str[i]))

    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()