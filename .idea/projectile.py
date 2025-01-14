import pygame
import os
from pygame.math import Vector2
from images import projectile_images

class Cast:
    def __init__(self, position, spell, direction):
        self.position = Vector2(position.x + 5, position.y + 15)
        self.image = projectile_images[spell]
        self.rect = self.image.get_rect(center=position)
        self.velocity = Vector2(0,0)
        self.acceleration = Vector2(0,0)
        self.friction = 0.75
        self.direction = direction
        if spell == 'energy_ball':
            self.speed = 1
            self.lifespan = 100
        if spell == 'light_shield':
            self.speed = 0.001
            self.lifespan = 50
    
    def move(self):
        if self.direction == 'right':
            self.velocity.x += self.speed
        if self.direction == 'left':
            self.velocity.x -= self.speed
        if self.direction == 'up':
            self.velocity.y -= self.speed
        if self.direction == 'down':
            self.velocity.y += self.speed
        
    def update(self):
        self.position += self.velocity
        self.rect.center = self.position
        self.lifespan -= 1

    
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def checkCollision(self, object):
        if self.rect.colliderect(object):
            return True
        return False

     