import pygame, os, sys, math
from pygame.locals import *

class Text():
    def __init__(self, text, size, color):
       self.color = color
       self.font = pygame.font.Font('Avilock_Bold.ttf', size)
       self.text = self.font.render(text, True, color)
    
    def draw(self, x, y):
       self.x = x
       self.y = y
       self.text_rect = self.text.get_rect(center=(self.x, self.y))
       screen.blit(self.text, self.text_rect)

class TempText():
    def __init__(self, text, size, color, duration):
        self.color = color
        self.font = pygame.font.Font('Avilock_Bold.ttf', size)
        self.text = self.font.render(text, True, color)
        self.duration = duration
        self.tick_var = 0

    def draw(self, x, y):
        self.x = x
        self.y = y
        self.tick_var += 1
        self.text_rect = self.text.get_rect(center=(self.x, self.y))

        if self.tick_var < self.duration:
            screen.blit(self.text, self.text_rect)



# Text bouncing effect logic
class BouncingText():
   def __init__(self, text, size, color):
       self.color = color
       self.font = pygame.font.Font('fontTest.ttf', size)
       self.text = self.font.render(text, True, color)


   def draw(self, x, y, bounce, screen):
       self.t = pygame.time.get_ticks() / 2 % 580
       self.x = x
       self.y = y - math.fabs(math.cos(self.t / 90)* bounce)
       self.y = int(self.y)
       self.text_rect = self.text.get_rect(center=(self.x, self.y))
       screen.blit(self.text, self.text_rect)

def draw_text(text, color, size, x, y, screen):
    font = pygame.font.Font('fontTest.ttf', size)
    textobj = font.render(text, True, color)
    text_rect = textobj.get_rect(center=(x,y))
    screen.blit(textobj, text_rect)


intro_text_dict = {"equip_sword": "It seems to be empty . . . try Xylaris ?[E].",
             "use_sword": "Fire a soul spark at the star.[right arrow]",
             "sword_used": "Do you hear that?"}