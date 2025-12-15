import pygame
import math

from gun import Guns

class Player(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen

        self.og_image = pygame.image.load("assets/player.png").convert_alpha()
        self.image = self.og_image

        self.rect = self.image.get_rect()
        self.rectwo = self.rect

        self.heart_image = pygame.image.load("assets/heart.png").convert_alpha()
        self.hitpoints = 5
        self.amialive = True

        self.spawnpoint = (0, 0)
        self.position = pygame.math.Vector2(self.spawnpoint)
        self.lasvoss = [[0, 0]]
        self.spawninvuln = False
        self.speed = 6
        self.angle = 0

        self.guns = Guns()
        self.equipped_slot = 1
    
    def healthbar(self):
        health_bar = []
        for i in range(self.hitpoints):
            health_bar.append(self.heart_image)
        return health_bar

    def rotation(self, offset):
        cursor_position = pygame.mouse.get_pos() 

        cursor_position_of_the_x_kind = cursor_position[0] - self.rect.centerx + offset[0]
        cursor_position_of_the_y_kind = cursor_position[1] - self.rect.centery + offset[1]

        self.angle = math.degrees(math.atan2(cursor_position_of_the_y_kind, cursor_position_of_the_x_kind))

        self.image = pygame.transform.rotate(self.og_image, -self.angle)
        self.rectwo = self.image.get_rect(center = self.position)

    def movement(self):
        self.move = pygame.math.Vector2(0,0)
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.move.y -= 1
        if keys[pygame.K_a]:
            self.move.x -= 1
        if keys[pygame.K_s]:
            self.move.y += 1
        if keys[pygame.K_d]:
            self.move.x += 1
        
        if self.move.x != 0 and self.move.y !=0: 
            self.move *= 0.707 
        
        self.position += self.move * self.speed
        self.rect.center = self.position
    
    def undo_movement(self):
        self.position -= self.move * self.speed
        self.rect.center = self.position

    def amialivequestionmark(self):
        if self.hitpoints <= 0:
            self.amialive = False
            
    def update(self, offset):
        self.movement()
        self.rotation(offset)
        self.amialivequestionmark()
        self.guns.gun_inventory[self.equipped_slot].update()

        self.rect.center = self.position

