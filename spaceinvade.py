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
        
        
class attackers(graphical_object):
    h_velocity = 10
    v_velocity = 4
    health = 1
    left = 1
    color = (255, 100, 0) 
    def move(self, xmax):
        if self.xloc <= 0 or (self.xloc+self.xsize) >= xmax:  
            self.left = abs(self.left-1)
            self.yloc = self.yloc + self.v_velocity
            self.h_velocity = self.h_velocity +1
        if self.left:
            self.xloc = max(self.xloc - self.h_velocity, 0)
        else:
            self.xloc = min(self.xloc + self.h_velocity, xmax)            
        return [self]
        

import pygame

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
        if len(listofattackers) < 5:
            listofattackers.append(attackers(xmax-25, 0,
                                             20, 20))
        for invaders in listofattackers:
            invaders = invaders.move(xmax)
        screen.fill((0, 0, 0))    
        for instance in listofattackers:
            instance.draw(screen)
                        
        pygame.display.flip()
        clock.tick(30)        
