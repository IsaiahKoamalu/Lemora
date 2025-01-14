import pygame, sys, os, random, math, time
from pygame.locals import *
from pygame.math import Vector2
from images import prop_images, ambienceImages
from particle import (SnowParticle, Effect, NonImageParticle,
                      weapon_draw_ptc, create_projectile_ptc,
                      create_explosion_ptc, projectileHitParticle)
from object import StaticObject, DynamicObject
from player import Player
from text import draw_text, BouncingText, intro_text_dict
from projectile import Cast
from audio import sound_effects
from enemyBase import Enemy, EnemySpawner

# Initialize Pygame
pygame.init()
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

#------------------------------------Display Setup-----------------------------------------------------
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_icon(prop_images['pot'])
clock = pygame.time.Clock()
FPS = 60

background = pygame.image.load(os.path.join('Assets', 'Images', 'Ambience', 'lemoraBackgroundTestV1.png'))
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

#------------------------------------Defining Variables and Objects--------------------------------------
player = Player((200, 300), screen)
spawner1 = EnemySpawner((400,400))
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

mainAudio = pygame.mixer.Sound(os.path.join('Assets', 'Audio', 'mainTitle.wav'))

current_text = BouncingText(" ", 12, WHITE)

pot_object = StaticObject(prop_images['pot'], (500, 300))
soul_star_object = DynamicObject(prop_images['soul_star'], (500, 260), 2)

startButton = pygame.Rect(368, 490, 68, 15)
startColor = WHITE


