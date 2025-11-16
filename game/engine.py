import pygame
import random
from .snake import Snake
from .food import Food
from .ai import EasyAI, MediumAI, HardAI

# Grid and display constants
CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 30
SCREEN_WIDTH = GRID_WIDTH * CELL_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * CELL_SIZE

class Game:
    def __init__(self, difficulty="Easy"):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snake.io: AI Arena")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", 20)

        self.difficulty = difficulty
        self.player = Snake((0, 200, 0), (5, 5), is_player=True)

        # Create AI snakes based on difficulty
        self.snakes = [self.player]
        self.create_ai_snakes()
        self.food = Food(GRID_WIDTH, GRID_HEIGHT)
        self.running = True
        self.score = 0

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.player.direction != (0, 1):
            self.player.direction = (0, -1)
        elif keys[pygame.K_DOWN] and self.player.direction != (0, -1):
            self.player.direction = (0, 1)
        elif keys[pygame.K_LEFT] and self.player.direction != (1, 0):
            self.player.direction = (-1, 0)
        elif keys[pygame.K_RIGHT] and self.player.direction != (-1, 0):
            self.player.direction = (1, 0)

    def update_ai(self):
        for snake in self.snakes:
            if snake.is_player:
                continue  # skip player
            # Use the AI controller attached to the snake
            if hasattr(snake, 'ai_controller') and snake.ai_controller:
                # Create a simple grid info object
                grid_info = type('obj', (object,), {'width': GRID_WIDTH, 'height': GRID_HEIGHT})()
                new_direction = snake.ai_controller.choose_direction(
                    snake, self.snakes, self.food, grid_info
                )
                snake.direction = new_direction

    
    def create_ai_snakes(self):
        num_ai = 1
        ai_controller = None
        
        if self.difficulty == "Easy":
            num_ai = 1
            ai_controller = EasyAI()
        elif self.difficulty == "Medium":
            num_ai = 1
            ai_controller = MediumAI()
        elif self.difficulty == "Hard":
            num_ai = 1
            ai_controller = HardAI()
        elif self.difficulty == "Impossible":
            num_ai = 2
            ai_controller = HardAI()


        colors = [(200,0,0),(0,0,200),(200,200,0)]
            
        for i in range(num_ai):
            snake = Snake(colors[i % len(colors)], (10+i*5, 10+i*5))
            snake.ai_controller = ai_controller  # Attach AI controller
            self.snakes.append(snake)

    def check_food(self):
        for snake in self.snakes:
            if snake.head() == self.food.position:
                snake.grow()
                self.food.respawn(self.snakes)
                if snake.is_player:
                    self.score += 10

    def check_collisions(self):
        for snake in self.snakes:
            if snake.check_collision(self.snakes):
                if snake.is_player:
                    self.running = False  # player dies
                else:
                    # Respawn AI
                    snake.body = [(random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))]


    def game_over_screen(self):
        # If the display has already been quit, don't try to draw on it.
        if not pygame.display.get_init():
            return False

        try:
            # Create button rectangle
            button_width, button_height = 250, 60
            button_x = SCREEN_WIDTH // 2 - button_width // 2
            button_y = SCREEN_HEIGHT // 2 + 80
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return False  # Signal to quit the game entirely
                    
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if button_rect.collidepoint(event.pos):
                            return True  # Signal to return to menu
                    
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                            return True  # Return to menu on ESC or ENTER

                # Draw game over screen
                self.screen.fill((30, 30, 30))
                
                # Game over text
                font_large = pygame.font.SysFont("consolas", 50)
                text = font_large.render(f"Game Over!", True, (255, 0, 0))
                rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
                self.screen.blit(text, rect)

                # Score text
                font_medium = pygame.font.SysFont("consolas", 30)
                score_text = font_medium.render(f"Score: {self.score}", True, (255, 255, 255))
                score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                self.screen.blit(score_text, score_rect)

                # Check if mouse is hovering over button
                mouse_pos = pygame.mouse.get_pos()
                is_hovering = button_rect.collidepoint(mouse_pos)
                
                # Draw button
                button_color = (80, 80, 200) if is_hovering else (50, 50, 150)
                pygame.draw.rect(self.screen, button_color, button_rect)
                pygame.draw.rect(self.screen, (255, 255, 255), button_rect, 3)  # Border

                # Button text
                font_button = pygame.font.SysFont("consolas", 25)
                button_text = font_button.render("Return to Menu", True, (255, 255, 255))
                button_text_rect = button_text.get_rect(center=button_rect.center)
                self.screen.blit(button_text, button_text_rect)

                pygame.display.flip()
                self.clock.tick(30)  # 30 FPS for menu

            return False
        except pygame.error:
            # If any display error occurs (e.g. surface quit), skip the screen.
            return False


    def draw_ui(self):
        text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(text, (10, 10))

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return "Quit"  # User closed the window

            self.handle_input()
            self.update_ai()

            for snake in self.snakes:
                snake.move(GRID_WIDTH, GRID_HEIGHT)

            self.check_food()
            self.check_collisions()

            # Draw
            self.screen.fill((20, 20, 20))
            self.food.draw(self.screen)
            for snake in self.snakes:
                snake.draw(self.screen, CELL_SIZE)
            self.draw_ui()

            pygame.display.flip()
            self.clock.tick(10)  # speed

        # Show game over screen while the display is still initialized
        return_to_menu = self.game_over_screen()
        
        # Don't call pygame.quit() here - let main.py handle it
        # Return signal to indicate whether to return to menu or quit
        if return_to_menu:
            return "Menu"
        else:
            return "Quit"
        
    
    
