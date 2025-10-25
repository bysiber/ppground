# 🛠️ Developer Guide

## Extending the Particle Physics Playground

This guide shows you how to extend and customize the framework for advanced use cases.

## Table of Contents
1. [Creating Custom Extensions](#creating-custom-extensions)
2. [Custom Physics Behaviors](#custom-physics-behaviors)
3. [Custom Renderers](#custom-renderers)
4. [Advanced Collision Handling](#advanced-collision-handling)
5. [Performance Optimization](#performance-optimization)
6. [Constraints and Connections](#constraints-and-connections)

---

## Creating Custom Extensions

Extensions add new properties and behaviors to particles.

### Example: Particle with Health

```python
from dataclasses import dataclass

@dataclass
class HealthExtension:
    health: float = 100.0
    max_health: float = 100.0
    is_alive: bool = True
    
    def take_damage(self, amount: float):
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.is_alive = False
    
    def heal(self, amount: float):
        self.health = min(self.health + amount, self.max_health)

# Usage
particle = Particle(x=100, y=100)
particle.register_extension('health', HealthExtension)

# Access the extension
health_ext = particle.extensions['health']
health_ext.take_damage(25)
```

### Example: Particle with Lifetime

```python
@dataclass
class LifetimeExtension:
    lifetime: float = 5.0  # seconds
    age: float = 0.0
    fade_out: bool = True
    
    def update(self, dt: float, particle):
        self.age += dt
        if self.age >= self.lifetime:
            particle.state.is_active = False
        elif self.fade_out:
            # Fade out alpha
            ratio = 1.0 - (self.age / self.lifetime)
            # Modify particle color alpha (would need RGBA support)

# In your playground update:
def update(self, dt):
    super().update(dt)
    for particle in self.particles:
        if 'lifetime' in particle.extensions:
            particle.extensions['lifetime'].update(dt, particle)
```

---

## Custom Physics Behaviors

### Adding Custom Forces

```python
class MagneticPlayground(BasePlayground):
    def __init__(self):
        super().__init__()
        self.magnetic_center = (400, 300)
        self.magnetic_strength = 5000.0
    
    def update(self, dt):
        # Apply magnetic force before physics update
        for particle in self.particles:
            if particle.state.is_static:
                continue
            
            # Calculate direction to magnetic center
            dx = self.magnetic_center[0] - particle.position.x
            dy = self.magnetic_center[1] - particle.position.y
            distance = (dx*dx + dy*dy) ** 0.5
            
            if distance > 0:
                # Inverse square law
                force = self.magnetic_strength / (distance * distance)
                
                # Normalize and apply
                fx = (dx / distance) * force
                fy = (dy / distance) * force
                
                particle.apply_force('magnetic', fx, fy)
        
        # Now do normal physics
        super().update(dt)
```

### Wind Force

```python
class WindyPlayground(BasePlayground):
    def __init__(self):
        super().__init__()
        self.wind_speed = 100.0
        self.wind_direction = (1, 0)  # Right
    
    def update(self, dt):
        import math
        
        # Vary wind over time
        time = pygame.time.get_ticks() / 1000.0
        wind_variation = math.sin(time * 2) * 0.5 + 0.5
        
        for particle in self.particles:
            if not particle.state.is_static:
                wind_force = self.wind_speed * wind_variation
                fx = self.wind_direction[0] * wind_force
                fy = self.wind_direction[1] * wind_force
                particle.apply_force('wind', fx, fy)
        
        super().update(dt)
```

---

## Custom Renderers

### Example: Trail Renderer

```python
from collections import deque

class TrailRenderer(PygameRenderer):
    def __init__(self, system, width=800, height=600):
        super().__init__(system, width, height)
        self.trails = {}  # particle_id -> deque of positions
        self.trail_length = 20
    
    def draw_particle(self, particle):
        # Get or create trail
        particle_id = id(particle)
        if particle_id not in self.trails:
            self.trails[particle_id] = deque(maxlen=self.trail_length)
        
        # Add current position to trail
        trail = self.trails[particle_id]
        trail.append((int(particle.position.x), int(particle.position.y)))
        
        # Draw trail
        if len(trail) > 1:
            for i in range(len(trail) - 1):
                alpha = int(255 * (i / len(trail)))
                color = (particle.state.color[0], 
                        particle.state.color[1], 
                        particle.state.color[2])
                pygame.draw.line(self.screen, color, trail[i], trail[i+1], 2)
        
        # Draw particle normally
        super().draw_particle(particle)

# Use it
class TrailDemo(BasePlayground):
    def __init__(self):
        system = System()
        self.system = system
        self.renderer = TrailRenderer(system)
        # ... rest of init
```

### Example: Debug Renderer

```python
class DebugRenderer(PygameRenderer):
    def __init__(self, system, width=800, height=600):
        super().__init__(system, width, height)
        self.show_velocity = True
        self.show_forces = True
        self.font = pygame.font.Font(None, 20)
    
    def draw_particle(self, particle):
        super().draw_particle(particle)
        
        x = int(particle.position.x)
        y = int(particle.position.y)
        
        # Draw velocity vector
        if self.show_velocity:
            vx = particle.state.velocity_x * 0.1
            vy = particle.state.velocity_y * 0.1
            pygame.draw.line(self.screen, (0, 255, 0), 
                           (x, y), (x + vx, y + vy), 2)
        
        # Draw forces
        if self.show_forces:
            for force_name, (fx, fy, fz) in particle.forces.items():
                fx_scaled = fx * 0.01
                fy_scaled = fy * 0.01
                pygame.draw.line(self.screen, (255, 255, 0),
                               (x, y), (x + fx_scaled, y + fy_scaled), 1)
        
        # Draw info text
        info = f"v:{particle.state.get_speed():.1f} m:{particle.state.mass}"
        text = self.font.render(info, True, (255, 255, 255))
        self.screen.blit(text, (x + 10, y - 10))
```

---

## Advanced Collision Handling

### Custom Collision Response

```python
class ExplosiveParticle(Particle):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.explosive = True
        self.explosion_force = 5000.0

class ExplosivePhysicsEngine(PhysicsEngine):
    def handle_particle_collision(self, p1, p2):
        super().handle_particle_collision(p1, p2)
        
        # Check if either is explosive
        if hasattr(p1, 'explosive') and p1.explosive:
            self.explode(p1, p2)
        elif hasattr(p2, 'explosive') and p2.explosive:
            self.explode(p2, p1)
    
    def explode(self, explosive_particle, other_particle):
        # Calculate direction
        dx = other_particle.position.x - explosive_particle.position.x
        dy = other_particle.position.y - explosive_particle.position.y
        distance = (dx*dx + dy*dy) ** 0.5
        
        if distance > 0:
            # Apply explosion force
            force = explosive_particle.explosion_force / distance
            nx = dx / distance
            ny = dy / distance
            
            other_particle.apply_force('explosion', nx * force, ny * force)
            explosive_particle.state.is_active = False  # Remove explosive
```

---

## Performance Optimization

### Spatial Partitioning with Quadtree

```python
class QuadTree:
    def __init__(self, bounds, capacity=4):
        self.bounds = bounds  # (x, y, width, height)
        self.capacity = capacity
        self.particles = []
        self.divided = False
        self.children = []
    
    def insert(self, particle):
        # Check if particle is in bounds
        x, y, w, h = self.bounds
        px, py = particle.position.x, particle.position.y
        
        if not (x <= px < x + w and y <= py < y + h):
            return False
        
        if len(self.particles) < self.capacity:
            self.particles.append(particle)
            return True
        
        if not self.divided:
            self.subdivide()
        
        for child in self.children:
            if child.insert(particle):
                return True
        
        return False
    
    def subdivide(self):
        x, y, w, h = self.bounds
        hw, hh = w / 2, h / 2
        
        self.children = [
            QuadTree((x, y, hw, hh), self.capacity),
            QuadTree((x + hw, y, hw, hh), self.capacity),
            QuadTree((x, y + hh, hw, hh), self.capacity),
            QuadTree((x + hw, y + hh, hw, hh), self.capacity),
        ]
        self.divided = True
    
    def query(self, range_bounds, found=None):
        if found is None:
            found = []
        
        # Check if range intersects this quad
        if not self.intersects(range_bounds):
            return found
        
        for particle in self.particles:
            px, py = particle.position.x, particle.position.y
            rx, ry, rw, rh = range_bounds
            if rx <= px < rx + rw and ry <= py < ry + rh:
                found.append(particle)
        
        if self.divided:
            for child in self.children:
                child.query(range_bounds, found)
        
        return found
    
    def intersects(self, range_bounds):
        x, y, w, h = self.bounds
        rx, ry, rw, rh = range_bounds
        return not (rx > x + w or rx + rw < x or ry > y + h or ry + rh < y)

# Use in physics engine
class OptimizedPhysicsEngine(PhysicsEngine):
    def update(self, particles, dt):
        # Build quadtree
        quadtree = QuadTree((0, 0, 800, 600))
        for particle in particles:
            quadtree.insert(particle)
        
        # Apply forces
        for particle in particles:
            if not particle.state.is_active:
                continue
            self.apply_gravity(particle)
            self.apply_friction(particle)
        
        # Update positions
        for particle in particles:
            particle.update(dt)
            self.handle_boundary_collision(particle)
        
        # Check collisions using quadtree
        for particle in particles:
            if not particle.state.is_active:
                continue
            
            # Query nearby particles
            radius = particle.state.radius * 3
            query_bounds = (
                particle.position.x - radius,
                particle.position.y - radius,
                radius * 2,
                radius * 2
            )
            nearby = quadtree.query(query_bounds)
            
            for other in nearby:
                if particle is not other and other.state.is_active:
                    self.handle_particle_collision(particle, other)
        
        # Clear forces
        for particle in particles:
            particle.clear_forces()
```

---

## Constraints and Connections

### Spring Constraint

```python
class Spring:
    def __init__(self, particle_a, particle_b, rest_length=None, stiffness=0.5, damping=0.1):
        self.particle_a = particle_a
        self.particle_b = particle_b
        self.rest_length = rest_length or particle_a.distance_to(particle_b)
        self.stiffness = stiffness
        self.damping = damping
    
    def apply(self):
        # Calculate distance
        dx = self.particle_b.position.x - self.particle_a.position.x
        dy = self.particle_b.position.y - self.particle_a.position.y
        distance = (dx*dx + dy*dy) ** 0.5
        
        if distance == 0:
            return
        
        # Normalize
        nx = dx / distance
        ny = dy / distance
        
        # Calculate spring force (Hooke's law)
        displacement = distance - self.rest_length
        force_magnitude = displacement * self.stiffness
        
        # Add damping
        relative_vx = self.particle_b.state.velocity_x - self.particle_a.state.velocity_x
        relative_vy = self.particle_b.state.velocity_y - self.particle_a.state.velocity_y
        relative_v_along_spring = relative_vx * nx + relative_vy * ny
        damping_force = relative_v_along_spring * self.damping
        
        total_force = force_magnitude + damping_force
        
        # Apply forces
        fx = nx * total_force
        fy = ny * total_force
        
        if not self.particle_a.state.is_static:
            self.particle_a.apply_force('spring', fx, fy)
        if not self.particle_b.state.is_static:
            self.particle_b.apply_force('spring', -fx, -fy)

# Usage in playground
class SpringDemo(BasePlayground):
    def setup(self):
        # Create two particles
        p1 = Particle(x=300, y=300, mass=1.0, radius=10, color=(255, 0, 0))
        p2 = Particle(x=500, y=300, mass=1.0, radius=10, color=(0, 0, 255))
        p1.state.is_static = True
        
        self.add_particle(p1)
        self.add_particle(p2)
        
        # Create spring between them
        self.springs = [Spring(p1, p2, rest_length=100, stiffness=0.8)]
    
    def update(self, dt):
        # Apply spring forces
        for spring in self.springs:
            spring.apply()
        
        # Normal physics update
        super().update(dt)
    
    def render(self):
        super().render()
        
        # Draw springs
        for spring in self.springs:
            p1 = spring.particle_a
            p2 = spring.particle_b
            pygame.draw.line(self.screen, (255, 255, 0),
                           (int(p1.position.x), int(p1.position.y)),
                           (int(p2.position.x), int(p2.position.y)), 2)
        
        pygame.display.flip()
```

---

## Best Practices

1. **Keep extensions simple**: One responsibility per extension
2. **Use dataclasses**: Easy serialization and clean code
3. **Profile before optimizing**: Use cProfile to find bottlenecks
4. **Test incrementally**: Add features one at a time
5. **Document custom behavior**: Future you will thank you
6. **Version physics parameters**: Save configurations for reproducibility

---

## Testing Custom Code

```python
def test_spring():
    p1 = Particle(x=0, y=0, mass=1.0)
    p2 = Particle(x=100, y=0, mass=1.0)
    
    spring = Spring(p1, p2, rest_length=50, stiffness=1.0)
    spring.apply()
    
    # p2 should be pulled left
    assert p2.forces['spring'][0] < 0
    # p1 should be pulled right (if not static)
    print("✅ Spring test passed")

test_spring()
```

---

## Further Reading

- Check out `entities/particle/actions/joining.py` for particle connections
- See `entities/particle/models/extensions.py` for LinkedList example
- Read pygame documentation for advanced rendering

Happy extending! 🚀
