import pygame
import os
pygame.init()

soul_sound = pygame.mixer.Sound(os.path.join('Assets', 'Audio', 'soul_star.wav'))

sound_effects = {"soul": soul_sound}