# pygame for display and control, sys for control
import pygame
import sys

# Victory/ending screen
class GameWon:
    def __init__(self, screen, fps):
        # Inherits screen for display, and fps for timers
        self.screen = screen
        self.fps = fps

        # Determines how long the program stays on the ending screen, in this case, 300 frames or 5 seconds
        self.timer_duration_in_seconds = 5
        self.timer = self.fps * self.timer_duration_in_seconds

        # Creates a congratulation text and places it on the center of the screen
        screen_size = self.screen.get_size()
        self.triumph = pygame.font.Font(None, 140).render("You've Won!", True, (255, 255, 255))
        self.triumph_position = self.triumph.get_rect(center=(screen_size[0] // 2, screen_size[1] // 2))

    def reset(self):
        # Reset all dynamic variables to default
        self.timer = self.fps * self.timer_duration_in_seconds

    def control(self):
        # Basic exit controls
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

        # Dark background
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.triumph, self.triumph_position)

        # Keeps user at ending screen for like, 5 seconds, then returns menu, also reset some stuff
        if self.timer <= 0:
            self.reset()
            return "reset"
        
        # Stays on current state and reduce timer
        self.timer -= 1
        return "game_won"