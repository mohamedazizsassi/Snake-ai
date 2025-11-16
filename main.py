import pygame
from game.menu import Menu
from game.engine import Game

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((600,600))
    menu = Menu(screen)

    running = True
    while running:
        choice = menu.run()
        if choice == "Quit":
            running = False
        else:
            game = Game(difficulty=choice)
            result = game.run()
            if result == "Quit":
                running = False
            # If result == "Menu", loop continues and shows menu again
    
    pygame.quit()
