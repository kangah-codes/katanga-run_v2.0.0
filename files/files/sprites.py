'''
Sprites script for creating all game objects
'''

import pygame
from animate import Animation
import random
import sys
import math
pygame.init()

__author__ = 'Joshua Akangah'

# creating sprite groups for game entities
player_group = pygame.sprite.Group()
kunai_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
robot_group = pygame.sprite.Group()
fireball_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
barrel_group = pygame.sprite.Group()
mine_group = pygame.sprite.Group()
snake_group = pygame.sprite.Group()
powerup_group = pygame.sprite.Group()

# there shouldnt be a reason for a screen here but in order for animations to be loaded a screen
# object has to beavailable :)
screen = pygame.display.set_mode((800, 500))


class Background:
    def __init__(self):
        self.image = pygame.image.load('../assets/bg1.png')
        self.x = 0
        self.y = 0
        self.speed = 1
        self.rect = self.image.get_rect()

    def draw(self, display):
        display.blit(self.image, (self.x, self.y))

        if self.x < 0:
            new_x = 700 - math.fabs(self.x)
            display.blit(self.image, (new_x, self.y))

    def update(self):
        self.x -= self.speed

        if self.x < -700:
            self.x = 0



class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.states = {
            'run' : player_run,
            'jump' : player_jump,
            'fall' : player_fall,
            'slide' : player_slide,
            'die' : player_die
        }
        self.pos = pygame.math.Vector2()
        self.pos.x, self.pos.y = 100, 200
        self.state = self.states['run']
        self.image = self.state.get_current_image()
        self.rect = self.image.get_rect()
        self.is_jumping = False
        self.is_falling = True
        self.is_dead = False
        self.life = 5
        self.score = 0
        self.acc = 800
        self.vel = 0
        self.is_sliding = False
        self.slide_timer = 0
        self.game_over = False
        self.kunai = 10
        self.font = pygame.font.Font('../assets/airstrike.ttf', 32)
        self.score_render = None

    def update(self, dt, display):
        key = pygame.key.get_pressed()
        self.image = self.state.get_current_image()
        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = self.pos.x, self.pos.y

        self.state.animate(dt)

        self.score_render = self.font.render('Score: {}'.format(self.score), True, (255, 255, 255))

        if self.is_dead:
            self.state = self.states['die']
            if self.state.is_last_image():
                player_die.index = 0
                self.kill()
                self.game_over = True

        if not (self.is_jumping or self.is_falling or self.is_sliding or self.is_dead or self.is_sliding):
            self.state = self.states['run']

        if self.is_sliding:
            self.state = self.states['slide']
            self.slide_timer += dt

            if self.slide_timer >= 5:
                self.is_sliding = False
                self.slide_timer = 0

        if self.is_jumping or self.is_falling:
            self.pos.y += self.vel * (30/1000.0)
            self.vel += self.acc * (30/1000.0)
            if self.vel >= 0 and self.is_sliding:
                self.state = self.states['slide']
            elif self.vel >= 0 and not self.is_sliding:
                self.state = self.states['fall']
            elif self.vel < 0 and self.is_sliding:
                self.state = self.states['slide']
            elif self.vel < 0 and not self.is_sliding:
                self.state = self.states['jump']

        for platform in platform_group:
            if self.rect.bottom < platform.rect.top + 5:
                self.is_falling = True
                self.is_jumping = False

            if self.rect.bottom > platform.rect.top + 5 and not self.is_sliding:
                self.rect.bottom = platform.rect.top + 5
                self.is_falling, self.is_jumping = False, False

            if self.rect.bottom > platform.rect.top + 20 and self.is_sliding:
                self.rect.bottom = platform.rect.top + 20
                self.is_falling, self.is_jumping = False, False

            if key[pygame.K_SPACE] and self.rect.bottom == platform.rect.top + 5 and not (self.is_sliding or self.is_dead):
                self.is_jumping = True
                self.vel = -600

        if self.life <= 0:
            self.is_dead = True

        for enemy in enemy_group:
            if pygame.sprite.collide_mask(self, enemy):
                if enemy.type == 'fireball' and not self.is_falling:
                    self.life -= 1
                    enemy.kill()

                elif enemy.type == 'mine':
                    if enemy.is_exploded:
                        pass
                    else:
                        self.life -= 5
                    enemy.is_exploded = True

                elif enemy.type == 'robot':
                    if self.vel >= 0 and self.is_falling:
                        if self.pos.x + self.rect.width > enemy.pos.x + enemy.rect.width / 2:
                            enemy.is_dead = True
                            self.vel = -300
                            self.score += 1
                    else:
                        if enemy.is_dead:
                            pass
                        else:
                            self.life -= 2
                        enemy.is_dead = True

                elif enemy.type == 'snake':
                    self.life -= 2
                    enemy.kill()

        for powerup in powerup_group:
            if pygame.sprite.collide_mask(self, powerup):
                if powerup.type == 'coin':
                    if powerup.sub_type == 'life':
                        self.life += 1
                        powerup.kill()
                    elif powerup.sub_type == 'silver':
                        self.score += 2
                        powerup.kill()
                    elif powerup.sub_type == 'gold':
                        self.score += 5
                        powerup.kill()

                if powerup.type == 'kunai':
                    self.kunai += 2
                    powerup.kill()

        if self.kunai >= 20:
            self.kunai = 20

        if self.life >= 5:
            self.life = 5

        display.blit(self.score_render, (570, 15))

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, group):
        loaded_image = pygame.image.load('../assets/tile.png')
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(loaded_image, (100, 80))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = 500 - self.rect.height
        self.rect.x, self.rect.y = self.x, self.y
        self.group = group
        self.speed = 5

    def update(self):
        self.rect.x, self.rect.y = self.x, self.y
        self.x -= self.speed

        if len(self.group) < width/self.rect.width + 1:
            self.group.add(Platform(self.group.sprites()[0].x + (self.rect.width * len(self.group)), self.group))

        if self.x + self.rect.width < 0:
            self.kill()

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class Kunai(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.loaded = pygame.image.load('../assets/Kunai.png')
        self.image = pygame.transform.scale(self.loaded, (90, 20))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.speed = 10

    def update(self):
        self.rect.x, self.rect.y = self.x, self.y
        self.x += self.speed

        if self.x > width:
            self.kill()

    def draw(self, screen):
        screen.draw(self.image, (self.x, self.y))

class Mine(pygame.sprite.Sprite):
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.states = {
            'on' : mine_on,
            'explode' : mine_explode
        }
        self.state = self.states['on']
        self.image = self.state.get_current_image()
        self.rect = self.image.get_rect()
        self.pos = pygame.math.Vector2()
        self.pos.x, self.pos.y = x, 500 - self.rect.height - 80
        self.rect.x, self.rect.y = self.pos.x, self.pos.y
        self.is_exploded = False
        self.count = 1
        self.type = 'mine'
        self.speed = 5

    def update(self, dt):
        self.pos.y = 500 - self.rect.height - 80

        self.image = self.state.get_current_image()
        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = self.pos.x, self.pos.y

        self.pos.x -= self.speed

        self.state.animate(dt)

        if not self.is_exploded:
            self.state = self.states['on']

        if self.is_exploded:
            self.state = self.states['explode']
            self.pos.y = 500 - 80 - self.rect.height
            self.rect.y = self.pos.y
            if self.state.is_last_image():
                self.kill()
                mine_explode.index = 0

        if len(mine_group) < 1:
            mine_group.add(Mine(random.randrange(2000, 3500)))

        if self.pos.x + self.rect.width < 0:
            self.kill()

        for mine in mine_group:
            enemy_group.add(mine)

class Robot(pygame.sprite.Sprite):
    def __init__(self, x, group):
        pygame.sprite.Sprite.__init__(self)
        self.states = {
            'go' : robot_go,

            'die' : robot_die
        }
        self.type = 'robot'
        self.state = self.states['go']
        self.image = self.state.get_current_image()
        self.rect = self.image.get_rect()
        self.pos = pygame.math.Vector2()
        self.pos.x, self.pos.y = x, 500 - self.rect.height - 80
        self.rect.x, self.rect.y = self.pos.x, self.pos.y
        self.is_dead = False
        self.speed = 7
        self.life = 2
        self.group = group
        self.start = 0
        self.shoot_timer = 0
        self.count = 4

    def update(self, dt):
        self.pos.x -= self.speed
        self.pos.y = 500 - self.rect.height - 80

        self.image = self.state.get_current_image()
        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = self.pos.x, self.pos.y

        self.state.animate(dt)

        if not self.is_dead:
            self.state = self.states['go']

        if self.is_dead:
            self.state = self.states['die']
            if self.state.is_last_image():
                robot_die.index = 0
                self.kill()

        if self.pos.x + self.rect.width < 0:
            self.kill()

        if self.life <= 0:
            self.is_dead = True

        if self.pos.x < width and not self.is_dead:
            self.shoot_timer += 1

            if self.shoot_timer >= 30:
                self.shoot_timer = 0
                fireball_group.add(Fireball(self.pos.x, self.pos.y + 30))

        if len(self.group) < self.count:
            robot_group.add(Robot(random.randint(1000, 5000), self.group))

        for robot in robot_group:
            enemy_group.add(robot)

        for kunai in kunai_group:
            if pygame.sprite.collide_mask(kunai, self):
                self.life -= 1
                kunai.kill()

class Fireball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self, fireball_group)
        self.states = {
            'burn' : fireball_burn,

            'die' : fireball_die
        }
        self.state = self.states['burn']
        self.image = self.state.get_current_image()
        self.rect = self.image.get_rect()
        self.pos = pygame.math.Vector2()
        self.pos.x, self.pos.y = x, y
        self.rect.x, self.rect.y = self.pos.x, self.pos.y
        self.speed = 10
        self.is_dead = False
        self.type = 'fireball'

    def update(self, dt):
        self.state.animate(dt)

        self.image = self.state.get_current_image()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.pos.x, self.pos.y

        self.pos.x -= self.speed

        if not self.is_dead:
            self.state = self.states['burn']

        if self.is_dead:
            self.state = self.states['die']
            if self.state.is_last_image():
                self.kill()

        if self.pos.x + self.rect.width < 0:
            self.kill()

        for fireball in fireball_group:
            enemy_group.add(fireball)

        for kunai in kunai_group:
            if pygame.sprite.collide_mask(kunai, self):
                kunai.kill()
                self.kill()

