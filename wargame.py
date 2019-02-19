import pygame
import numpy

pygame.init()
xmax = 800
ymax = 600

pygame.display.set_caption('Tutorial 1')
done = False
clock = pygame.time.Clock()

bullet_size = 40
vel_multiplier = 2
ticks = 0 
pygame.mixer.init()
boom_sound = pygame.mixer.Sound("sounds/boom.wav")
rowan_boom  = pygame.mixer.Sound("sounds/rowan_boom.wav") 
shoot = pygame.mixer.Sound("sounds/shoot.wav") 

def rect(ob):
    return pygame.Rect(ob.xloc, ob.yloc, ob.xsize, ob.ysize)


class graphical_object:
    alive = 1
    def __init__(self, xloc, yloc,
                 xsize, ysize):

        
        self.xloc = xloc
        self.yloc = yloc
        self.xsize = xsize
        self.ysize = ysize
        self.rect = rect(self)
        
    def draw(self, screen):
        import pygame
        if self.alive == 1:
            pygame.draw.rect(screen, 
                         self.color,
                         self.rect)
            
class player(graphical_object):
    color = (0, 128, 255)
    direction = (True, -3)
    
    def move(self, x, amount):
        if x:
            new = self.xloc + amount
            if new < xmax and new > 0:
                self.xloc = new
        else:
            new = self.yloc + amount
            if new < ymax and new > 0:
                self.yloc = new
        self.direction = (x, amount)
        self.rect = rect(self)
        
class badguy(graphical_object):
    color =  (255, 0, 0)
    
    def move(self, velocity, facing):
                if facing:
                    new = self.xloc + velocity
                    if new < xmax and new > 0:
                        self.xloc = new
                else:
                    new = self.yloc + velocity
                    if new < ymax and new > 0:
                           self.yloc = new
                self.rect = rect(self)
        

class bullet(graphical_object):
        def __init__(self, player):
            newxloc = player.xloc
            newyloc = player.yloc
            if player.direction[0]:
                  newyloc = newyloc - bullet_size/2 + player.ysize/2
                  if player.direction[1] < 0:
                     newxloc = newxloc - bullet_size
                  else:
                     newxloc = newxloc + player.xsize
            else:
                  newxloc = newxloc - bullet_size/2 + player.xsize/2
                  if player.direction[1] < 0:
                     newyloc = newyloc - bullet_size
                  else:
                     newyloc = newyloc + player.ysize
            
            self.xloc = newxloc
            self.yloc =  newyloc
            self.xsize = bullet_size
            self.ysize = bullet_size
            self.rect = rect(self)
            self.facing = player.direction[0]
            self.velocity = player.direction[1] * vel_multiplier
    
        color = (0, 255, 0)
    
        
        def move(self):
            if self.facing:
                self.xloc = self.xloc + self.velocity
            else:
                self.yloc = self.yloc + self.velocity
            self.rect = rect(self)
                
        def explode(self, targets):
           hits = []
           index = 0 
           for target in targets:
               if self.rect.colliderect(target.rect):
                   hits.append(index)
               index = index + 1
           return hits    
                   
    


player = player(300, 300, 10, 10)

screen = pygame.display.set_mode((xmax, ymax))
screen.fill((255,255,255)) 

player.draw(screen)
pygame.display.flip()

bullets = []
badguys = []
winner = False

while (len(badguys) < 5):
    rand_xloc = numpy.random.randint(xmax)
    rand_yloc = numpy.random.randint(ymax)
    badguys.append(badguy(rand_xloc, rand_yloc, 6, 6))

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = False        
    pressed = pygame.key.get_pressed() 
    
    if pressed[pygame.K_UP]: player.move(False, -3)
    if pressed[pygame.K_DOWN]: player.move(False, 3)
    if pressed[pygame.K_LEFT]: player.move(True, -3)
    if pressed[pygame.K_RIGHT]: player.move(True, 3)
    
    if pressed[pygame.K_SPACE]:
        pygame.mixer.Channel(1).play(shoot)
        bullets.append(bullet(player))
        
    if (ticks % 3600 == 0) and len(badguys) < 5:
        rand_xloc = numpy.random.randint(xmax)
        rand_yloc = numpy.random.randint(ymax)
        badguys.append(badguy(rand_xloc, rand_yloc, 6, 6))
        
    

        
        
    
    screen.fill((255,255,255))
    
    for bad in badguys:
        bad.move(numpy.random.choice([0, -1, 0, 1, 0, 0], 1),
                 numpy.random.choice([True, False], 1)
                                     )
        bad.draw(screen)
        
    for bull in bullets:
        bull.move()
        check = bull.explode(badguys)
        if len(check) > 0:
            if numpy.random.sample(1)> 0.5:
                pygame.mixer.Channel(0).play(boom_sound)
            else: pygame.mixer.Channel(0).play(rowan_boom)
            for rem in check:
                del badguys[rem]
        bull.draw(screen)
    
    player.draw(screen)
    
    if (pressed[pygame.K_ESCAPE]):
        done = True
        
    pygame.display.flip()
    clock.tick(60)
    ticks = ticks + 1
    
    if (len(badguys) == 0):
        done = True
        winner = True

if winner:
    done = False
    while not done:
        for event in pygame.event.get():
           if  event.type == pygame.QUIT:
                done = False        
        pressed = pygame.key.get_pressed()
        if (pressed[pygame.K_ESCAPE]):
            done = True
        screen.fill((0,0,0))
        pygame.font.init()
        myfont = pygame.font.SysFont("Comic Sans MS", 30)
        textsurface = myfont.render('Rowan Wins!', False, (255, 255, 255))
        screen.blit(textsurface,(100,100))
        pygame.display.flip()
        clock.tick(60)
        
        
pygame.quit()
        
