import pygame
from abc import ABC, abstractmethod

from ..entities.system import System

class Renderer(ABC):
    def __init__(self, 
            system: System = None
        ):
        super().__init__()
        if system is None: raise ValueError("system is required")
        self.system = system

    @abstractmethod
    def draw_dot(self, surface, color, position, radius):
        pass

    @abstractmethod
    def update_system(self, system: System):
        pass

class PygameRenderer(Renderer):
    def __init__(self, system):
        super().__init__(system)  # Call parent ABC __init__

        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((800, 600))

        pygame.display.set_caption("Demo System")
        
    def draw_dot(self, surface, color, position, radius):
        pygame.draw.circle(surface, color, position, radius)

    def update_system(self, system: System):
        # Apply system parameters to the PygameRenderer
        self.system = system