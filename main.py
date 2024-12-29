"""
A horror-themed corridor game built with Ursina engine.
The player must navigate through a corridor while avoiding anomalies and an NPC.
"""

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from direct.actor.Actor import Actor
import random
import time

app = Ursina()
mouse.visible = False

# Create corridor walls, floor and ceiling
main_floor = Entity(model='cube', position=(0, 0, 0), scale=(10, 1, 100), color=color.gray, collider='box')
main_ceiling = Entity(model='cube', position=(0, 10, 0), scale=(10, 1, 100), color=color.gray, collider='box')
main_left_wall = Entity(model='cube', position=(-5, 5, -5), scale=(1, 10, 110), collider='box', texture='assets/wall.jpg', texture_scale=(16, 10))
main_right_wall = Entity(model='cube', position=(5, 5, 5), scale=(1, 10, 110), collider='box', texture='assets/wall.jpg', texture_scale=(16, 10))

# Create floor tiles
for i in range(-90, 90):
    tiles = Entity(model='cube', position=(0, 0.5, i*0.5), scale=(0.5, 0, 0.5), texture='assets/yellow_tile.jpg')

# Create front section geometry
front_floor = Entity(model='cube', position=(-25, 0, 55), scale=(60, 1, 10), color=color.gray, collider='box')
front_ceiling = Entity(model='cube', position=(-25, 10, 55), scale=(60, 1, 10), color=color.gray, collider='box')
front_left_wall = Entity(model='cube', position=(-30, 5, 50), scale=(50, 10, 1), collider='box', texture='assets/wall.jpg', texture_scale=(16, 10))
front_right_wall = Entity(model='cube', position=(-20, 5, 60), scale=(50, 10, 1), collider='box', texture='assets/wall.jpg', texture_scale=(16, 10))

front_floor_2 = Entity(model='cube', position=(-50, 0, 80), scale=(10, 1, 60), color=color.gray, collider='box')
front_ceiling_2 = Entity(model='cube', position=(-50, 10, 80), scale=(10, 1, 60), color=color.gray, collider='box')
front_left_wall_2 = Entity(model='cube', position=(-55, 5, 75), scale=(1, 10, 50), collider='box', texture='assets/wall.jpg', texture_scale=(16, 10))
front_right_wall_2 = Entity(model='cube', position=(-45, 5, 85), scale=(1, 10, 50), collider='box', texture='assets/wall.jpg', texture_scale=(16, 10))

# Create back section geometry
back_floor = Entity(model='cube', position=(25, 0, -55), scale=(60, 1, 10), color=color.gray, collider='box')
back_ceiling = Entity(model='cube', position=(25, 10, -55), scale=(60, 1, 10), color=color.gray, collider='box')
back_left_wall = Entity(model='cube', position=(30, 5, -50), scale=(50, 10, 1), collider='box', texture='assets/wall.jpg', texture_scale=(16, 10))
back_right_wall = Entity(model='cube', position=(20, 5, -60), scale=(50, 10, 1), collider='box', texture='assets/wall.jpg', texture_scale=(16, 10))

back_floor_2 = Entity(model='cube', position=(50, 0, -80), scale=(10, 1, 60), color=color.gray, collider='box')
back_ceiling_2 = Entity(model='cube', position=(50, 10, -80), scale=(10, 1, 60), color=color.gray, collider='box')
back_left_wall_2 = Entity(model='cube', position=(55, 5, -75), scale=(1, 10, 50), collider='box', texture='assets/wall.jpg', texture_scale=(16, 10))
back_right_wall_2 = Entity(model='cube', position=(45, 5, -85), scale=(1, 10, 50), collider='box', texture='assets/wall.jpg', texture_scale=(16, 10))

