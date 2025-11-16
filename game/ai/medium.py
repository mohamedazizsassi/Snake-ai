"""Medium difficulty AI — BFS pathfinding strategy.
"""

from collections import deque
from typing import Tuple, List, Optional

class MediumAI:
    def __init__(self):
        pass

    def choose_direction(self, snake, snakes, food, grid) -> Tuple[int, int]:
        head = snake.body[0] 
        food_pos = food.position 
        current_dir = getattr(snake, "direction", (1, 0))
        
        # Use BFS to find path to food
        path = self._bfs_to_food(head, food_pos, snakes, grid.width, grid.height)

        if path and len(path) > 1:
            # Follow the path: path[0] is current head, path[1] is next step
            next_pos = path[1]
            direction = (next_pos[0] - head[0], next_pos[1] - head[1])
            
            # Ensure we're not reversing
            if direction != (-current_dir[0], -current_dir[1]):
                return direction


        #keep current direction
        return current_dir

    def _bfs_to_food(self, start: Tuple[int, int], goal: Tuple[int, int], 
                     snakes: List, grid_width: int, grid_height: int) -> Optional[List[Tuple[int, int]]]:
        """Find shortest path from start to goal using BFS.
        Returns a list of coordinates from start to goal (inclusive), or None if unreachable.
        Following mentor's BFS strategy with parent pointers."""
        
        queue = deque([start])            # FIFO queue
        visited = {start}                 # mark visited nodes
        parent = {start: None}            # parent pointers to reconstruct path

        # BFS loop
        while queue:
            current = queue.popleft()
            
            if current == goal:
                # reconstruct path
                path = []
                node = current
                while node is not None:
                    path.append(node)
                    node = parent[node]
                path.reverse()
                return path
            
            x, y = current
            # explore four neighbors
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx = (x + dx) % grid_width
                ny = (y + dy) % grid_height
                
                neighbor = (nx, ny)
                
                #(no obstacle checking)
                if neighbor not in visited:
                    visited.add(neighbor)      # mark visited when enqueuing
                    parent[neighbor] = current
                    queue.append(neighbor)
        return None
