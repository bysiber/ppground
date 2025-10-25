"""
Physics Engine for particle simulation.
Handles forces, collisions, and constraints.
"""

from typing import List, Tuple
from ..particle import Particle
from .models.physics import Physics
import math


class PhysicsEngine:
    """
    Physics engine that applies forces and handles collisions between particles.
    """
    
    def __init__(self, physics_config: Physics = None):
        """
        Initialize the physics engine.
        
        Args:
            physics_config: Physics configuration object with parameters
        """
        self.config = physics_config or Physics()
        self.bounds: Tuple[float, float, float, float] = None  # (min_x, min_y, max_x, max_y)
    
    def set_bounds(self, min_x: float, min_y: float, max_x: float, max_y: float) -> None:
        """Set simulation bounds for collision detection."""
        self.bounds = (min_x, min_y, max_x, max_y)
    
    def apply_gravity(self, particle: Particle) -> None:
        """
        Apply gravity force to a particle.
        
        Args:
            particle: The particle to apply gravity to
        """
        if particle.state.is_static or not particle.state.is_active:
            return
        
        # F = m * g (downward)
        gravity_force = particle.state.mass * self.config.gravity
        particle.apply_force('gravity', 0, gravity_force, 0)
    
    def apply_friction(self, particle: Particle) -> None:
        """
        Apply friction force opposite to velocity.
        
        Args:
            particle: The particle to apply friction to
        """
        if particle.state.is_static or not particle.state.is_active:
            return
        
        # Friction force proportional to velocity
        friction_x = -particle.state.velocity_x * self.config.friction
        friction_y = -particle.state.velocity_y * self.config.friction
        friction_z = -particle.state.velocity_z * self.config.friction
        
        particle.apply_force('friction', friction_x, friction_y, friction_z)
    
    def apply_air_resistance(self, particle: Particle) -> None:
        """
        Apply air resistance (drag) force.
        
        Args:
            particle: The particle to apply drag to
        """
        if particle.state.is_static or not particle.state.is_active:
            return
        
        # Drag force: F = -0.5 * ρ * v² * Cd * A
        # Simplified: F = -k * v²
        speed = particle.state.get_speed()
        if speed > 0:
            drag_magnitude = self.config.air_resistance * speed * speed
            
            # Apply in opposite direction of velocity
            drag_x = -(particle.state.velocity_x / speed) * drag_magnitude
            drag_y = -(particle.state.velocity_y / speed) * drag_magnitude
            drag_z = -(particle.state.velocity_z / speed) * drag_magnitude
            
            particle.apply_force('drag', drag_x, drag_y, drag_z)
    
    def handle_boundary_collision(self, particle: Particle) -> None:
        """
        Handle collision with simulation boundaries.
        
        Args:
            particle: The particle to check
        """
        if not self.bounds or particle.state.is_static:
            return
        
        min_x, min_y, max_x, max_y = self.bounds
        bounce = self.config.bounce_coefficient
        
        # Left/Right boundaries
        if particle.position.x - particle.state.radius < min_x:
            particle.position.x = min_x + particle.state.radius
            particle.state.velocity_x = abs(particle.state.velocity_x) * bounce
        elif particle.position.x + particle.state.radius > max_x:
            particle.position.x = max_x - particle.state.radius
            particle.state.velocity_x = -abs(particle.state.velocity_x) * bounce
        
        # Top/Bottom boundaries
        if particle.position.y - particle.state.radius < min_y:
            particle.position.y = min_y + particle.state.radius
            particle.state.velocity_y = abs(particle.state.velocity_y) * bounce
        elif particle.position.y + particle.state.radius > max_y:
            particle.position.y = max_y - particle.state.radius
            particle.state.velocity_y = -abs(particle.state.velocity_y) * bounce
            
            # Apply additional friction on ground collision
            particle.state.velocity_x *= (1 - self.config.friction * 2)
    
    def handle_particle_collision(self, p1: Particle, p2: Particle) -> None:
        """
        Handle elastic collision between two particles.
        
        Args:
            p1: First particle
            p2: Second particle
        """
        if not p1.is_colliding_with(p2):
            return
        
        # Skip if both are static
        if p1.state.is_static and p2.state.is_static:
            return
        
        # Calculate collision normal
        dx = p2.position.x - p1.position.x
        dy = p2.position.y - p1.position.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance == 0:
            return
        
        # Normalize
        nx = dx / distance
        ny = dy / distance
        
        # Separate particles
        overlap = (p1.state.radius + p2.state.radius) - distance
        if not p1.state.is_static and not p2.state.is_static:
            p1.position.x -= nx * overlap * 0.5
            p1.position.y -= ny * overlap * 0.5
            p2.position.x += nx * overlap * 0.5
            p2.position.y += ny * overlap * 0.5
        elif p1.state.is_static:
            p2.position.x += nx * overlap
            p2.position.y += ny * overlap
        else:
            p1.position.x -= nx * overlap
            p1.position.y -= ny * overlap
        
        # Calculate relative velocity
        dvx = p2.state.velocity_x - p1.state.velocity_x
        dvy = p2.state.velocity_y - p1.state.velocity_y
        
        # Relative velocity in collision normal direction
        dvn = dvx * nx + dvy * ny
        
        # Don't resolve if velocities are separating
        if dvn > 0:
            return
        
        # Calculate impulse
        e = self.config.elasticity
        m1 = p1.state.mass
        m2 = p2.state.mass
        
        if not p1.state.is_static and not p2.state.is_static:
            impulse = -(1 + e) * dvn / (1/m1 + 1/m2)
            
            # Apply impulse
            p1.state.velocity_x -= (impulse / m1) * nx
            p1.state.velocity_y -= (impulse / m1) * ny
            p2.state.velocity_x += (impulse / m2) * nx
            p2.state.velocity_y += (impulse / m2) * ny
        elif p1.state.is_static:
            # Only p2 bounces
            p2.state.velocity_x -= 2 * dvn * nx * e
            p2.state.velocity_y -= 2 * dvn * ny * e
        else:
            # Only p1 bounces
            p1.state.velocity_x -= 2 * dvn * nx * e
            p1.state.velocity_y -= 2 * dvn * ny * e
    
    def update(self, particles: List[Particle], dt: float) -> None:
        """
        Update all particles with physics.
        
        Args:
            particles: List of particles to update
            dt: Time step in seconds
        """
        # Apply forces to all particles
        for particle in particles:
            if not particle.state.is_active:
                continue
            
            self.apply_gravity(particle)
            self.apply_friction(particle)
            self.apply_air_resistance(particle)
        
        # Update particle positions and velocities
        for particle in particles:
            particle.update(dt)
        
        # Handle collisions
        for particle in particles:
            self.handle_boundary_collision(particle)
        
        # Check particle-particle collisions
        for i in range(len(particles)):
            for j in range(i + 1, len(particles)):
                if particles[i].state.is_active and particles[j].state.is_active:
                    self.handle_particle_collision(particles[i], particles[j])
        
        # Clear forces for next frame
        for particle in particles:
            particle.clear_forces()
