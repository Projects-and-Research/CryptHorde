from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import core.config as config


def render_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glRasterPos2f(x, y)
    i = 0
    while (i < len(text)):
        glutBitmapCharacter(font, ord(text[i]))
        i += 1


def draw_main_menu():
    glDisable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, 1280, 0, 720, -1, 1)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    # 1. Dark Atmospheric Background Panel (1280x720)
    glColor3f(0.08, 0.08, 0.12)
    glBegin(GL_QUADS)
    glVertex2f(0, 0)
    glVertex2f(1280, 0)
    glVertex2f(1280, 720)
    glVertex2f(0, 720)
    glEnd()

    # 2. Game Title Banner Box ("CryptHorde") - Centered
    glColor3f(0.4, 0.08, 0.7)
    glBegin(GL_QUADS)
    glVertex2f(380, 430)
    glVertex2f(900, 430)
    glVertex2f(900, 550)
    glVertex2f(380, 550)
    glEnd()

    # Title Border Accent Line (Using GL_LINES)
    glColor3f(0.8, 0.6, 0.2)
    glLineWidth(3.0)
    glBegin(GL_LINES)
    glVertex2f(380, 430)
    glVertex2f(900, 430)
    
    glVertex2f(900, 430)
    glVertex2f(900, 550)
    
    glVertex2f(900, 550)
    glVertex2f(380, 550)
    
    glVertex2f(380, 550)
    glVertex2f(380, 430)
    glEnd()

    # Title Text Inside Banner
    glColor3f(1.0, 1.0, 1.0)
    render_text(575, 482, "CryptHorde", GLUT_BITMAP_TIMES_ROMAN_24)

    # 3. Play Option Button Box ("Start") - Centered
    glColor3f(0.15, 0.5, 0.25)
    glBegin(GL_QUADS)
    glVertex2f(460, 260)
    glVertex2f(820, 260)
    glVertex2f(820, 330)
    glVertex2f(460, 330)
    glEnd()

    # Play Button Border (Using GL_LINES)
    glColor3f(0.3, 0.8, 0.4)
    glBegin(GL_LINES)
    glVertex2f(460, 260)
    glVertex2f(820, 260)
    
    glVertex2f(820, 260)
    glVertex2f(820, 330)
    
    glVertex2f(820, 330)
    glVertex2f(460, 330)
    
    glVertex2f(460, 330)
    glVertex2f(460, 260)
    glEnd()

    # Start Text Inside Play Button
    glColor3f(1.0, 1.0, 1.0)
    render_text(620, 288, "Start", GLUT_BITMAP_HELVETICA_18)

    # 4. Quit / Exit Instruction Box - Centered
    glColor3f(0.4, 0.15, 0.15)
    glBegin(GL_QUADS)
    glVertex2f(500, 150)
    glVertex2f(780, 150)
    glVertex2f(780, 210)
    glVertex2f(500, 210)
    glEnd()

    # Exit Text Inside Quit Button
    glColor3f(1.0, 1.0, 1.0)
    render_text(625, 172, "Exit", GLUT_BITMAP_HELVETICA_18)

    # Correctly restore matrix states
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()

    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glEnable(GL_DEPTH_TEST)