class LifeBar:
    def __init__(self):
        self.player = player_group.sprites()[0]
        self.color = (0, 255, 0)

    def update(self, screen):
        if self.player.life > 0:
            pygame.draw.rect(screen, self.color, (20, 20, self.player.life*100, 20))

class KunaiBar:
    def __init__(self):
        self.player = player_group.sprites()[0]
        self.color = (0, 0, 255)

    def update(self, screen):
        if self.player.kunai > 0:
            pygame.draw.rect(screen, self.color, (20, 50, self.player.kunai * 10, 20))

class Barrell(pygame.sprite.Sprite):
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.states = {
            'normal' : barrel_normal,
            'exploded' : barrel_explode
        }
        self.state = self.states['normal']
        self.image = self.state.get_current_image()
        self.rect = self.image.get_rect()
        self.pos = pygame.math.Vector2()
        self.pos.x, self.pos.y = x, 500 - self.rect.height - 80
        self.rect.x, self.rect.y = self.pos.x, self.pos.y
        self.is_exploded = False
        self.speed = 5
        self.count = 1

    def update(self, dt):
        self.pos.y = 500 - self.rect.height - 80
        self.pos.x -= self.speed

        self.image = self.state.get_current_image()
        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = self.pos.x, self.pos.y

        self.state.animate(dt)

        if not self.is_exploded:
            self.state = self.states['normal']

        if self.is_exploded:
            self.state = self.states['exploded']

            robots = [robot for robot in robot_group]

            for robot in robots:
                if robot.pos.x < self.pos.x + self.rect.width + 50:
                    if robot.pos.x > self.pos.x - 50:
                        robot.is_dead = True

            snakes = [snake for snake in snake_group]

            for snake in snakes:
                if snake.pos.x < self.pos.x + self.rect.width + 70:
                    if snake.pos.x > self.pos.x - 70:
                        snake.kill()

            if self.state.is_last_image():
                self.kill()
                barrel_explode.index = 0

        if len(barrel_group) < self.count:
            barrel_group.add(Barrell(random.randrange(2000, 3000)))

        if self.pos.x + self.rect.width < 0:
            self.kill()

        for kunai in kunai_group:
            if pygame.sprite.collide_mask(kunai, self):
                self.is_exploded = True

