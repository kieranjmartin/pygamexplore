class graphical_object:
    def __init__(self, xloc, yloc,
                 xsize, ysize):
        self.xloc = xloc
        self.yloc = yloc
        self.xsize = xsize
        self.ysize = ysize
        
    def draw(self, screen):
        import pygame
        pygame.draw.rect(screen, 
                         self.color,
                         pygame.Rect(self.xloc,
                                     self.yloc,
                                     self.xsize,
                                     self.ysize))

class tower(graphical_object):
    range = 10
    power = 1
    health = 1
    color = (0, 128, 255)
    
    def shoot(self, targets):
        import math
        targ_return = []
        for choice in targets:
            if math.sqrt((choice.xloc - self.xloc)**2  + (choice.yloc - self.yloc)**2) <= self.range:
                choice.health = choice.health - self.power
                if choice.health > 0:
                    targ_return.append(choice)
        return targ_return            
    
class attackers(graphical_object):
    velocity = 1
    health = 10
    power = 1
    color = (255, 100, 0) 
    def move(self, targets):
        targ_return = []
        if len(targets) == 0:
            self.yloc = self.yloc + self.velocity
        else:     
            for choice in targets:
                if (choice.xloc <= self.xloc) and ((choice.xloc + choice.xsize) >= self.xloc) and (self.yloc >= choice.yloc) and self.yloc <= (choice.yloc + choice.ysize):
                    choice.health = choice.health - self.power
                else:
                    self.yloc = self.yloc + self.velocity
                if choice.health > 0:
                    targ_return.append(choice)
        return [self, targ_return]

import pygame
import numpy

pygame.init()
xmax = 800
ymax = 600
screen = pygame.display.set_mode((xmax, ymax))
done = False
towers = []
listofattackers = []
clock = pygame.time.Clock()

while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
                if  pygame.mouse.get_pressed()[0]:
                    loc = pygame.mouse.get_pos()
                    towers.append(tower(loc[0], loc[1],
                                  20,20))
                if len(listofattackers) < 10:
                    rand_xloc = numpy.random.randint(xmax)
                    listofattackers.append(attackers(rand_xloc, 0,
                                                     20, 20))
                for shooters in towers:
                    listofattackers = shooters.shoot(listofattackers)
                for army in listofattackers:
                    newvalues = army.move(towers)
                    army = newvalues[0]
                    towers = newvalues[1] 
                screen.fill((0, 0, 0))    
                for instance in towers:
                    instance.draw(screen)
                for instance in listofattackers:
                    instance.draw(screen)
                        
        pygame.display.flip()
        clock.tick(60)    
                    






    
