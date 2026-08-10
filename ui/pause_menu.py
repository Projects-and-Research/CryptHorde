from OpenGL.GL import *
from OpenGL.GLUT import *
import core.config as config


def draw_text(x, y, text):
    glRasterPos2f(x, y)
    i = 0
    while i < len(text):
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(text[i]))
        i += 1


def draw_pause_menu():
    # Switch to 2D orthographic projection over the existing frame using standard glOrtho (1280x720)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, 1280, 0, 720, -1, 1)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glDisable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)

    # Semi-transparent dark background tint overlay spanning 1280x720
    glColor3f(0.05, 0.05, 0.08)
    glBegin(GL_QUADS)
    glVertex2f(0, 0)
    glVertex2f(1280, 0)
    glVertex2f(1280, 720)
    glVertex2f(0, 720)
    glEnd()

    # Pause Menu Box - Centered for 1280x720
    glColor3f(0.2, 0.2, 0.25)
    glBegin(GL_QUADS)
    glVertex2f(440, 140)
    glVertex2f(840, 140)
    glVertex2f(840, 580)
    glVertex2f(440, 580)
    glEnd()

    # Pause Menu Border Accent
    glColor3f(0.6, 0.6, 0.7)
    glLineWidth(2.0)
    glBegin(GL_LINES)
    glVertex2f(440, 140)
    glVertex2f(840, 140)
    glVertex2f(440, 580)
    glVertex2f(840, 580)
    glVertex2f(440, 140)
    glVertex2f(440, 580)
    glVertex2f(840, 140)
    glVertex2f(840, 580)
    glEnd()

    # Title Text
    glColor3f(1.0, 1.0, 1.0)
    draw_text(575, 535, "GAME PAUSED")
    
    # Gather General Game Stats Info
    wave_val = str(getattr(config, "current_wave", 1))
    gold_val = str(getattr(config, "player_gold", getattr(config, "player_money", 0)))
    zombies_val = str(getattr(config, "zombies_remaining", getattr(config, "enemies_remaining", 0)))
    score_val = str(getattr(config, "score", 0))

    # Render Clean Two-Column Stats Block
    label_x = 490
    value_x = 730

    draw_text(label_x, 485, "Wave Count")
    draw_text(value_x, 485, wave_val)

    draw_text(label_x, 455, "Gold")
    draw_text(value_x, 455, gold_val)

    draw_text(label_x, 425, "Zombies Left")
    draw_text(value_x, 425, zombies_val)

    draw_text(label_x, 395, "Score")
    draw_text(value_x, 395, score_val)

    # Resume Instruction Box
    glColor3f(0.2, 0.4, 0.3)
    glBegin(GL_QUADS)
    glVertex2f(490, 260)
    glVertex2f(790, 260)
    glVertex2f(790, 320)
    glVertex2f(490, 320)
    glEnd()
    
    glColor3f(1.0, 1.0, 1.0)
    draw_text(565, 282, "Resume (Press P)")

    # Quit / Main Menu Instruction Box
    glColor3f(0.4, 0.2, 0.2)
    glBegin(GL_QUADS)
    glVertex2f(490, 175)
    glVertex2f(790, 175)
    glVertex2f(790, 235)
    glVertex2f(490, 235)
    glEnd()
    
    glColor3f(1.0, 1.0, 1.0)
    draw_text(560, 197, "Exit to Main Menu")

    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()