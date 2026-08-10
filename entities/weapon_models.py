from OpenGL.GL import *
from OpenGL.GLU import *
import math
import core.config as config
import entities.player_model as player_model


def draw_cylinder_between(quad, x1, y1, z1, x2, y2, z2, radius_start, radius_end, slices=10):
    """
    Draws a solid cylinder connecting two arbitrary 3D points.
    Used to build curved shapes (bow limbs, crossbow arms) out of short straight segments,
    since gluCylinder on its own can only draw a straight tube along its local Z axis.
    """

    direction_x = x2 - x1
    direction_y = y2 - y1
    direction_z = z2 - z1

    segment_length = math.sqrt(direction_x * direction_x + direction_y * direction_y + direction_z * direction_z)

    if segment_length < 0.0001:
        return

    glPushMatrix()
    glTranslatef(x1, y1, z1)

    if abs(direction_z) < 0.9999 * segment_length:
        rotation_axis_x = -direction_y
        rotation_axis_y = direction_x
        rotation_axis_z = 0.0
        rotation_angle = math.degrees(math.acos(direction_z / segment_length))
        glRotatef(rotation_angle, rotation_axis_x, rotation_axis_y, rotation_axis_z)
    elif direction_z < 0.0:
        glRotatef(180.0, 1.0, 0.0, 0.0)

    gluCylinder(quad, radius_start, radius_end, segment_length, slices, 1)

    glPopMatrix()


def build_arc_points(start_x, start_y, start_z, end_x, end_y, end_z, bulge_amount, bulge_axis, segment_count):
    """
    Returns a list of points approximating a curved arc between two endpoints.
    bulge_axis (e.g. (0, 0, -1)) controls which direction the middle of the arc bulges towards.
    """

    points = []

    for i in range(segment_count + 1):
        t = float(i) / float(segment_count)

        base_x = start_x + (end_x - start_x) * t
        base_y = start_y + (end_y - start_y) * t
        base_z = start_z + (end_z - start_z) * t

        bulge_factor = math.sin(t * math.pi) * bulge_amount

        point_x = base_x + bulge_axis[0] * bulge_factor
        point_y = base_y + bulge_axis[1] * bulge_factor
        point_z = base_z + bulge_axis[2] * bulge_factor

        points.append((point_x, point_y, point_z))

    return points


def draw_arc(quad, points, radius_start, radius_end):
    point_count = len(points)

    for i in range(point_count - 1):
        segment_t_start = float(i) / float(point_count - 1)
        segment_t_end = float(i + 1) / float(point_count - 1)

        segment_radius_start = radius_start + (radius_end - radius_start) * segment_t_start
        segment_radius_end = radius_start + (radius_end - radius_start) * segment_t_end

        point_a = points[i]
        point_b = points[i + 1]

        draw_cylinder_between(
            quad,
            point_a[0], point_a[1], point_a[2],
            point_b[0], point_b[1], point_b[2],
            segment_radius_start, segment_radius_end
        )


def draw_arcane_staff():
    quad = gluNewQuadric()

    # Grip pulled in close to the camera (natural resting point for hands later), tip extended
    # much further out so the shaft reads as a proper full-length staff, not a short wand.
    # Shifted towards the bottom-right corner so it doesn't dominate the center of the screen.
    grip_point = (1.4, -1.5, 1)
    tip_point = (0.7, -0.3, -5.0)

    glColor3f(0.35, 0.22, 0.10)
    draw_cylinder_between(
        quad,
        grip_point[0], grip_point[1], grip_point[2],
        tip_point[0], tip_point[1], tip_point[2],
        0.26, 0.18
    )

    # Push the orb a bit further out past the physical rod tip, along the same grip-to-tip
    # direction, so it has room to grow while charging without clipping into the shaft
    direction_x = tip_point[0] - grip_point[0]
    direction_y = tip_point[1] - grip_point[1]
    direction_z = tip_point[2] - grip_point[2]
    direction_length = math.sqrt(direction_x * direction_x + direction_y * direction_y + direction_z * direction_z)

    orb_gap = 0.5
    orb_x = tip_point[0] + (direction_x / direction_length) * orb_gap
    orb_y = tip_point[1] + (direction_y / direction_length) * orb_gap
    orb_z = tip_point[2] + (direction_z / direction_length) * orb_gap

    glPushMatrix()
    glTranslatef(orb_x, orb_y, orb_z)

    orb_scale = 0.6
    if config.mb1_pressed and config.current_weapon == 0:
        orb_scale += min(config.charge_time * 0.03, 1.5)

    glColor3f(0.75, 0.25, 1.0)
    gluSphere(quad, orb_scale, 16, 16)

    glColor3f(0.9, 0.65, 1.0)
    gluSphere(quad, orb_scale * 0.5, 12, 12)

    glPopMatrix()


def draw_magic_hand():
    quad = gluNewQuadric()

    # Just the floating energy orb here - hand geometry is handled separately in player_model.py
    glPushMatrix()
    glTranslatef(0.3, -0.2, -1.3)

    orb_scale = 0.6
    if config.mb1_pressed and config.current_weapon == 1:
        orb_scale += min(config.charge_time * 0.03, 1.4)

    glColor3f(0.25, 0.6, 1.0)
    gluSphere(quad, orb_scale, 14, 14)

    glColor3f(0.7, 0.85, 1.0)
    gluSphere(quad, orb_scale * 0.5, 10, 10)

    glPopMatrix()


