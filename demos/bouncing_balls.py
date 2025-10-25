"""
Bouncing Balls Demo
A demonstration of the particle physics system with gravity, collisions, and bouncing.
"""

import random
import sys
import os

# Add parent directory to path to import playground
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from playground import BasePlayground
from entities import Particle, System


class BouncingBallsDemo(BasePlayground):
    """
    Demo showing multiple bouncing balls with realistic physics.
    """
    
    def __init__(self):
        # Create custom physics with adjusted parameters
        system = System()
        system.physics.gravity = 500.0  # Pixels per second squared
        system.physics.friction = 0.1
        system.physics.air_resistance = 0.001
        system.physics.bounce_coefficient = 0.8
        system.physics.elasticity = 0.9
        
        super().__init__(system=system, width=800, height=600, fps=60)
    
    def setup(self):
        """Set up the demo with various particles."""
        
        # Add some bouncing balls
        colors = [
            (255, 100, 100),  # Red
            (100, 255, 100),  # Green
            (100, 100, 255),  # Blue
            (255, 255, 100),  # Yellow
            (255, 100, 255),  # Magenta
            (100, 255, 255),  # Cyan
        ]
        
        # Create random particles
        for i in range(15):
            x = random.randint(100, 700)
            y = random.randint(50, 200)
            mass = random.uniform(0.5, 2.0)
            radius = 5 + mass * 10
            color = random.choice(colors)
            
            particle = Particle(x=x, y=y, mass=mass, radius=radius, color=color)
            
            # Give initial velocity
            particle.state.velocity_x = random.uniform(-100, 100)
            particle.state.velocity_y = random.uniform(-50, 50)
            
            self.add_particle(particle)
        
        # Add some static particles (platforms)
        platform_color = (150, 150, 150)
        
        # Bottom platforms
        for x in range(100, 700, 80):
            platform = Particle(x=x, y=550, mass=10.0, radius=20, color=platform_color)
            platform.state.is_static = True
            self.add_particle(platform)
        
        # Side platforms
        platform = Particle(x=150, y=400, mass=10.0, radius=25, color=platform_color)
        platform.state.is_static = True
        self.add_particle(platform)
        
        platform = Particle(x=650, y=400, mass=10.0, radius=25, color=platform_color)
        platform.state.is_static = True
        self.add_particle(platform)
        
        print("\n=== Bouncing Balls Demo ===")
        print(f"Created {len(self.particles)} particles")
        print("\nControls:")
        print("  SPACE - Pause/Resume")
        print("  R - Reset simulation")
        print("  ESC - Quit")
        print("\nPress SPACE to pause and observe the physics!")


class GravityWellDemo(BasePlayground):
    """
    Demo showing particles falling with different masses.
    """
    
    def __init__(self):
        system = System()
        system.physics.gravity = 300.0
        system.physics.friction = 0.05
        system.physics.bounce_coefficient = 0.7
        system.physics.elasticity = 0.8
        
        super().__init__(system=system, width=800, height=600, fps=60)
    
    def setup(self):
        """Create particles at the top that fall down."""
        
        # Create particles with varying masses
        for i in range(10):
            x = 100 + i * 70
            mass = 0.5 + i * 0.3
            radius = 8 + mass * 5
            
            # Color based on mass (red = heavy, blue = light)
            red = min(255, int(50 + mass * 50))
            blue = max(50, int(255 - mass * 50))
            
            particle = Particle(x=x, y=50, mass=mass, radius=radius, color=(red, 100, blue))
            self.add_particle(particle)
        
        # Add floor
        for x in range(50, 750, 30):
            floor = Particle(x=x, y=580, mass=100.0, radius=15, color=(100, 100, 100))
            floor.state.is_static = True
            self.add_particle(floor)
        
        print("\n=== Gravity Well Demo ===")
        print("Particles with different masses falling")
        print("Notice how they all fall at the same rate (physics!)")
        print("But interact differently on collision due to mass differences")


class ChainDemo(BasePlayground):
    """
    Demo showing connected particles (future extension).
    """
    
    def __init__(self):
        system = System()
        system.physics.gravity = 400.0
        system.physics.friction = 0.2
        system.physics.air_resistance = 0.005
        system.physics.bounce_coefficient = 0.6
        
        super().__init__(system=system, width=800, height=600, fps=60)
    
    def setup(self):
        """Create a cluster of particles."""
        
        # Create a pyramid of particles
        start_x = 300
        start_y = 100
        spacing = 50
        
        for row in range(5):
            for col in range(5 - row):
                x = start_x + col * spacing + row * spacing / 2
                y = start_y + row * spacing
                
                particle = Particle(
                    x=x, y=y, 
                    mass=1.0, 
                    radius=12, 
                    color=(255, 200, 100)
                )
                self.add_particle(particle)
        
        # Add ground
        for x in range(20, 780, 40):
            ground = Particle(x=x, y=580, mass=50.0, radius=20, color=(80, 80, 80))
            ground.state.is_static = True
            self.add_particle(ground)
        
        print("\n=== Chain/Cluster Demo ===")
        print("Pyramid of particles collapsing under gravity")


def main():
    """Run the demo."""
    print("\n" + "="*50)
    print("PARTICLE PHYSICS PLAYGROUND - DEMOS")
    print("="*50)
    print("\nChoose a demo:")
    print("1. Bouncing Balls (default)")
    print("2. Gravity Well")
    print("3. Pyramid Collapse")
    print()
    
    choice = input("Enter choice (1-3) or press Enter for demo 1: ").strip()
    
    if choice == "2":
        demo = GravityWellDemo()
    elif choice == "3":
        demo = ChainDemo()
    else:
        demo = BouncingBallsDemo()
    
    demo.run()


if __name__ == "__main__":
    main()
