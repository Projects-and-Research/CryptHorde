import math
import core.config as config
 
 
def update_view_bob(dt):
    # Decay rate is in "units per second" now, matching the dt-scaled increment in
    # controls.py (config.bob_step += 5.0 * dt while moving). Previously this subtracted a
    # fixed 0.05 every single frame regardless of dt - at high frame rates that fixed
    # per-frame subtraction outpaced the dt-scaled increment, so bob_step got yanked back
    # towards 0 almost immediately even while actively moving, and the bob never built up.
    # Amplitude tuned for the current weapon_models.py coordinate scale (roughly 0.1 to 1.5
    # units). Start here and adjust to taste - now that the duplicate logic in weapon_anims.py
    # is gone, this is the only place controlling the bob amplitude.
    bob_amplitude = 0.2
    decay_rate_per_second = 3.0
 
    if config.bob_step > 0.0:
        config.view_bob = math.sin(config.bob_step) * bob_amplitude
 
        config.bob_step -= decay_rate_per_second * dt
        if config.bob_step < 0.0:
            config.bob_step = 0.0
            config.view_bob = 0.0
    else:
        config.view_bob = 0.0