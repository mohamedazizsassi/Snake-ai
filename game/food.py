import random

class Food:
    def __init__(self, grid_width=30, grid_height=30):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.position = (random.randint(0, grid_width-1), random.randint(0, grid_height-1))

    def respawn(self, snakes):
        while True:
            pos = (random.randint(0, self.grid_width-1), random.randint(0, self.grid_height-1))
            if not any(pos in s.body for s in snakes):
                self.position = pos
                break

    def draw(self, surface, color=(255, 0, 0), cell_size=20):
        import pygame
        rect = pygame.Rect(self.position[0]*cell_size, self.position[1]*cell_size, cell_size, cell_size)
        pygame.draw.rect(surface, color, rect)