class Snake(pygame.sprite.Sprite):
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.state = snake_alive
        self.image = self.state.get_current_image()
        self.rect = self.image.get_rect()
        self.pos = pygame.math.Vector2()
        self.pos.x, self.pos.y = x, 500 - self.rect.height - 80
        self.rect.x, self.rect.y = self.pos.x, self.pos.y
        self.speed = 5
        self.life = 2
        self.type = 'snake'

    def update(self, dt):
        self.state.animate(dt)
        self.image = self.state.get_current_image()
        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = self.pos.x, self.pos.y

        self.pos.x -= self.speed

        if self.life <= 0:
            self.kill()
            player_group.sprites()[0].score += 5

        if self.pos.x + self.rect.width < 0:
            self.kill()

        if len(snake_group) < 1:
            snake_group.add(Snake(random.randint(2000, 6000)))

        for snake in snake_group:
            enemy_group.add(snake)

        for kunai in kunai_group:
            if pygame.sprite.collide_mask(kunai, self):
                self.life -= 1
                kunai.kill()

class Coin(pygame.sprite.Sprite):
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.states = {
            'bronze' : coin_bronze,
            'silver' : coin_silver,
            'gold' : coin_gold
        }
        self.random_choice = random.randrange(1, 3)
        if self.random_choice == 1:
            self.state = self.states['bronze']
            self.sub_type = 'life'
        elif self.random_choice == 2:
            self.state = self.states['silver']
            self.sub_type = 'silver'
        else:
            self.state = self.states['gold']
            self.sub_type = 'gold'
        self.image = self.state.get_current_image()
        self.rect = self.image.get_rect()
        self.pos = pygame.math.Vector2()
        self.pos.x, self.pos.y = x, 500 - 80 - self.rect.height
        self.rect.x, self.rect.y = self.pos.x, self.pos.y
        self.speed = 5
        self.type = 'coin'

    def update(self, dt):
        self.state.animate(dt)

        self.pos.x -= self.speed

        self.image = self.state.get_current_image()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.pos.x, self.pos.y

        pow = [powerup for powerup in powerup_group if powerup.type == 'coin']

        if len(pow) < 2:
            powerup_group.add(Coin(random.randint(3000, 5000)))

        if self.pos.x + self.rect.width < 0:
            self.kill()

