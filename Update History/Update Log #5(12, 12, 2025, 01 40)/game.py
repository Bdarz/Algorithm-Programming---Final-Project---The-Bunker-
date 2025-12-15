import pygame

from level import *
from player import Player

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.player = Player(self.screen)

        self.levels = [
            None,
            Level_1(self.screen, self.player),
            Level_2(self.screen, self.player)
        ]
        self.current_level = 1

        self.sound = pygame.mixer.Sound("assets/mortis.mp3")
        self.deathbell = 0

    def mortis(self):
        mortis = pygame.font.Font(None, 140).render("MORTIS", True, (255, 255, 255))

        screen_size = self.screen.get_size()
        mortis_position = mortis.get_rect(center=(screen_size[0] // 2, screen_size[1] // 2))

        self.screen.fill((0, 0, 0))
        self.screen.blit(mortis, mortis_position)

        if self.deathbell < 1:
            self.sound.play()
        if self.deathbell > 240:
            return "mortis"
        self.deathbell += 1

    def run(self):
        next_level = self.levels[self.current_level].run()

        if self.player.amialive != True:
            return self.mortis()
        elif next_level == "menu":
            return "menu"
        elif next_level in range (len(self.levels)) and next_level != 0:
            self.current_level = next_level

        return "game"
