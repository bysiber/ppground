"""
Main entry point for Particle Physics Playground
Run this to see available demos and simulations.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def print_menu():
    """Print the main menu."""
    print("\n" + "="*60)
    print(" 🎮  PARTICLE PHYSICS PLAYGROUND  🎮")
    print("="*60)
    print("\nAvailable Demos:")
    print()
    print("  1. Bouncing Balls Demo")
    print("     - Multiple particles with realistic physics")
    print("     - Gravity, collisions, and elastic bouncing")
    print()
    print("  2. Gravity Well Demo")
    print("     - Particles with different masses falling")
    print("     - Demonstrates mass effects on collisions")
    print()
    print("  3. Pyramid Collapse Demo")
    print("     - Pyramid structure collapsing under gravity")
    print("     - Complex multi-particle interactions")
    print()
    print("  4. Interactive Spawner")
    print("     - Click to spawn particles!")
    print("     - Most fun and interactive demo")
    print()
    print("  5. Exit")
    print()
    print("="*60)


def run_demo(choice):
    """Run the selected demo."""
    try:
        if choice == "1":
            from demos.bouncing_balls import BouncingBallsDemo
            demo = BouncingBallsDemo()
            demo.run()
        elif choice == "2":
            from demos.bouncing_balls import GravityWellDemo
            demo = GravityWellDemo()
            demo.run()
        elif choice == "3":
            from demos.bouncing_balls import ChainDemo
            demo = ChainDemo()
            demo.run()
        elif choice == "4":
            from demos.interactive_spawner import InteractiveSpawner
            demo = InteractiveSpawner()
            demo.run()
        elif choice == "5":
            print("\nThanks for using Particle Physics Playground! 👋\n")
            return False
        else:
            print("\n❌ Invalid choice. Please select 1-5.")
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted. Returning to menu...")
    except Exception as e:
        print(f"\n❌ Error running demo: {e}")
        import traceback
        traceback.print_exc()
    
    return True


def main():
    """Main entry point."""
    print("\n🌟 Welcome to Particle Physics Playground! 🌟")
    print("\nA modular physics simulation framework built with Python & Pygame")
    
    # Check if pygame is installed
    try:
        import pygame
        print("✅ Pygame detected")
    except ImportError:
        print("\n❌ Pygame not found!")
        print("Please install dependencies:")
        print("  pip install -r requirements.txt")
        return
    
    while True:
        print_menu()
        choice = input("Enter your choice (1-5): ").strip()
        
        if not run_demo(choice):
            break


if __name__ == "__main__":
    main()
