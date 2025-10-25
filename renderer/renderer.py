import pygame
from abc import ABC, abstractmethod
from typing import Tuple

from entities.system import System
from entities.particle import Particle


class Renderer(ABC):
    """Abstract base class for renderers."""
    
    def __init__(self, 
            system: System = None
        ):
        super().__init__()
        if system is None: 
            raise ValueError("system is required")
        self.system = system

    @abstractmethod
    def draw_particle(self, particle: Particle):
        """Draw a single particle."""
        pass

    @abstractmethod
    def draw_dot(self, surface, color, position, radius):
        """Draw a dot at a specific position."""
        pass

    @abstractmethod
    def update_system(self, system: System):
        """Update the physics system."""
        pass


class PygameRenderer(Renderer):
    """Pygame-based renderer for the particle simulation."""
    
    def __init__(self, system: System, width: int = 800, height: int = 600):
        """
        Initialize the Pygame renderer.
        
        Args:
            system: Physics system
            width: Window width
            height: Window height
        """
        super().__init__(system)  # Call parent ABC __init__

        pygame.init()
        self.clock = pygame.time.Clock()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))

        pygame.display.set_caption("Particle Playground")
    
    def draw_particle(self, particle: Particle):
        """
        Draw a particle on the screen.
        
        Args:
            particle: The particle to draw
        """
        # Convert position to screen coordinates
        x = int(particle.position.x)
        y = int(particle.position.y)
        radius = int(particle.state.radius)
        color = particle.state.color
        
        # Draw the particle
        pygame.draw.circle(self.screen, color, (x, y), radius)
        
        # Optionally draw velocity vector (for debugging)
        # vx = particle.state.velocity_x * 2
        # vy = particle.state.velocity_y * 2
        # pygame.draw.line(self.screen, (255, 255, 0), (x, y), (x + vx, y + vy), 1)
        
    def draw_dot(self, surface, color: Tuple[int, int, int], position: Tuple[int, int], radius: int):
        """
        Draw a simple dot.
        
        Args:
            surface: Pygame surface to draw on
            color: RGB color tuple
            position: (x, y) position
            radius: Dot radius
        """
        pygame.draw.circle(surface, color, position, radius)

    def update_system(self, system: System):
        """
        Update the physics system.
        
        Args:
            system: New physics system
        """
        self.system = system