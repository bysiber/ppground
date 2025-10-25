"""
Interactive Particle Spawner Demo
Click to spawn particles!
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame
from playground import BasePlayground
from entities import Particle, System
import random


class InteractiveSpawner(BasePlayground):
    """
    Interactive demo where you can click to spawn particles.
    """
    
    def __init__(self):
        system = System()
        system.physics.gravity = 400.0
        system.physics.friction = 0.05
        system.physics.air_resistance = 0.002
        system.physics.bounce_coefficient = 0.75
        system.physics.elasticity = 0.85
        
        super().__init__(system=system, width=800, height=600, fps=60)
        
        self.mouse_down = False
        self.spawn_cooldown = 0
    
    def setup(self):
        """Initial setup with floor."""
        # Add floor
        for x in range(20, 780, 35):
            floor = Particle(x=x, y=580, mass=100.0, radius=15, color=(80, 80, 80))
            floor.state.is_static = True
            self.add_particle(floor)
        
        # Add side walls
        for y in range(50, 550, 40):
            left_wall = Particle(x=20, y=y, mass=100.0, radius=15, color=(80, 80, 80))
            left_wall.state.is_static = True
            self.add_particle(left_wall)
            
            right_wall = Particle(x=780, y=y, mass=100.0, radius=15, color=(80, 80, 80))
            right_wall.state.is_static = True
            self.add_particle(right_wall)
        
        print("\n=== Interactive Particle Spawner ===")
        print("\nControls:")
        print("  LEFT CLICK - Spawn particles at mouse position")
        print("  SPACE - Pause/Resume")
        print("  R - Reset (clear all particles)")
        print("  ESC - Quit")
        print("\nClick anywhere to spawn particles!")
    
    def handle_events(self):
        """Handle pygame events including mouse clicks."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.key == pygame.K_r:
                    # Clear only dynamic particles
                    self.particles = [p for p in self.particles if p.state.is_static]
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self.mouse_down = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.mouse_down = False
    
    def update(self, dt: float):
        """Update with mouse spawning."""
        # Handle mouse spawning
        if self.mouse_down and self.spawn_cooldown <= 0:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.spawn_particle(mouse_x, mouse_y)
            self.spawn_cooldown = 0.05  # 50ms cooldown between spawns
        
        if self.spawn_cooldown > 0:
            self.spawn_cooldown -= dt
        
        # Update physics
        super().update(dt)
    
    def spawn_particle(self, x: float, y: float):
        """Spawn a particle at the given position."""
        colors = [
            (255, 100, 100),  # Red
            (100, 255, 100),  # Green
            (100, 100, 255),  # Blue
            (255, 255, 100),  # Yellow
            (255, 100, 255),  # Magenta
            (100, 255, 255),  # Cyan
            (255, 150, 100),  # Orange
        ]
        
        mass = random.uniform(0.5, 2.0)
        radius = 8 + mass * 6
        color = random.choice(colors)
        
        particle = Particle(x=x, y=y, mass=mass, radius=radius, color=color)
        
        # Random initial velocity
        particle.state.velocity_x = random.uniform(-100, 100)
        particle.state.velocity_y = random.uniform(-50, 50)
        
        self.add_particle(particle)
    
    def render(self):
        """Render with crosshair at mouse position."""
        super().render()
        
        # Draw crosshair at mouse position
        if not self.paused:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            crosshair_color = (255, 255, 0)
            pygame.draw.circle(self.renderer.screen, crosshair_color, (mouse_x, mouse_y), 8, 2)
            pygame.draw.line(self.renderer.screen, crosshair_color, 
                           (mouse_x - 10, mouse_y), (mouse_x + 10, mouse_y), 2)
            pygame.draw.line(self.renderer.screen, crosshair_color, 
                           (mouse_x, mouse_y - 10), (mouse_x, mouse_y + 10), 2)
        
        pygame.display.flip()


def main():
    demo = InteractiveSpawner()
    demo.run()


if __name__ == "__main__":
    main()
