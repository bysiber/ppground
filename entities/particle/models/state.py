from dataclasses import dataclass, field
from typing import Tuple

@dataclass
class ParticleState:
    """Represents the dynamic state of a particle including motion properties."""
    
    # Motion properties
    velocity_x: float = 0.0
    velocity_y: float = 0.0
    velocity_z: float = 0.0
    
    acceleration_x: float = 0.0
    acceleration_y: float = 0.0
    acceleration_z: float = 0.0
    
    # Physical properties
    mass: float = 1.0
    radius: float = 5.0
    
    # Color (RGB)
    color: Tuple[int, int, int] = (255, 255, 255)
    
    # State flags
    is_active: bool = True
    is_static: bool = False  # Static particles don't move
    
    def get_velocity(self) -> Tuple[float, float, float]:
        """Returns velocity as a tuple."""
        return (self.velocity_x, self.velocity_y, self.velocity_z)
    
    def set_velocity(self, vx: float, vy: float, vz: float = 0.0) -> None:
        """Sets the velocity components."""
        self.velocity_x = vx
        self.velocity_y = vy
        self.velocity_z = vz
    
    def get_acceleration(self) -> Tuple[float, float, float]:
        """Returns acceleration as a tuple."""
        return (self.acceleration_x, self.acceleration_y, self.acceleration_z)
    
    def set_acceleration(self, ax: float, ay: float, az: float = 0.0) -> None:
        """Sets the acceleration components."""
        self.acceleration_x = ax
        self.acceleration_y = ay
        self.acceleration_z = az
    
    def apply_force(self, fx: float, fy: float, fz: float = 0.0) -> None:
        """Applies a force to the particle (F = ma, so a = F/m)."""
        if self.mass > 0 and not self.is_static:
            self.acceleration_x += fx / self.mass
            self.acceleration_y += fy / self.mass
            self.acceleration_z += fz / self.mass
    
    def reset_acceleration(self) -> None:
        """Resets acceleration to zero (call this each frame after applying forces)."""
        self.acceleration_x = 0.0
        self.acceleration_y = 0.0
        self.acceleration_z = 0.0
    
    def get_speed(self) -> float:
        """Returns the magnitude of velocity."""
        return (self.velocity_x**2 + self.velocity_y**2 + self.velocity_z**2) ** 0.5
    
    def get_kinetic_energy(self) -> float:
        """Returns kinetic energy (0.5 * m * v^2)."""
        speed = self.get_speed()
        return 0.5 * self.mass * speed * speed
