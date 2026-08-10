import math
import animations.weapon_anims as weapon_anims
import behaviors.deployable_logic as deployable_logic
import core.config as config
import core.sound as sound
import entities.projectile_models as projectile_models


def handle_weapon_input(mouse_pressed, key_pressed=None):
    # If reloading, block new input
    if config.reload_timer > 0:
        return

    # Handle MB1 Press / Hold (Charging for Staff, Magic Hand, & Bow)
    if mouse_pressed:
        if not config.mb1_pressed:
            config.mb1_pressed = True
            config.charge_time = 0.0

            # Play bow string pull sound when first holding down the bow (only if ammo available)
            if config.current_weapon == 3:
                arrows = getattr(config, "player_arrows", 0)
                if arrows > 0:
                    sound.play_bow_draw()
    else:
        # MB1 Released - Fire Weapon if it was previously held/pressed
        if config.mb1_pressed:
            fire_current_weapon()
            config.mb1_pressed = False
            config.charge_time = 0.0


def fire_current_weapon():
    # Weapon 0: Arcane Staff (Longer MB1 hold = bigger, higher-damage ball, AOE)
    # Level 1: 100 max damage | Level 2: 150 max damage
    if config.current_weapon == 0:
        mana_cost = 15.0
        if getattr(config, "overdrive_active", False):
            mana_cost = 0.0  # Mana overdrive makes magic free

        if config.player_mana >= mana_cost:
            config.player_mana -= mana_cost
            sound.play_shoot_sound(0)

            charge_ratio = min(1.0, config.charge_time / 90.0)

            # Retrieve dynamic staff level from config
            staff_lvl = getattr(config, "staff_level", 1)

            # Damage: Level 1 ranges from 25 to 100. Level 2 ranges from 30 to 150.
            if staff_lvl >= 2:
                damage = 30.0 + (charge_ratio * 120.0)  # Max 150 at level 2
                radius = 3.5 + (charge_ratio * 4.5)
            else:
                damage = min(100.0, 20.0 + (charge_ratio * 80.0))  # Strictly capped at 100 max at level 1
                radius = 3.0 + (charge_ratio * 4.0)

            projectile_models.create_projectile(
                config.player_x,
                config.player_y,
                config.eye_z,
                config.player_angle,
                config.player_pitch,
                speed=18.0,
                damage=damage,
                p_type="magic_ball",
                radius=radius,
                is_aoe=True,
            )
            weapon_anims.trigger_thrust(5.0)

    # Weapon 1: Magic From Hand (Longer MB1 hold = bigger, higher-damage magic)
    # Level 1: 40 max damage | Level 2: 80 max damage | Level 3: 100 max damage
    elif config.current_weapon == 1:
        mana_cost = 10.0
        if getattr(config, "overdrive_active", False):
            mana_cost = 0.0

        if config.player_mana >= mana_cost:
            config.player_mana -= mana_cost
            sound.play_shoot_sound(1)

            charge_ratio = min(1.0, config.charge_time / 90.0)

            # Retrieve dynamic hand level from config
            hand_lvl = getattr(config, "hand_level", 1)

            # Damage scaling based on levels 1, 2, and 3
            if hand_lvl >= 3:
                damage = 30.0 + (charge_ratio * 70.0)   # Max 100 at level 3
            elif hand_lvl == 2:
                damage = 20.0 + (charge_ratio * 60.0)   # Max 80 at level 2
            else:
                damage = 10.0 + (charge_ratio * 30.0)   # Max 40 at level 1

            radius = 2.5 + (charge_ratio * 2.5)

            projectile_models.create_projectile(
                config.player_x,
                config.player_y,
                config.eye_z,
                config.player_angle,
                config.player_pitch,
                speed=22.0,
                damage=damage,
                p_type="magic_hand",
                radius=radius,
                is_aoe=False,
            )
            weapon_anims.trigger_thrust(4.0)

    # Weapon 2: Crossbow (Very slow reload, instant fire, high accuracy)
    # Level 1: 75 damage | Level 2: 100 damage | Level 3: 150 damage
    elif config.current_weapon == 2:
        # Strictly block firing if crossbow hasn't been reloaded yet
        if not getattr(config, "crossbow_ready", True):
            sound.play_no_ammo()
            return

        arrows = getattr(config, "player_arrows", 0)

        if arrows > 0:
            config.player_arrows = arrows - 1
            config.crossbow_ready = False  # Lock firing until explicitly reloaded

            sound.play_shoot_sound(2)
            
            # Retrieve dynamic crossbow level from config
            crossbow_lvl = getattr(config, "crossbow_level", 1)

            # Explicit damage per level
            if crossbow_lvl >= 3:
                damage = 150.0
                reload_ticks = 100
            elif crossbow_lvl == 2:
                damage = 100.0
                reload_ticks = 140
            else:
                damage = 75.0
                reload_ticks = 180

            projectile_models.create_projectile(
                config.player_x,
                config.player_y,
                config.eye_z,
                config.player_angle,
                config.player_pitch,
                speed=35.0,
                damage=damage,
                p_type="bolt",
                radius=2.0,
                is_aoe=False,
            )

            weapon_anims.trigger_reload(reload_ticks)
            weapon_anims.trigger_recoil(8.0)
        else:
            sound.play_no_ammo()

    # Weapon 3: Bow (Fast reload, hold for tension, medium damage, 3 levels)
    # Damage upgrades same as hand magic (Level 1: 40 max, Level 2: 80 max, Level 3: 100 max)
    elif config.current_weapon == 3:
        arrows = getattr(config, "player_arrows", 0)

        if arrows > 0:
            config.player_arrows = arrows - 1

            sound.play_shoot_sound(3)
            
            # Retrieve dynamic bow level from config
            bow_lvl = getattr(config, "bow_level", 1)

            charge_ratio = min(1.0, config.charge_time / 90.0)

            # Same damage progression as hand magic
            if bow_lvl >= 3:
                damage = 30.0 + (charge_ratio * 70.0)   # Max 100 at level 3
            elif bow_lvl == 2:
                damage = 20.0 + (charge_ratio * 60.0)   # Max 80 at level 2
            else:
                damage = 10.0 + (charge_ratio * 30.0)   # Max 40 at level 1

            speed = 20.0 + (charge_ratio * 15.0)

            projectile_models.create_projectile(
                config.player_x,
                config.player_y,
                config.eye_z,
                config.player_angle,
                config.player_pitch,
                speed=speed,
                damage=damage,
                p_type="arrow",
                radius=1.5,
                is_aoe=False,
            )
            weapon_anims.trigger_reload(20)  # Fast reload
            weapon_anims.trigger_recoil(4.0)
        else:
            sound.play_no_ammo()


def update_weapons():
    # Accumulate charge time while holding down left click
    if getattr(config, "mb1_pressed", False):
        if config.current_weapon in [0, 1, 3]:
            config.charge_time += 1.0
            if config.charge_time > 90.0:
                config.charge_time = 90.0