class Kunai_Powerup(pygame.sprite.Sprite):
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.image_loaded = pygame.image.load('../assets/Kunai.png')
        self.scaled = pygame.transform.scale(self.image_loaded, (100, 30))
        self.image = pygame.transform.rotate(self.scaled, 90)
        self.rect = self.image.get_rect()
        self.pos = pygame.math.Vector2()
        self.pos.x, self.pos.y = x, 500 - 80 - self.rect.height
        self.speed = 5
        self.type = 'kunai'

    def update(self, dt):
        self.pos.x -= self.speed

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.pos.x, self.pos.y

        if self.pos.x + self.rect.width < 0:
            self.kill()

        pow = [sprites for sprites in powerup_group if sprites.type == 'kunai']

        if len(pow) < 1:
            powerup_group.add(Kunai_Powerup(random.randint(2000, 4000)))

width = 800

# loading all game animations once to prevent fps drops when creating new instances of any animated class

robot_go = Animation([
                    '../assets/enemies/robot/go/go_1.png',
                    '../assets/enemies/robot/go/go_2.png',
                    '../assets/enemies/robot/go/go_3.png',
                    '../assets/enemies/robot/go/go_4.png',
                    '../assets/enemies/robot/go/go_5.png',
                ], 0.4, frame_duration=0.4)

