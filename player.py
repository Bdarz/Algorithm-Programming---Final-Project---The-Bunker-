# Pygame for textures and rects, math for texture rotations
import pygame
import math

# Import guns/weapons for player to store and manage
from gun import Gun_Inventory

# Load images, with some error handling
try:
    player_image = pygame.image.load("assets/player.png")
    hitpoint_image = pygame.image.load("assets/heart.png")
except:
    default_texture = pygame.surface.Surface((30, 30))
    default_texture.fill((50, 50, 50))

    player_image = default_texture
    hitpoint_image = default_texture

class Player(pygame.sprite.Sprite):
    def __init__(self, screen):
        # Inherit Pygame's sprite class
        super().__init__()

        # Inherits screen
        self.screen = screen

        # Original image and image for display post rotation or other modifications
        self.og_image = player_image.convert_alpha()
        self.image = self.og_image

        # Original rect and rect for rotation or other modifications
        self.rect = self.image.get_rect()
        self.rotation_rect = self.rect

        # Hitpoint texture and count, alongside alive status
        self.heart_image = hitpoint_image
        self.hitpoints = 10
        self.is_player_alive = True

        # Spawnpoint/base position, and current position
        self.spawnpoint = (0, 0)
        self.position = pygame.math.Vector2(self.spawnpoint)

        # Stores a list of last position in every previously visited level
        self.last_position = [[0, 0]]

        # Spawn invulnurability to avoid undesired outcomes after entering a new level
        self.spawninvuln = False

        # Base movement and speed
        self.base_movement = 1
        self.speed = 8

        # Base rotation angle
        self.angle = 0

        # Stores guns and which one is equipped
        self.guns = Gun_Inventory()
        self.equipped_slot = 0
    
    def healthbar(self):
        # Stores hitpoints
        health_bar = []

        # returns a list containing current hitpoint count
        for i in range(self.hitpoints):
            health_bar.append(self.heart_image)
        return health_bar

    def rotation(self, offset):
        # Obtains rotation based on angle between player and mouse cursor
        cursor_position = pygame.mouse.get_pos() 

        cursor_position_of_the_x_kind = cursor_position[0] - self.rect.centerx + offset[0]
        cursor_position_of_the_y_kind = cursor_position[1] - self.rect.centery + offset[1]

        self.angle = math.degrees(math.atan2(cursor_position_of_the_y_kind, cursor_position_of_the_x_kind))

        # Rotatees the image and rotation rect to face toward cursor
        self.image = pygame.transform.rotate(self.og_image, -self.angle)
        self.rotation_rect = self.image.get_rect(center = self.position)

    def movement(self):
        # Player doesn't move, because movement is 0
        self.move = pygame.math.Vector2(0,0)
        
        # Pressing one of these keys changes the player's movement vector to a certain direction
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.move.y -= self.base_movement
        if keys[pygame.K_a]:
            self.move.x -= self.base_movement
        if keys[pygame.K_s]:
            self.move.y += self.base_movement
        if keys[pygame.K_d]:
            self.move.x += self.base_movement
        
        # Ensures that diagonal movement is not faster than horizontal or vertical movement
        if self.move.x != 0 and self.move.y !=0: 
            self.move *= math.sqrt(self.base_movement * 2) / 2
        
        # Updates the player's position by multiplying direction with player speed
        self.position += self.move * self.speed

        # Updates rect as well
        self.rect.center = self.position
    
    def undo_movement(self):
        # Reverts movement if collision is detected
        self.position -= self.move * self.speed

        # Reverts rect as well
        self.rect.center = self.position

    def dead_or_alive(self):
        # Checks if the player is dead
        if self.hitpoints <= 0:
            self.is_player_alive = False
            
    def update(self, offset):
        # Updates movement, rotation, living conditions, weapon status, and rect
        self.movement()
        self.rotation(offset)
        self.dead_or_alive()
        self.guns.gun_inventory[self.equipped_slot].update()

        self.rect.center = self.position

