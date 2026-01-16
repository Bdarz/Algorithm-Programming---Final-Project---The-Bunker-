# pygame for display and control, sys for control
import pygame
import sys
import os

# Menu/home screen
class Menu:
    def __init__(self, screen, fps):
        # Inherits screen for display, and fps for timers
        self.screen = screen
        self.fps = fps

        # Get screen dimensions
        self.width, self.height = self.screen.get_size()

        # Creates background image, with some error handling
        try:
            self.bg = pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets/main_menu_background.png"))
            self.bg = pygame.transform.scale(self.bg, (self.width, self.height))
        except:
            self.bg = pygame.surface.Surface((self.width, self.height))
            self.bg.fill((0, 0, 0))

        # Creates "Title" text
        self.title = pygame.font.Font(None, 140).render("The Bunker", True, (255, 255, 255))
        self.title_position = self.title.get_rect(center=(self.width // 4, self.height * 0.2))

        # Creates "Start game" text
        self.start_text =  pygame.font.Font(None, 50).render("Press ENTER to start", True, (255, 255, 255))
        self.start_text_position = self.start_text.get_rect(center=(self.width // 2, self.height * 0.85))

        # "Start game" text animation
        self.start_text_fading_animation = 0 # Text goes from invisible to visible
        self.start_text_fading_animation_speed = self.fps // 60 # Animation speed, starts at 1/60 of a second, later will be 2/60
        self.start_text_fading_animation_delay = self.fps * 2 # Some nice delay

        # Start transition overlay
        self.start_animation_display = pygame.Surface((1280, 720))
        self.start_animation_display.fill((0, 0, 0)) # Black is the color of choice

        # Start transition animation
        self.start = False
        self.start_animation = 0

    def reset(self):
        # Resets all dynamic variables to default
        self.start_text_fading_animation = 0
        self.start_text_fading_animation_speed = self.fps // 60
        self.start_text_fading_animation_delay = self.fps * 2

        self.start = False
        self.start_animation = 0

    def control(self):
        # Basic exit and start controls
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                
                if event.key == pygame.K_RETURN:
                    self.start = True
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.start = True
                
    def run(self):
        self.control()
        
        # Text is invisible, checks if there is delay, if none, make text visible
        if self.start_text_fading_animation_delay > 0:
            self.start_text_fading_animation_delay -= self.fps // 30 
        
        # Text becomes visible, then back to being invisible
        else:
            # Makes text visible or invisible, depending on speed, which can be + or - depending on state
            self.start_text_fading_animation += self.start_text_fading_animation_speed

            # Checks if text is fully visible, then changes speed to negative to have it become invisible again
            if self.start_text_fading_animation >= 255:
                self.start_text_fading_animation = 255
                self.start_text_fading_animation_speed = -self.fps // 30 # Subsequent speed after the first animation loop is faster

            # Checks if text is invisible, then ensures speed is positive, and resets delay between text becoming invisible and beginning to become visible
            elif self.start_text_fading_animation <= 0:
                self.start_text_fading_animation = 0
                self.start_text_fading_animation_speed = self.fps // 30 # Subsequent speed after the first animation loop is faster
                self.start_text_fading_animation_delay = self.fps # Subsequent delays after the first animation loop is intentionally shorter

        # Changes transparency/visibility of the "Start game" text
        self.start_text.set_alpha(self.start_text_fading_animation)

        # Displays them, in order from background first, then the texts later on top
        self.screen.blit(self.bg, (0,0)) 
        self.screen.blit(self.start_text, self.start_text_position) 
        self.screen.blit(self.title, self.title_position)

        # Checks if player has started the game, then plays a transition animation, then enters game and reset menu
        if self.start:
            self.start_animation += self.fps // 30
            if self.start_animation >= 255:
                self.reset()
                return "gameplay"
            
            # Changes transparency of dark overlay
            self.start_animation_display.set_alpha(self.start_animation)

            # Displays dark overlay
            self.screen.blit(self.start_animation_display, (0,0))

        return "menu"
