import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Archer Shooter Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Archer settings
archer_width, archer_height = 50, 60
archer_x = WIDTH // 2
archer_y = HEIGHT - 100
archer_speed = 5
aim_angle = -45  # Start aiming diagonally

# Arrow settings
arrow_speed = 10
arrows = []

# Target settings
target_size = 30
targets = []
target_speed = 2
spawn_timer = 0

# Font for score
font = pygame.font.Font(None, 36)
score = 0

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
    
    # Move archer left/right
    if keys[pygame.K_LEFT] and archer_x > 0:
        archer_x -= archer_speed
    if keys[pygame.K_RIGHT] and archer_x < WIDTH - archer_width:
        archer_x += archer_speed

    # Change aim angle (up/down)
    if keys[pygame.K_UP] and aim_angle > -90:
        aim_angle -= 2
    if keys[pygame.K_DOWN] and aim_angle < -10:
        aim_angle += 2

    # Shoot arrow
    if keys[pygame.K_SPACE]:
        arrow_dx = math.cos(math.radians(aim_angle)) * arrow_speed
        arrow_dy = math.sin(math.radians(aim_angle)) * arrow_speed
        arrows.append([archer_x + archer_width // 2, archer_y, arrow_dx, arrow_dy])

    # Move arrows
    for arrow in arrows:
        arrow[0] += arrow[2]  # X movement
        arrow[1] += arrow[3]  # Y movement

    # Remove off-screen arrows
    arrows = [arrow for arrow in arrows if arrow[1] > 0 and 0 < arrow[0] < WIDTH]

    # Spawn targets
    spawn_timer += 1
    if spawn_timer > 50:  # Every ~1 sec
        targets.append([random.randint(0, WIDTH - target_size), 0])
        spawn_timer = 0

    # Move targets
    for target in targets:
        target[1] += target_speed

    # Check for collisions
    for arrow in arrows[:]:
        for target in targets[:]:
            if (target[0] < arrow[0] < target[0] + target_size and
                    target[1] < arrow[1] < target[1] + target_size):
                targets.remove(target)
                arrows.remove(arrow)
                score += 1

    # Draw archer
    pygame.draw.rect(screen, BLUE, (archer_x, archer_y, archer_width, archer_height))

    # Draw aim line
    aim_x = archer_x + archer_width // 2 + math.cos(math.radians(aim_angle)) * 40
    aim_y = archer_y + math.sin(math.radians(aim_angle)) * 40
    pygame.draw.line(screen, RED, (archer_x + archer_width // 2, archer_y), (aim_x, aim_y), 3)

    # Draw arrows
    for arrow in arrows:
        pygame.draw.circle(screen, BLACK, (int(arrow[0]), int(arrow[1])), 5)

    # Draw targets
    for target in targets:
        pygame.draw.rect(screen, GREEN, (target[0], target[1], target_size, target_size))

    # Draw score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
