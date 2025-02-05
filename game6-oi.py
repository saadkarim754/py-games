import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 600
CELL_SIZE = 30
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Solver - Save the Princess")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Load castle background
background = pygame.image.load("c.webp")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Generate a random maze (0 = path, 1 = wall)
def generate_maze():
    while True:
        maze = [[1 if random.random() < 0.3 else 0 for _ in range(COLS)] for _ in range(ROWS)]
        maze[0][0] = 0  # Start position
        maze[ROWS - 1][COLS - 1] = 0  # Goal position
        if is_solvable(maze):
            return maze

# Check if maze is solvable (simple BFS path check)
def is_solvable(maze):
    from collections import deque
    queue = deque([(0, 0)])
    visited = set()
    while queue:
        x, y = queue.popleft()
        if (x, y) == (COLS - 1, ROWS - 1):
            return True
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < COLS and 0 <= ny < ROWS and maze[ny][nx] == 0 and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append((nx, ny))
    return False

# Game variables
level = 1
timer = 30  # 30 seconds per level
player_x, player_y = 0, 0
maze = generate_maze()
running = True
clock = pygame.time.Clock()

# Game loop
while running:
    screen.blit(background, (0, 0))
    start_time = time.time()

    while timer > 0:
        screen.blit(background, (0, 0))
        pygame.draw.rect(screen, YELLOW, ((COLS - 1) * CELL_SIZE, (ROWS - 1) * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.circle(screen, BLUE, (player_x * CELL_SIZE + CELL_SIZE // 2, player_y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2)
        
        # Draw maze
        for y in range(ROWS):
            for x in range(COLS):
                if maze[y][x] == 1:
                    pygame.draw.rect(screen, BLACK, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Move player
        keys = pygame.key.get_pressed()
        new_x, new_y = player_x, player_y
        if keys[pygame.K_LEFT] and player_x > 0:
            new_x -= 1
        if keys[pygame.K_RIGHT] and player_x < COLS - 1:
            new_x += 1
        if keys[pygame.K_UP] and player_y > 0:
            new_y -= 1
        if keys[pygame.K_DOWN] and player_y < ROWS - 1:
            new_y += 1
        if keys[pygame.K_s]:  # Skip level
            level += 1
            player_x, player_y = 0, 0
            timer = 30
            maze = generate_maze()
            break

        if maze[new_y][new_x] == 0:
            player_x, player_y = new_x, new_y
        
        # Win condition
        if player_x == COLS - 1 and player_y == ROWS - 1:
            level += 1
            player_x, player_y = 0, 0
            timer = 30  # Reset timer
            maze = generate_maze()
            break
        
        # Timer update
        elapsed_time = time.time() - start_time
        timer = max(0, 30 - int(elapsed_time))

        # Display timer and level
        font = pygame.font.Font(None, 36)
        timer_text = font.render(f"Time: {timer}s", True, WHITE)
        level_text = font.render(f"Level: {level}", True, WHITE)
        screen.blit(timer_text, (10, 10))
        screen.blit(level_text, (WIDTH - 120, 10))

        pygame.display.update()
        clock.tick(10)
    
    # If time runs out, restart level
    if timer == 0:
        player_x, player_y = 0, 0
        timer = 30

pygame.quit()
