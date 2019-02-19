import pygame

pygame.init()
xmax = 800
ymax = 600
screen = pygame.display.set_mode((xmax, ymax))
done = False
towers = []
listofattackers = []
clock = pygame.time.Clock()

pygame.display.set_caption('Tutorial 1')
screen.fill(255,255,255) 

while not done:
    pygame.event.pump()
    screen.fill((0,0, 0))    
    keys = pygame.key.get_pressed() 
    
    if (keys[pygame.K_ESCAPE]):
        done = True
        
        
pygame.quit()
        
