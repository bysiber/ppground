# Architecture Overview

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         PLAYGROUND                              │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  BasePlayground                                            │ │
│  │  - run()           : Main game loop                        │ │
│  │  - update(dt)      : Physics update                        │ │
│  │  - render()        : Draw all particles                    │ │
│  │  - handle_events() : Input handling                        │ │
│  │  - setup()         : Override for custom simulations       │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                             │
                ┌────────────┴────────────┐
                │                         │
                ▼                         ▼
┌───────────────────────────┐   ┌──────────────────────┐
│       RENDERER            │   │      SYSTEM          │
│  ┌─────────────────────┐  │   │  ┌────────────────┐  │
│  │  PygameRenderer     │  │   │  │  Physics       │  │
│  │  - draw_particle()  │  │   │  │  - gravity     │  │
│  │  - draw_dot()       │  │   │  │  - friction    │  │
│  │  - screen           │  │   │  │  - elasticity  │  │
│  │  - clock            │  │   │  │  - etc...      │  │
│  └─────────────────────┘  │   │  └────────────────┘  │
└───────────────────────────┘   │                      │
                                │  ┌────────────────┐  │
                                │  │ PhysicsEngine  │  │
                                │  │ - apply_*()    │  │
                                │  │ - collisions   │  │
                                │  │ - boundaries   │  │
                                │  └────────────────┘  │
                                └──────────────────────┘
                                          │
                                          │
                                          ▼
                        ┌─────────────────────────────────┐
                        │         PARTICLE                │
                        │  ┌────────────────────────────┐ │
                        │  │  Position                  │ │
                        │  │  - x, y, z                 │ │
                        │  └────────────────────────────┘ │
                        │  ┌────────────────────────────┐ │
                        │  │  ParticleState             │ │
                        │  │  - velocity_x/y/z          │ │
                        │  │  - acceleration_x/y/z      │ │
                        │  │  - mass, radius, color     │ │
                        │  │  - is_static, is_active    │ │
                        │  └────────────────────────────┘ │
                        │  ┌────────────────────────────┐ │
                        │  │  Extensions                │ │
                        │  │  - Custom behaviors        │ │
                        │  │  - LinkedList, etc.        │ │
                        │  └────────────────────────────┘ │
                        └─────────────────────────────────┘
```

## Data Flow

```
User Input
    │
    ▼
┌─────────────┐
│ Playground  │
└─────────────┘
    │
    ├──► handle_events() ──► Keyboard/Mouse ──► Actions
    │
    ▼
┌─────────────┐
│  update(dt) │
└─────────────┘
    │
    ▼
┌──────────────────────┐
│  PhysicsEngine       │
│  1. Apply forces     │
│  2. Update particles │───► Particle.update(dt)
│  3. Check collisions │         │
└──────────────────────┘         ▼
    │                    ┌───────────────────┐
    │                    │ Position += vel*dt│
    │                    │ Velocity += acc*dt│
    │                    └───────────────────┘
    ▼
┌─────────────┐
│  render()   │
└─────────────┘
    │
    ▼
┌──────────────────────┐
│  PygameRenderer      │
│  - Clear screen      │
│  - Draw particles    │
│  - Update display    │
└──────────────────────┘
```

## Physics Update Cycle

```
Each Frame (1/60 second at 60 FPS):

1. Clear forces from previous frame
   ▼
2. Apply gravity (F = m * g)
   ▼
3. Apply friction (F = -v * k)
   ▼
4. Apply air resistance (F = -v² * k)
   ▼
5. Apply custom forces
   ▼
6. Calculate acceleration (a = F / m)
   ▼
7. Update velocity (v += a * dt)
   ▼
8. Update position (p += v * dt)
   ▼
9. Check boundary collisions
   ▼
10. Check particle-particle collisions
    ▼
11. Resolve collisions with impulses
    ▼
12. Render frame
```

## Collision Detection Algorithm

```
For each particle pair (i, j):
    
    1. Calculate distance
       d = sqrt((x2-x1)² + (y2-y1)²)
    
    2. Check if colliding
       if d < (r1 + r2):
    
    3. Calculate normal vector
       n = (x2-x1)/d, (y2-y1)/d
    
    4. Separate particles
       overlap = (r1 + r2) - d
       move each particle by overlap/2
    
    5. Calculate relative velocity
       dv = v2 - v1
    
    6. Calculate impulse
       j = -(1 + e) * (dv · n) / (1/m1 + 1/m2)
    
    7. Apply impulse
       v1 -= (j/m1) * n
       v2 += (j/m2) * n
```

## Extension System

```
Particle
   │
   ├─► Extensions (Dict)
   │     │
   │     ├─► "linked_list" ──► LinkedListExtension
   │     │                        ├─► prev
   │     │                        └─► next
   │     │
   │     ├─► "custom" ──► Your Custom Extension
   │     │                  └─► custom behaviors
   │     │
   │     └─► "actions" ──► Action handlers
   │
   └─► register_extension(name, class)
```

## Class Hierarchy

```
Renderer (ABC)
    │
    └─► PygameRenderer
    └─► (Future: OpenGLRenderer, WebRenderer, etc.)

Playground
    │
    └─► BasePlayground
          │
          ├─► BouncingBallsDemo
          ├─► GravityWellDemo
          ├─► ChainDemo
          ├─► InteractiveSpawner
          └─► (Your custom playgrounds!)

Particle
    ├─► Position
    ├─► ParticleState
    └─► Extensions (dict)

System
    ├─► Physics (config)
    └─► PhysicsEngine
```

## Key Design Principles

1. **Separation of Concerns**
   - Particles know their state
   - Physics engine knows physics
   - Renderer knows drawing
   - Playground orchestrates

2. **Open/Closed Principle**
   - Open for extension (Extensions, custom playgrounds)
   - Closed for modification (core classes stable)

3. **Dependency Inversion**
   - Depend on abstractions (Renderer ABC)
   - Not on concrete implementations

4. **Single Responsibility**
   - Each class has one job
   - Each module has one purpose

5. **Composition over Inheritance**
   - Particles have extensions
   - Not rigid inheritance hierarchies
```
