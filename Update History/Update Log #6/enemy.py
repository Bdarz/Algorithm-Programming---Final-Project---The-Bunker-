import pygame
import math
import random

from projectile import Bullet, Enemy_Projectile_1

enemy_img = {
    "placeholder": pygame.image.load("assets/player.png"),
    "boss normal": pygame.image.load("assets/boss1Norm.png"),
    "boss attack": pygame.image.load("assets/boss1Att.png")
}

class Rangers(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()

        self.player = player
    
    def scan(self):
        player_distance = self.position.distance_to(self.player.position)
        if player_distance < self.range and self.cooldown == 0:
            self.cooldown = self.attack_speed
            return self.attack()
        return None
    
    def update(self):
        self.scan()
class Rangers(pygame.sprite.Sprite):
    def __init__(self, image, player, attack_speed, hp, damage, position, scan_range = 600):
        super().__init__()
        
        self.og_image = pygame.image.load(image).convert_alpha()
        self.att_image = pygame.image.load("assets/boss1Att.png").convert_alpha()
        self.image = self.og_image
        self.player = player
        
        self.position = position
        self.rect = self.image.get_rect(center = self.position)

        self.hp = hp
        self.damage = damage
        self.attack_speed = attack_speed
        self.cooldown = self.attack_speed
        self.scan_range = scan_range

    def scan(self):
        player_distance = self.position.distance_to(self.player.position)
        if player_distance < self.scan_range and self.cooldown == 0:
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

class SingleShooter(Rangers):
    def __init__(self, player, position = pygame.math.Vector2(100, 100)):
        super().__init__("assets/player.png", player, 120, 2, 1, position)
    
    def attack(self):
        player_position_x = self.player.position[0] - self.rect.centerx
        player_position_y = self.player.position[1] - self.rect.centery

        angle = math.degrees(math.atan2(player_position_y, player_position_x))

        projectiles = []
        pattern = random.randint(0, 4)
        if pattern < 3:
            for i in range(1):
                projectiles.append(Enemy_Projectile_1(self.position, angle))
        else:
            angle -= 30
            for i in range(3):
                angle += 15
                projectiles.append(Enemy_Projectile_1(self.position, angle))
        return projectiles

class PlusShooter(Rangers):
    def __init__(self, player, position = pygame.math.Vector2(100, 100)):
        super().__init__("assets/player.png", player, 240, 4, 1, position)
    
    def attack(self):
        angle = 0

        projectiles = []
        for i in range(4):
            angle += 90
            projectiles.append(Enemy_Projectile_1(self.position, angle))
        return projectiles
    
class XShooter(Rangers):
    def __init__(self, player, position = pygame.math.Vector2(100, 100)):
        super().__init__("assets/player.png", player, 240, 4, 1, position)
    
    def attack(self):
        angle = 45

        projectiles = []
        for i in range(4):
            angle += 90
            projectiles.append(Enemy_Projectile_1(self.position, angle))
        return projectiles

class BossShooter1(Rangers):
    def __init__(self, player, position = pygame.math.Vector2(100, 100)):
        super().__init__("assets/boss1Norm.png", player, 1, 10, 1, position, 1600)

        self.timer = 0
        self.custom_attack_speed = 120

        self.rposition = 0
        self.dimensions = 0
    
    def attack(self):
        projectiles = []
        self.timer += 1
        if self.hp <= 5:
            self.custom_attack_speed = 60
            
        if self.timer >= self.custom_attack_speed - 60:
            self.image = self.att_image

        if self.timer >= self.custom_attack_speed:
            pattern = random.randint(0, 2)
            if pattern == 0:
                angle = 0
                for i in range(20):
                    angle += 18
                    projectiles.append(Enemy_Projectile_1(self.position, angle))

            if pattern == 1:
                player_position_x = self.player.position[0] - self.rect.centerx
                player_position_y = self.player.position[1] - self.rect.centery

                angle = math.degrees(math.atan2(player_position_y, player_position_x)) - 18

                for i in range(5):
                    angle += 6
                    projectiles.append(Enemy_Projectile_1(self.position, angle))
            
            if pattern == 2:
                new_position = random.randint(0, 4)
                positions = [
                    pygame.math.Vector2(self.rposition[0] + self.dimensions[0] * 5 // 48, self.rposition[1] + self.dimensions[1] * 5 // 48),
                    pygame.math.Vector2(self.rposition[0] + self.dimensions[0] * 5 // 48, self.rposition[1] + self.dimensions[1] * 43 // 48),
                    pygame.math.Vector2(self.rposition[0] + self.dimensions[0] * 43 // 48, self.rposition[1] + self.dimensions[1] * 5 // 48),
                    pygame.math.Vector2(self.rposition[0] + self.dimensions[0] * 43 // 48, self.rposition[1] + self.dimensions[1] * 43 // 48),
                    pygame.math.Vector2(self.rposition[0] + self.dimensions[0] // 2, self.rposition[1] + self.dimensions[1] // 2),
                ]
                self.position = positions[new_position]
                self.rect = self.image.get_rect(center = self.position)

            self.image = self.og_image
            self.timer = 0
        return projectiles

            