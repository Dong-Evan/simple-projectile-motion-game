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

class Tank():
    def __init__(self):

        self.hp = 100
        self.fuel = 100

        self.state = [100, 100, 0, 0] #no need for velocity ?

        self.aimSpeed = 10
        self.aimAngle = 45

        self.bullets = [bullet.Shell()] #maybe just use ints? 0 = normal, 1 = bouncy, 2 = reflecting...
        self.currentBullet = 0

        return
    
    def move(self, direction = 0):
        #direction can be -1 (left), or +1 (right)
        self.state[0] = self.state[0] + direction
        self.fuel = self.fuel - 1

        return
    
    def shoot(self):
        bulletType = self.bullets[self.currentBullet]

        #check what bullet (just multiple if statements?)
        if type(bulletType) == type(bullet.Shell):
            pass #if it's a normal bullet, don't remove it
        else:
            #remove bullet from list
            self.bullets.remove(bulletType)

        #create (and return) that bullet with speed and angle
        newBullet = bullet.Shell().setup(self.state[0], self.state[1], self.aimSpeed, self.aimAngle)


        return
    
    def nextBullet(self):
        #in 'main' method where environemnt is run, we can use tank.bullets[self.currentBullet] to get info on the current bullet (to display)
            #quite 'hard-coded' and naive but simple...
        self.currentBullet = self.currentBullet + 1 

        return
    
