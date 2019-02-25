'''
KATANGA RUN V 2.0

This version is an *update* to the first version of the game I made back in 2016

This is a very simple side scroller game with enemies and some other cool stuff :)

Feel free to change the code as you like!

'''

import pygame
import sys
from animate import Animation
import random
import database
from sprites import *
pygame.init()

__author__ = 'Joshua Akangah'

# Global game variables
clock = pygame.time.Clock()
screen = pygame.display.set_mode((800, 500))
pygame.display.set_caption('Katanga Run')
pygame.display.set_icon(pygame.image.load('../assets/tile.png'))
fps = 60

# creating a database instance
db = database.Database()

# Loading player animations for the main menu
player_idle = Animation([
        '../assets/player/idle/Idle__000.png',
        '../assets/player/idle/Idle__001.png',
        '../assets/player/idle/Idle__002.png',
        '../assets/player/idle/Idle__003.png',
        '../assets/player/idle/Idle__004.png',
        '../assets/player/idle/Idle__005.png',
        '../assets/player/idle/Idle__006.png',
        '../assets/player/idle/Idle__007.png',
        '../assets/player/idle/Idle__008.png',
        '../assets/player/idle/Idle__009.png',
    ], 0.4, frame_duration=0.5)

# loading platform image
platform = pygame.image.load('../assets/tile.png')
platform_image = pygame.transform.scale(platform, (100, 80))

# Font packages
main_font = pygame.font.Font('../assets/iomanoid back.ttf', 100)
smaller_font = pygame.font.Font('../assets/iomanoid front.ttf', 50)
smallest_font = pygame.font.Font('../assets/iomanoid front.ttf', 30)

font = pygame.font.Font('../assets/iomanoid back.ttf', 70)
font1 = pygame.font.Font('../assets/iomanoid front.ttf', 50)
font2 = pygame.font.Font('../assets/iomanoid front.ttf', 30)

# rendering texts
game_name = main_font.render('Katanga Run', True, (255, 255, 255))
start = smaller_font.render('S to Start', True, (255, 255, 255))
about = smaller_font.render('A for About', True, (255, 255, 255))
quit = smaller_font.render('Q to Quit', True, (255, 255, 255))

show_menu_items = True

# checking if there is already a table in the database, otherwise we would create a new table
try:
    if db.get_length('SCORES') > 0:
        pass
except:
    db.create_table('SCORES')


# game menu
def main_menu():
    # if there is no score in the table the default score value will be set to zero
    # else the highest score in the database would be displayed
    if not db.get_length('SCORES'):
        high_score = smallest_font.render('Highscore: {}'.format(0), True, (255, 255, 255))
    else:
        high_score = smallest_font.render('Highscore: {}'.format(db.max('SCORES')), True, (255, 255, 255))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    game()
                elif event.key == pygame.K_a:
                    about_game()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        screen.fill((0, 0, 0))

        # animating the player graphic in the main menu
        player_idle.animate(100)

        # Drawing surfaces to screen
        screen.blit(player_idle.get_current_image(), (100, 420 - player_idle.get_rect().height))
        screen.blit(platform_image, (0, 420))
        screen.blit(platform_image, (100, 420))
        screen.blit(platform_image, (200, 420))
        screen.blit(platform_image, (300, 420))
        screen.blit(platform_image, (400, 420))
        screen.blit(platform_image, (500, 420))
        screen.blit(platform_image, (600, 420))
        screen.blit(platform_image, (700, 420))

        if show_menu_items:
            screen.blit(game_name, (400 - game_name.get_width() / 2, 20))
            screen.blit(start, (400 - start.get_width() / 2, 250))
            screen.blit(about, (400 - about.get_width() / 2, 300))
            screen.blit(quit, (400 - quit.get_width() / 2, 350))
            screen.blit(high_score, (400 - high_score.get_width() / 2, 170))

        # setting the frames per second at a very low rate to avoid overusage of system resources
        clock.tick(10)

        pygame.display.flip()


