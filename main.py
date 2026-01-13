# MVP of the entire project
import pygame 

# Importing the four main gamestates
from gamestate_menu import Menu 
from gamestate_gameplay import GamePlay
from gamestate_game_over import GameOver
from gamestate_game_won import GameWon

# Initiate Pygame
pygame.init()

# Creates screen, window name, and frame management
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("The Bunker")
time = pygame.time.Clock()
fps = 60

# The main four gamestates
main_states = {
    "menu": Menu(screen, fps),
    "gameplay": GamePlay(screen),
    "game_over": GameOver(screen, fps),
    "game_won": GameWon(screen, fps)
}
current_main_state = "menu" # Start at the menu

# Main game loop
while True:
    next_main_state = main_states[current_main_state].run() # Runs whichever gamestate is currently active. Each gamestate has a run method called every frame
    
    # Ensures that each state returns something valid, be it itself, or a different existing state
    if next_main_state in main_states:
        current_main_state = next_main_state

    # When the player dies or wins, it resets the game gamestate and returns to the menu
    elif next_main_state == "reset":
        main_states["gameplay"] = GamePlay(screen) # Resets the game gamestate
        current_main_state = "menu"

    # Updates display and keeps fps at 60
    pygame.display.flip()
    time.tick(fps)