#------------------------------List Initiations--------------------------------------------------------------
particles = []
projectiles = []
proj_ptc = []
explosion_ptcs = []
enemies = []
projectileHitParticles =[]
enemies = spawner1.spawnEnemy(screen, 2)
#--------------------------------Main Menu Loop----------------------------------------------------------------------
def main_menu():
    click = False
    startColor = WHITE
    running = True
    while running:
        mx, my = pygame.mouse.get_pos()
        if startButton.collidepoint(mx, my):
            startColor = RED
            if click:
                running = False
        else:
            startColor = WHITE
        #mainAudio.play()
        screen.fill((0, 0, 0))  # Clear screen with black

        # Add new particles
        if random.random() < 0.2:  # Adjust this to control the particle spawn rate
            particles.append(SnowParticle(WIDTH))

        # Update and draw particles
        for particle in particles[:]:
            particle.update()
            if particle.lifespan <= 0 or particle.y > HEIGHT:
                particles.remove(particle)  # Remove particle when lifetime expires or out of screen
            else:
                particle.draw(screen)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
            if event.type == JOYBUTTONDOWN:
                if event.button == 0:
                    running = False;
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    click = False

        draw_text("L  E  M", WHITE, 55, 275, HEIGHT//2, screen )
        draw_text("  O  ", YELLOW, 55, 425, HEIGHT//2, screen )
        draw_text("  R  A", WHITE, 55, 525, HEIGHT//2, screen )
        #pygame.draw.rect(screen, WHITE, startButton)
        draw_text("Start", startColor, 20, WIDTH//2, 500, screen )
        pygame.display.flip()  # Update the screen
        clock.tick(FPS)  # 60 FPS
        pygame.display.set_caption(f'Main Menu: {int(clock.get_fps())}')

weapon_particles = []
def game():
    spell = "energy_ball"
    sword_equipped = False
    e_pressed = False
    running = True
    text = False
    while running:
#--------------------Updating Particles-------------------------------------------------
        for particle in weapon_particles[:]:
            particle.update()
            if particle.lifespan <= 0:
                weapon_particles.remove(particle)
            else:
                particle.draw(screen)
#---------------------Handling Events--------------------------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == JOYBUTTONDOWN:
                if event.button == 0:
                    if not sword_equipped:
                        sword_equipped = True
                        e_pressed = True
                        weapon_draw_ptc(player.position,weapon_particles, WHITE)
                    else:
                        sword_equipped = False
                if event.button == 5 and sword_equipped == True:
                    projectile_position = player.position + Vector2(player.rect.width // 2, 0)
                    projectiles.append(Cast(projectile_position, spell))



            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_e:
                    if not sword_equipped:
                        sword_equipped = True
                        e_pressed = True
                        weapon_draw_ptc(player.position,weapon_particles, WHITE)
                    else:
                        sword_equipped = False
                # Weapon Events
                if event.key == pygame.K_2:
                    spell = "light_shield"
                if event.key == pygame.K_1:
                    spell = "energy_ball"
                if event.key == pygame.K_RIGHT and sword_equipped:
                    e_pressed = False
                    current_text.text = current_text.font.render(intro_text_dict["sword_used"], True, current_text.color)
                    projectile_position = player.position + Vector2(player.rect.width // 2, 0)
                    projectiles.append(Cast(projectile_position, spell, "right"))
                if event.key == pygame.K_LEFT and sword_equipped and spell == "energy_ball":
                    projectile_position = player.position - Vector2(player.rect.width // 2, 0)
                    projectiles.append(Cast(projectile_position, spell, "left"))
                if event.key == pygame.K_UP and sword_equipped and spell == "energy_ball":
                    projectile_position = player.position + Vector2(10, -20)
                    projectiles.append(Cast(projectile_position, spell, "up"))
                if event.key == pygame.K_DOWN and sword_equipped and spell == "energy_ball":
                    projectile_position = player.position + Vector2(10, 10)
                    projectiles.append(Cast(projectile_position, spell, "down"))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and spell == "light_shield":
            projectile_position = player.position + Vector2(player.rect.width // 2, 0)
            projectiles.append(Cast(projectile_position, spell))

    #---------------------------------Updates------------------------------------------
        player.keyboard_movement(sword_equipped)
        player.update()
        soul_star_object.update()

        if player.rect.colliderect(soul_star_object.rect):
            text = True

        for elm in projectiles:
            elm.move()
            elm.update()
            create_projectile_ptc(elm.position, proj_ptc, spell)
            if elm.lifespan <= 0:
                projectiles.remove(elm)
            if elm.rect.colliderect(soul_star_object.rect):
                projectiles.remove(elm)
                create_explosion_ptc(soul_star_object.position, explosion_ptcs)
                running = False

#------------------Particle Updates----------------------------------------------

        for particle in proj_ptc:
            particle.update()
            if particle.lifespan <= 0:
                proj_ptc.remove(particle)

        for particle in projectileHitParticles:
            particle.update()
            if particle.lifespan <= 0:
                projectileHitParticles.remove(particle)

        for particle in explosion_ptcs:
            particle.update()
            if particle.lifespan <= 0:
                explosion_ptcs.remove(particle)

#-----------------------------Drawing to Screen-------------------------------------
        screen.fill(BLACK)
        screen.blit(background, (0,0))
        if not sword_equipped:
            current_text.text = current_text.font.render(intro_text_dict["equip_sword"], True, current_text.color)
        if e_pressed:
            current_text.text = current_text.font.render(intro_text_dict["use_sword"], True, current_text.color)


        if text:
            current_text.draw(400, 200, 20, screen)

        soul_star_object.draw(screen)#SOULSTAR

        player.draw()#PLAYER

        #Drawing Particles
        for particle in weapon_particles:
            particle.draw(screen)
        for particle in explosion_ptcs:
            particle.draw(screen)
        for particle in proj_ptc:
            particle.draw(screen)
        for particle in projectileHitParticles:
            particle.draw(screen)

        #for elm in projectiles:# PROJECTILES
            #elm.draw(screen)

#--------------------------------Display Updates--------------------------------------------
        pygame.display.flip()
        clock.tick(FPS)
        pygame.display.update()
        pygame.display.set_caption(f'Intro Loop: {int(clock.get_fps())}')
#-------------------------------Stage Test loop-----------------------------------------------
topLeft = []
topRight = []
bottomLeft = []
bottomRight = []
playerDamaged = []

def stageTest():
    wave = 3
    spell = "energy_ball"
    sword_equipped = False
    running = True
    while running:
        # --------------------Updating Particles-------------------------------------------------
        for particle in weapon_particles[:]:
            particle.update()
            if particle.lifespan <= 0:
                weapon_particles.remove(particle)
            else:
                particle.draw(screen)
        # ---------------------Handling Events--------------------------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_e:
                    if not sword_equipped:
                        sword_equipped = True
                        weapon_draw_ptc(player.position, weapon_particles, WHITE)
                    else:
                        sword_equipped = False
                # Weapon Events
                if event.key == pygame.K_2:
                    spell = "light_shield"
                if event.key == pygame.K_1:
                    spell = "energy_ball"
                if event.key == pygame.K_RIGHT and sword_equipped:
                    projectile_position = player.position + Vector2(player.rect.width // 2, 0)
                    projectiles.append(Cast(projectile_position, spell, "right"))
                if event.key == pygame.K_LEFT and sword_equipped and spell == "energy_ball":
                    projectile_position = player.position - Vector2(player.rect.width // 2, 0)
                    projectiles.append(Cast(projectile_position, spell, "left"))
                if event.key == pygame.K_UP and sword_equipped and spell == "energy_ball":
                    projectile_position = player.position + Vector2(10, -20)
                    projectiles.append(Cast(projectile_position, spell, "up"))
                if event.key == pygame.K_DOWN and sword_equipped and spell == "energy_ball":
                    projectile_position = player.position + Vector2(10, 10)
                    projectiles.append(Cast(projectile_position, spell, "down"))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and spell == "light_shield":
            projectile_position = player.position + Vector2(player.rect.width // 2, 0)
            projectiles.append(Cast(projectile_position, spell))

        if random.random() < 0.2:
            bottomRight.append(Effect(700, 750, 600, 'up', WHITE))
            bottomLeft.append(Effect(50, 100, 600, 'up', BLACK ))
            topRight.append(Effect(700, 750, 0, 'down', BLACK))
            topLeft.append(Effect(50, 100, 0, 'down', WHITE))

        for particle in topLeft:
            if particle.lifespan <= 0 or particle.y > HEIGHT:
                topLeft.remove(particle)
        for particle in bottomRight:
            if particle.lifespan <= 0 or particle.y > HEIGHT:
                bottomRight.remove(particle)
        for particle in topRight:
            if particle.lifespan <= 0 or particle.y > HEIGHT:
                topRight.remove(particle)
        for particle in bottomLeft:
            if particle.lifespan <= 0 or particle.y > HEIGHT:
                bottomLeft.remove(particle)

        # ---------------------------------Updates------------------------------------------
        player.keyboard_movement(sword_equipped)
        player.update()
        if not player.checkAlive():
            running = False

        for object in enemies:
            if player.checkCollision(object.rect):
                enemies.remove(object)
                player.affectHealth(25)
                weapon_draw_ptc(player.position, playerDamaged, RED)
                player.applyKnockback(object.position, 10)
            for proj in projectiles:
                if proj.checkCollision(object.rect):
                    sound_effects['soul'].play()
                    object.applyKnockback(proj.position, 5)
                    projectileHitParticle(object.position, projectileHitParticles)
                    object.health -= 50
                    if object.checkHealth():
                        pass
                    else:
                        enemies.remove(object)
                        create_explosion_ptc(object.position, explosion_ptcs)
                    projectiles.remove(proj)
            object.moveToPlayer(player)

        for elm in projectiles:
            elm.move()
            elm.update()
            create_projectile_ptc(elm.position, proj_ptc, spell)
            if elm.lifespan <= 0:
                projectiles.remove(elm)
            if elm.rect.colliderect(soul_star_object.rect):
                projectiles.remove(elm)
                create_explosion_ptc(soul_star_object.position, explosion_ptcs)
        if wave > 0:
            if len(enemies) == 0:
                tempList = spawner1.spawnEnemy(screen, 2)
                wave -= 1

        # ------------------Particle Updates----------------------------------------------

        for particle in playerDamaged:
            particle.update()
            if particle.lifespan <= 0:
                playerDamaged.remove(particle)

        for particle in proj_ptc:
            particle.update()
            if particle.lifespan <= 0:
                proj_ptc.remove(particle)

        for particle in projectileHitParticles:
            particle.update()
            if particle.lifespan <= 0:
                projectileHitParticles.remove(particle)

        for particle in explosion_ptcs:
            particle.update()
            if particle.lifespan <= 0:
                explosion_ptcs.remove(particle)

        for particle in topLeft:
            particle.update()
        for particle in bottomRight:
            particle.update()
        for particle in bottomLeft:
            particle.update()
        for particle in topRight:
            particle.update()

        spawner1.move()

        # -----------------------------Drawing to Screen-------------------------------------
        screen.fill(BLACK)
        screen.blit(ambienceImages['backgroundVoid'], (0,0))
        player.draw()  # PLAYER

        for object in enemies:
            object.draw()

        # Drawing Particles
        for particle in playerDamaged:
            particle.draw(screen)
        for particle in weapon_particles:
            particle.draw(screen)
        for particle in explosion_ptcs:
            particle.draw(screen)
        for particle in proj_ptc:
            particle.draw(screen)
        for particle in projectileHitParticles:
            particle.draw(screen)
        for particle in topLeft:
            particle.draw(screen)
        for particle in bottomRight:
            particle.draw(screen)
        for particle in bottomLeft:
            particle.draw(screen)
        for particle in topRight:
            particle.draw(screen)
        # for elm in projectiles:# PROJECTILES
        # elm.draw(screen)
        player.draw()  # PLAYER


        # --------------------------------Display Updates--------------------------------------------
        pygame.display.flip()
        clock.tick(FPS)
        pygame.display.update()
        pygame.display.set_caption(f'Intro Loop: {int(clock.get_fps())}')

        if int(clock.get_fps()) < 59:
            dip = int(clock.get_fps())
            print(f"Frame Dip: {dip}" )

main_menu()
game()
stageTest()

