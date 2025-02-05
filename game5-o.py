import pygame
import random

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

# Maze generation (0 = open path, 1 = wall)
maze = [[1 if random.random() < 0.3 else 0 for _ in range(COLS)] for _ in range(ROWS)]
maze[0][0] = 0  # Start position
maze[ROWS - 1][COLS - 1] = 0  # Goal position (Princess)

# Player settings
player_x, player_y = 0, 0
player_size = CELL_SIZE // 2

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(WHITE)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get key states
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

    # Move player if not hitting a wall
    if maze[new_y][new_x] == 0:
        player_x, player_y = new_x, new_y

    # Draw maze
    for y in range(ROWS):
        for x in range(COLS):
            if maze[y][x] == 1:
                pygame.draw.rect(screen, BLACK, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw princess (goal)
    pygame.draw.rect(screen, RED, ((COLS - 1) * CELL_SIZE, (ROWS - 1) * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw player
    pygame.draw.circle(screen, BLUE, (player_x * CELL_SIZE + CELL_SIZE // 2, player_y * CELL_SIZE + CELL_SIZE // 2), player_size)

    # Check for win condition
    if player_x == COLS - 1 and player_y == ROWS - 1:
        print("You saved the princess! 🎉")
        running = False

    pygame.display.update()
    clock.tick(10)

pygame.quit()
