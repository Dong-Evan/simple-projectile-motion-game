import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Load the background image
background = pygame.image.load('terrain.png')
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
COLORS = [RED, GREEN, BLUE, WHITE]  # List of colors for the bricks

# Game elements
BRICK_WIDTH, BRICK_HEIGHT = 60, 30
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 20
BALL_RADIUS = 10
NUM_ROWS = 5  # Number of rows of bricks
NUM_COLS = 13  # Number of columns of bricks
BRICK_PADDING = 10

# Frames per second
FPS = 60
clock = pygame.time.Clock()

class Brick2:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
        self.color = color

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

# class Paddle:
#     def __init__(self, x, y):
#         self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
#         self.color = WHITE
#         self.speed = 5

#     def move(self, direction):
#         if direction == "left" and self.rect.left > 0:
#             self.rect.x -= self.speed
#         if direction == "right" and self.rect.right < SCREEN_WIDTH:
#             self.rect.x += self.speed

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

class Ball:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BALL_RADIUS * 2, BALL_RADIUS * 2)
        self.color = WHITE
        self.dx, self.dy = 5, -5

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Bounce off walls
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.dx = -self.dx
        if self.rect.top <= 0:
            self.dy = -self.dy

    def draw(self):
        pygame.draw.circle(screen, self.color, self.rect.center, BALL_RADIUS)

NUM_BRICKS = 10 # Total number of bricks to place

def create_bricks():
    bricks = []
    positions = set()
    while len(bricks) < NUM_BRICKS:
        row = random.randint(0, NUM_ROWS - 1)
        col = random.randint(0, NUM_COLS - 1)
        if (row, col) not in positions:  # Ensure no duplicate positions
            positions.add((row, col))
            x = col * (BRICK_WIDTH + BRICK_PADDING) + BRICK_PADDING
            y = row * (BRICK_HEIGHT + BRICK_PADDING) + 10  # Start 10 pixels down from the top
            color = random.choice(COLORS)  # Choose a random color for each brick
            bricks.append(Brick2(x, y, color))
    return bricks


bricks = create_bricks()

# # Create paddle
# paddle = Paddle(SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2, SCREEN_HEIGHT - 40)

# # Create ball
# ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_LEFT]:
    #     paddle.move("left")
    # if keys[pygame.K_RIGHT]:
    #     paddle.move("right")

    # Update ball position
    # ball.move()

    # # Check for ball collision with paddle
    # if ball.rect.colliderect(paddle.rect):
    #     ball.dy = -ball.dy

    # Check for ball collision with bricks
    # for brick in bricks[:]:
    #     if ball.rect.colliderect(brick.rect):
    #         ball.dy = -ball.dy
    #         bricks.remove(brick)  # Remove the brick when hit

    # Clear screen and redraw background
    screen.fill(BLACK)  # Optionally fill the screen with a solid color before blitting the background
    screen.blit(background, (0, 0))

    # Redraw game elements
    for brick in bricks:
        brick.draw()

    # paddle.draw()
    # ball.draw()

    # Update display
    pygame.display.flip()

    # Cap the framerate
    clock.tick(FPS)

pygame.quit()

