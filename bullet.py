#used to store all the different bullet types... idk if this is efficient at all
#definitely need to combine some of these types and just use different values instead of creating more child classes

import pygame, sys
import numpy as np
import random

from scipy.integrate import ode

# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

windowWidth = 1000
windowHeight = 600

#TODO move display / sprite over here instead of in the 'sim' / 'environment'

#create a superclass for the other ones to extend
class Bullet(pygame.sprite.Sprite):
    def __init__(self, color = RED, width = 5, height = 5):
        pygame.sprite.Sprite.__init__(self)

        self.color = RED
        self.width = width
        self.height = height

        # self.image = pygame.Surface([self.width, self.height])    #kind of like the background of the square
        # self.rect = self.image.get_rect()               #get the rectangle representing the background
        # self.image.fill(WHITE)                          #set background to white 

        self.rect = pygame.Rect(0, 0, self.width, self.height)

        self.state = np.array([0.0, 0.0, 0.0, 0.0])   #[0] = x position, [1] = y position, [2] = x velocity, [3] = y velocity 

        self.initialSpeed = 10
        self.initialAngle = 45

        self.mass = 1.0
        self.gravity = -9.8
        self.gamma = 0.05            #coefficient of friction
        self.wind = 0               #not sure if this should be in the 'environment' or set to the bullet + environment and set speed on bullet in environment

        self.dt = 0.1               #delta time or change in time (how 'fast' the bullet will take its 'steps')
        self.cur_time = 0.0         #current time

        self.pierce = 1             #number of blocks that the projectile can break before it disappears

        self.initialRandomness = 0  #used to add 'shifts/randomness' to how bullets will be shot (might not actually use this)

        self.isActive = True

        #rk4 ... may not use this for every bullet type... 
        self.solver = ode(self.f)
        self.solver.set_integrator('dop853')
        self.solver.set_initial_value(self.state, self.cur_time) #not neccessary?
        self.solver.set_f_params(self.gamma, self.gravity)

    def setup(self, x, y, initialSpeed, initialAngle, pierce):

        self.state[0] = x
        self.state[1] = y

        self.initialSpeed = initialSpeed
        self.initialAngle = initialAngle

        self.pierce = pierce

        #split speed into x and y components
        self.state[2] = self.initialSpeed * np.cos(self.initialAngle / 180.0 * np.pi)   #x velocity (convert angle_degrees to radians since np uses radians in calculation)
        self.state[3] = -self.initialSpeed * np.sin(self.initialAngle / 180.0 * np.pi)  #y velocity

        self.trace_x = [self.state[0]]
        self.trace_y = [self.state[1]]

    def f(self, t, state, friction, gravity):

        #t: time
        #state: x velocty, y velocity
        #arg1: gravity
        #arg2: coefficient of friction

        xForce = - friction * state[2] # m*a = -gamma*vx

        yForce = friction * state[3] + self.mass * gravity   # m*a = -gamma*vy - m*g

        return np.array([state[2], state[3], xForce / self.mass, -yForce / self.mass])
    
    #used to update the bullet (get the next 'step') to its next location
    #idk how this will work for the other bullet types... simply not using rk4 for those 
    def step(self):

        self.solver.integrate(self.solver.t + self.dt)
        self.state = self.solver.y
        self.cur_time = self.solver.t

        self.rect.x, self.rect.y = self.state[0], self.state[1]

        #collision detection + response will be implemented in the child classes (this class will simply 'update' the bullet' position)
                    
    #collision response code - just used to break the bullet  
    #collision detection will be in the blocks ? idk how to efficiently detect if a bullet has collided with one of the blocks
    def breakBullet(self): 
        #check number of hits for the bullet, if less than 0, delete bullet 
        #if greater than 0, subtract 1 from it
        return
    
    def printLocation(self):
        print(f"Bullet at ({self.x}, {self.y})")

    def draw(self, screen):

        pygame.draw.circle(screen, self.color, self.rect.center, 5)    #draw circle 

class Shell(Bullet):
    def __init__(self, color = RED, width = 5, height = 5):
        super().__init__(  color, width, height)
    
    def step(self):
        super().step()

        #collision detection
        #check for collision against border (keep projectile inside 'map')
        if self.state[0] < 0 or self.state[0] > windowWidth-100:
            self.pierce = self.pierce - 1
            self.state[2] = -self.state[2] - (self.state[2] * 0.01) #subtract a bit of speed from the bullet when it collides... not really needed at all
        if self.state[1] < 0 or self.state[1] > windowHeight -100:
            self.pierce = self.pierce - 1
            self.state[3] = self.state[3] - (self.state[3] * 0.01)

        #reponse
        if self.pierce < 1:
            self.isActive = False