# about page of the game
def about_game():
    show_menu_items = False

    escape = font1.render("Press ESCAPE to return", 1, (255, 255, 255))
    katanga = font.render('Katanga Run V 2.0 (2019)', True, (255, 255, 255))
    jump = font2.render('Press SPACE for jump', 1, (255, 255, 255))
    throw = font2.render('Press H to throw', 1, (255, 255, 255))
    slide = font2.render('Press S to slide', 1, (255, 255, 255))
    name = font1.render('Joshua Akangah', 1, (255, 255, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()

        player_idle.animate(100)
        screen.fill((0, 0, 0))

        screen.blit(player_idle.get_current_image(), (100, 420 - player_idle.get_rect().height))
        screen.blit(platform_image, (0, 420))
        screen.blit(platform_image, (100, 420))
        screen.blit(platform_image, (200, 420))
        screen.blit(platform_image, (300, 420))
        screen.blit(platform_image, (400, 420))
        screen.blit(platform_image, (500, 420))
        screen.blit(platform_image, (600, 420))
        screen.blit(platform_image, (700, 420))

        screen.blit(katanga, (400 - katanga.get_width() / 2, 10))
        screen.blit(escape, (400 - escape.get_width() / 2, 500 - escape.get_height()))
        screen.blit(jump, (400 - jump.get_width() / 2, 500 - escape.get_height()*5.5))
        screen.blit(throw, (400- throw.get_width() / 2, 500 - escape.get_height()*4.5))
        screen.blit(slide, (400 - slide.get_width() / 2, 500 - escape.get_height()*3.5))
        screen.blit(name, (400 - name.get_width() / 2, 500 - escape.get_height()*2 - 10))

        clock.tick(10)

        pygame.display.flip()


# game pause state
def pause():
    text = main_font.render('Paused', True, (255, 255, 255))
    continue_game = smallest_font.render('Press escape to continue', True, (255, 255, 255))

    paused = True

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False

        screen.blit(text, (400 - text.get_width() / 2, 100))
        screen.blit(continue_game, (400 - continue_game.get_width() / 2, 300))

        clock.tick(10)
        pygame.display.flip()


# game over state
def game_over(score):
    over = main_font.render('GAME OVER', True, (255, 0, 0))
    score = smaller_font.render('Your score: {}'.format(score), True, (255, 0, 0))
    retry = smaller_font.render('R to Retry', True, (255, 255, 255))
    quit = smaller_font.render('Q to Quit', True, (255, 255, 255))
    home = smaller_font.render('H to go to main', True, (255, 255, 255))
    done = True

    while done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    done = False
                    game()
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_h:
                    main_menu()

        screen.fill((0, 0, 0))

        screen.blit(over, (400 - over.get_width() / 2, 100))
        screen.blit(score, (400 - score.get_width() / 2, 250))
        screen.blit(retry, (400 - retry.get_width() / 2, 330))
        screen.blit(quit, (400 - quit.get_width() / 2, 380))
        screen.blit(home, (400 - home.get_width() / 2, 430))

        clock.tick(10)
        pygame.display.flip()

def game():
    player = Player()

    player_group.add(player)

    platform_group.add(Platform(0, platform_group))

    # adding enemies
    robot_group.add(Robot(random.randrange(2000, 3000), robot_group))

    life = LifeBar()

    barrel_group.add(Barrell(1000))

    powerup_group.add(Coin(random.randrange(1500, 3000)), Kunai_Powerup(random.randrange(1300, 2500)))

    snake_group.add(Snake(random.randrange(3000, 4500)))

    mine_group.add(Mine(random.randrange(2000, 4000)))

    kunai_bar = KunaiBar()

    background = Background()

    over = False

    while not over:
        dt = fps * 0.001

        if len(player_group) != 0:
            player = player_group.sprites()[0]

        # creating a temporary variable for player score so that when the player object is *killed*
        # we can still reference its score during the game
        temp_score = player.score

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    # allow shooting only if the players kunais are more than zero
                    if player.kunai > 0:
                        kunai_group.add(Kunai(player.pos.x + player.rect.width // 2, player.pos.y + 70))
                        player.kunai -= 1

                if event.key == pygame.K_s:
                    player.is_sliding = True

                if event.key == pygame.K_ESCAPE:
                    pause()

        if player.game_over == True:
            # setting the player score to zero after death
            player.score = 0
            if len(player_group) == 0:
                pygame.time.wait(500)
                # emptying all sprite groups to prevent them appearing abckwhen game is loaded
                robot_group.empty()
                mine_group.empty()
                snake_group.empty()
                barrel_group.empty()
                powerup_group.empty()
                platform_group.empty()
                fireball_group.empty()

                # if there is no score in the table, insert this score into it
                # else if the current score is higher than the highest score in the Database
                # we will replace that score
                if db.get_length('SCORES') == 0:
                        print(db.insert(temp_score, 'SCORES'))
                else:
                    if temp_score > db.max('SCORES'):
                        print(db.update_data('SCORES', temp_score, 1))

                # calling the game_over function
                game_over(temp_score)

        # drawing everything to the screens

        screen.fill((0, 0, 0))
        player_group.draw(screen)
        robot_group.draw(screen)
        platform_group.draw(screen)
        fireball_group.draw(screen)
        snake_group.draw(screen)
        mine_group.draw(screen)
        powerup_group.draw(screen)
        kunai_group.draw(screen)
        barrel_group.draw(screen)

        life.update(screen)
        kunai_bar.update(screen)
        player_group.update(dt, screen)
        robot_group.update(dt)
        platform_group.update()
        fireball_group.update(dt)
        snake_group.update(dt)
        mine_group.update(dt)
        powerup_group.update(dt)
        kunai_group.update()
        barrel_group.update(dt)

        clock.tick(fps)
        pygame.display.flip()

if __name__ == '__main__':
    main_menu()
