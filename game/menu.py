import pygame

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("consolas", 40)
        self.options = ["Easy", "Medium", "Hard", "Impossible", "Quit"]
        self.selected = 0

    def draw(self):
        self.screen.fill((30, 30, 30))
        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected else (255, 255, 255)
            text = self.font.render(option, True, color)
            rect = text.get_rect(center=(self.screen.get_width()//2, 150 + i*60))
            self.screen.blit(text, rect)
        pygame.display.flip()

    def run(self):
        clock = pygame.time.Clock()
        while True:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "Quit"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected = (self.selected - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        return self.options[self.selected]
            clock.tick(30)
