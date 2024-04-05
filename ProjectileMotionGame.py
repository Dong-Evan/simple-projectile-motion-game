#the 'main' simulation environment 

import pygame, sys
import numpy as np
from scipy.integrate import ode
import bullet
import tank

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

    #set up obstacles (bricks to block bullets)


    #set up a sprite group which will be drawn on the screen
        #essentially every object that will be drawn should be stored here
    #...sike this bad (?) just call the object's draw method for each object that needs to be drawn, or instead of creating a sprite group, create an objects list and loop through that to call each object's draw
    # spriteGroup = pygame.sprite.Group()

    #create tank for p1
    tank1 = tank.Tank()
    #create tank for p2
    tank2 = tank.Tank()

    # shotBullet = bullet.Firework(RED, 10, 10) 

    tanks = [tank1, tank2]

    #not sure how to add bullets right now (since they have to be created and deleted)
    #one option is to to create these sprites (circles) and then update their
        #position using the positions of the actual bullets, but that doesn't seem right...
    
    #temporary code for drawing bullet ...
    # shell = bullet.Shell(RED, 10, 10) 
    # shell.setup(0.0, 400.0, 70.0, 25.0)

    # sim = bullet.ReflectingBullet()

    # sim.setup(0.0, 400.0, 70.0, 25.0, 3)  #will probably need to set up the position and velocity of the bullets differently

    print('--------------------------------')
    print('Use A & D to move')
    print('Use W & D to change shot power')
    print('Use Q & E to change shot direction')
    print('Press R to cycle through avaiable bullets')
    print('Press Space to shoot')
    print('Press P to pause and K to resume')
    print('Press L to step forward in game when paused')
    print('--------------------------------')

    '''
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
    '''

    paused = True

    while True:
        # 30 fps (this is from lab... not sure what to do with it)
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

        #int control variable that determines who is currently in control (since we want turn based)
            #start with letting p1 have control
            #i.e. pressing keys will affect tank1
        control = 0
        currentTank = tanks[control] #get the tank corresponding to current control from list of tanks

        #get key presses
        keys = pygame.key.get_pressed()

        #controls for pausing and resuming the game
        if keys[pygame.K_p]:
            paused = True
        elif keys[pygame.K_k]:
            paused = False
        
        #clear the background (to re-draw the sprites) 
        screen.fill(WHITE)

        if not paused:

            # #check for tank controls (need to implement these properly after tank class is done)
            if keys[pygame.K_a]:
                print('left')
                # currentTank.move(-1)
            elif keys[pygame.K_d]:
                print('right')
                # currentTank.move(1)

            #controls for changing shot power of bullet(s) (could either pass a number to method or have no parameter and just have a fixed number in the method itself)
                #*make sure power is between 10 to 100 (10 might be too high? definitely don't want 0)
            if keys[pygame.K_w]:
                print('increase shot power')
                #currentTank.increasePower(1)
            elif keys[pygame.K_s]:
                print('decrease shot power')
                #currentTank.decreasePower(1)

            #controls for aiming tank barrel / bullet (change 1 degree at a time?)
                #*make sure angle is between 0 to 180 (the upper side of the tank)
            if keys[pygame.K_q]:
                print('shift aim left')
                #currentTank.shiftAimAngle(-1)
            elif keys[pygame.K_e]:
                print('shift aim right')
                #currentTank.shiftAimAngle(1)

            #control for cycling bullet type 
            if keys[pygame.K_r]:
                print('cycle bullet')
                #currentTank.nextBullet()

            if keys[pygame.K_SPACE]:
                print('shoot')
                #shotBullet = currentTank.shoot() #this will simply remove the selected bullet from the tank's bullet list and return it
                shotBullet = bullet.Firework(RED, 10, 10) 
                shotBullet.setup(0.0, 400.0, 40.0, 45.0, 5) #setup should use the tank's aim power and angle (maybe have the setup in tank and return fully setup bullet from tank.shoot())
                print(len(shotBullet.shells))
                #while the bullet is still 'alive', only update the bullet and don't let anything else have control
                while len(shotBullet.shells) > 0:
                    clock.tick(30)
                    screen.fill(WHITE)
                    #draw everything

                    shotBullet.step()
                    shotBullet.draw(screen)
                    
                    pygame.display.flip()

                if control == 0:
                    control = 1 
                else:
                    control = 0

            #display procedure (re-draw everything)

            # if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # shell.step()

        
        pygame.display.flip()

    # print("r: %10.2f" % sim.trace_x[-1])

if __name__ == '__main__':
    main()