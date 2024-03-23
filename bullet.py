#used to store all the different bullet types... idk if this is efficient at all
#definitely need to combine some of these types and just use different values instead of creating more child classes

import pygame, sys
import numpy as np
from scipy.integrate import ode

#create a superclass for the other ones to extend
class Bullet:
    def __init__(self):
        
        self.state = np.array([0.0, 0.0, 0.0, 0.0])   #[0] = x position, [1] = y position, [2] = x velocity, [3] = y velocity 

        self.initialSpeed = 10
        self.initialAngle = 45

        self.mass = 1.0
        self.gravity = -9.8
        self.gamma = 0.1        #coefficient of friction

        self.dt = 0.1           #delta time or change in time
        self.cur_time = 0.0     #current time

        self.pierce = 1     #number of blocks that the projectile can break before it disappears
        
        self.paused = True # starting in paused mode, used for testing

        self.solver = ode(self.f)
        self.solver.set_integrator('dop853')
        self.solver.set_initial_value(self.state, self.cur_time) #not neccessary?
        self.solver.set_f_params(self.gamma, self.gravity)

    def setup(self, x, y, initialSpeed, initialAngle):

        self.state[0] = x
        self.state[1] = y

        self.initialSpeed = initialSpeed
        self.initialAngle = initialAngle

        #split speed into x and y components
        self.state[2] = self.initialSpeed * np.cos(self.initialAngle / 180.0 * np.pi)   #x velocity (convert angle_degrees to radians since np uses radians in calculation)
        self.state[3] = self.initialSpeed * np.sin(self.initialAngle / 180.0 * np.pi)   #y velocity

        self.trace_x = [self.state[0]]
        self.trace_y = [self.state[1]]

    def f(self, t, state, gravity, friction):

        #t: time
        #state: x velocty, y velocity
        #arg1: gravity
        #arg2: coefficient of friction

        xForce = - gravity * state[2] # m*a = -gamma*vx

        yForce = - gravity * state[3] + friction * self.mass   # m*a = -gamma*vy - m*g

        return np.array([state[2], state[3], xForce / self.mass, yForce / self.mass])
    
    #used to update the bullet (get the next 'step') to its next location
    #idk how this will work for the other bullet types... maybe we just don't use rk4 for those xD
    def step(self):

        self.solver.integrate(self.solver.t + self.dt)
        self.state = self.solver.y
        self.cur_time = self.solver.t

        print(self.state)

    #collision response code - just used to break the bullet  
    #collision detection will be in the blocks ? idk how to efficiently detect if a bullet has collided with one of the blocks
    def breakBullet(self): 
        #check number of hits for the bullet, if less than 0, delete bullet 
        #if greater than 0, subtract 1 from it

        return
    
    def printLocation(self):
        print(f"Bullet at ({self.x}, {self.y})")

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

class Shell(Bullet):
    def __init__(self):
        super().__init__()

class Firework(Bullet):
    def __init__(self):
        super().__init__()
        
        self.splits = 3 #number of projectiles that will split off of the main projectile
         
    def setup(self, x, y, initialSpeed, initialAngle, splits):
        super().setup(x, y, initialSpeed, initialAngle)
        self.splits = splits

    def step(self):
        super().step()
        #if firework projectile has been in air for 3(?) seconds (or use distance?), split projectile

class PiercingShell(Bullet):
    def __init__(self):
        super().__init__()
        self.pierce = 3

    def setup(self, x, y, initialSpeed, initialAngle, pierce):
        super().setup(x, y, initialSpeed, initialAngle)
        self.pierce = pierce
    
    def step(self):
        super().step()


class Volley(Bullet):   #shoots a volley of bullets instead of just one 
                        #(should probably just add another variable to Bullet and use Shell with a different 'projectile count')
    def __init__(self):
        super().__init__()
        self.pierce = 3

    def setup(self, x, y, initialSpeed, initialAngle, pierce):
        super().setup(x, y, initialSpeed, initialAngle)
        self.pierce = pierce

class Bomb(Bullet): #creates an 'explosion' 
                    #(simply has bigger collision 'response' where it checks in a radius around it)
    def __init__(self):
        super().__init__()
        self.pierce = 3

    def setup(self, x, y, initialSpeed, initialAngle, pierce):
        super().setup(x, y, initialSpeed, initialAngle)
        self.pierce = pierce

    def step(self):
        super().step()
        #change collision response to 'break' blocks and hit tanks around point of collision

class BouncyBullet(Bullet): #will bounce on contact, has 
    def __init__(self):
        super().__init__()
        self.pierce = 3

    def setup(self, x, y, initialSpeed, initialAngle, pierce):
        super().setup(x, y, initialSpeed, initialAngle)
        self.pierce = pierce
    
    def step(self):
        super().step()
        #need to change behaviour of collision response so that bullet bounces properly

class ReflectingBullet(Bullet): #shoots straight and reflect ('bounce') on contact 
    def __init__(self):
        super().__init__()
        self.pierce = 3

    def setup(self, x, y, initialSpeed, initialAngle, pierce):
        super().setup(x, y, initialSpeed, initialAngle)
        self.pierce = pierce
    
    def step(self):
        super().step()

class Rapid(Bullet): #shoots a bunch of bullets with a bit of randomess for each (maybe too similar to volley)
    def __init__(self):
        super().__init__()
        self.pierce = 3

    def setup(self, x, y, initialSpeed, initialAngle, pierce):
        super().setup(x, y, initialSpeed, initialAngle)
        self.pierce = pierce
    
    def step(self):
        super().step()

class FillingBullet(Bullet): #shoots a normal bullet, but fills the terrain with blocks... maybe too complicated?
    def __init__(self):
        super().__init__()
        self.pierce = 3

    def setup(self, x, y, initialSpeed, initialAngle, pierce):
        super().setup(x, y, initialSpeed, initialAngle)
        self.pierce = pierce
    
    def step(self):
        super().step()