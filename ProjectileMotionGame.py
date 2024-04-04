#the 'main' simulation environment 

import pygame, sys
import numpy as np
from scipy.integrate import ode
import bullet

# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# clock object that ensure that animation has the same
# on all machines, regardless of the actual machine speed.
clock = pygame.time.Clock()

def load_image(name):
    image = pygame.image.load(name)
    return image

class MyCircle(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width, height])
        self.rect = self.image.get_rect()
        self.image.fill(WHITE)
        cx = self.rect.centerx
        cy = self.rect.centery
        pygame.draw.circle(self.image, color, (width//2, height//2), cx, cy)
        self.rect = self.image.get_rect()

    def update(self):
        pass

'''
#don't need this...
# def sim_to_screen(win_height, x, y):

#     # x += 10
#     # y += 10

#     return x, win_height - y
'''

def main():
    #a lot of this will have to be changed so that we have different bullets and can create them when we want to shoot

    # initializing pygame
    pygame.init()

    #set up window and game border
    # top left corner is (0,0)
    win_width = 640
    win_height = 640
    screen = pygame.display.set_mode((win_width, win_height))
    pygame.display.set_caption('Tank Game')

    #windSpeed = 0 #can represent this with two bars horizontally (only 1 bar will be filled; left bar meaens wind blowing left, same for right), or just use a number

    #set up terrain (start with simple flat floor)

    #set up a sprite group which will be drawn on the screen
        #essentially every object that will be drawn should be stored here
    #...sike this bad (?) just call the object's draw method for each object that needs to be drawn, or instead of creating a sprite group, create an objects list and loop through that to call each object's draw
    spriteGroup = pygame.sprite.Group()
    #create tank for p1
    #tank1 = 
    #create tank for p2
    #tank2 = 


    #not sure how to add bullets right now (since they have to be created and deleted)
    #one option is to to create these sprites (circles) and then update their
        #position using the positions of the actual bullets, but that doesn't seem right...
    
    #temporary code for drawing bullet ...
    # shell = bullet.Shell(RED, 10, 10) 
    # shell.setup(0.0, 400.0, 70.0, 25.0)

    shell = bullet.Firework(RED, 10, 10) 
    shell.setup(0.0, 400.0, 70.0, 25.0, 3)
    
    # spriteGroup.add(shell)

    # sim = bullet.ReflectingBullet()

    # sim.setup(0.0, 400.0, 70.0, 25.0, 3)  #will probably need to set up the position and velocity of the bullets differently
    #...

    # print('--------------------------------')
    # print('Usage:')
    # print('Press (r) to start/resume simulation')
    # print('Press (p) to pause simulation')
    # print('Press (space) to step forward simulation when paused')
    # print('--------------------------------')

    #main loop of the game (infinite loop while both tanks are alive)
        #basic rundown: 
            #determine who has control (who's turn it is), 
            #check for key presses 
                #update position of tank (A & D)
                #update position / size (or color?) of arrow showing where bullet would go (Q & E for turning left/right, W & S for speed/power of bullet) 
                #update bullet selection (R? loops through bullet list each time it's pressed)
                #if fire button pressed (space for fire?), create and add new bullet 
            #if there are bullet(s), update bullets' position
                #check for collisions
                #update things accordingly; break bullets, break blocks/terrain, damage tanks
            #check hp of tanks, if one is 0, other wins
            #draw everything (spriteGroup (tank, bullet), terrain, hp, aim trajectory arrow, numbers (power (and angle) of shot))
    
    while True:
        # 30 fps (this is from lab... not sure what to do with it)
        clock.tick(30)

        #int control variable that determines who is currently in control (since we want turn based)
            #start with letting p1 have control
            #i.e. pressing keys will affect tank1
        control = 0

        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            shell.pause()
            continue
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            shell.resume()
            continue
        else:
            pass

        #temporary ...
        # update sprite x, y position using values
        # returned from the simulation
        # my_sprite.rect.x, my_sprite.rect.y =  sim.state[0], sim.state[1]
        # print(sim.state[:2])
        #...

        #display procedure (re-draw everything)
            #clear the background, and draw the sprites 
        screen.fill(WHITE)
        # spriteGroup.update()
        # spriteGroup.draw(screen)

        #updating the simulation
            #want 
        if not shell.paused:
            shell.step()
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                shell.step()

        shell.draw(screen)
        pygame.display.flip()

    # print("r: %10.2f" % sim.trace_x[-1])

if __name__ == '__main__':
    main()