def draw_crossbow():
    quad = gluNewQuadric()

    # Solid stock/body running back towards the grip - a rifle-like straight tube, not curved
    glColor3f(0.36, 0.22, 0.10)
    glPushMatrix()
    glTranslatef(0.0, 0.0, 3.5)
    glRotatef(180.0, 0.0, 1.0, 0.0)
    gluCylinder(quad, 0.50, 0.42, 6.0, 10, 4)
    glPopMatrix()

    # Metal rail / barrel section towards the front
    glColor3f(0.22, 0.22, 0.25)
    glPushMatrix()
    glTranslatef(0.0, 0.15, -2.0)
    glRotatef(180.0, 0.0, 1.0, 0.0)
    gluCylinder(quad, 0.20, 0.15, 2.2, 8, 4)
    glPopMatrix()

    # Rigid horizontal crossbar limbs - straight, not curved, so this reads as a crossbow rather than a bow
    glColor3f(0.5, 0.5, 0.55)
    glPushMatrix()
    glTranslatef(0.0, 0.15, -3.0)
    glRotatef(90.0, 0.0, 1.0, 0.0)
    gluCylinder(quad, 0.16, 0.08, 3.4, 8, 4)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.0, 0.15, -3.0)
    glRotatef(-90.0, 0.0, 1.0, 0.0)
    gluCylinder(quad, 0.16, 0.08, 3.4, 8, 4)
    glPopMatrix()

    # Taut string spanning the two crossbar tips
    glColor3f(0.85, 0.85, 0.85)
    glLineWidth(2.0)
    glBegin(GL_LINES)
    glVertex3f(3.4, 0.15, -3.0)
    glVertex3f(0.0, 0.15, -1.7)
    glVertex3f(-3.4, 0.15, -3.0)
    glVertex3f(0.0, 0.15, -1.7)
    glEnd()


def draw_bow():
    quad = gluNewQuadric()

    grip_x = 0.0
    grip_y = -1.0
    grip_z = -1.4

    # Wooden grip at the center of the bow
    glColor3f(0.42, 0.26, 0.12)
    glPushMatrix()
    glTranslatef(grip_x, grip_y, grip_z)
    gluSphere(quad, 0.5, 8, 8)
    glPopMatrix()

    # Curved upper and lower limbs, bulging forward and tapering towards the tips.
    # Kept shorter than before (3.6 / -3.2 instead of the original 6.5 / -6.5) so the
    # whole bow fits inside the visible frame instead of the tip running off the top.
    upper_limb_points = build_arc_points(grip_x, grip_y, grip_z, grip_x, grip_y + 3.6, grip_z, 1.1, (0.0, 0.0, -1.0), 8)
    lower_limb_points = build_arc_points(grip_x, grip_y, grip_z, grip_x, grip_y - 3.2, grip_z, 1.1, (0.0, 0.0, -1.0), 8)

    glColor3f(0.5, 0.32, 0.15)
    draw_arc(quad, upper_limb_points, 0.30, 0.10)
    draw_arc(quad, lower_limb_points, 0.34, 0.10)

    upper_tip = upper_limb_points[-1]
    lower_tip = lower_limb_points[-1]

    # String pulls towards the camera as MB1 is held, simulating drawing the bow
    string_pull_z = grip_z
    if config.mb1_pressed and config.current_weapon == 3:
        string_pull_z += min(config.charge_time * 0.05, 2.2)

    glColor3f(0.9, 0.9, 0.9)
    glLineWidth(2.0)
    glBegin(GL_LINES)
    glVertex3f(upper_tip[0], upper_tip[1], upper_tip[2])
    glVertex3f(grip_x, grip_y, string_pull_z)

    glVertex3f(lower_tip[0], lower_tip[1], lower_tip[2])
    glVertex3f(grip_x, grip_y, string_pull_z)
    glEnd()

    # Arrow nocked against the string, visible while drawing back, pointing forward through the grip
    if config.mb1_pressed and config.current_weapon == 3:
        glColor3f(0.42, 0.28, 0.12)
        glPushMatrix()
        glTranslatef(grip_x, grip_y, string_pull_z)
        glRotatef(180.0, 0.0, 1.0, 0.0)
        gluCylinder(quad, 0.08, 0.08, 5.0, 6, 3)
        glPopMatrix()


def draw_current_weapon():
    glPushMatrix()

    glLoadIdentity()

    # Base view-space position, reactive to recoil, reload lowering, and view bob.
    # Pulled back to -3.5 (instead of the original -2.0) so weapons sit at a consistent,
    # sane distance from the camera instead of being magnified right up against it.
    glTranslatef(1.3, -1.6 + config.weapon_y_offset + config.view_bob, -3.5 + config.recoil_offset)
    player_model.draw_player_hands()

    # Shared forward tilt and rightward lean applied to all four weapons
    glRotatef(3.0, 1.0, 0.0, 0.0)
    glRotatef(-12.0, 0.0, 0.0, 1.0)

    if config.current_weapon == 0:
        draw_arcane_staff()
    elif config.current_weapon == 1:
        draw_magic_hand()
    elif config.current_weapon == 2:
        draw_crossbow()
    elif config.current_weapon == 3:
        draw_bow()

    glPopMatrix()