robot_die = Animation([
                    '../assets/enemies/robot/die/die_1.png',
                    '../assets/enemies/robot/die/die_2.png',
                    '../assets/enemies/robot/die/die_3.png',
                    '../assets/enemies/robot/die/die_4.png',
                    '../assets/enemies/robot/die/die_5.png',
                    '../assets/enemies/robot/die/die_6.png',
                    '../assets/enemies/robot/die/die_7.png',
                    '../assets/enemies/robot/die/die_8.png',
                    '../assets/enemies/robot/die/die_9.png',
                ], 0.4, frame_duration=0.5)

fireball_burn = Animation(
                [
                    '../assets/enemies/fireball/burn/fire.png',
                    '../assets/enemies/fireball/burn/fire2.png',
                    '../assets/enemies/fireball/burn/fire3.png',
                    '../assets/enemies/fireball/burn/fire4.png',
                    '../assets/enemies/fireball/burn/fire5.png',
                ], 0.5
            )

fireball_die = Animation(
                [
                    '../assets/enemies/fireball/die/fire6.png',
                    '../assets/enemies/fireball/die/fire7.png',
                    '../assets/enemies/fireball/die/fireball_die_3.png',
                    '../assets/enemies/fireball/die/fireball_die_4.png',
                    '../assets/enemies/fireball/die/fireball_die_5.png',
                    '../assets/enemies/fireball/die/fireball_die_6.png',
                ], 0.5, frame_duration=0.5
            )

barrel_normal = Animation(['../assets/enemies/Barrel (1).png'], 0.4)

barrel_explode = Animation([
                '../assets/enemies/mine_explode/explosion_1.png',
                '../assets/enemies/mine_explode/explosion_2.png',
                '../assets/enemies/mine_explode/explosion_3.png',
                '../assets/enemies/mine_explode/explosion_4.png',
                '../assets/enemies/mine_explode/explosion_5.png',
                '../assets/enemies/mine_explode/explosion_6.png',
                '../assets/enemies/mine_explode/explosion_7.png',
            ], 0.6, frame_duration=0.5)

mine_on = Animation([
                    '../assets/enemies/mine/mine_1.png',
                    '../assets/enemies/mine/mine_2.png',
                ], 0.5, frame_duration=0.5)

mine_explode = Animation([
                    '../assets/enemies/mine_explode/explosion_1.png',
                    '../assets/enemies/mine_explode/explosion_2.png',
                    '../assets/enemies/mine_explode/explosion_3.png',
                    '../assets/enemies/mine_explode/explosion_4.png',
                    '../assets/enemies/mine_explode/explosion_5.png',
                    '../assets/enemies/mine_explode/explosion_6.png',
                    '../assets/enemies/mine_explode/explosion_7.png',
                ], 0.5, frame_duration=0.5)

snake_alive = Animation([
            '../assets/enemies/snake/idle_1.png',
            '../assets/enemies/snake/idle_2.png',
            '../assets/enemies/snake/idle_3.png',
            '../assets/enemies/snake/idle_4.png',
            '../assets/enemies/snake/idle_5.png',
            '../assets/enemies/snake/idle_6.png',
    ], 0.5, frame_duration=0.4)

