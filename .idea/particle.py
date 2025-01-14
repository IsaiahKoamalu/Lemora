import pygame, random
from pygame.math import Vector2

WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

class SnowParticle:
    def __init__(self, width):
        self.x = random.randint(0, width)
        self.y = 0  # Start at the top of the screen
        self.size = random.randint(1, 5)
        self.speed_y = random.uniform(1, 2)  # Falling speed
        self.lifespan = random.randint(50, 300)  # Random lifetime before disappearing
    
    def update(self):
        self.y += self.speed_y
        self.lifespan -= 1
    
    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.size)


class Effect:
    def __init__(self, xMin, Xmax, y, direction, color):
        self.direction = direction
        self.color = color
        self.x = random.randint(xMin, Xmax)
        self.y = y
        self.size = random.randint(1, 2)
        self.speed_y = random.uniform(1, 2)  # Falling speed
        self.lifespan = random.randint(50, 300)  # Random lifetime before disappearing

    def update(self):
        if self.direction == 'up':
            self.y -= self.speed_y
        if self.direction == 'down':
            self.y += self.speed_y
        self.lifespan -= 1

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
    
class NonImageParticle:
    def __init__(self, position, color, size, lifespan, a1, b1, a2, b2):
        self.position = position
        self.color = color
        self.size = size
        self.lifespan = lifespan
        self.velocity = Vector2(random.uniform(a1, b1), random.uniform(a2, b2))

    def update(self):
        self.position += self.velocity
        self.lifespan -= 1

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.position[0]), (int(self.position[1]))), self.size)



def weapon_draw_ptc(position, list, color):
    for _ in range(10):
        offset = Vector2(random.uniform(-2, 2), random.uniform(-2, 2))
        player_particle = NonImageParticle(position + offset, random.choice([color, YELLOW]),
                                           random.randint(1, 2), random.randint(10, 15), 5, -4, -5, 4)
        list.append(player_particle)

def create_projectile_ptc(position, list, spell):
    if spell == 'energy_ball':
        color = RED
        lifespan = random.randint(10, 15)
        a1, b1, a2, b2 = -1, 2, -1, 1
    else:
        color = YELLOW
        lifespan = random.randint(0, 10)
        a1, b1, a2, b2 = 1.5, 1.5, -2, 2
    for _ in range(1):
        offset = Vector2(random.uniform(-2, 2), random.uniform(-2, 2))
        rocket_particle = NonImageParticle(position + offset, random.choice([WHITE, color]), random.randint(1, 2),
                                           lifespan,a1, b1, a2, b2)
        list.append(rocket_particle)

def projectileHitParticle(position, list):
     lifespan = random.randint(10, 15)
     a1, b1, a2, b2 =  -2, 4, -2, 1
     for _ in range(10):
        offset = Vector2(random.uniform(-2, 2), random.uniform(-2, 2))
        pHitParticle = NonImageParticle(position + offset, random.choice([WHITE, RED]),random.randint(3, 5), lifespan, a1, b1, a2, b2)
        list.append(pHitParticle)

def create_explosion_ptc(position, list):
    for _ in range(100):
        offset = Vector2(random.uniform(-10, 10), random.uniform(-10, 10))
        explosion_particle = NonImageParticle(position + offset, RED, random.randint(1, 4),
                                              random.randint(50, 100),-2, 4, -2, 1)
        list.append(explosion_particle)