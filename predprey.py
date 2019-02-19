# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 08:02:27 2019

@author: martik32
"""
import pygame
import math
import numpy

pygame.init()
xmax = 300
ymax = xmax
square_size = 10
screen = pygame.display.set_mode((xmax, ymax))
done = False
clock = pygame.time.Clock()
grass_col = (0, 255, 0)
herb_col = (0, 0, 255)
pred_col = (255, 0, 0)
back_color = (255, 255, 255)

class grass:
    def __init__(self, alive):
        self.alive = alive
        self.color = grass_col
        self.name = "grass"
        self.breedvalue = 0.90
        self.deathval = 0.05
        
    def grow(self, neighbours):
        
        if not self.alive:
            grass_count = 1
            for n in neighbours:
                n = n.life[self.name]
                if n.alive:
                    grass_count = grass_count + 1
            if (numpy.random.random_sample(1) > self.breedvalue * grass_count ):
               self.alive = True
               
    def die(self, neighbours):
        if self.alive:
             grass_count = 0
             for n in neighbours:
                n = n.life[self.name]
                if n.alive:
                    grass_count = grass_count + 1
             if (numpy.random.random_sample(1) < self.deathval * grass_count ):
                 self.alive = False
    
class herb:
    def __init__(self, alive):
        self.alive = alive
        self.color = herb_col
        self.name = "herb"
        self.starve = 0
        self.death = 4
        self.moved = False
        self.breedval = 0.6
        self.fightval = 0.1
    
    def grow(self, neighbours):
        self.alive = self.alive
    
    def move(self, square, neighbours):  
        if self.alive and not self.moved:
          if not square.life["grass"].alive:
            candidates_grass = []
            candidates_none = []
            for i in range(len(neighbours)):
                grass = neighbours[i].life["grass"]
                herb = neighbours[i].life["herb"]
                pred = neighbours[i].life["pred"]
                if grass.alive and not herb.alive and not pred.alive:
                    candidates_grass.append(i) 
                if not herb.alive and not pred.alive :
                    candidates_none.append(i) 
            if len(candidates_grass) >0:
                ind = int(numpy.random.choice(candidates_grass, 1))
                self.alive = False
                neighbours[ind].life[self.name].alive = True
                neighbours[ind].life[self.name].moved = True
            elif len(candidates_none) >0:
                ind = int(numpy.random.choice(candidates_none, 1))
                self.alive = False
                neighbours[ind].life[self.name].alive = True
                neighbours[ind].life[self.name].moved = True
            
                    

   
    def reset(self):
        self.moved = False
        
    def eat (self, square, neighbours):
        if self.alive and square.life["grass"].alive:
            square.life["grass"].alive = False
            self.starve = 0
        elif self.alive:
            self.starve = self.starve + 1
            
    def breed (self, neighbours):
        if self.alive:
            empty = []
            partner = False
            for i in range(len(neighbours)):
                if neighbours[i].life["herb"].alive == True & neighbours[i].life["herb"].starve <=2:
                    partner = True
                else:
                    empty.append(i)
            if partner and len(empty) > 0 and numpy.random.sample(1)< self.breedval and self.starve <=2:
                ind = int(numpy.random.choice(empty, 1))
                neighbours[ind].life["herb"].alive = True
                neighbours[ind].life["herb"].starve = 1
           
    def die(self, neighbours):
        if self.alive and self.starve >=  self.death:
             self.alive = False

class predator(herb):
    def __init__(self, alive):
        self.alive = alive
        self.color = pred_col
        self.name = "pred"
        self.starve = 0
        self.death = 2
        self.moved = False
        self.breedval = 0.4
        self.fightval = 0.6
        
        
    def move(self, square, neighbours):  
        if self.alive and not self.moved:
            candidates_none = []
            for i in range(len(neighbours)):
                herb = neighbours[i].life["herb"]
                pred = neighbours[i].life["pred"]
                if not herb.alive and not pred.alive :
                    candidates_none.append(i) 
            if len(candidates_none) >0:
                ind = int(numpy.random.choice(candidates_none, 1))
                self.alive = False
                neighbours[ind].life[self.name].alive = True
                neighbours[ind].life[self.name].moved = True    
    
    def fight(self, enemy):
        (self.fightval + numpy.random.sample(1)) > (enemy.fightval + numpy.random.sample(1) )
    
    def eat (self, square, neighbours):
        if self.alive:
            candidates = []
            for i in range(len(neighbours)):
                herb = neighbours[i].life["herb"]
                if  herb.alive:
                    candidates.append(i) 
            if len(candidates) >0:
                ind = int(numpy.random.choice(candidates, 1))
                if self.fight(neighbours[ind].life["herb"]):
                    neighbours[ind].life["herb"].alive = False
                    self.starve = 0
                else: 
                    self.starve = self.starve + 1 
            else:
                self.starve = self.starve + 1

class square:
    def __init__(self, xloc, yloc, size, grassalive, herbalive, predalive, xco, yco, rsq):
        self.rect = pygame.Rect(xloc, yloc, size, size)
        self.life = { "grass": grass(grassalive),
                     "herb" : herb(herbalive),
                     "pred": predator(predalive)}
        self.xco = xco
        self.yco = yco
        
        self.neighbours = []
        for i in range(-1, 2):
            for j in range (-1, 2):
                if (i != 0) or (j != 0):
                    xn = self.xco + i
                    yn = self.yco + j
                    if (xn>=0 and xn <= rsq and yn>=0 and yn <= rsq):
                        self.neighbours.append(int(xn + yn * rsq))

                
    def colorin(self):
        self.color = back_color
        keys = sorted(self.life)
        for key in keys:
            if self.life[key].alive:
                self.color = self.life[key].color
        


        
    def draw(self, screen):
        self.colorin()
        pygame.draw.rect(screen, 
                         self.color,
                         self.rect)

                    
    


class grid:
    def __init__(self, xmax, ymax, square_size):
        self.nsquares_row = int(xmax/square_size)
        self.nsquares = int(xmax* self.nsquares_row )
        self.nsquares_row = self.nsquares/xmax
        self.squares = []
        for i in range(self.nsquares):
            xval = ((i - 1) %  self.nsquares_row) * square_size
            yval = math.floor(i/self.nsquares_row) * square_size
            xco = int(((i - 1) %  self.nsquares_row))
            yco = int(math.floor(i/self.nsquares_row))
            herb = False
            pred = False
            if numpy.random.random_sample(1) < 0.15:
                herb = True
            if numpy.random.random_sample(1) < 0.2 and not herb:
                pred = True
            self.squares.append(
                    square(xval, yval, square_size, True, herb, pred,
                           xco, yco, self.nsquares_row)
                    )

        
    def draw(self, screen):
        for square in self.squares:
            square.draw(screen)
    
    def move(self):
        for square in self.squares:
            for life in square.life.values():
                if life.name != "grass":
                    life.move(square, [self.squares[i] for i in square.neighbours])
        for square in self.squares:
            for life in square.life.values():
                if life.name != "grass":
                    life.reset()           
    def eat(self):
        for square in self.squares:
            for life in square.life.values():
                if life.name != "grass":
                    life.eat(square, [self.squares[i] for i in square.neighbours])
     
    def breed(self):
        for square in self.squares:
            for life in square.life.values():
                if life.name != "grass":
                    life.breed([self.squares[i] for i in square.neighbours])    
        
    def die_grow(self, growT):
        gsave = self.squares
        for square in self.squares:
            for life in square.life.values():
                if growT:
                    life.grow([gsave[i] for i in square.neighbours])
                elif not growT and life.name != "grass":
                    life.die([gsave[i] for i in square.neighbours])
            
            
        

plot_grid = grid(xmax, ymax, square_size)

while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
        pressed = pygame.key.get_pressed()                
        if pressed[pygame.K_ESCAPE]:
            done = True           
            
        screen.fill(back_color)
        plot_grid.move()
        plot_grid.eat()
        plot_grid.die_grow(True)
        plot_grid.breed()
        plot_grid.die_grow(False)
        plot_grid.draw(screen)
        
        
        pygame.display.flip()
        clock.tick(1)    
        
pygame.quit()
