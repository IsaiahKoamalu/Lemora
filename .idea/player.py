import pygame
from pygame.locals import *
from pygame.math import Vector2
from images import (player_images, player_sword_images, ambienceImages)



class Player:
    def __init__(self, position, screen):
        self.position = Vector2(position)
        self.screen = screen
        self.current_image = player_images["idle"]
        self.rect = self.current_image.get_rect(center=position)
        self.velocity = Vector2(0,0)
        self.speed = 3
        self.friction = 0.91
        self.player_state = "idle"
        self.health = 100
        self.healthBarRect = pygame.Rect(25, 30, self.health, 30)
        self.healthBackRect = pygame.Rect(25, 30, self.health, 30)
        self.healthBarImage = ambienceImages["healthBar"]
        self.isKnockedBack = False
        self.knockBackVelocity = Vector2(0,0)
        
    def move(self, direction):
        if direction == 'right':
            self.velocity.x = self.speed
        elif direction == 'left':
            self.velocity.x = -self.speed
        elif direction == 'up':
            self.velocity.y = -self.speed
        elif direction == 'down':
            self.velocity.y = self.speed

    def applyKnockback(self, projPos, intensity):
        self.knockBackVelocity = (self.position - projPos).normalize() * intensity
        self.isKnockedBack = True
    
    def update(self):
        if self.isKnockedBack:
            self.position += self.knockBackVelocity
            self.rect.center = self.position
            self.knockBackVelocity *= 0.9

            if self.knockBackVelocity.length() < 0.1:
                self.knockBackVelocity = Vector2(0, 0)
                self.isKnockedBack = False
        self.position += self.velocity
        self.velocity *= self.friction
        self.rect.center = self.position
        
        self.position.x = max(0, min(self.position.x, self.screen.get_width()))
        self.position.y = max(0, min(self.position.y, self.screen.get_height()))
    
    def keyboard_movement(self, sword_equipped):
        if not sword_equipped:
            image_group = player_images
        if sword_equipped:
            image_group = player_sword_images
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.move('left')
            self.current_image = image_group["left"]
        elif keys[pygame.K_d]:
            self.move('right')
            self.current_image = image_group["right"]
        elif keys[pygame.K_w]:
            self.move('up')
            self.current_image = image_group["up"]
        elif keys[pygame.K_s]:
            self.move("down")
            self.current_image = image_group["down"]
        elif keys[pygame.K_RIGHT] and sword_equipped:
            self.current_image = image_group["right_cast"]
        elif keys[pygame.K_LEFT] and sword_equipped:
            self.current_image = image_group["left_cast"]
        elif keys[pygame.K_UP] and sword_equipped:
            self.current_image = image_group["up_cast"]
        elif keys[pygame.K_DOWN] and sword_equipped:
            self.current_image = image_group["down_cast"]
        else:
            self.current_image = image_group["idle"]
    
    def draw(self):
        pygame.draw.rect(self.screen, (255, 0, 0), self.healthBackRect)
        pygame.draw.rect(self.screen, (0, 150, 0), self.healthBarRect)
        self.screen.blit(self.healthBarImage, (21, 25))
        self.screen.blit(self.current_image, self.rect)

    def affectHealth(self, amount):
        self.health -= amount
        self.healthBarRect.width = self.health


    def checkCollision(self, object):
        if self.rect.colliderect(object):
            return True
        return False

    def interact(self, action, object):
        if action == 'pickup':
            pass

    def checkAlive(self):
        if self.health <= 0:
            return False
        else:
            return True