coin_bronze = Animation([
    '../assets/items/bronze/Bronze_11.png',
    '../assets/items/bronze/Bronze_12.png',
    '../assets/items/bronze/Bronze_13.png',
    '../assets/items/bronze/Bronze_14.png',
    '../assets/items/bronze/Bronze_15.png',
    '../assets/items/bronze/Bronze_16.png',
    '../assets/items/bronze/Bronze_17.png',
    '../assets/items/bronze/Bronze_18.png',
    '../assets/items/bronze/Bronze_19.png',
    '../assets/items/bronze/Bronze_20.png',
], 0.1, frame_duration=0.3)

coin_gold = Animation([
    '../assets/items/gold/Gold_1.png',
    '../assets/items/gold/Gold_2.png',
    '../assets/items/gold/Gold_3.png',
    '../assets/items/gold/Gold_4.png',
    '../assets/items/gold/Gold_5.png',
    '../assets/items/gold/Gold_6.png',
    '../assets/items/gold/Gold_7.png',
    '../assets/items/gold/Gold_8.png',
    '../assets/items/gold/Gold_9.png',
    '../assets/items/gold/Gold_10.png',
], 0.1, frame_duration=0.3)

coin_silver = Animation([
    '../assets/items/silver/Silver_0.png',
    '../assets/items/silver/Silver_1.png',
    '../assets/items/silver/Silver_2.png',
    '../assets/items/silver/Silver_3.png',
    '../assets/items/silver/Silver_4.png',
    '../assets/items/silver/Silver_5.png',
    '../assets/items/silver/Silver_6.png',
    '../assets/items/silver/Silver_7.png',
    '../assets/items/silver/Silver_8.png',
    '../assets/items/silver/Silver_9.png',
], 0.1, frame_duration=0.3)

player_run = Animation([
                    '../assets/player/run/Run__000.png',
                    '../assets/player/run/Run__001.png',
                    '../assets/player/run/Run__002.png',
                    '../assets/player/run/Run__003.png',
                    '../assets/player/run/Run__004.png',
                    '../assets/player/run/Run__005.png',
                    '../assets/player/run/Run__006.png',
                    '../assets/player/run/Run__007.png',
                    '../assets/player/run/Run__008.png',
                    '../assets/player/run/Run__009.png',
                ], 0.4, frame_duration = 0.15)

player_jump = Animation([
                    '../assets/player/jump/Jump__002.png',
                    '../assets/player/jump/Jump__003.png',
                    '../assets/player/jump/Jump__004.png',
                    '../assets/player/jump/Jump__005.png'
                ], 0.4)

player_fall = Animation([
                    '../assets/player/jump/Jump__006.png',
                    '../assets/player/jump/Jump__007.png',
                    '../assets/player/jump/Jump__008.png',
                    '../assets/player/jump/Jump__009.png',
                ], 0.4, frame_duration=0.5)

player_slide = Animation([
                    '../assets/player/slide/Slide__000.png',
                    '../assets/player/slide/Slide__001.png',
                    '../assets/player/slide/Slide__002.png',
                    '../assets/player/slide/Slide__003.png',
                    '../assets/player/slide/Slide__004.png',
                    '../assets/player/slide/Slide__005.png',
                    '../assets/player/slide/Slide__006.png',
                    '../assets/player/slide/Slide__007.png',
                    '../assets/player/slide/Slide__008.png',
                    '../assets/player/slide/Slide__009.png',
                ], 0.4, frame_duration=0.3)

player_die = Animation([
                    '../assets/player/die/Dead__000.png',
                    '../assets/player/die/Dead__001.png',
                    '../assets/player/die/Dead__002.png',
                    '../assets/player/die/Dead__003.png',
                    '../assets/player/die/Dead__004.png',
                    '../assets/player/die/Dead__005.png',
                    '../assets/player/die/Dead__006.png',
                    '../assets/player/die/Dead__007.png',
                    '../assets/player/die/Dead__008.png',
                    '../assets/player/die/Dead__009.png',
                ], 0.4, frame_duration=0.3)
