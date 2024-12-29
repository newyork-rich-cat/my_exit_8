# 창연이의 Exit 8

창연이의 Exit 8, Python, Ursina game engine
![alt text](image.png)

## Game Overview
A horror-themed corridor game where players must navigate through a mysterious hallway while avoiding anomalies and an NPC.

## Key Features
- First-person perspective gameplay
- Patrolling NPC that must be avoided
- Random anomaly events that affect the environment:
  - NPC size changes
  - Floor color shifts
  - Wall texture alterations 
  - NPC movement direction changes
  - Poster transformations
  - Interactive eye poster that follows player
- Progress tracking via exit signs
- Multiple sections including main corridor and side areas
- Victory achieved after 8 successful loops

## Code Structure
- Uses Ursina engine for 3D graphics and physics
- Clean separation of game mechanics:
  - Environment setup (walls, floor, ceiling, decorations)
  - Player and NPC controls
  - Anomaly system with various effects
  - Game state management (progress, win/loss conditions)
  - Update loop for continuous gameplay

## Technical Implementation
- Proper use of global state management
- Modular functions for different game aspects
- Collision detection and position-based triggers
- Animation system for movement and effects
- Asset management for textures and 3D models
- Randomized event system for anomalies

## Areas for Potential Enhancement
- Additional anomaly types
- More varied NPC behaviors
- Sound effects and background music
- Difficulty progression
- Save/load system

