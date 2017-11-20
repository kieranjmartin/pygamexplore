import pygame
import os

_image_library = {}
def get_image(path):
        global _image_library
        image = _image_library.get(path)
        if image == None:
                canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
                image = pygame.image.load(canonicalized_path)
                _image_library[path] = image
        return image



pygame.init()
max_x = 800
max_y = 800
screen = pygame.display.set_mode((max_x, max_y))
done = False
clock = pygame.time.Clock()
x = 30
y = 30
mom = 'Still'
snake_length = 10

while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
        
        screen.fill((255, 255, 255))
        
        screen.blit(get_image('images/ball.png'), (20, 20))
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]: mom = 'N'
        if pressed[pygame.K_DOWN]: mom = 'S'
        if pressed[pygame.K_LEFT]: mom = 'W'
        if pressed[pygame.K_RIGHT]: mom = 'E'
        if mom == 'N':
            y -= 3
        if mom == 'S':
            y += 3
        if mom == 'E':
            x += 3
        if mom == 'W':
            x -= 3    
        if pressed[pygame.K_ESCAPE]:
            done = True
        if x <= 0 or x >= max_x or y <= 0 or y >= max_y:
            done = True
        screen.fill((0, 0, 0)) 
        pygame.draw.rect(screen, (255, 100, 0), pygame.Rect(x, y, 20, 20))
        
        pygame.display.flip()
        clock.tick(60)