#redundant class... just use Shell but with different number pierce 
class PiercingShell(Bullet):
    def __init__(self, color = RED, width = 5, height = 5):
        super().__init__(self, color, width, height)
        self.pierce = 3

    def setup(self, x, y, initialSpeed, initialAngle, pierce):
        super().setup(x, y, initialSpeed, initialAngle)
        self.pierce = pierce
    
    def step(self):
        super().step()


class Bomb(Bullet): #creates an 'explosion' 
                    #(simply has bigger collision 'response' where it checks in a radius around it)
    def __init__(self, color = RED, width = 5, height = 5):
        super().__init__(self, color = RED, width = 5, height = 5)
        self.pierce = 3

    def setup(self, x, y, initialSpeed, initialAngle, pierce):
        super().setup(x, y, initialSpeed, initialAngle)
        self.pierce = pierce

    def step(self):
        super().step()
        #change collision response to 'break' blocks and hit tanks around point of collision

class BouncyBullet(Bullet): #will bounce on contact
    def __init__(self, color = RED, width = 5, height = 5):
        super().__init__(color, width, height)
        self.pierce = 3

    def setup(self, x, y, initialSpeed, initialAngle, pierce):
        super().setup(x, y, initialSpeed, initialAngle, pierce)
    
    def step(self):
        super().step()

        #simply just reversing velocity when it hits a surface
        #proper response should be to calculate the colliding surface normal and use that to calculate the 'bounce' 
            #but that seems too complicated...
        if self.state[0] < 0 or self.state[0] > windowWidth-100:
            self.pierce = self.pierce - 1
            self.state[2] = -self.state[2]
        if self.state[1] < 0 or self.state[1] > windowHeight -100:
            self.pierce = self.pierce - 1
            self.state[3] = -self.state[3] 

        #response
        if self.pierce < 1:
            self.isActive = False

class ReflectingBullet(Bullet): #shoots straight and reflect ('bounce') on contact 
    def __init__(self, color = RED, width = 5, height = 5):
        super().__init__(color, width, height)
        self.pierce = 3

    def setup(self, x, y, initialSpeed, initialAngle, pierce):
        super().setup(x, y, 10, initialAngle)

        self.pierce = pierce
        
        #this bullet simply has constant speed / velocity
        self.state[2] = self.state[2] 
        self.state[3] = self.state[3] 

    def step(self):
        self.cur_time = self.cur_time + self.dt

        self.state[0] = self.state[0] + self.state[2]
        self.state[1] = self.state[1] + self.state[3]
        
        #check for collision against border (keep projectile inside 'map')
        if self.state[0] < 0 or self.state[0] > windowWidth:
            self.state[2] = -self.state[2]
            self.pierce = self.pierce - 1
        if self.state[1] < 0 or self.state[1] > windowHeight:
            self.state[3] = -self.state[3]
            self.pierce = self.pierce - 1

        #check for collision against blocks,
            #check which side it collides?
            #if hit bottom side of block (projectile going up) or hit top side of block (projectile going down) 
                #reverse y velcoty 
                #self.state[3] = -self.state[3]
            #if hit side of block (projectile going left / right)
                #reverse x velocity
                # self.state[2] = -self.state[2]
                
        self.rect.x, self.rect.y = self.state[0], self.state[1]
            
        if self.pierce < 1:
            self.isActive = False

class FillingBullet(Bullet): #shoots a normal bullet, but fills the terrain with blocks... maybe too complicated?
    def __init__(self, color = RED, width = 5, height = 5):
        super().__init__(self, color, width, height)
        self.pierce = 3

    def setup(self, x, y, initialSpeed, initialAngle, pierce):
        super().setup(x, y, initialSpeed, initialAngle)
        self.pierce = pierce
    
    def step(self):
        super().step()

