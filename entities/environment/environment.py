from typing import List
from ..particle import Particle
from ..system import System


class Environment:
    """
    Environment manages a collection of particles and their system.
    """
    
    def __init__(self, system: System = None):
        """
        Initialize the environment.
        
        Args:
            system: Physics system (creates default if None)
        """
        self.particles: List[Particle] = []
        self.system: System = system or System()
    
    def add_particle(self, particle: Particle) -> None:
        """Add a particle to the environment."""
        self.particles.append(particle)
    
    def remove_particle(self, particle: Particle) -> None:
        """Remove a particle from the environment."""
        if particle in self.particles:
            self.particles.remove(particle)
    
    def update(self, dt: float) -> None:
        """Update all particles in the environment."""
        self.system.engine.update(self.particles, dt)
