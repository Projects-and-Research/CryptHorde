import math

# Window Resolution
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Arena Boundaries
GRID_LENGTH = 600
BOUND_LIMIT = 570

# Game States
STATE_MAIN_MENU = 0
STATE_PLAYING = 1
STATE_PAUSED = 2
STATE_SHOP = 3
STATE_GAME_OVER = 4
current_state = STATE_MAIN_MENU

# Player Attributes
player_x = 0.0
player_y = 0.0
player_z = 0.0
player_angle = 90.0  # Facing direction in degrees
player_pitch = 0.0

player_health = 100
max_health = 100
player_mana = 100.0
max_mana = 100.0
player_gold = 50

# Player Buffs & Timers
overdrive_timer = 0
invincible_timer = 0
overdrive_active = False
invincible_active = False

# Camera Settings (FPS)
eye_z = 35.0
first_person = True

# Camera View Vectors
dir_x = 0.0
dir_y = 0.0
dir_z = 0.0

# Weapon Definitions & Inventory
# 0: Arcane Staff, 1: Magic Hand, 2: Crossbow, 3: Bow
current_weapon = 0
weapon_names = ["Arcane Staff", "Magic Hand", "Crossbow", "Bow"]
weapon_levels = [1, 1, 1, 1]

# Individual Weapon Levels for explicit attribute access
staff_level = 1
crossbow_level = 1
hand_level = 1
bow_level = 1

# Deployable Shooter Configuration
deployable_level = 1      # Level from 1 to 5
max_deployables = 1       # Starts at 1, can buy 1 extra from shop (max 2)

# Fire & Reload Controls
mb1_pressed = False
charge_time = 0.0
reload_timer = 0
crossbow_ready = True  # Crossbow firing lock state

# Dodge Cooldown Timer
dodge_cooldown_timer = 0.0

# Procedural Animation Offsets
recoil_offset = 0.0
weapon_y_offset = 0.0
weapon_down_offset = 0.0
weapon_forward_offset = 0.0
view_bob = 0.0
bob_step = 0.0

# Ability Stocks & Consumables
deployable_stock = 1
health_elixir_stock = 2

# Wave & Game Progression
wave_number = 1
wave_timer = 0
enemies_remaining = 0
game_score = 0
score = 0

# Shop Proximity & Wave Activity Control
near_shop = False
wave_active = False  # True during active combat waves, False during breaks
shop_open = False    # Tracks if the shop menu interface is currently open

# Dynamic Entity Containers
player_projectiles = []  # Player magic balls, bolts, and arrows
bullets = player_projectiles  # Alias compatibility if needed elsewhere
enemy_arrows = []         # Archer enemy arrows
projectiles = []          # General projectiles list
enemies = []              # Active enemies (Archer, Regular, Heavy, Sage)
runes = []                # Pickups (Health/Mana/Invincibility)
pickups = runes           # Alias for runes
traps = []                # Spiked floor hazards
spiked_traps = traps      # Alias for traps
hazards = traps           # Alias for hazards
deployables = []          # Deployable turrets/barriers
shops = []                # Active shops
particles = []            # Visual particle effects

# Sage Enemy Aura Settings
sage_heal_radius = 150
sage_buff_radius = 150


def init_game():
    global current_state, score, game_score, player_health, player_mana, player_gold
    global player_x, player_y, player_z, player_angle, player_pitch
    global overdrive_timer, invincible_timer, overdrive_active, invincible_active
    global current_weapon, reload_timer, mb1_pressed, charge_time, crossbow_ready
    global wave_number, enemies_remaining, near_shop, wave_active, shop_open
    global player_projectiles, enemy_arrows, projectiles, enemies
    global runes, traps, deployables, shops, particles
    global staff_level, crossbow_level, hand_level, bow_level, weapon_levels
    global deployable_level, max_deployables

    current_state = STATE_PLAYING
    score = 0
    game_score = 0
    player_health = max_health
    player_mana = max_mana
    player_gold = 50
    player_x = 0.0
    player_y = 0.0
    player_z = 0.0
    player_angle = 90.0
    player_pitch = 0.0
    overdrive_timer = 0
    invincible_timer = 0
    overdrive_active = False
    invincible_active = False
    current_weapon = 0
    reload_timer = 0
    mb1_pressed = False
    charge_time = 0.0
    crossbow_ready = True
    wave_number = 1
    wave_timer = 0
    enemies_remaining = 0
    near_shop = False
    wave_active = False
    shop_open = False

    staff_level = 1
    crossbow_level = 1
    hand_level = 1
    bow_level = 1
    weapon_levels = [1, 1, 1, 1]

    deployable_level = 1
    max_deployables = 1

    player_projectiles.clear()
    enemy_arrows.clear()
    projectiles.clear()
    enemies.clear()
    runes.clear()
    traps.clear()
    deployables.clear()
    shops.clear()
    particles.clear()