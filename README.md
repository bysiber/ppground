# 🎮 Particle Physics Playground

A modular, extensible particle physics simulation framework built with Python and Pygame. Create complex physics simulations with particles, forces, collisions, and custom behaviors.

## ✨ Features

- **Modular Architecture**: Clean separation of concerns with entities, systems, renderers, and playgrounds
- **Realistic Physics**: 
  - Gravity and friction
  - Elastic collisions between particles
  - Boundary collision detection
  - Air resistance and drag
  - Configurable physics parameters
- **Extensible Particles**: Add custom properties and behaviors through extensions
- **Multiple Renderers**: Abstract renderer design (currently Pygame, easily extensible)
- **Interactive Playground**: Built-in controls for pausing, resetting, and observing simulations

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd pygame-p1

# Install dependencies
pip install -r requirements.txt
```

### Run a Demo

```bash
# Run the bouncing balls demo
python demos/bouncing_balls.py
```

## 🎯 Usage

### Creating a Simple Simulation

```python
from playground import BasePlayground
from entities import Particle, System

class MySimulation(BasePlayground):
    def setup(self):
        # Create particles
        particle = Particle(x=400, y=100, mass=1.0, radius=10, color=(255, 100, 100))
        particle.state.velocity_y = 50  # Initial downward velocity
        
        self.add_particle(particle)
        
        # Add a static platform
        platform = Particle(x=400, y=500, mass=10.0, radius=30, color=(150, 150, 150))
        platform.state.is_static = True
        self.add_particle(platform)

# Run the simulation
sim = MySimulation()
sim.run()
```

### Customizing Physics

```python
from entities import System

# Create custom physics configuration
system = System()
system.physics.gravity = 500.0  # Increase gravity
system.physics.friction = 0.2   # Increase friction
system.physics.bounce_coefficient = 0.8  # More bouncy
system.physics.elasticity = 0.9  # Elastic collisions

# Use in playground
playground = BasePlayground(system=system)
```

## 📁 Project Structure

```
pygame-p1/
├── entities/           # Core entity definitions
│   ├── particle/       # Particle entity and models
│   │   ├── particle.py         # Main particle class
│   │   ├── models/
│   │   │   ├── position.py     # 3D position
│   │   │   ├── state.py        # Velocity, mass, etc.
│   │   │   └── extensions.py  # Extension system
│   │   └── actions/
│   │       └── joining.py      # Particle connections
│   ├── environment/    # Environment container
│   │   └── environment.py
│   └── system/         # Physics system
│       ├── system.py           # System manager
│       ├── physics_engine.py   # Physics calculations
│       └── models/
│           └── physics.py      # Physics configuration
├── renderer/           # Rendering abstraction
│   └── renderer.py     # Pygame renderer
├── playground/         # Simulation orchestrator
│   └── playground.py   # Main playground class
└── demos/              # Example simulations
    ├── bouncing_balls.py  # Interactive demos
    └── test.py
```

## 🎨 Architecture

### Core Components

1. **Particle**: The fundamental entity with position, state (velocity, mass, etc.), and extensible properties
2. **System**: Manages physics configuration and the physics engine
3. **PhysicsEngine**: Handles force application, collision detection, and integration
4. **Renderer**: Abstract rendering interface with Pygame implementation
5. **Playground**: Orchestrates particles, physics, and rendering in a simulation loop

### Key Design Patterns

- **Entity-Component Pattern**: Particles can have extensions for modular functionality
- **Abstract Factory**: Renderer is abstracted for multiple implementations
- **Observer Pattern**: Forces are accumulated and applied each frame
- **Strategy Pattern**: Physics parameters can be swapped without code changes

## 🎮 Controls

When running a simulation:

- **SPACE**: Pause/Resume simulation
- **R**: Reset simulation
- **ESC**: Quit

## 🔧 Advanced Usage

### Creating Custom Extensions

```python
from dataclasses import dataclass

@dataclass
class CustomExtension:
    custom_property: float = 0.0
    
    def update(self, particle, dt):
        # Custom behavior
        pass

# Register extension
particle.register_extension('custom', CustomExtension)
```

### Custom Forces

```python
# Apply custom forces to particles
particle.apply_force('wind', fx=50.0, fy=0.0)
particle.apply_force('magnetic', fx=0.0, fy=-20.0)

# Forces are automatically cleared each frame after physics update
```

### Creating Custom Renderers

```python
from renderer import Renderer

class MyCustomRenderer(Renderer):
    def draw_particle(self, particle):
        # Custom drawing logic
        pass
    
    def draw_dot(self, surface, color, position, radius):
        # Custom dot drawing
        pass
```

## 🧪 Physics Parameters

The `Physics` configuration includes extensive parameters:

- **Basic**: gravity, friction, air_resistance, bounce_coefficient
- **Material**: mass, elasticity, viscosity
- **Advanced**: drag_coefficient, terminal_velocity, pressure, temperature
- **And many more** for complex simulations

See `entities/system/models/physics.py` for the complete list.

## 📚 Examples

### Bouncing Balls Demo
Shows multiple particles with gravity, elastic collisions, and boundary bouncing.

### Gravity Well Demo
Demonstrates particles with different masses falling and colliding.

### Pyramid Collapse Demo
Creates a pyramid structure that collapses under gravity.

## 🛠️ Future Enhancements

- [ ] Particle-to-particle constraints (springs, rods)
- [ ] Force fields (gravity wells, magnetic fields)
- [ ] Particle emitters and particle systems
- [ ] Spatial partitioning for performance (quadtree)
- [ ] Recording and playback
- [ ] Different rendering backends (OpenGL, web canvas)
- [ ] Soft body physics
- [ ] Fluid simulation

## 🤝 Contributing

This is a modular framework designed to be extended! Feel free to:

- Add new particle extensions
- Create new physics behaviors
- Build custom renderers
- Design new simulation types
- Optimize the physics engine

## 📄 License

See LICENSE file for details.

## 🙏 Acknowledgments

Built with Python and Pygame for educational and experimental purposes.

---

**Happy Simulating! 🎉**
