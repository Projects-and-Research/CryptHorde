import core.config as config


def update_hazard_animations(dt=0.016):
    # --- 1. Spiked Floor Trap Animation Logic ---
    # Cycle: 1 second up, 4 seconds down = 5 seconds total cycle (300 frames at 60fps equivalent)
    if not hasattr(config, "spike_timer"):
        config.spike_timer = 0.0

    # Accumulate time using delta time (dt in seconds)
    config.spike_timer += dt
    cycle_duration = 5.0  # 5 seconds total cycle

    if config.spike_timer >= cycle_duration:
        config.spike_timer = 0.0

    # First 1.0 second spikes are active/up, remaining 4 seconds they are retracted/down
    if config.spike_timer <= 1.0:
        config.hazard_spikes_active = True
    else:
        config.hazard_spikes_active = False

    # --- 2. Rotating Magic Beam Animation Logic ---
    # Continuous rotation independent of FPS using dt
    if not hasattr(config, "beam_rotation_angle"):
        config.beam_rotation_angle = 0.0

    # Rotation speed: e.g., 90 degrees per second
    rotation_speed = 90.0
    config.beam_rotation_angle += rotation_speed * dt

    # Keep angle bounded between 0 and 360 degrees
    if config.beam_rotation_angle >= 360.0:
        config.beam_rotation_angle -= 360.0