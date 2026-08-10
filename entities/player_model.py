from OpenGL.GL import *
from OpenGL.GLU import *
import math
import core.config as config


# Placeholder tones - plain sleeve + skin. Swap for real textures/materials later; for now
# these just make "arm" and "hand" read as distinct shapes at a glance.
SLEEVE_COLOR = (0.18, 0.18, 0.22)
SKIN_COLOR = (0.85, 0.70, 0.55)


def lerp_point(point_a, point_b, t):
    x = point_a[0] + (point_b[0] - point_a[0]) * t
    y = point_a[1] + (point_b[1] - point_a[1]) * t
    z = point_a[2] + (point_b[2] - point_a[2]) * t

    return (x, y, z)


def draw_cylinder_between(quad, x1, y1, z1, x2, y2, z2, radius_start, radius_end, slices=8):
    """
    Same trick as weapon_models.draw_cylinder_between: gluCylinder only draws along its
    local Z axis, so we translate/rotate to line that axis up with the two points we want
    to connect. Duplicated here rather than imported, because weapon_models.py already
    imports this module - importing it back the other way would create a circular import.
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


def draw_hand_at(quad, x, y, z, size=0.42):
    glPushMatrix()
    glTranslatef(x, y, z)

    glColor3f(*SKIN_COLOR)
    gluSphere(quad, size, 10, 10)

    glPopMatrix()


def draw_arm(quad, shoulder, hand, shoulder_radius=0.42, hand_radius=0.30, hand_size=0.42):
    """
    One straight sleeve segment from an off-screen shoulder anchor to the hand, capped
    with a hand sphere. Deliberately a single segment, no elbow bend - it's a placeholder,
    and at FPS viewmodel angles a single tapered cylinder reads fine as a foreshortened
    forearm.
    """

    glColor3f(*SLEEVE_COLOR)
    draw_cylinder_between(
        quad,
        shoulder[0], shoulder[1], shoulder[2],
        hand[0], hand[1], hand[2],
        shoulder_radius, hand_radius
    )
    draw_hand_at(quad, hand[0], hand[1], hand[2], size=hand_size)


def draw_player_model():
    for i in range(0, 1, 1):
        pass


# ---------------------------------------------------------------------------------------
# Per-weapon arm placement. Grip/tip/orb coordinates below are copied straight from the
# matching draw_*() functions in weapon_models.py so hands land exactly on the weapon
# regardless of how it's angled - keep these in sync if that geometry ever moves.
# ---------------------------------------------------------------------------------------

def _draw_arcane_staff_arms(quad):
    grip_point = (0, -1.5, 1.0)
    tip_point = (0.7, -0.3, -5.0)

    # Left hand reaches further up the shaft towards the tip and is fully extended, so we
    # see a proper left arm. Right hand stays back near the grip, tucked close to the body
    # - it's that short reach (not any occlusion trick) that keeps the right arm from
    # reading as visible.
    left_hand = lerp_point(grip_point, tip_point, 0.55)
    right_hand = lerp_point(grip_point, tip_point, 0.10)

    left_shoulder = (0.4, -3.6, 1.2)
    right_shoulder = (1.7, -2.1, 1.3)  # close to right_hand on purpose - short stub only

    draw_arm(quad, left_shoulder, left_hand, shoulder_radius=0.40, hand_radius=0.28)
    draw_arm(quad, right_shoulder, right_hand, shoulder_radius=0.34, hand_radius=0.26, hand_size=0.40)


def _draw_magic_hand_arms(quad):
    # Both arms now extend up into view from off-screen shoulder anchors to reach the
    # floating energy ball positions, maintaining full movement when charging MB1.
    orb_x, orb_y, orb_z = 0.3, -0.2, -1.3

    hand_pull = 0.0
    if config.mb1_pressed and config.current_weapon == 1:
        hand_pull = min(config.charge_time * 0.03, 0.9)

    main_hand = (orb_x, orb_y - 1.3, orb_z - 0.3 - hand_pull)
    support_hand = (orb_x - 0.9, orb_y - 0.75, orb_z + 0.35 - hand_pull)

    # Shoulders anchored off-screen bottom-right and bottom-left
    main_shoulder = (0.8, -3.8, 1.0)
    support_shoulder = (-1.2, -3.5, 1.2)

    draw_arm(quad, main_shoulder, main_hand, shoulder_radius=0.42, hand_radius=0.28, hand_size=0.40)
    draw_arm(quad, support_shoulder, support_hand, shoulder_radius=0.40, hand_radius=0.26, hand_size=0.38)


def _draw_crossbow_arms(quad):
    # The crossbow is big and held rifle-style tucked into the body, so only the left
    # arm/hand - gripping the stock near the trigger - shows at all.
    grip_point = (0.0, -0.35, -0.5)
    shoulder = (0.6, -3.5, -0.15)

    draw_arm(quad, shoulder, grip_point, shoulder_radius=0.44, hand_radius=0.30)


def _draw_bow_arms(quad):
    grip_x, grip_y, grip_z = 0.0, -1.0, -1.4

    # Left hand holds the riser at the bow's fixed grip point - a full, visible left arm.
    left_shoulder = (-0.6, -3.6, 1.0)
    draw_arm(quad, left_shoulder, (grip_x, grip_y, grip_z), shoulder_radius=0.42, hand_radius=0.28)

    # Right hand pulls the string using the exact same charge-based offset as the string
    # itself in draw_bow(). Right shoulder is anchored further down off-screen so a full,
    # distinct right sleeve arm is visible extending to the drawing hand.
    string_pull_z = grip_z
    if config.mb1_pressed and config.current_weapon == 3:
        string_pull_z += min(config.charge_time * 0.05, 2.2)

    right_hand = (grip_x, grip_y, string_pull_z)
    right_shoulder = (0.8, -3.6, string_pull_z + 0.8)

    draw_arm(quad, right_shoulder, right_hand, shoulder_radius=0.40, hand_radius=0.28, hand_size=0.40)


def draw_player_hands():
    quad = gluNewQuadric()

    current_weapon = getattr(config, "current_weapon", 0)

    if current_weapon == 0:
        _draw_arcane_staff_arms(quad)
    elif current_weapon == 1:
        _draw_magic_hand_arms(quad)
    elif current_weapon == 2:
        _draw_crossbow_arms(quad)
    elif current_weapon == 3:
        _draw_bow_arms(quad)