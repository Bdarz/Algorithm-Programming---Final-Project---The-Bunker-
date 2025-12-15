import pygame
import math

proj_img = {
    "bullet": pygame.image.load("assets/bullet.png"),
    "enemy proj 1": pygame.image.load("assets/enemy_projectile_1.png")
}

class Projectile(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.speed = 10
        self.age = 60
        self.angle = 0

        self.position = pygame.math.Vector2(0, 0)
        
    def move(self):
        move = pygame.math.Vector2(
            math.cos(math.radians(self.angle)),
            math.sin(math.radians(self.angle))
        )
        self.position += move * self.speed

    def lifespan(self):
        self.age -= 1
        if self.age < 1:
            self.kill()

    def update(self):
        self.move()
        self.lifespan()
        
        self.rect.center = self.position

class Bullet(Projectile):
    def __init__(self, player_position = pygame.math.Vector2(0, 0), angle = 0):
        super().__init__()

        self.speed = 50
        self.age = 120
        self.angle = angle

        self.position = pygame.math.Vector2(player_position)
        
        self.og_image = proj_img["bullet"].convert_alpha()
        self.image = pygame.transform.rotate(self.og_image, -self.angle)
        self.rect = self.image.get_rect(center = self.position)

class Enemy_Projectile_1(Projectile):
    def __init__(self, position = pygame.math.Vector2(0, 0), angle = 0):
        super().__init__()

        self.speed = 10
        self.age = 240
        self.angle = angle - 90

        self.position = pygame.math.Vector2(position)

        self.og_image = proj_img["enemy proj 1"].convert_alpha()
        self.image = pygame.transform.rotate(self.og_image, -self.angle)
        self.rect = self.image.get_rect(center = self.position)
    

