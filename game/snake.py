import pygame
import random

class Snake:
    def __init__(self, color, start_pos, is_player=False):
        self.body = [start_pos]
        self.direction = (1, 0)
        self.color = color
        self.grow_flag = False
        self.is_player = is_player

    def head(self):
        return self.body[0]

    def move(self, grid_width, grid_height):
        x, y = self.head()
        dx, dy = self.direction
        new_head = ((x + dx) % grid_width, (y + dy) % grid_height)
        self.body.insert(0, new_head)
        if not self.grow_flag:
            self.body.pop()
        else:
            self.grow_flag = False

    def grow(self):
        self.grow_flag = True

    def check_collision(self, snakes):
        # If snake hits itself or another snake
        for s in snakes:
            if s != self and self.head() in s.body:
                return True
        # Self collision
        if self.head() in self.body[1:]:
            return True
        return False

    def draw(self, surface, cell_size):
        for (x, y) in self.body:
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            pygame.draw.rect(surface, self.color, rect)
