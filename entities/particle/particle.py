from .models.position import Position
from .models.state import ParticleState
from .models.extensions import (
    LinkedList as LinkedListExtension,
)
from typing import Dict, Any, Tuple

class Particle:
    """
    A particle entity with position, state (velocity, mass, etc.), and extensible properties.
    """
    
    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0, 
                 mass: float = 1.0, radius: float = 5.0,
                 color: Tuple[int, int, int] = (255, 255, 255)):
        """
        Initialize a particle.
        
        Args:
            x, y, z: Initial position coordinates
            mass: Mass of the particle
            radius: Radius for rendering and collision detection
            color: RGB color tuple
        """
        self.position = Position(x, y, z)
        self.state = ParticleState(mass=mass, radius=radius, color=color)
        self.extensions: Dict[str, Any] = {}
        self.forces: Dict[str, Tuple[float, float, float]] = {}  # Named forces applied to particle

    def get_action_result(self, action_name: str) -> Any:
        """Get the result of an action from extensions."""
        for extension in self.extensions.values():
            if hasattr(extension, 'actions'):
                if isinstance(extension, dict) and 'actions' in extension:
                    return extension['actions'].get(action_name, None)
        return None

    def register_extension(self, name: str, extension_class) -> None:
        """
        Register an extension to add functionality to the particle.
        
        Args:
            name: Name of the extension
            extension_class: Class or callable that creates the extension
        """
        self.extensions[name] = extension_class()
    
    def apply_force(self, name: str, fx: float, fy: float, fz: float = 0.0) -> None:
        """
        Apply a named force to the particle.
        
        Args:
            name: Name of the force (e.g., 'gravity', 'wind')
            fx, fy, fz: Force components
        """
        self.forces[name] = (fx, fy, fz)
    
    def clear_forces(self) -> None:
        """Clear all forces applied to the particle."""
        self.forces.clear()
    
    def update(self, dt: float) -> None:
        """
        Update particle physics using Verlet integration.
        
        Args:
            dt: Time step in seconds
        """
        if self.state.is_static or not self.state.is_active:
            return
        
        # Reset acceleration
        self.state.reset_acceleration()
        
        # Apply all accumulated forces
        for force in self.forces.values():
            self.state.apply_force(force[0], force[1], force[2])
        
        # Update velocity: v = v + a * dt
        self.state.velocity_x += self.state.acceleration_x * dt
        self.state.velocity_y += self.state.acceleration_y * dt
        self.state.velocity_z += self.state.acceleration_z * dt
        
        # Update position: p = p + v * dt
        self.position.x += self.state.velocity_x * dt
        self.position.y += self.state.velocity_y * dt
        self.position.z += self.state.velocity_z * dt
    
    def distance_to(self, other: 'Particle') -> float:
        """Calculate distance to another particle."""
        dx = self.position.x - other.position.x
        dy = self.position.y - other.position.y
        dz = self.position.z - other.position.z
        return (dx**2 + dy**2 + dz**2) ** 0.5
    
    def is_colliding_with(self, other: 'Particle') -> bool:
        """Check if this particle is colliding with another."""
        distance = self.distance_to(other)
        return distance < (self.state.radius + other.state.radius)
    
    def __repr__(self) -> str:
        return f"Particle(pos=({self.position.x:.1f}, {self.position.y:.1f}), vel=({self.state.velocity_x:.1f}, {self.state.velocity_y:.1f}), mass={self.state.mass})"
