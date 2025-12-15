import pygame
import sys

# Death screen
class Mortis():
    def __init__(self, screen):
        self.screen = screen

        self.screen_size = self.screen.get_size()
        self.mortis = pygame.font.Font(None, 140).render("MORTIS", True, (255, 255, 255))
        self.mortis_position = self.mortis.get_rect(center=(self.screen_size[0] // 2, self.screen_size[1] // 2))

        self.sound = pygame.mixer.Sound("assets/mortis.mp3")
        self.deathbell = 0

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
        self.screen.blit(self.mortis, self.mortis_position)
        if self.deathbell <= 0:
            self.sound.play()
        self.deathbell += 1
        if self.deathbell >= 240:
            return "its over"
        return "mortis"