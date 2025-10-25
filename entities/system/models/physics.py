from dataclasses import dataclass

@dataclass
class Physics:
    gravity: float = 9.81
    friction: float = 0.1

    # future parameters --->
    air_resistance: float = 0.01
    bounce_coefficient: float = 0.5
    mass: float = 1.0
    inertia: float = 1.0
    drag_coefficient: float = 0.47
    terminal_velocity: float = 53.0  # Approximate terminal velocity in m/s for a human
    time_step: float = 0.016  # Approximate time step for 60 FPS
    collision_tolerance: float = 0.01
    sleep_threshold: float = 0.1
    max_velocity: float = 100.0
    min_velocity: float = 0.0
    wind_resistance: float = 0.02
    water_resistance: float = 0.03
    buoyancy: float = 1.0
    elasticity: float = 0.3
    pressure: float = 101.325  # kPa at sea level
    temperature: float = 20.0  # Celsius
    humidity: float = 50.0  # Percentage
    light_intensity: float = 1.0  # Arbitrary units
    sound_speed: float = 343.0  # m/s in air at 20 degrees Celsius
    magnetic_field: float = 0.00005  # Tesla, approximate Earth's magnetic field
    electric_field: float = 0.0  # V/m
    radiation_level: float = 0.0  # Arbitrary units
    viscosity: float = 0.001  # Pa·s for water at room temperature
    surface_tension: float = 0.0728  # N/m for water at room temperature
    cohesion: float = 0.5  # Arbitrary units
    adhesion: float = 0.5  # Arbitrary units
    turbulence: float = 0.1  # Arbitrary units
    laminar_flow: float = 0.9  # Arbitrary units
    convection: float = 0.1  # Arbitrary units
    conduction: float = 0.5  # Arbitrary units
    radiation: float = 0.2  # Arbitrary units
    phase_change_temp: float = 0.0  # Celsius for water
    melting_point: float = 0.0  # Celsius for water
    boiling_point: float = 100.0  # Celsius for water
    sublimation_point: float = -78.5  # Celsius for dry ice
    deposition_point: float = -78.5  # Celsius for dry ice
    crystallization_point: float = 0.0  # Celsius for water
    vaporization_point: float = 100.0  # Celsius for water
    condensation_point: float = 100.0  # Celsius for water
    latent_heat_fusion: float = 334.0  # kJ/kg for water
    latent_heat_vaporization: float = 2260.0  # kJ/kg
    latent_heat_sublimation: float = 2834.0  # kJ/kg for dry ice
    latent_heat_deposition: float = 2834.0  # kJ/kg for dry ice
    latent_heat_crystallization: float = 334.0  # kJ/kg for wate