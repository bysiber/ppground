from typing import List

from entities import (
    Particle,
    System,
)

from renderer import (
    PygameRenderer,
)

class BasePlayground:
    def __init__(self, system: System = None):
        self.renderer = PygameRenderer(system or System())
        self.particles: List[Particle] = []

    def add_particle(self, particle: Particle):
        self.particles.append(particle)
        self.renderer.system.add_particle(particle)
