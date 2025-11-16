"""AI module for Snake+AI game.

Each difficulty has its own AI class:
- EasyAI: Simple random movements
- MediumAI: BFS Pathfinding towards food
- HardAI: A* with collision avoidance 
"""

from .easy import EasyAI
from .medium import MediumAI
from .hard import HardAI

__all__ = ['EasyAI', 'MediumAI', 'HardAI']