# Create signage
sign_ceiling = Entity(model='cube', position=(0, 9, 25), scale=(5.2, 1, 0.1), texture='assets/exit_8_ceiling.jpg')
sign_wall_front = Entity(model='cube', position=(-54.4, 4.5, 55), scale=(0.1, 3.8, 2), texture='assets/exit_0_wall.jpg')
sign_wall_back = Entity(model='cube', position=(-4.4, 4.5, -55), scale=(0.1, 3.8, 2), texture='assets/exit_0_wall.jpg')

# Create lighting
for z in range(-40, 41, 20):
    lamp = Entity(model='sphere', position=(0, 9.5, z), scale=(0.3, 0.3, 0.3), color=color.yellow)

# Create eye poster
eye_poster = Entity(
    model='cube', 
    position=(-4.4, 4.5, -25),
    scale=(0.1, 3.8, 2.4),
    texture='assets/eye_front.png'
)

# Create decorative wall posters
poster_positions_left = [(-4.4, 4.5, -10), (-4.4, 4.5, -5), (-4.4, 4.5, 0), (-4.4, 4.5, 5), (-4.4, 4.5, 10)]
posters = []
for i, pos in enumerate(poster_positions_left):
    poster_num = (i % 5) + 1
    poster = Entity(model='cube', position=pos, scale=(0.1, 3.8, 2.4), texture=f'assets/poster{poster_num}.jpg')
    posters.append(poster)

# Initialize player
player = FirstPersonController()
player.cursor.visible = False
player.gravity = 0.5
player.speed = 15
player.position = Vec3(0, 1, -45)

# Initialize NPC
npc = Entity(position=(-1.5, 0.5, 45), scale=(1.25, 1.25, 1.25), collider='box')
actor = Actor('assets/npc.glb')
actor.reparent_to(npc)
print(actor.getAnimNames())
actor.loop('Armature|mixamo.com|Layer0')

# Game state variables
count = 0  # Progress counter
is_game_over = False  # Game over flag
npc_dir = -1  # NPC movement direction
is_anomaly_active = False  # Anomaly state
current_anomaly = None  # Current active anomaly
is_walking_backward = False  # NPC walking direction

def game_over():
    """Handle game over state by animating walls falling and player falling."""
    global is_game_over
    is_game_over = True
    for wall in [main_left_wall, main_right_wall]:
        wall.animate_position(wall.position + Vec3(0, -10, 0), duration=3)
    main_floor.animate_position(main_floor.position + Vec3(0, -10, 0), duration=3)
    invoke(player.animate_position, player.position + Vec3(0, -50, 0), duration=5, curve=curve.linear)
    Text(text='GAME OVER', scale=2, origin=(0, 0), color=color.red)

def clear_game():
    """Display victory message when game is cleared."""
    Text(text='CLEAR!', scale=2, origin=(0, 0), color=color.green)

def update_exit_posters():
    """Update exit sign textures based on current progress."""
    sign_wall_front.texture = f'assets/exit_{count}_wall.jpg'
    sign_wall_back.texture = f'assets/exit_{count}_wall.jpg'

def trigger_anomaly():
    """Randomly trigger and apply an anomaly effect."""
    global is_anomaly_active, current_anomaly, is_walking_backward, used_anomalies
    
    if 'used_anomalies' not in globals():
        used_anomalies = []
        
    random_value = random.random()
    print(f"Random value: {random_value:.3f}")
    if not is_anomaly_active and random_value < 0.5:  # 50% chance
        is_anomaly_active = True
        available_anomalies = [x for x in ['scale_npc', 'floor_color', 'wall_texture', 'backward_npc', 'change_poster_a', 'change_poster_b', 'eye_direction', 'eye_flash'] if x not in used_anomalies]
        if not available_anomalies:
            used_anomalies = []
            available_anomalies = ['scale_npc', 'floor_color', 'wall_texture', 'backward_npc', 'change_poster_a', 'change_poster_b', 'eye_direction', 'eye_flash']
        current_anomaly = random.choice(available_anomalies)
        used_anomalies.append(current_anomaly)
        print(f"Triggered anomaly: {current_anomaly}")
        
        # Apply anomaly effects
        if current_anomaly == 'scale_npc':
            npc.scale *= 2
        elif current_anomaly == 'floor_color':
            main_floor.color = color.rgb(0.4, 0.4, 0.35)  
        elif current_anomaly == 'wall_texture':
            main_left_wall.texture = 'assets/wallkill.jpg'
            main_right_wall.texture = 'assets/wallkill.jpg'
        elif current_anomaly == 'backward_npc':
            is_walking_backward = True
            actor.setPlayRate(-1, 'Armature|mixamo.com|Layer0')
            npc.rotation_y = 180 if npc_dir == -1 else 0
        elif current_anomaly == 'change_poster_a':
            for i, poster in enumerate(posters):
                poster.texture = f'assets/aposter{i+1}.jpg'
        elif current_anomaly == 'change_poster_b':
            for i, poster in enumerate(posters):
                poster.texture = f'assets/bposter{i+1}.jpg'

