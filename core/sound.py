import os

sound_enabled = False
sound_cache = {}

try:
    import pygame
    # Explicitly set frequency, size, channels, and buffer to guarantee driver compatibility
    pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
    pygame.mixer.init()
    sound_enabled = True
    print("Pygame mixer successfully initialized.")
except Exception as e:
    print(f"Pygame mixer initialization failed: {e}")
    sound_enabled = False


def preload_sounds():
    if not sound_enabled:
        return
    
    sound_files = [
        "fireball.mp3",
        "magic-spell.mp3",
        "crossbow-firing.mp3",
        "bow-release.mp3",
        "bow-loading.mp3",
        "hurt.mp3",
        "item-pickup.mp3",
        "no_ammo.mp3",
        "buy.mp3",
        "deployable_deploy.mp3",
        "deployable_fire.mp3"
    ]
    
    for filename in sound_files:
        filepath = os.path.join("assets", "sounds", filename)
        if os.path.exists(filepath):
            try:
                sound_cache[filename] = pygame.mixer.Sound(filepath)
            except Exception as e:
                print(f"Error preloading sound {filename}: {e}")
        else:
            print(f"Sound file not found during preload: {filepath}")


def play_sound(sound_name):
    if not sound_enabled:
        return

    if sound_name in sound_cache:
        try:
            sound_cache[sound_name].play()
        except Exception as e:
            print(f"Error playing sound {sound_name}: {e}")
    else:
        filepath = os.path.join("assets", "sounds", sound_name)
        if os.path.exists(filepath):
            try:
                snd = pygame.mixer.Sound(filepath)
                sound_cache[sound_name] = snd
                snd.play()
            except Exception as e:
                print(f"Error loading/playing fallback {sound_name}: {e}")
        else:
            print(f"Sound missing on play request: {filepath}")


def play_shoot_sound(weapon_type):
    # 0: Arcane Staff, 1: Magic Hand, 2: Crossbow, 3: Bow
    if weapon_type == 0:
        play_sound("fireball.mp3")
    elif weapon_type == 1:
        play_sound("magic-spell.mp3")
    elif weapon_type == 2:
        play_sound("crossbow-firing.mp3")
    elif weapon_type == 3:
        play_sound("bow-release.mp3")


def play_bow_draw():
    play_sound("bow-loading.mp3")


def play_hit_sound():
    play_sound("hurt.mp3")


def play_pickup_sound():
    play_sound("item-pickup.mp3")


def play_no_ammo():
    play_sound("no_ammo.mp3")