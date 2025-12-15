import pygame
import math
import random

from projectile import *

class Rangers(pygame.sprite.Sprite):
    def __init__(self, image, player, attack_speed, hp, damage, position):
        super().__init__()
        
        self.image = pygame.image.load(image).convert_alpha()
        self.player = player
        
        self.position = position
        self.rect = self.image.get_rect(center = self.position)

        self.hp = hp
        self.damage = damage
        self.attack_speed = attack_speed
        self.cooldown = self.attack_speed

    def scan(self):
        player_distance = self.position.distance_to(self.player.position)
        if player_distance < 600 and self.cooldown == 0:
            self.cooldown = self.attack_speed
            return self.attack()
        return None

    def update(self):
        if self.cooldown > 0:
            self.cooldown -= 1

        projectile = self.scan()
        if projectile:
            return projectile
        return []

class RangedEnemy1(Rangers):
    def __init__(self, player, position = pygame.math.Vector2(100, 100)):
        super().__init__("assets/player.png", player, 180, 2, 1, position)

        self.angle = 0

    def attack(self):
        projectiles = []
        for i in range(8):
            projectiles.append(Enemy_Projectile_1(self.position, self.angle))
            self.angle += 90
        self.angle = 0
        return projectiles

class RangedEnemy2(Rangers):
    def __init__(self, player, position = pygame.math.Vector2(100, 100)):
        super().__init__("assets/player.png", player, 120, 2, 1, position)

        self.player_position = player.position

    def attack(self):
        player_position_x = self.player_position[0] - self.rect.centerx
        player_position_y = self.player_position[1] - self.rect.centery

        angle = math.degrees(math.atan2(player_position_y, player_position_x)) - 30

        projectiles = []
        for i in range(3):
            angle += 15
            projectiles.append(Enemy_Projectile_1(self.position, angle))
        return projectiles

class RangedEnemy3(Rangers):
    def __init__(self, player, position = pygame.math.Vector2(100, 100)):
        super().__init__("assets/player.png", player, 4, 2, 1, position)

        self.player_position = player.position

        self.angle = 0
    
    def attack(self):
        self.angle = random.randint(1, 360)

        projectiles = []
        projectiles.append(Enemy_Projectile_1(self.position, self.angle))
        return projectiles
