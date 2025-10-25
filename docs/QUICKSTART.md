# 🚀 Quick Start Guide

## Installation (5 minutes)

### Step 1: Install Dependencies

```bash
cd /test/test/Documents/test-projects/pygame-test
pip install -r requirements.txt
```

This will install:
- `pygame` - The rendering and window management library

### Step 2: Run the Main Menu

```bash
python main.py
```

You'll see an interactive menu with all available demos!

### Step 3: Try the Interactive Demo

The most fun way to start:

```bash
python demos/interactive_spawner.py
```

**Click anywhere to spawn particles!** Watch them fall, bounce, and collide with physics.

## 🎮 Controls

All demos support:
- **SPACE** - Pause/Resume the simulation
- **R** - Reset (clear dynamic particles)
- **ESC** - Quit

Interactive Spawner adds:
- **LEFT CLICK** - Spawn particles at mouse position

## 📝 Create Your First Simulation (2 minutes)

Create a file `my_simulation.py`:

```python
import sys
sys.path.insert(0, '.')

from playground import BasePlayground
from entities import Particle

class MySimulation(BasePlayground):
    def setup(self):
        # Create a falling ball
        ball = Particle(
            x=400,        # Center X
            y=100,        # Top of screen
            mass=1.0,     # Normal mass
            radius=15,    # Size
            color=(255, 0, 0)  # Red
        )
        ball.state.velocity_y = 50  # Initial downward velocity
        self.add_particle(ball)
        
        # Create a static platform
        platform = Particle(
            x=400, 
            y=500, 
            mass=10.0, 
            radius=40, 
            color=(150, 150, 150)
        )
        platform.state.is_static = True  # Won't move!
        self.add_particle(platform)

# Run it!
if __name__ == "__main__":
    MySimulation().run()
```

Run it:
```bash
python my_simulation.py
```

## 🎯 Next Steps

### Try Different Physics

```python
from entities import System

system = System()
system.physics.gravity = 800.0  # More gravity!
system.physics.bounce_coefficient = 0.95  # Very bouncy!
system.physics.friction = 0.3  # More friction

playground = BasePlayground(system=system)
```

### Add Multiple Particles

```python
def setup(self):
    import random
    
    # Create 20 random particles
    for i in range(20):
        x = random.randint(100, 700)
        y = random.randint(50, 200)
        mass = random.uniform(0.5, 2.0)
        radius = 5 + mass * 8
        
        color = (
            random.randint(100, 255),
            random.randint(100, 255),
            random.randint(100, 255)
        )
        
        particle = Particle(x, y, mass=mass, radius=radius, color=color)
        self.add_particle(particle)
```

### Create Interactive Simulations

```python
def handle_events(self):
    super().handle_events()  # Keep default controls
    
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            particle = Particle(x, y, mass=1.0, radius=10, color=(255, 255, 0))
            self.add_particle(particle)
```

## 📚 Learn More

- Read `README.md` for full documentation
- Check `ARCHITECTURE.md` for system design
- See `ENHANCEMENTS.md` for what was added
- Explore demos in `demos/` folder

## 🐛 Troubleshooting

### "pygame not found"
```bash
pip install pygame
```

### "No module named 'entities'"
Make sure you're running from the project root directory:
```bash
cd /test/test/Documents/test-projects/pygame-test
python your_script.py
```

### Window doesn't appear
- Check if pygame initialized correctly
- Try running one of the demo files first
- Make sure you called `.run()` on your playground

### Particles fall through floor
- Make sure boundary is set: `system.set_bounds(0, 0, width, height)`
- Or add static particles as floor

## 🎨 Customization Ideas

1. **Change colors** - Modify particle colors dynamically
2. **Add trails** - Draw lines following particles
3. **Different shapes** - Override `draw_particle()` in renderer
4. **Force fields** - Apply custom forces in `update()`
5. **Particle effects** - Create emitters and particle systems
6. **Sound effects** - Add sounds on collision using pygame.mixer
7. **Levels** - Create different scenarios with setup variations

## 💡 Pro Tips

1. **Lower gravity** = floaty, space-like physics
2. **Higher friction** = particles slow down faster
3. **Large radius + small mass** = beach ball effect
4. **Static particles** = platforms, walls, obstacles
5. **Pause (SPACE)** = great for debugging and screenshots

## 🎉 Have Fun!

You now have a complete physics playground. Experiment, learn, and create amazing simulations!

Need help? Check the documentation files or examine the demo code.

**Happy coding! 🚀**
