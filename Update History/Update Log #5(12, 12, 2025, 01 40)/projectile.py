import pygame
import math

class Projectile():
    def move(self):
        move = pygame.math.Vector2(
            math.cos(math.radians(self.angle)),
            math.sin(math.radians(self.angle))
        )
        self.position += move * self.speed

        self.age -= 1
        if self.age < 1:
            self.kill()

    def update(self):
        self.move()
        
        self.rect.center = self.position

class Bullet(Projectile, pygame.sprite.Sprite):
    def __init__(self, player_position, angle):
        super().__init__()

        self.angle = angle
        self.player_position = player_position

        self.position = pygame.math.Vector2(self.player_position)
        
        self.og_image = pygame.image.load("assets/bullet.png").convert_alpha()
        self.image = pygame.transform.rotate(self.og_image, -self.angle)
        self.rect = self.image.get_rect(center = self.position)

        self.speed = 50
        self.age = 120

class Enemy_Projectile_1(Projectile, pygame.sprite.Sprite):
    def __init__(self, position, angle):
        super().__init__()

        self.angle = angle
        self.position = pygame.math.Vector2(position)

        self.og_image = pygame.image.load("assets/enemy_projectile_1.png").convert_alpha()
        self.image = pygame.transform.rotate(self.og_image, -self.angle - 90)
        self.rect = self.image.get_rect(center = self.position)

        self.speed = 10
        self.age = 120
    