def resolve_anomaly():
    """Reset any active anomaly effects."""
    global is_anomaly_active, current_anomaly, is_walking_backward
    if current_anomaly == 'scale_npc':
        npc.scale /= 2
    elif current_anomaly == 'floor_color':
        main_floor.color = color.gray
    elif current_anomaly == 'wall_texture':
        main_left_wall.texture = 'assets/wall.jpg'
        main_right_wall.texture = 'assets/wall.jpg'
    elif current_anomaly == 'backward_npc':
        is_walking_backward = False
        actor.setPlayRate(1, 'Armature|mixamo.com|Layer0')
        npc.rotation_y = 180 if npc_dir == 1 else 0
    elif current_anomaly in ['change_poster_a', 'change_poster_b']:
        for i, poster in enumerate(posters):
            poster.texture = f'assets/poster{i+1}.jpg'
    is_anomaly_active = False
    current_anomaly = None

def update():
    """Main game loop update function."""
    global npc_dir, count, is_game_over, is_anomaly_active

    if is_game_over:
        return

    # Update eye poster behavior
    if current_anomaly == 'eye_direction':
        if player.z < eye_poster.z - 2:
            eye_poster.texture = 'assets/eye_left.png'
        elif player.z > eye_poster.z + 2:
            eye_poster.texture = 'assets/eye_right.png'
        else:
            eye_poster.texture = 'assets/eye_front.png'
    
    if current_anomaly == 'eye_flash':
        if abs(player.z - eye_poster.z) < 2:
            eye_poster.texture = 'assets/eye_red.png'
        else:
            eye_poster.texture = 'assets/eye_front.png'

    # Update NPC patrol movement
    if npc_dir == -1 and npc.position.z < -45:
        npc_dir = 1
        npc.rotation_y = 0 if is_walking_backward else 180
    elif npc_dir == 1 and npc.position.z > 45:
        npc_dir = -1
        npc.rotation_y = 180 if is_walking_backward else 0

    npc.position += Vec3(0, 0, npc_dir * 15 * time.dt)

    # Check player collision with NPC
    if distance(player.position, npc.position) < 2:
        game_over()
        return

    # Handle player teleportation and progress
    if player.position.x < -25 and player.position.z > 50:
        if is_anomaly_active:
            game_over()
        else:
            player.position = Vec3(50 + player.position.x, player.position.y, -110 + player.position.z)
            count += 1
            update_exit_posters()
            trigger_anomaly()
    elif player.position.x > 25 and player.position.z < -50:
        if is_anomaly_active:
            player.set_position((-50 + player.position.x, player.position.y, 110 + player.position.z))
            resolve_anomaly()
        else:
            player.position = Vec3(-50 + player.position.x, player.position.y, 110 + player.position.z)
            count += 1
            update_exit_posters()
            trigger_anomaly()

    # Check win condition
    if count >= 8:
        clear_game()
        return

    # Check fall death
    if player.position.y < -10:
        game_over()

app.run()
