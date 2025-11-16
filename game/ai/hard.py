"""Hard difficulty AI — advanced strategy with A* pathfinding.
"""

import heapq
from typing import Tuple, List, Optional

class HardAI:
    def __init__(self):
        pass

    def choose_direction(self, snake, snakes, food, grid) -> Tuple[int, int]:
        head = snake.body[0] if hasattr(snake, 'body') and snake.body else (0, 0)
        food_pos = food.position if hasattr(food, 'position') else (10, 10)
        current_dir = getattr(snake, "direction", (1, 0))

        # Try A* pathfinding
        path = self._astar(head, food_pos, snakes, grid)
        
        if path and len(path) > 1:
            next_pos = path[1]  # path[0] is current head
            direction = (next_pos[0] - head[0], next_pos[1] - head[1])
            # Validate it's not a reverse
            if direction != (-current_dir[0], -current_dir[1]):
                return direction

        all_dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        safe_dirs = []
        for direction in all_dirs:
            if direction == (-current_dir[0], -current_dir[1]):
                continue
            next_pos = (head[0] + direction[0], head[1] + direction[1])
            if not self._is_collision(next_pos, snakes, grid):
                # Score by available space (simple heuristic: distance from walls)
                space_score = self._count_reachable_cells(next_pos, snakes, grid)
                safe_dirs.append((space_score, direction))

        if safe_dirs:
            safe_dirs.sort(reverse=True)  # prefer more open space
            return safe_dirs[0][1]

        # Last resort
        return current_dir

    def _astar(self, start: Tuple[int, int], goal: Tuple[int, int], snakes: List, grid) -> Optional[List[Tuple[int, int]]]:
        """A* pathfinding from start to goal."""
        grid_width = getattr(grid, 'width', 40) if hasattr(grid, 'width') else 40
        grid_height = getattr(grid, 'height', 30) if hasattr(grid, 'height') else 30

        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: heuristic(start, goal)}

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == goal:
                # Reconstruct path
                path = [current]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                path.reverse()
                return path

            for dx, dy in [(0,1), (0,-1), (1,0), (-1,0)]:
                neighbor = (current[0] + dx, current[1] + dy)
                
                if self._is_collision(neighbor, snakes, grid):
                    continue

                tentative_g = g_score[current] + 1

                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return None  # No path found

    def _is_collision(self, pos: Tuple[int, int], snakes: List, grid) -> bool:
        """Check if position collides with walls or snake bodies."""
        grid_width = getattr(grid, 'width', 40) if hasattr(grid, 'width') else 40
        grid_height = getattr(grid, 'height', 30) if hasattr(grid, 'height') else 30
        
        if pos[0] < 0 or pos[0] >= grid_width or pos[1] < 0 or pos[1] >= grid_height:
            return True

        for snake in snakes:
            if hasattr(snake, 'body') and pos in snake.body:
                return True

        return False

    def _count_reachable_cells(self, start: Tuple[int, int], snakes: List, grid, max_depth: int = 5) -> int:
        """BFS to count how many cells are reachable within max_depth steps."""
        visited = {start}
        queue = [(start, 0)]
        count = 0

        while queue:
            pos, depth = queue.pop(0)
            count += 1
            if depth >= max_depth:
                continue

            for dx, dy in [(0,1), (0,-1), (1,0), (-1,0)]:
                neighbor = (pos[0] + dx, pos[1] + dy)
                if neighbor not in visited and not self._is_collision(neighbor, snakes, grid):
                    visited.add(neighbor)
                    queue.append((neighbor, depth + 1))

        return count
