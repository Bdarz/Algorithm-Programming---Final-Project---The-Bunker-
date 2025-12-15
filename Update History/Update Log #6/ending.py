import pygame

class Ending:
    def __init__(self, screen):
        self.screen = screen

        self.timer = 300
    
    def run(self):
        self.screen.fill((0, 0, 0))
        
        triumph = pygame.font.Font(None, 140).render("Congratulations, You've Won!", True, (255, 255, 255))

        screen_size = self.screen.get_size()
        mortis_position = triumph.get_rect(center=(screen_size[0] // 2, screen_size[1] // 2))

        self.screen.fill((0, 0, 0))
        self.screen.blit(triumph, mortis_position)

        if self.timer < 1:
            return "menu"
        else:
            self.timer -= 1
        return "ending"