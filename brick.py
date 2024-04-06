import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
windowWidth = 1000
windowHeight = 600
screen = pygame.display.set_mode((windowWidth, windowHeight))

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
COLORS = [RED, GREEN, BLUE, WHITE]  # List of colors for the bricks

class Brick:
    def __init__(self, x, y, brickWidth, brickHeight, color):

        self.rect = pygame.Rect(x, y, brickWidth, brickHeight)
        self.color = color

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

class BrickManager:
    def __init__(self):

        self.occupiedPositions = set()

        self.brickWidth = 20
        self.brickHeight = 20
        self.numberOfRows = windowHeight / self.brickHeight  #max number of rows of bricks 
        self.numberOfColumns = windowWidth / self.brickWidth  #max number of columns of bricks 

    def create_bricks(self, numberOfBricks = 0, startColumn = 0, endColumn = 0, startRow = 0, endRow = 0, color = GREEN):

        bricks = []
        
        for i in range(numberOfBricks):
            column = random.randint(startColumn, endColumn)
            row = random.randint(startRow, endRow)
            newPosition = (column, row)

            if newPosition not in self.occupiedPositions:
                self.occupiedPositions.add(newPosition)
                xPos = column * self.brickWidth
                yPos = row * self.brickHeight
                newBrick = Brick(xPos, yPos, color)
                bricks.append(newBrick)

        return bricks
