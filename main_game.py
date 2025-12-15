import pygame
import sys

from level import Level_0, Level_1, Level_2, Boss_1
from player import Player

# Game screen
class Game:
    def __init__(self, screen):
        self.screen = screen
        self.player = Player(self.screen)

        # Stores all of the levels
        self.levels = (
            Level_0(self.screen, self.player),
            Level_1(self.screen, self.player),
            Level_2(self.screen, self.player),
            Boss_1(self.screen, self.player)
        )
        self.current_level = 1 # Starts at level 1 (not 0)

    def control(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    if len(self.player.guns.gun_inventory) > 0:
                        self.player.equipped_slot = 0
                
                if event.key == pygame.K_2:
                    if len(self.player.guns.gun_inventory) > 1:
                        self.player.equipped_slot = 1

                if event.key == pygame.K_n:
                    bullet = self.player.guns.gun_inventory[self.player.equipped_slot].shoot(self.player.position, self.player.angle)
                    if bullet:
                        self.levels[self.current_level].sprites["playerproj"].add(bullet)
            
            heldkey = pygame.key.get_pressed()
            if heldkey[pygame.K_n]:
                bullet = self.player.guns.gun_inventory[self.player.equipped_slot].shoot(self.player.position, self.player.angle)
                if bullet:
                    self.levels[self.current_level].sprites["playerproj"].add(bullet)

    def custom_sprite_draw(self):
        self.screen.fill((0, 0, 0))

        # Draws every sprite from current level according to offset based on player location in the level itself
        for key in self.levels[self.current_level].sprites:
            for sprite in self.levels[self.current_level].sprites[key]:
                resulting_offset = sprite.rect.topleft - self.levels[self.current_level].current_offset
                self.screen.blit(sprite.image, resulting_offset)

        # Draws the player sprite with extra offset due to drawing topleft/center issues
        extra_offset = pygame.math.Vector2(self.player.rectwo.width//2, self.player.rectwo.height//2)
        resulting_offset = self.player.position - extra_offset - self.levels[self.current_level].current_offset
        self.screen.blit(self.player.image, resulting_offset)

        # Draws health bar according to how many health the player have
        health_bar = self.player.healthbar()
        heart_position = pygame.math.Vector2(10, 10)
        if health_bar:
            for i in health_bar:
                self.screen.blit(i, heart_position)
                heart_position[0] += 50

    def run(self):
        self.control()
        self.custom_sprite_draw()
        next_level = self.levels[self.current_level].run() # Runs whichever level is active

        if not self.player.amialive: # If dead
            return "mortis"
        elif next_level == "menu": # If return to menu
            return "menu"
        elif next_level == (len(self.levels)): # If it is the final stage 
            return "ending"
        elif next_level in range (len(self.levels)) and next_level != 0: # If it is a normal stage (starts at 1)
            self.current_level = next_level
        else: # Keeps you at level
            next_level = self.current_level

        return "game" # Stays at game screen
