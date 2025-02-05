import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CELL_SIZE = 40
PLAYER_SIZE = 30
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PINK = (255, 192, 203)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = PLAYER_SIZE
        self.speed = 5
    
    def move(self, dx, dy, walls):
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        
        player_rect = pygame.Rect(new_x, new_y, self.size, self.size)
        
        # Check collision with walls
        can_move = True
        for wall in walls:
            if player_rect.colliderect(wall):
                can_move = False
                break
        
        if can_move:
            self.x = max(0, min(new_x, SCREEN_WIDTH - self.size))
            self.y = max(0, min(new_y, SCREEN_HEIGHT - self.size))
    
    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, (self.x, self.y, self.size, self.size))

class Princess:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = PLAYER_SIZE
    
    def draw(self, screen):
        pygame.draw.rect(screen, PINK, (self.x, self.y, self.size, self.size))

def generate_maze():
    walls = []
    # Create outer walls
    walls.extend([
        pygame.Rect(0, 0, SCREEN_WIDTH, CELL_SIZE),  # Top
        pygame.Rect(0, SCREEN_HEIGHT - CELL_SIZE, SCREEN_WIDTH, CELL_SIZE),  # Bottom
        pygame.Rect(0, 0, CELL_SIZE, SCREEN_HEIGHT),  # Left
        pygame.Rect(SCREEN_WIDTH - CELL_SIZE, 0, CELL_SIZE, SCREEN_HEIGHT),  # Right
    ])
    
    # Generate random internal walls
    for _ in range(15):
        if random.random() < 0.5:  # Horizontal wall
            x = random.randint(1, (SCREEN_WIDTH // CELL_SIZE) - 3) * CELL_SIZE
            y = random.randint(1, (SCREEN_HEIGHT // CELL_SIZE) - 2) * CELL_SIZE
            width = random.randint(2, 5) * CELL_SIZE
            walls.append(pygame.Rect(x, y, width, CELL_SIZE))
        else:  # Vertical wall
            x = random.randint(1, (SCREEN_WIDTH // CELL_SIZE) - 2) * CELL_SIZE
            y = random.randint(1, (SCREEN_HEIGHT // CELL_SIZE) - 3) * CELL_SIZE
            height = random.randint(2, 5) * CELL_SIZE
            walls.append(pygame.Rect(x, y, CELL_SIZE, height))
    
    return walls

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Princess Rescue Maze")
    clock = pygame.time.Clock()
    
    # Create walls
    walls = generate_maze()
    
    # Create player at top-left corner (with some offset)
    player = Player(CELL_SIZE + 5, CELL_SIZE + 5)
    
    # Create princess at bottom-right corner (with some offset)
    princess = Princess(SCREEN_WIDTH - CELL_SIZE * 2, SCREEN_HEIGHT - CELL_SIZE * 2)
    
    # Game states
    game_won = False
    font = pygame.font.Font(None, 74)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and game_won:
                if event.key == pygame.K_r:  # Reset game
                    walls = generate_maze()
                    player = Player(CELL_SIZE + 5, CELL_SIZE + 5)
                    game_won = False
        
        if not game_won:
            # Handle continuous keyboard input
            keys = pygame.key.get_pressed()
            dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
            dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]
            player.move(dx, dy, walls)
            
            # Check if player reached princess
            player_rect = pygame.Rect(player.x, player.y, player.size, player.size)
            princess_rect = pygame.Rect(princess.x, princess.y, princess.size, princess.size)
            if player_rect.colliderect(princess_rect):
                game_won = True
        
        # Draw everything
        screen.fill(WHITE)
        
        # Draw walls
        for wall in walls:
            pygame.draw.rect(screen, BLACK, wall)
        
        # Draw player and princess
        player.draw(screen)
        princess.draw(screen)
        
        # Draw victory message
        if game_won:
            win_text = font.render("Princess Rescued!", True, RED)
            restart_text = font.render("Press R to Restart", True, BLACK)
            text_rect = win_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50))
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 50))
            screen.blit(win_text, text_rect)
            screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()