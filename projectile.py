import pygame
import math
import os

# Load base images, with some error handling
try:
    proj_img = {
        "bullet": pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets/bullet.png")),
        "enemy proj 1": pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets/enemy_projectile_1.png"))
    }
except:
    default_texture = pygame.surface.Surface((10, 10))
    default_texture.fill((20, 20, 20))

    proj_img = {
        "bullet": default_texture,
        "enemy proj 1": default_texture
    }

# Base projectile class
class Projectile(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Base attributes
        self.speed = 10
        self.age = 60
        self.angle = 0

        self.position = pygame.math.Vector2(0, 0)
    
    # Manages movement
    def move(self):
        # Moves at angle which it is shot in and keeps moving at that angle
        move = pygame.math.Vector2(
            math.cos(math.radians(self.angle)),
            math.sin(math.radians(self.angle))
        )
        self.position += move * self.speed

    # Manages lifespan
    def lifespan(self):
        self.age -= 1
        if self.age < 1:
            self.kill()

    # Keep the proj moving and living
    def update(self):
        self.move()
        self.lifespan()
        
        self.rect.center = self.position

# Bullet projectile class
class Bullet(Projectile):
    def __init__(self, player_position = pygame.math.Vector2(0, 0), angle = 0):
        super().__init__()

        # Base attributes
        self.speed = 50
        self.age = 120
        self.angle = angle

        self.position = pygame.math.Vector2(player_position)
        
        # Manages texture and rect
        self.og_image = proj_img["bullet"].convert_alpha()
        self.image = pygame.transform.rotate(self.og_image, -self.angle)
        self.rect = self.image.get_rect(center = self.position)

# Basic enemy proj class
class Enemy_Projectile_1(Projectile):
    def __init__(self, position = pygame.math.Vector2(0, 0), angle = 0):
        super().__init__()

        # Base attributes
        self.speed = 10
        self.age = 240
        self.angle = angle

        self.position = pygame.math.Vector2(position)

        # Manages texture and rect
        self.og_image = proj_img["enemy proj 1"].convert_alpha()
        self.image = pygame.transform.rotate(self.og_image, -self.angle - 90)
        self.rect = self.image.get_rect(center = self.position)

