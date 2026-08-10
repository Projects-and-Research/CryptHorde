from OpenGL.GL import *
from OpenGL.GLUT import *
import core.config as config


def draw_text(x, y, text, r=1.0, g=1.0, b=1.0, font=GLUT_BITMAP_9_BY_15):
    glColor3f(r, g, b)
    glRasterPos2f(x, y)

    for i in range(0, len(text), 1):
        glutBitmapCharacter(font, ord(text[i]))


def draw_shop_ui():
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, 1280, 0, 720, -1, 1)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glDisable(GL_DEPTH_TEST)

    # 1. Dark background overlay to dim the game (1280x720)
    glColor3f(0.0, 0.0, 0.05)
    glBegin(GL_QUADS)
    glVertex2f(0, 0)
    glVertex2f(1280, 0)
    glVertex2f(1280, 720)
    glVertex2f(0, 720)
    glEnd()

    # 2. Main Shop Interface Window - Enlarged and Centered
    glColor3f(0.15, 0.15, 0.2)
    glBegin(GL_QUADS)
    glVertex2f(90, 50)
    glVertex2f(1190, 50)
    glVertex2f(1190, 680)
    glVertex2f(90, 680)
    glEnd()

    # Shop Window Border Accent (Using GL_LINES)
    glColor3f(0.8, 0.7, 0.2)
    glLineWidth(3.0)
    glBegin(GL_LINES)
    glVertex2f(90, 50)
    glVertex2f(1190, 50)

    glVertex2f(90, 680)
    glVertex2f(1190, 680)

    glVertex2f(90, 50)
    glVertex2f(90, 680)

    glVertex2f(1190, 50)
    glVertex2f(1190, 680)
    glEnd()

    # Title Header and Player Gold Display
    draw_text(480, 635, "MAGIC & WEAPON SHOP", 1.0, 0.85, 0.2, GLUT_BITMAP_TIMES_ROMAN_24)

    if hasattr(config, "player_gold"):
        gold_val = config.player_gold
    elif hasattr(config, "player_money"):
        gold_val = config.player_money
    else:
        gold_val = 0

    draw_text(130, 635, "GOLD: " + str(gold_val), 0.2, 0.9, 0.2, GLUT_BITMAP_9_BY_15)

    # Helper getters for weapon levels & deployable specs
    staff_lvl = getattr(config, "staff_level", 1)
    crossbow_lvl = getattr(config, "crossbow_level", 1)
    hand_lvl = getattr(config, "hand_level", 1)
    bow_lvl = getattr(config, "bow_level", 1)
    
    turret_lvl = getattr(config, "deployable_level", 1)
    max_turrets = getattr(config, "max_deployables", 1)

    # Dynamic pricing strings
    staff_cost_str = "MAX" if staff_lvl >= 2 else "Cost: 5000"
    crossbow_cost_str = "MAX" if crossbow_lvl >= 3 else ("Cost: 4000" if crossbow_lvl == 2 else "Cost: 2000")
    hand_cost_str = "MAX" if hand_lvl >= 3 else ("Cost: 3000" if hand_lvl == 2 else "Cost: 1500")
    bow_cost_str = "MAX" if bow_lvl >= 3 else ("Cost: 2000" if bow_lvl == 2 else "Cost: 1000")
    
    # Turret Upgrade Pricing: Lvl 2=500, Lvl 3=1500, Lvl 4=3500, Lvl 5=8000
    if turret_lvl >= 5:
        turret_lvl_cost_str = "MAX"
    elif turret_lvl == 4:
        turret_lvl_cost_str = "Cost: 8000"
    elif turret_lvl == 3:
        turret_lvl_cost_str = "Cost: 3500"
    elif turret_lvl == 2:
        turret_lvl_cost_str = "Cost: 1500"
    else:
        turret_lvl_cost_str = "Cost: 500"

    # Turret Slot Pricing: 2nd slot = 5000, 3rd slot = 15000
    if max_turrets >= 3:
        turret_slot_cost_str = "MAX"
    elif max_turrets == 2:
        turret_slot_cost_str = "Cost: 15000"
    else:
        turret_slot_cost_str = "Cost: 5000"

    # Row 3: Consumables (4 items)
    c_names = ["Health Elixir", "Mana Potion", "Invincibility", "Ammo Pack"]
    c_costs = ["Cost: 50", "Cost: 50", "Cost: 150", "Cost: 30"]
    c_descs = ["+50 Health", "+50 Mana", "2 Min Shield", "+20 Arrows"]

    for i in range(0, 4, 1):
        box_x = 130 + (i * 265)

        glColor3f(0.2, 0.2, 0.25)
        glBegin(GL_QUADS)
        glVertex2f(box_x, 90)
        glVertex2f(box_x + 240, 90)
        glVertex2f(box_x + 240, 260)
        glVertex2f(box_x, 260)
        glEnd()

        glColor3f(0.4, 0.4, 0.45)
        glLineWidth(2.0)
        glBegin(GL_LINES)
        glVertex2f(box_x, 90)
        glVertex2f(box_x + 240, 90)
        glVertex2f(box_x, 260)
        glVertex2f(box_x + 240, 260)
        glVertex2f(box_x, 90)
        glVertex2f(box_x, 260)
        glVertex2f(box_x + 240, 90)
        glVertex2f(box_x + 240, 260)
        glEnd()

        draw_text(box_x + 30, 230, c_names[i], 0.9, 0.9, 0.9, GLUT_BITMAP_9_BY_15)
        draw_text(box_x + 70, 175, c_costs[i], 1.0, 0.8, 0.2, GLUT_BITMAP_9_BY_15)
        draw_text(box_x + 55, 120, c_descs[i], 0.5, 0.8, 1.0, GLUT_BITMAP_8_BY_13)

    # Row 2: Weapon Upgrades (4 items)
    w_names = ["Arcane Staff", "Crossbow", "Hand Magic", "Bow"]
    w_costs = [staff_cost_str, crossbow_cost_str, hand_cost_str, bow_cost_str]
    w_levels = [
        "Lvl: " + str(staff_lvl) + "/2",
        "Lvl: " + str(crossbow_lvl) + "/3",
        "Lvl: " + str(hand_lvl) + "/3",
        "Lvl: " + str(bow_lvl) + "/3",
    ]

    for i in range(0, 4, 1):
        box_x = 130 + (i * 265)

        glColor3f(0.22, 0.18, 0.28)
        glBegin(GL_QUADS)
        glVertex2f(box_x, 285)
        glVertex2f(box_x + 240, 285)
        glVertex2f(box_x + 240, 455)
        glVertex2f(box_x, 455)
        glEnd()

        glColor3f(0.6, 0.4, 0.7)
        glLineWidth(2.0)
        glBegin(GL_LINES)
        glVertex2f(box_x, 285)
        glVertex2f(box_x + 240, 285)
        glVertex2f(box_x, 455)
        glVertex2f(box_x + 240, 455)
        glVertex2f(box_x, 285)
        glVertex2f(box_x, 455)
        glVertex2f(box_x + 240, 285)
        glVertex2f(box_x + 240, 455)
        glEnd()

        draw_text(box_x + 30, 425, w_names[i], 1.0, 0.9, 0.4, GLUT_BITMAP_9_BY_15)
        draw_text(box_x + 70, 375, w_levels[i], 0.8, 1.0, 0.8, GLUT_BITMAP_9_BY_15)
        draw_text(box_x + 55, 320, w_costs[i], 1.0, 0.6, 0.2, GLUT_BITMAP_9_BY_15)

    # Row 1: Turret Upgrades & Capacity (2 items on the left/middle)
    t_names = ["Turret Upgrade", "Max Turret Slots"]
    t_costs = [turret_lvl_cost_str, turret_slot_cost_str]
    t_levels = [
        f"Lvl: {turret_lvl}/5",
        f"Slots: {max_turrets}/3"
    ]

    for i in range(0, 2, 1):
        box_x = 130 + (i * 265)

        glColor3f(0.18, 0.25, 0.28)
        glBegin(GL_QUADS)
        glVertex2f(box_x, 480)
        glVertex2f(box_x + 240, 480)
        glVertex2f(box_x + 240, 610)
        glVertex2f(box_x, 610)
        glEnd()

        glColor3f(0.3, 0.7, 0.6)
        glLineWidth(2.0)
        glBegin(GL_LINES)
        glVertex2f(box_x, 480)
        glVertex2f(box_x + 240, 480)
        glVertex2f(box_x, 610)
        glVertex2f(box_x + 240, 610)
        glVertex2f(box_x, 480)
        glVertex2f(box_x, 610)
        glVertex2f(box_x + 240, 480)
        glVertex2f(box_x + 240, 610)
        glEnd()

        draw_text(box_x + 30, 580, t_names[i], 0.6, 1.0, 0.9, GLUT_BITMAP_9_BY_15)
        draw_text(box_x + 70, 540, t_levels[i], 0.9, 1.0, 1.0, GLUT_BITMAP_9_BY_15)
        draw_text(box_x + 55, 500, t_costs[i], 1.0, 0.6, 0.2, GLUT_BITMAP_9_BY_15)

    # Exit Instruction Box
    glColor3f(0.4, 0.15, 0.15)
    glBegin(GL_QUADS)
    glVertex2f(720, 480)
    glVertex2f(1150, 480)
    glVertex2f(1150, 610)
    glVertex2f(720, 610)
    glEnd()

    draw_text(760, 545, "PRESS P / F / B TO EXIT SHOP", 1.0, 1.0, 1.0, GLUT_BITMAP_9_BY_15)

    # Purchase Feedback Message & Insufficient Funds Warning Popup
    shop_msg_timer = getattr(config, "shop_message_timer", 0)
    if shop_msg_timer > 0:
        shop_msg = getattr(config, "shop_message", "")
        msg_status = getattr(config, "shop_message_type", "success")

        if msg_status == "error":
            glColor3f(1.0, 0.2, 0.2)  # Red for insufficient funds
        else:
            glColor3f(0.2, 1.0, 0.3)  # Green for successful purchase confirmation

        raster_x = 640 - (len(shop_msg) * 4.5)
        draw_text(raster_x, 25, shop_msg, 1.0, 1.0, 1.0, GLUT_BITMAP_9_BY_15)
        config.shop_message_timer = shop_msg_timer - 1

    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()