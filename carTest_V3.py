#!venv\Scripts\python.exe
# -*- coding: utf-8 -*-

import pygame
from math import radians, cos, sin

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    KEYUP,
    QUIT,
)

SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 800

BLACK = (0,0,0)
WHITE = (255,255,255)
GREY = (100,100,100)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        #Load the car sprite and set a original car sprite
        self.image_original = pygame.image.load('car3.png').convert() # We keap a original sprite for rotation
        self.image_original.set_colorkey((255,255,255), RLEACCEL)     # Beacuse if we rotate the same sprite to many times it looks lite poo
        
        #Make a copy of the car and a rect object
        self.image = self.image_original            
        self.rect = self.image.get_rect(center = (500, 400))
        
        self.angle = 0
        self.drift_angle = 0
        self.drif_speed = 7
        self.turn_speed = 5

        
        self.speed = 0
        self.start_speed = 0
        self.acceleration = 0.1
        self.top_speed = 10
        self.top_revers_speed = -8
        
        
    def update(self, keys):
        #input controle
        
        #Turning
        if keys[K_LEFT] and (self.speed > 1 or self.speed < -1):
            self.turn_car('left')
        if keys[K_RIGHT] and (self.speed > 1 or self.speed < -1):
            self.turn_car('right')
        
        #Accelerate and brake
        if keys[K_UP]:
            self.speed_control('up')
        if keys[K_DOWN]:
            self.speed_control('down')
        
        #If no keys to accelerate the car are pressed slow the car down
        if not keys[K_UP] and not keys[K_DOWN]:
            self.slow_car_down()
        
        self.move_car()
        
        self.border_control()
        
    def turn_car(self, direction):
        if direction == 'left':
            if self.speed < 0:
                self.angle -= self.turn_speed
            else:
                self.angle += self.turn_speed 
            if self.angle < -360 or self.angle > 360:
                self.angle = 0
            self.image = pygame.transform.rotate(self.image_original, self.angle)
            self.rect = self.image.get_rect(center = (self.rect.center))
        if direction == 'right':
            if self.speed < 0:
                self.angle += self.turn_speed
            else:
                self.angle -= self.turn_speed 
            if self.angle < -360 or self.angle > 360:
                self.angle = 0
            self.image = pygame.transform.rotate(self.image_original, self.angle)
            self.rect = self.image.get_rect(center = (self.rect.center))
            
    
    def drift(self):
        if self.speed > 7:
            pass
    
    #Move the car back or forwads depending on the speed
    def move_car(self):
        if self.speed > 0.1 or self.speed < -0.1:
            rad = radians(self.angle)
            self.direction = pygame.Vector2(sin(rad), cos(rad))
            print(self.direction * self.speed)
            self.rect.center -= self.direction * self.speed


    #Slow the car down to a speed of 0
    def slow_car_down(self):
        if self.speed > 0:
            self.speed -= self.acceleration
            if self.speed < 0.3: # Fale safe to get the car to actualy stop moving
                self.speed = 0
        elif self.speed < 0:
            self.speed += self.acceleration
            if self.speed > -0.3:
                self.speed = 0
    
    
    # if the car is moving under the top speeds accelerate it forwads or backwards
    def speed_control(self, direction):
        if direction == 'up':
            if self.speed < self.top_speed:
                self.speed += self.acceleration
        if direction == 'down':
            if self.speed > self.top_revers_speed:
                self.speed -= self.acceleration * 2
            
        
    # Make it so you cant drive out side of the screen
    def border_control(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


class Obs (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        self.surf = pygame.Surface((100,150))
        self.surf.fill((100,100,100))
        
        self.rect = self.surf.get_rect(
            center =(
                300, 
                500,
            )
        )
        
        


#Game loop
#...................................................................................
def main():
    running = True
    while running:

        #Checking for events to close the game 
        for event in pygame.event.get():
            print(event)
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
        
            elif event.type == QUIT:
                running = False
    
        #Get all the pressed keys 
        keys = pygame.key.get_pressed()
        #Send the pressed keys to the player update function 
        player.update(keys)
    
    
        screen.fill(BLACK)
    
        #Draw all sprites to the screen
        screen.blit(ob.surf, ob.rect)
        
        for entity in all_sprites:
            screen.blit(entity.image, entity.rect)
        
        pygame.display.flip()
        clock.tick(60)
    
    
#Start game 
#...............................................................................
if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    player = Player()
    ob = Obs()

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)




    clock = pygame.time.Clock()

    main()
    
    
    
    