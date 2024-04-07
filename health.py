

import pygame
import numpy as np
import random
import bullet

# Initialize Pygame
pygame.init()

# Screen dimensions and setup
display_width = 800
display_height = 600
game_layout_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('2 Player Tanks Game')

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Tank parameters
tnk_width = 40
tnk_height = 20
tur_width = 5
whl_width = 5

# Movement and game settings
clock = pygame.time.Clock()
FPS = 15

# Fonts
small_font = pygame.font.SysFont("comicsansms", 25)
large_font = pygame.font.SysFont("comicsansms", 25)

# Simplified Shell class
class Shell:
    def __init__(self, x, y, speed_x, speed_y, color):
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.color = color

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        # Draw the bullet
        pygame.draw.circle(game_layout_display, self.color, (int(self.x), int(self.y)), 5)

# Tank Class
class Tank:
    def __init__(self, x, y, color, orientation='right'):
        self.x = x
        self.y = y
        self.color = color
        self.hp = 100
        self.fuel = 100
        self.aimSpeed = 50
        self.aimAngle = 45
        self.bullets = []
        self.orientation = orientation
        self.aimDirection = 1 if orientation == 'right' else -1
        self.tempDirection = 0 if orientation == 'right' else 90

    def move(self, direction):
        # Restrict tank movement within screen boundaries
        self.x += max(min(direction * 5, display_width - self.x - tnk_width), -self.x)

    def shoot(self):
        angle_rad = np.radians(self.aimAngle)
        speed_x = self.aimSpeed * np.cos(angle_rad) * self.aimDirection
        speed_y = -self.aimSpeed * np.sin(angle_rad)
        newBullet = bullet.Shell()
        if self.aimDirection == -1:
            aimAngle = 180 - self.aimAngle
        else: 
            aimAngle = self.aimAngle
        newBullet.setup(self.x + tnk_width // 2, self.y, self.aimSpeed + 30, aimAngle, 1)
        self.bullets.append(newBullet)

    def draw(self):
        pygame.draw.rect(game_layout_display, self.color, (self.x, self.y, tnk_width, tnk_height))
        turret_end_x = self.x + tnk_width / 2 + np.cos(np.radians(self.aimAngle)) * 20 * self.aimDirection
        turret_end_y = self.y - np.sin(np.radians(self.aimAngle)) * 20
        pygame.draw.line(game_layout_display, self.color, (self.x + tnk_width / 2, self.y), (turret_end_x, turret_end_y), tur_width)

    def update_bullets(self):
        for bullet in self.bullets:
            bullet.step()
            bullet.draw(game_layout_display)
            if bullet.state[1] < 0 or bullet.state[0] < 0 or bullet.state[0] > display_width:
                self.bullets.remove(bullet)

        # Method to draw the health bar
    # Method to draw the health bar
    def draw_health_bar(self):
        if self.hp < 0: self.hp = 0

        smaller_font = pygame.font.SysFont("comicsansms", 15)
        health_bar_text = smaller_font.render("Health", True, BLACK)
        game_layout_display.blit(health_bar_text, (self.x, self.y + tnk_height))

        BAR_LENGTH = 100  # Adjusted bar length for the display
        BAR_HEIGHT = 10
        fill = (self.hp / 100) * BAR_LENGTH
        # The y coordinate is now set to self.y + tnk_height (the bottom of the tank) + a small offset
        outline_rect = pygame.Rect(self.x, self.y + tnk_height + 20, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(self.x, self.y + tnk_height + 20, self.hp, BAR_HEIGHT)
        pygame.draw.rect(game_layout_display, RED, fill_rect)
        pygame.draw.rect(game_layout_display, BLACK, outline_rect, 2)  # Draw outline

    # Method to draw the power bar
    def draw_power_bar(self):

        # Constants for the power bar dimensions
        BAR_LENGTH = 100  # Adjusted bar length for the display
        BAR_HEIGHT = 10
        
        smaller_font = pygame.font.SysFont("comicsansms", 15)
        power_bar_text = smaller_font.render("Power", True, BLACK)
        game_layout_display.blit(power_bar_text, (self.x, self.y + tnk_height + BAR_HEIGHT + 16))
        
        # Drawing the power bar directly underneath the tank
        outline_rect = pygame.Rect(self.x, self.y + tnk_height + BAR_HEIGHT + 35, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(self.x, self.y + tnk_height + BAR_HEIGHT + 35, self.aimSpeed, BAR_HEIGHT)
        
        pygame.draw.rect(game_layout_display, BLUE, fill_rect)
        pygame.draw.rect(game_layout_display, BLACK, outline_rect, 2)
 
    def draw_angle_text(self, font):
        BAR_HEIGHT = 10

        smaller_font = pygame.font.SysFont("comicsansms", 15)

        angle_text = smaller_font.render("Angle: " + str(self.aimAngle) + "°", True, BLACK)
        # Positioning the angle text below the power bar
        game_layout_display.blit(angle_text, (self.x, self.y + tnk_height + 2 * BAR_HEIGHT + 32))

def game_loop():
    player1 = Tank(100, display_height - 100, GREEN, 'right')
    player2 = Tank(display_width - 140, display_height - 100, RED, 'left')
    
    player1_turn = True

    game_exit = False

    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
                
            if player1_turn:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        player1.move(-1)
                    elif event.key == pygame.K_d:
                        player1.move(1)
                    elif event.key == pygame.K_w:
                        player1.aimAngle = min(player1.aimAngle + 5, 90)
                    elif event.key == pygame.K_s:
                        player1.aimAngle = max(player1.aimAngle - 5, 0)
                    elif event.key == pygame.K_SPACE: # Fire
                        player1.shoot()
                        player1_turn = False # Switch turn to Player 2
                    elif event.key == pygame.K_LEFTBRACKET: # Decrease speed
                        player1.aimSpeed = max(player1.aimSpeed - 10, 0)
                        print(player1.aimSpeed)
                    elif event.key == pygame.K_RIGHTBRACKET: # Increase speed
                        player1.aimSpeed = min(player1.aimSpeed + 10, 100)
                        print(player1.aimSpeed)
            else:  # Player 2 controls
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        player2.move(-1)
                    elif event.key == pygame.K_RIGHT:
                        player2.move(1)
                    elif event.key == pygame.K_UP:
                        player2.aimAngle = min(player2.aimAngle + 5, 90)
                    elif event.key == pygame.K_DOWN:
                        player2.aimAngle = max(player2.aimAngle - 5, 0)
                    elif event.key == pygame.K_RETURN: # Fire (Return key for Player 2)
                        player2.shoot()
                        player1_turn = True # Switch turn back to Player 1
                    elif event.key == pygame.K_COMMA: # Decrease speed
                        player2.aimSpeed = max(player2.aimSpeed - 10, 10)
                    elif event.key == pygame.K_PERIOD: # Increase speed
                        player2.aimSpeed = min(player2.aimSpeed + 10, 100)
                
        game_layout_display.fill(WHITE)

        # # Draw power and angle bars for Player 1
        # power_range = 90  # Range of values for the speed
        # power_value_p1 = max(min(player1.aimSpeed, power_range), 10)  # Ensure power value is within range
        # power_bar_length_p1 = int((power_value_p1 - 10) / power_range * 400)  # Calculate length of power bar
        # angle_bar_length_p1 = player1.aimAngle  # Angle bar length
        # pygame.draw.rect(game_layout_display, BLUE, (10, 10, power_bar_length_p1, 20))  # Power bar for Player 1
        # pygame.draw.rect(game_layout_display, RED, (10, 40, angle_bar_length_p1 * 4, 20))  # Angle bar for Player 1

        # # Draw power and angle bars for Player 2
        # power_value_p2 = max(min(player2.aimSpeed, power_range), 10)  # Ensure power value is within range
        # power_bar_length_p2 = int((power_value_p2 - 10) / power_range * 400)  # Calculate length of power bar
        # angle_bar_length_p2 = player2.aimAngle  # Angle bar length
        # pygame.draw.rect(game_layout_display, BLUE, (display_width - power_bar_length_p2 - 10, 10, power_bar_length_p2, 20))  # Power bar for Player 2
        # pygame.draw.rect(game_layout_display, RED, (display_width - angle_bar_length_p2 * 4 - 10, 40, angle_bar_length_p2 * 4, 20))  # Angle bar for Player 2
        
                # Draw tanks, update/draw bullets, and draw health and power bars for both tanks
        player1.draw()
        player1.draw_health_bar()
        player1.draw_power_bar()
        player1.draw_angle_text(small_font)
        player1.update_bullets()

        player2.draw()
        player2.draw_health_bar()
        player2.draw_power_bar()
        player2.draw_angle_text(small_font)
        player2.update_bullets()

        # Collision detection and game over checks remain the same
        
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    quit()

# Call the game loop
game_loop()
