# MVP of the entire project
import pygame 

# Importing the main three gamestates
from menu import Menu 
from game import Game
from ending import Ending

# Initiate Pygame
pygame.init()

# Creates screen, window name, and frame management
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("The Bunker")
time = pygame.time.Clock()

# The main three gamestates
main_states = {
    "menu": Menu(screen),
    "game": Game(screen),
    "ending": Ending(screen)
}
current_main_state = "menu" # Start at the menu

# Main game loop:
while True:
    next_main_state = main_states[current_main_state].run() # Runs whichever gamestate is currently active. Each gamestate has a run method
    
    # Check just incase something goes wrong, which it probably never will. Also death screen
    if next_main_state in main_states:
        current_main_state = next_main_state
    elif next_main_state == "mortis":
        main_states["game"] = Game(screen) # Resets the game gamestate
        current_main_state = "menu"

    # Updates display and keeps fps at 60
    pygame.display.flip()
    time.tick(60)