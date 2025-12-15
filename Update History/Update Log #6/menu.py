import pygame
import sys

# Main menu
class Menu:
    def __init__(self, screen):
        # Inherit screen
        self.screen = screen

        # Creates background image.
        self.bg = pygame.image.load("assets/main_menu_background.png")
        self.bg = pygame.transform.scale(self.bg, (1280, 720))

        # Creates "title" text.
        self.title_font = pygame.font.Font(None, 140)
        self.title = self.title_font.render("The Bunker", True, (255, 255, 255))

        # Creates "start game" text.
        self.start_text_font = pygame.font.Font(None, 50)
        self.start_text = self.start_text_font.render("Press ENTER to start", True, (255, 255, 255))
        self.start_text_fading_animation = 0 # Text goes from invisible to existing.
        self.start_text_fading_animation_speed = 1 # How fast the animation. Here, it starts slower since it is 1, but later will always be 2.
        self.start_text_fading_animation_delay = 120 # Some nice delay.

        # Transition animation baby, I made this before I even made the gamemplay which is dumb but that's aight.
        self.start = False
        self.start_animation = 0
        self.start_animation_display = pygame.Surface((1280, 720))
        self.start_animation_display.fill((0, 0, 0)) # Black is the color of choice.

    def run(self):
        # Input handling.
        for event in pygame.event.get():
            # Exit.
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Keyboard.
            if event.type == pygame.KEYDOWN:
                # Exit.
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                
                # Start.
                if event.key == pygame.K_RETURN:
                    self.start = True
            
            # Mouse start.
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.start = True
        
        # Managing text animation.
        if self.start_text_fading_animation_delay > 0:
            self.start_text_fading_animation_delay -= 2

        else: #This else is necessary for the animation to not brick and for the delay to not get stuck at max value.
            self.start_text_fading_animation += self.start_text_fading_animation_speed

            if self.start_text_fading_animation >= 255:
                self.start_text_fading_animation = 255
                self.start_text_fading_animation_speed = -2 # Text now starts to fade out.

            elif self.start_text_fading_animation <= 0:
                self.start_text_fading_animation = 0
                self.start_text_fading_animation_speed = 2 # Text now starts to fade in. Originally 1, but now 2, so every animation after the first fade in is faster, purely stylistic.
                self.start_text_fading_animation_delay = 50 # Adds a delay after text is fully faded out, also purely stylistic.

        self.start_text.set_alpha(self.start_text_fading_animation)

        # Managing text location.
        width, height = self.screen.get_size()
        start_text_loc = self.start_text.get_rect(center=(width // 2, height * 0.85))
        title_loc = self.title.get_rect(center=(width // 4, height * 0.2))

        # Display handling.
        self.screen.blit(self.bg, (0,0)) # Background first.
        self.screen.blit(self.start_text, start_text_loc) # Texts on top.
        self.screen.blit(self.title, title_loc)

        # Managing exits or state change/start.
        if self.start: # Start the game.
            self.start_animation += 2
            if self.start_animation >= 255:
                self.start_animation = 255
                self.start = False
                self.start_animation = 0
                self.start_text_fading_animation = 0
                self.start_text_fading_animation_speed = 1 
                self.start_text_fading_animation_delay = 120
                return "game"
            
            self.start_animation_display.set_alpha(self.start_animation)
            self.screen.blit(self.start_animation_display, (0,0))

        return "menu" # Keeps gamestate on menu unless stated otherwise.
