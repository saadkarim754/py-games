import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class Archer:
    def __init__(self):
        self.width = 40
        self.height = 60
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - 80
        self.speed = 5
        self.aim_angle = 0  # Angle in degrees

    def move(self, direction):
        self.x += direction * self.speed
        self.x = max(0, min(self.x, SCREEN_WIDTH - self.width))

    def adjust_aim(self, direction):
        self.aim_angle += direction * 2
        self.aim_angle = max(-80, min(self.aim_angle, 80))

    def draw(self, screen):
        # Draw archer body
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))
        
        # Draw aim line
        angle_rad = math.radians(-self.aim_angle)
        end_x = self.x + self.width//2 + math.sin(angle_rad) * 40
        end_y = self.y - math.cos(angle_rad) * 40
        pygame.draw.line(screen, RED, 
                        (self.x + self.width//2, self.y),
                        (end_x, end_y), 3)

class Arrow:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.speed = 10
        self.angle = angle
        self.active = True

    def move(self):
        angle_rad = math.radians(-self.angle)
        self.x += math.sin(angle_rad) * self.speed
        self.y -= math.cos(angle_rad) * self.speed

    def draw(self, screen):
        if self.active:
            angle_rad = math.radians(-self.angle)
            end_x = self.x + math.sin(angle_rad) * 20
            end_y = self.y - math.cos(angle_rad) * 20
            pygame.draw.line(screen, BLACK, (self.x, self.y), (end_x, end_y), 2)

class Target:
    def __init__(self):
        self.width = 30
        self.height = 30
        self.x = random.randint(0, SCREEN_WIDTH - self.width)
        self.y = -self.height
        self.speed = random.uniform(2, 5)
        self.active = True

    def move(self):
        self.y += self.speed

    def draw(self, screen):
        if self.active:
            pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))

def check_collision(arrow, target):
    if not arrow.active or not target.active:
        return False
    
    arrow_rect = pygame.Rect(arrow.x - 5, arrow.y - 5, 10, 10)
    target_rect = pygame.Rect(target.x, target.y, target.width, target.height)
    return arrow_rect.colliderect(target_rect)

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Archer Game")
    clock = pygame.time.Clock()

    archer = Archer()
    arrows = []
    targets = []
    target_spawn_timer = 0
    score = 0
    font = pygame.font.Font(None, 36)

    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Shoot arrow
                    arrow = Arrow(archer.x + archer.width//2, archer.y, archer.aim_angle)
                    arrows.append(arrow)

        # Input handling
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            archer.move(-1)
        if keys[pygame.K_RIGHT]:
            archer.move(1)
        if keys[pygame.K_UP]:
            archer.adjust_aim(1)
        if keys[pygame.K_DOWN]:
            archer.adjust_aim(-1)

        # Spawn targets
        target_spawn_timer += 1
        if target_spawn_timer >= 60:  # Spawn every 60 frames
            targets.append(Target())
            target_spawn_timer = 0

        # Update
        for arrow in arrows:
            arrow.move()
            if arrow.y < 0 or arrow.y > SCREEN_HEIGHT or arrow.x < 0 or arrow.x > SCREEN_WIDTH:
                arrow.active = False

        for target in targets:
            target.move()
            if target.y > SCREEN_HEIGHT:
                target.active = False

        # Check collisions
        for arrow in arrows:
            for target in targets:
                if check_collision(arrow, target):
                    arrow.active = False
                    target.active = False
                    score += 10

        # Clean up inactive objects
        arrows = [arrow for arrow in arrows if arrow.active]
        targets = [target for target in targets if target.active]

        # Draw
        screen.fill(WHITE)
        archer.draw(screen)
        for arrow in arrows:
            arrow.draw(screen)
        for target in targets:
            target.draw(screen)

        # Draw score
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()