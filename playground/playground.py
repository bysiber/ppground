from typing import List
import pygame

from entities import (
    Particle,
    System,
)

from renderer import (
    PygameRenderer,
)


class BasePlayground:
    """
    Base playground class that manages particles, physics, and rendering.
    """
    
    def __init__(self, 
        system: System = None,
        width: int = 800,
        height: int = 600,
        fps: int = 60,
        ):
        """
        Initialize the playground.
        
        Args:
            system: Physics system (creates default if None)
            width: Window width in pixels
            height: Window height in pixels
            fps: Target frames per second
        """
        self.system = system or System()
        self.renderer = PygameRenderer(self.system, width, height)
        self.particles: List[Particle] = []
        
        # Simulation settings
        self.fps = fps
        self.running = False
        self.paused = False
        
        # Set physics boundaries to match window size
        self.system.set_bounds(0, 0, width, height)

    def add_particle(self, 
            particle: Particle,
            type: str = "default",
            actions = None,
        ):
        """
        Add a particle to the playground.
        
        Args:
            particle: The particle to add
            type: Type identifier (for future use)
            actions: Actions to apply (for future use)
        """
        self.particles.append(particle)
    
    def remove_particle(self, particle: Particle):
        """Remove a particle from the playground."""
        if particle in self.particles:
            self.particles.remove(particle)
    
    def clear_particles(self):
        """Remove all particles."""
        self.particles.clear()
    
    def update(self, dt: float):
        """
        Update physics simulation.
        
        Args:
            dt: Time delta in seconds
        """
        if not self.paused:
            # Update physics for all particles
            self.system.engine.update(self.particles, dt)
    
    def render(self):
        """Render all particles."""
        # Clear screen
        self.renderer.screen.fill((0, 0, 0))
        
        # Draw all active particles
        for particle in self.particles:
            if particle.state.is_active:
                self.renderer.draw_particle(particle)
        
        # Update display
        pygame.display.flip()
    
    def handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.key == pygame.K_r:
                    # Reset simulation
                    self.clear_particles()
                    self.setup()
    
    def setup(self):
        """
        Override this method to set up your simulation.
        Add particles and configure the environment here.
        """
        pass
    
    def run(self):
        """
        Main simulation loop.
        Call this to start the simulation.
        """
        self.running = True
        self.setup()
        
        while self.running:
            # Calculate delta time
            dt = self.renderer.clock.tick(self.fps) / 1000.0  # Convert to seconds
            
            # Handle input
            self.handle_events()
            
            # Update simulation
            self.update(dt)
            
            # Render
            self.render()
            
            # Update window title with FPS
            fps = self.renderer.clock.get_fps()
            pygame.display.set_caption(f"Playground - FPS: {fps:.1f} - Particles: {len(self.particles)} - [SPACE: Pause, R: Reset, ESC: Quit]")
        
        pygame.quit()

