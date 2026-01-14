import pygame
import math
import random

from projectile import Enemy_Projectile_1

# Load images, with some error handling
try:
    enemy_img = {
        "placeholder": pygame.image.load("assets/enemy.png"),
        "boss normal": pygame.image.load("assets/boss1Norm.png"),
        "boss attack": pygame.image.load("assets/boss1Att.png")
    }
except:
    default_texture = pygame.surface.Surface((30, 30))
    default_texture.fill((50, 50, 50))
    
    enemy_img = {
        "placeholder": default_texture,
        "boss normal": default_texture,
        "boss attack": default_texture
    }

# Base class for static/unmoving ranged enemies
class Static_Ranged(pygame.sprite.Sprite):
    def __init__(self, player, image, hp, atk_dmg, atk_spd, range, position):
        super().__init__()

        # Base attributes
        self.player = player # Tracks player
        self.og_image = image # Unmodified image
        self.hp = hp # Hit points
        self.atk_dmg = atk_dmg # Damage
        self.atk_spd = atk_spd # Attack speed or frequency
        self.range = range # Range

        # Image and rect
        self.image = self.og_image
        self.position = position
        self.rect = self.image.get_rect(center = self.position)

        # Active attack Cooldown
        self.cooldown = self.atk_spd
    
    # For getting angle toward player position
    def player_angle(self):
        player_position_x = self.player.position[0] - self.rect.centerx
        player_position_y = self.player.position[1] - self.rect.centery

        return math.degrees(math.atan2(player_position_y, player_position_x))

    # Base attack function
    def attack(self):
        return []
    
    # Scan if player is in range before initiating an attack or behavior
    def scan(self):
        # Obtain distance to player
        player_distance = self.position.distance_to(self.player.position)

        if player_distance < self.range and self.cooldown <= 0:
            self.cooldown = self.atk_spd
            return self.attack()
        else:
            return []
    
    # If collission is detected, call this
    def health(self):
        self.hp -= 1
        if self.hp <= 0:
            self.kill()
    
    # Keeps the enemy active and attacking
    def update(self):
        if self.cooldown > 0:
            self.cooldown -= 1

        projectile = self.scan()

        if projectile:
            return projectile
        else:
            return []

# Basic enemy with two attack pattern
class SingleShooter(Static_Ranged):
    def __init__(self, player, position = pygame.math.Vector2(100, 100)):
        super().__init__(player, enemy_img["placeholder"], 2, 1, 120, 600, position)
    
    # Attack pattern
    def attack(self):
        angle = self.player_angle()

        # Creates projectile list
        projectiles = []

        # 60% Chance to do pattern 1, 40% to do pattern 2
        pattern = random.randint(0, 4)

        # Pattern 1: Single shot aimed at player
        if pattern < 3:
            for i in range(1):
                # Adds projectile to list
                projectiles.append(Enemy_Projectile_1(self.position, angle))

        # Pattern 2: Spreadshot of three projectiles aimed at player
        else:
            angle -= 30
            for i in range(3):
                angle += 15
                # Adds projectile to list
                projectiles.append(Enemy_Projectile_1(self.position, angle))
            
        # Returns all projectiles
        return projectiles

# Basic plus shaped attacking enemy
class PlusShooter(Static_Ranged):
    def __init__(self, player, position = pygame.math.Vector2(100, 100)):
        super().__init__(player, enemy_img["placeholder"], 2, 1, 120, 800, position)
    
    # Plus attack pattern
    def attack(self):
        angle = 0

        # Creates projectile list
        projectiles = []

        # Shoots 4 projectiles each at a unique 90 degree angle
        for i in range(4):
            angle += 90
            projectiles.append(Enemy_Projectile_1(self.position, angle))
        
        # Returns all projectiles
        return projectiles

# Basic boss class with three attack pattern
class BossShooter1(Static_Ranged):
    def __init__(self, player, position = pygame.math.Vector2(100, 100)):
        super().__init__(player, enemy_img["boss normal"], 10, 1, 1, 1600, position)

        # Boss calls base class every frame, but has a custom attack speed and cooldown
        self.custom_cooldown = 0
        self.custom_atk_spd = 120

        # Obtain information of the room the boss is in
        self.room_position = 0
        self.room_dimensions = 0
    
    # 3 actions possible
    def attack(self):
        projectiles = []
        self.custom_cooldown += 1

        # Rage mode, doubles attack speed
        if self.hp <= 5:
            self.custom_atk_spd = 60
            
        # Change of sprite when 1 second before attacking
        if self.custom_cooldown >= self.custom_atk_spd - 60:
            self.image = enemy_img["boss attack"]

        # Initiates an action
        if self.custom_cooldown >= self.custom_atk_spd:
            # Chooses a random action
            pattern = random.randint(0, 2)

            # Shoots projectiles at all direction
            if pattern == 0:
                angle = 0
                for i in range(20):
                    angle += 18
                    projectiles.append(Enemy_Projectile_1(self.position, angle))

            # Shoots 5 projectiles toward player
            if pattern == 1:
                angle = self.player_angle() - 18
                for i in range(5):
                    angle += 6
                    projectiles.append(Enemy_Projectile_1(self.position, angle))
            
            # Moves to one of 5 random locations in the room
            if pattern == 2:
                new_position = random.randint(0, 4)
                positions = [
                    pygame.math.Vector2(self.room_position[0] + self.room_dimensions[0] * 5 // 48, self.room_position[1] + self.room_dimensions[1] * 5 // 48),
                    pygame.math.Vector2(self.room_position[0] + self.room_dimensions[0] * 5 // 48, self.room_position[1] + self.room_dimensions[1] * 43 // 48),
                    pygame.math.Vector2(self.room_position[0] + self.room_dimensions[0] * 43 // 48, self.room_position[1] + self.room_dimensions[1] * 5 // 48),
                    pygame.math.Vector2(self.room_position[0] + self.room_dimensions[0] * 43 // 48, self.room_position[1] + self.room_dimensions[1] * 43 // 48),
                    pygame.math.Vector2(self.room_position[0] + self.room_dimensions[0] // 2, self.room_position[1] + self.room_dimensions[1] // 2),
                ]
                self.position = positions[new_position]

                self.rect = self.image.get_rect(center = self.position)

            # Reverts sprite to normal
            self.image = enemy_img["boss normal"]
            self.custom_cooldown = 0
            
        # Returns all projectiles
        return projectiles

            