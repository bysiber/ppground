from .models.physics import Physics
from .physics_engine import PhysicsEngine

class System:
    """
    System manages the physics configuration and engine for the simulation.
    """
    
    def __init__(self, physics_config: Physics = None):
        """
        Initialize the system with physics configuration.
        
        Args:
            physics_config: Custom physics configuration, or default if None
        """
        self.physics = physics_config or Physics()
        self.engine = PhysicsEngine(self.physics)
    
    def set_bounds(self, min_x: float, min_y: float, max_x: float, max_y: float) -> None:
        """Set the simulation boundaries."""
        self.engine.set_bounds(min_x, min_y, max_x, max_y)
    
    def update_config(self, physics_config: Physics) -> None:
        """Update the physics configuration."""
        self.physics = physics_config
        self.engine = PhysicsEngine(self.physics)