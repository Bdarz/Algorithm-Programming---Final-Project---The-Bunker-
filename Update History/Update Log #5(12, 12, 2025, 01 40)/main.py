import pygame

from main_menu import Menu
from main_game import Game

pygame.init()

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("The Bunker")
time = pygame.time.Clock()

main_states = {
    "menu": Menu(screen),
    "game": Game(screen),
    "ending": "Ending(screen)",
}
current_main_state = "menu"

while True:
    next_main_state = main_states[current_main_state].run()
    
    if next_main_state in main_states:
        current_main_state = next_main_state
    elif next_main_state == "mortis":
        main_states["game"] = Game(screen)
        current_main_state = "menu"

    pygame.display.flip()
    time.tick(60)