#used for the classes that have multiple bullets used... maybe this is redundant because I'm still creating individual classes for the actual multi-bullet classes
class Bullets():    

    def __init__(self, color = RED, width = 5, height = 5):

        self.shells = [] 

        self.projectiles = 3 #number of projectiles that will split off of the main projectile

        self.dt = 0.1           #delta time or change in time (how 'fast' the bullet will take its 'steps')
        self.cur_time = 0.0     #current time

        newBullet = Shell()
        self.shells.append(newBullet)

        self.isActive = True

    #sets up the inital bullet(s) that will be fired from the group of bullets
    def setup(self, x, y, initialSpeed, initialAngle, projectiles):
        self.projectiles = projectiles

        for shell in self.shells:
            shell.setup(x, y, initialSpeed, initialAngle, 1)

    def step(self):
        self.cur_time = self.cur_time + self.dt

        for shell in self.shells:
            shell.step()
            #if shell collides, 
                #shell.breakBullet()
            if shell.rect.centery > windowHeight or shell.rect.centery < 0 or shell.rect.centerx < 0 or shell.rect.centerx > windowWidth:
                # print('remove')
                self.breakBullet(shell)

        if len(self.shells) < 1 and self.projectiles <= 1:
            self.isActive = False

    #just removes one bullet, given it's position/index, from the array  
    def breakBullet(self, shell): 
        # self.shells.pop(position)
        self.shells.remove(shell)
        return
    
    def printLocation(self):
        self.shells.printlocation()

    def draw(self, screen):
        for shell in self.shells:
            shell.draw(screen)

class Firework(Bullets):
    def __init__(self, color = RED, width = 5, height = 5):
        super().__init__(color, width, height)
        self.splitTime = 5
         
    def setup(self, x, y, initialSpeed, initialAngle, projectiles):
        super().setup(x, y, initialSpeed, initialAngle, projectiles)
        self.splitTime = (initialSpeed / 15) + (initialAngle / 20) + 1
        print(self.splitTime)

    def step(self):
        #if firework projectile has been in air for a while, split projectile
        #shells.remove(shell)
        #for i in range(self.splits)
            #shells.add(new Shell)

        super().step()

        #if the initial projectile has been in the air for a while (3 seconds?) and there are splits left, remove initial shell and create new shells
        if self.cur_time > self.splitTime and self.projectiles > 1:  
            # print(self.cur_time) 
            self.split()

        #if collided before split, split early 

    def split(self):
        projectiles = self.projectiles
                
        for i in range(projectiles):
            # print(i)
            self.projectiles = self.projectiles - 1

            speed = random.randint(30, 50)
            angle = random.randint(0, 360)

            newShell = Shell()
            newShell.setup(self.shells[0].state[0], self.shells[0].state[1], speed, angle, 1)
            self.shells.append(newShell)

        self.shells.pop(0)

class Volley(Bullets):   #shoots a volley of bullets at once instead of just one
    def __init__(self, color = RED, width = 5, height = 5):
        super().__init__(color, width, height)
        self.initialSpeed = 0
        self.initialAngle = 0

        self.xPos = 0
        self.yPos = 0

    def setup(self, x, y, initialSpeed, initialAngle, projectiles):
        super().setup(x, y, initialSpeed, initialAngle, projectiles)
        self.xPos = x
        self.yPos = y
        self.initialSpeed = initialSpeed
        self.initialAngle = initialAngle

    def step(self):
        super().step()

        while self.projectiles > 1:
            self.projectiles = self.projectiles - 1

            speed = random.randint(self.initialSpeed - 10, self.initialSpeed + 10)
            angle = random.randint(self.initialAngle - 20, self.initialAngle + 20)

            newShell = Shell()
            newShell.setup(self.xPos, self.yPos, speed, angle, 1)
            self.shells.append(newShell)

class Rapid(Bullets): #shoots a bunch of bullets in quick succession with a bit of randomess for each 
    def __init__(self, color = RED, width = 5, height = 5):
        super().__init__(color, width, height)        
        self.initialSpeed = 0
        self.initialAngle = 0

        self.xPos = 0
        self.yPos = 0

    def setup(self, x, y, initialSpeed, initialAngle, projectiles):
        super().setup(x, y, initialSpeed, initialAngle, projectiles)
        self.xPos = x
        self.yPos = y
        self.initialSpeed = initialSpeed
        self.initialAngle = initialAngle
    
    def step(self):
        super().step()
        
        #shoot a bullet every ~1 'second'
        if self.cur_time % 0.99 < 0.1 and self.projectiles > 1:
            self.projectiles = self.projectiles - 1

            angle = random.randint(self.initialAngle - 30, self.initialAngle + 30)

            newShell = Shell()
            newShell.setup(self.xPos, self.yPos, self.initialSpeed, angle, 1)
            self.shells.append(newShell)
