import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
COLORS = [RED, GREEN, BLUE, WHITE]  # List of colors for the bricks

# Game elements
BRICK_WIDTH, BRICK_HEIGHT = 10, 10
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 20
BALL_RADIUS = 10
NUM_ROWS = 20  # Number of rows of bricks
NUM_COLS = 80  # Number of columns of bricks
BRICK_PADDING = 0

# Frames per second
FPS = 60
clock = pygame.time.Clock()

class Brick:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
        self.color = color

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.color = WHITE
        self.speed = 5

    def move(self, direction):
        if direction == "left" and self.rect.left > 0:
            self.rect.x -= self.speed
        if direction == "right" and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

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

NUM_BRICKS = 200 # Total number of bricks to place

def create_bricks():
    bricks = []
    occupied_positions = set()

    for i in range(50):
        col = random.randint(5, 15)
        row = random.randint(10, 20)
        position = (row, col)

        # Check if the position is already occupied
        if position not in occupied_positions:
            occupied_positions.add(position)
            x = col * BRICK_WIDTH 
            y = row * BRICK_HEIGHT
            color = RED  # Keeping a single color for simplicity, can be randomized
            bricks.append(Brick(x, y, color))

    for i in range(50):
        col = random.randint(30, 40)
        row = random.randint(0, 20)
        position = (row, col)

        # Check if the position is already occupied
        if position not in occupied_positions:
            occupied_positions.add(position)
            x = col * BRICK_WIDTH 
            y = row * BRICK_HEIGHT
            color = RED  # Keeping a single color for simplicity, can be randomized
            bricks.append(Brick(x, y, color))

    for i in range(80):
        col = random.randint(50, 65)
        row = random.randint(5, 20)
        position = (row, col)

        # Check if the position is already occupied
        if position not in occupied_positions:
            occupied_positions.add(position)
            x = col * BRICK_WIDTH 
            y = row * BRICK_HEIGHT
            color = RED  # Keeping a single color for simplicity, can be randomized
            bricks.append(Brick(x, y, color))

    for i in range(80):
        col = random.randint(70, 80)
        row = random.randint(20, 30)
        position = (row, col)

        # Check if the position is already occupied
        if position not in occupied_positions:
            occupied_positions.add(position)
            x = col * BRICK_WIDTH 
            y = row * BRICK_HEIGHT
            color = RED  # Keeping a single color for simplicity, can be randomized
            bricks.append(Brick(x, y, color))

    for i in range(50):
        col = random.randint(0, NUM_COLS - 1)
        row = random.randint(0, NUM_ROWS - 1)
        position = (row, col)

        # Check if the position is already occupied
        if position not in occupied_positions:
            occupied_positions.add(position)
            x = col * BRICK_WIDTH 
            y = row * BRICK_HEIGHT
            color = RED  # Keeping a single color for simplicity, can be randomized
            bricks.append(Brick(x, y, color))

    for i in range(150):
        col = random.randint(25, NUM_COLS - 25)
        row = random.randint(20, NUM_ROWS + 20)
        position = (row, col)

        # Check if the position is already occupied
        if position not in occupied_positions:
            occupied_positions.add(position)
            x = col * BRICK_WIDTH 
            y = row * BRICK_HEIGHT
            color = RED  # Keeping a single color for simplicity, can be randomized
            bricks.append(Brick(x, y, color))

    return bricks

bricks = create_bricks()

# Create paddle
paddle = Paddle(SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2, SCREEN_HEIGHT - 40)

# Create ball
ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Main game loop
running = True

paused = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    event = pygame.event.poll()

    keys = pygame.key.get_pressed()

    # if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
    #     paused = True
    #     continue
    # elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
    #     paused = False
    #     print("unpause")
    #     continue

    if keys[pygame.K_p]:
        paused = True
    elif keys[pygame.K_r]:
        paused = False

    if not paused:
        # Update ball position
        ball.move()

    if keys[pygame.K_LEFT]:
        paddle.move("left")
    if keys[pygame.K_RIGHT]:
        paddle.move("right")

    # Check for ball collision with paddle
    if ball.rect.colliderect(paddle.rect):
        ball.dy = -ball.dy

    # Check for ball collision with bricks
    for brick in bricks[:]:
        if ball.rect.colliderect(brick.rect):
            ball.dy = -ball.dy
            bricks.remove(brick)

    # Clear screen
    screen.fill(BLACK)

    # Draw elements
    for brick in bricks:
        brick.draw()
    paddle.draw()
    ball.draw()

    # Update display
    pygame.display.flip()

    # Cap the framerate
    clock.tick(FPS)

pygame.quit()
