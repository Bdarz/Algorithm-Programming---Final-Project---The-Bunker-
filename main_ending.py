import pygame
import sys

class Ending:
    def __init__(self, screen):
        self.screen = screen

        self.timer = 300

        screen_size = self.screen.get_size()
        self.triumph = pygame.font.Font(None, 140).render("You've Won!", True, (255, 255, 255))
        self.triumph_position = self.triumph.get_rect(center=(screen_size[0] // 2, screen_size[1] // 2))

    def control(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    def run(self):
        self.control()

        self.screen.fill((0, 0, 0))
        self.screen.blit(self.triumph, self.triumph_position)

        if self.timer <= 0:
            return "menu"
        
        self.timer -= 1
        return "ending"