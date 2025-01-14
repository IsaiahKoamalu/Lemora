import pygame, os, sys, math
from pygame.locals import *
from pygame.math import Vector2

class StaticObject():
    def __init__(self, image, position):
        self.image = image
        self.position = position
        self.rect = self.image.get_rect(center=position)
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)

class DynamicObject:
    def __init__(self, image, position, bounce):
        self.image = image
        self.position = pygame.Vector2(position)  # Use Vector2 for easier position manipulation
        self.bounce = bounce
        self.rect = self.image.get_rect(center=position)

    def update(self):
        # Calculate the bounce effect
        t = pygame.time.get_ticks() / 2 % 580
        self.position.y += math.sin(t / 90) * self.bounce
        self.rect.center = (self.position.x, int(self.position.y))  # Update rect to match position

    def draw(self, screen):
        screen.blit(self.image, self.rect)