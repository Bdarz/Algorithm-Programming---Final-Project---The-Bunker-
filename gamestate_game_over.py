# pygame for display and control, sys for control
import pygame
import sys

# Game over/death screen
class GameOver:
    def __init__(self, screen, fps):
        # Inherits screen for display, and fps for timers
        self.screen = screen
        self.fps = fps

        # Determines how long the program stays on the game over screen, in this case, 240 frames or 4 seconds
        self.timer_duration_in_seconds = 4
        self.timer = self.fps * self.timer_duration_in_seconds

        # Creates a game over text (Mortis means death) and places it on the center of the screen
        self.screen_size = self.screen.get_size()
        self.mortis = pygame.font.Font(None, 140).render("MORTIS", True, (255, 255, 255))
        self.mortis_position = self.mortis.get_rect(center=(self.screen_size[0] // 2, self.screen_size[1] // 2))

        # Creates a game over sound if the asset is found, and plays it only once per death screen
        self.sound_has_played = False
        self.sound_found = True
        try:
            self.sound = pygame.mixer.Sound("assets/mortis.wav")
        except:
            self.sound_found = False

    def reset(self):
        # Resets all dynamic variables to default
        self.sound_has_played = False
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
        self.screen.blit(self.mortis, self.mortis_position)

        # Plays the sound once
        if self.sound_has_played == False and self.sound_found == True:
            self.sound_has_played = True
            self.sound.play()

        # Keeps user at ending screen for like, 4 seconds, then returns menu, also reset some stuff
        if self.timer < 1:
            self.reset()
            return "reset"
        
        # Stays on current state and reduce timer
        self.timer -= 1
        return "game_over"