import pygame, os

scale = 50
def load_image(image_type, file_path, scale=None):
    image = pygame.image.load(os.path.join(f'Assets/Images/{image_type}', file_path ))
    if scale is not None:
        image = pygame.transform.scale(image, scale)
    
    return image

def rotateImage(image, angle, x, y):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(center=(x, y)).center)

    return rotated_image, new_rect

#--------------------Display Images-------------------------------

#--------------------Base Player Images---------------------------
player_idle = load_image('Player', 'player_idle.png', (scale, scale))
player_up = load_image('Player', 'player_up.png', (scale, scale))
player_down = load_image('Player', 'player_down.png', (scale, scale))
player_right = load_image('Player', 'player_right.png', (scale, scale))
player_left = load_image('Player', 'player_left.png', (scale, scale))

player_images = {"up": player_up, "down": player_down,
                 "right": player_right, "left": player_left,
                 "idle": player_idle}

#----------------------------Player-Sword Images---------------------
player_idle_sword = load_image('Player', 'player_idle_sword.png', (scale, scale))
player_right_sword = load_image('Player', 'player_right_sword.png', (scale, scale))
player_left_sword = load_image('Player', 'player_left_sword.png', (scale, scale))
player_up_sword = load_image('Player', 'player_up_sword.png', (scale, scale))
player_down_sword = load_image('Player', 'player_down_sword.png', (scale, scale))
player_right_cast = load_image('Player', 'player_cast_right.png', (scale, scale))
player_left_cast = load_image('Player', 'player_cast_left.png', (scale, scale))
player_up_cast = load_image('Player', 'player_cast_up.png', (scale, scale))
player_down_cast = load_image('Player', 'player_cast_down.png', (scale, scale))

player_sword_images = {"up": player_up_sword, "down": player_down_sword,
                       "right": player_right_sword, "left": player_left_sword,
                       "idle": player_idle_sword, "up_cast": player_up_cast,
                       "down_cast": player_down_cast, "right_cast": player_right_cast,
                       "left_cast": player_left_cast}


#----------------------------Prop Images-------------------------------
pot = load_image('Props', 'pixel_pot.png', (30, 30))
soul_star = load_image('Props', 'soul_star.png', (30, 30))

prop_images = {"pot": pot, 'soul_star': soul_star}

#---------------------------Projectile Images---------------------------
basic_cast = load_image('Projectiles', 'player_projectile(a).png', (30, 30))
light_cast = load_image('Projectiles', 'projectile_light_cast.png', (15, 15))
energy_ball = load_image('Projectiles', 'player_energy_ball.png', (15, 15))
light_shield = load_image('Projectiles', 'player_light_shield.png', (30, 30))

projectile_images = {"basic_cast": basic_cast, "light_cast": light_cast,
                     "energy_ball": energy_ball, "light_shield": light_shield}

#----------------------------Enemy Images---------------------------------

amalg = load_image('Enemies', 'amalgamation.png', (200,200))
amalg2 = load_image('Enemies', 'amalgamation2.png', (200,200))

enemyImages = {"amalg": amalg, "amalg2": amalg2}

#----------------------------Ambience Images--------------------------------
backgroundIntro = load_image('Ambience', 'lemoraBackgroundTest.png', (scale, scale))
backgroundVoid = load_image('Ambience', 'LemoraVoid.png', (800, 600))
healthBarImage = load_image('Ambience', 'LemoraHealthBarV3.png', )


ambienceImages = {"backgroundIntro": backgroundIntro,
                  "backgroundVoid": backgroundVoid, "healthBar": healthBarImage}