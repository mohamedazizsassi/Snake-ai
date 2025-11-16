"""Easy difficulty AI — very simple, mostly random.
"""

import random
from typing import Tuple

class EasyAI:
    def __init__(self):
        pass

    def choose_direction(self, snake, snakes, food, grid) -> Tuple[int, int]:
        """Return a direction tuple (dx, dy).
        Simple behavior: 70% keep current direction, 30% random (but not reverse).
        """
        directions = [(0,1),(0,-1),(1,0),(-1,0)]
        current = getattr(snake, "direction", (1,0))
        # 70% chance to keep going the same way
        if random.random() < 0.7:
            return current

        # else pick a random non-reverse direction
        allowed = [d for d in directions if d != (-current[0], -current[1])]
        return random.choice(allowed)
