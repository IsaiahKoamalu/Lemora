import pygame, math, random, os
from pygame.locals import *
from pygame.math import Vector2
from images import enemyImages
from particle import NonImageParticle

class Enemy:
    def __init__(self, position, screen, speed):
        self.position = Vector2(position)
        self.screen = screen
        self.health = 100
        self.image = pygame.image.load(os.path.join('Assets/Images/Enemies', 'amalgamation2.png'))
        #self.image = enemyImages["amalg2"]
        self.image = pygame.transform.scale(self.image, (50,50))
        self.rect = self.image.get_rect(center=position)
        self.velocity = Vector2(0,0)
        self.speed = speed
        self.friction = 0.91
        self.isKnockedBack = False
        self.knockBackVelocity = Vector2(0,0)
        self.trailingParticles = []


    def moveToPlayer(self, player):
        if self.isKnockedBack:
            self.position += self.knockBackVelocity
            self.rect.center = self.position
            self.knockBackVelocity *= 0.9

            if self.knockBackVelocity.length() < 0.1:
                self.knockBackVelocity = Vector2(0,0)
                self.isKnockedBack = False
        else:
            #self.bounce = 1
           #self.t = pygame.time.get_ticks() / 2 % 580
            #self.position.y = self.position.y - math.fabs(math.cos(self.t / 90)* self.bounce)
            self.position.y = int(self.position.y)
            self.direction = (player.position - self.position).normalize()
            self.position += self.direction * self.speed
            self.rect.center = self.position

    def applyKnockback(self, projPos, intensity):
        self.knockBackVelocity = (self.position - projPos).normalize() * intensity
        self.isKnockedBack = True

    def checkHealth(self):
        if self.health > 0:
            return True
        return False

    def createTrailingParticle(self, position, list):
        self.lifespan = random.randint(5, 10)
        for _ in range(1):
            offset = Vector2(random.uniform(-2, 2), random.uniform(-2, 2))
            trailingParticle = NonImageParticle(position + offset, (255,0,0), 1, self.lifespan, -1, 2, -2, 1)
            list.append(trailingParticle)

    def draw(self):
        self.createTrailingParticle(self.position, self.trailingParticles)
        for particle in self.trailingParticles:
            particle.update()
            particle.draw(self.screen)
            if particle.lifespan <= 0:
                self.trailingParticles.remove(particle)
        self.screen.blit(self.image, self.rect)
        
class EnemySpawner:
    def __init__(self, position):
        self.position = Vector2(position)
        self.enemies = []
        self.moveRight = True
        self.rect = pygame.Rect(self.position.x, self.position.y, 50, 50)
    
    def spawnEnemy(self, screen, amount):
        for i in range(amount):
            #tempPosition = Vector2(900, random.randint(0, 600))
            tempPosition = self.position
            enemy = Enemy(tempPosition, screen, random.randint(1, 2))
            self.enemies.append(enemy)
        return self.enemies

    def move(self):
        if self.moveRight:
            self.position.x += 1
            if self.position.x > 600:
                self.moveRight = False

        if not self.moveRight:
            self.position.x -= 1
            if self.position.x < 10:
                self.moveRight = True