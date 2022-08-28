import pygame
import os
from sys import exit
from random import randint

def animation():
    global player_index, player_surface

    if player_rect.bottom < 340:
        player_surface = player_jump
    else:
        player_index += 0.1
        if player_index >= 2: player_index = 0
        player_surface = player_walk[int(player_index)]


def obstacle(obstacle_list, score):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5 + score / 2
            if obstacle_rect.x + 49 < 0:
                score += 1
            screen.blit(flower_surface, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -50]
        return obstacle_list, score
    else:
        return [], score


def collisions(man, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if man.colliderect(obstacle_rect):
                return False
    return True


def display_score(score_value, num_function):
    if num_function == 1:
        score = font_70.render("score is  " + str(score_value), False, "paleturquoise")
        score_rect = score.get_rect(center=(400, 375))
        screen.blit(score, score_rect)
    else:
        score = font_70.render("score " + str(score_value), True, (74, 171, 134))
        screen.blit(score, (270, 50))


if __name__ == '__main__':
    pygame.init()

    clock = pygame.time.Clock()
    game_active = False

    #font = pygame.font.Font(os.path.join(os.path.dirname(__file__), "font/ddd.otf"), 70)
    font_30 = pygame.font.Font(os.path.join(os.path.dirname(__file__), "font/pizza.TTF"), 30)
    font_70 = pygame.font.Font(os.path.join(os.path.dirname(__file__), "font/pizza.TTF"), 70)
    font_100 = pygame.font.Font(os.path.join(os.path.dirname(__file__), "font/pizza.TTF"), 100)

    flower_surface = pygame.image.load(os.path.join(os.path.dirname(__file__), "image/flower.png"))
    flower_surface = pygame.transform.scale(flower_surface, (60, 70))
    flower_rect = flower_surface.get_rect(bottomright=(400, 250))

    obstacle_rect_list = []

    intro_cat = pygame.image.load(os.path.join(os.path.dirname(__file__), "image/cat_walk1.png"))
    intro_cat = pygame.transform.scale(intro_cat, (100, 150))
    intro_cat_rect = intro_cat.get_rect(center=(280, 230))
    intro_caterpillar = pygame.image.load(os.path.join(os.path.dirname(__file__), "image/caterpillar_walk1.png"))
    intro_caterpillar = pygame.transform.scale(intro_caterpillar, (130, 70))
    intro_caterpillar_rect = intro_caterpillar.get_rect(center=(480, 240))

    player_walk1 = pygame.image.load(os.path.join(os.path.dirname(__file__), "image/caterpillar_walk1.png"))
    player_walk1 = pygame.transform.scale(player_walk1, (80, 110))
    player_walk2 = pygame.image.load(os.path.join(os.path.dirname(__file__), "image/caterpillar_walk2.png"))
    player_walk2 = pygame.transform.scale(player_walk2, (80, 110))
    player_jump = pygame.image.load(os.path.join(os.path.dirname(__file__), "image/caterpillar_jump.png"))
    player_jump = pygame.transform.scale(player_jump, (80, 110))
    player_rect = player_walk1.get_rect(center=(150, -100))
    player_gravity = 0
    player_index = 0
    player_walk = [player_walk1, player_walk2]
    player_surface = player_walk[player_index]

    grass_surface = pygame.image.load(os.path.join(os.path.dirname(__file__), "image/grass.png"))
    grass_surface = pygame.transform.scale(grass_surface, (800, 135))
    grass_rect = grass_surface.get_rect(topleft=(0, 340))

    screen = pygame.display.set_mode((800, 450))

    pygame.display.set_caption("pixel game")
    background_color = (171, 216, 255)

    # intro screen
    first_screen = pygame.image.load(os.path.join(os.path.dirname(__file__), "image/screen.png"))
    first_screen = pygame.transform.scale(first_screen, (800, 440))
    first_screen_rect = first_screen.get_rect(center=(400, 230))

    game_name = font_100.render("pixe l game", False, (0, 0, 0))
    game_name_rect = game_name.get_rect(center=(410, 70))

    message_text = font_30.render("to   start  playing   select   player", False, (98, 169, 199))
    message_text_rect = message_text.get_rect(center=(400, 125))

    cat_text = font_30.render("press F", False, (0, 0, 0))
    cat_text_rect = cat_text.get_rect(center=(285, 325))

    caterpillar_text = font_30.render("press A", False, (0, 0, 0))
    caterpillar_text_rect = caterpillar_text.get_rect(center=(480, 325))

    score_text = font_100.render("game over", False, 15)
    score_text_rect = score_text.get_rect(center=(400, 70))

    restart_text = font_30.render("to  start again  press   LEFT  SHIFT", False, (0, 0, 0))
    restart_text_rect = restart_text.get_rect(center=(400, 420))

    timer_flowers = pygame.USEREVENT + 1
    pygame.time.set_timer(timer_flowers, 1050)

    score_value = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if game_active:
                # if event.type == pygame.MOUSEMOTION:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and player_rect.bottom >= 340:
                        player_gravity = -23
            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_LSHIFT:
                    game_active = True
                    score_value = 0
                    flower_rect.left = 800
            if event.type == timer_flowers and game_active:
                obstacle_rect_list.append(flower_surface.get_rect(bottomright=(randint(900, 1000), 340)))

        screen.fill(background_color)
        if game_active:
            display_score(score_value, 0)

            player_gravity += 1
            player_rect.y += player_gravity

            if player_rect.bottom >= 340:
                player_rect.bottom = 340

            screen.blit(flower_surface, flower_rect)
            animation()
            screen.blit(player_surface, player_rect)
            screen.blit(grass_surface, grass_rect)

            obstacle_rect_list, score_value = obstacle(obstacle_rect_list, score_value)

            game_active = collisions(player_rect, obstacle_rect_list)
        else:
            obstacle_rect_list.clear()

            if score_value == 0:
                screen.blit(first_screen, first_screen_rect)
                screen.blit(intro_cat, intro_cat_rect)
                screen.blit(intro_caterpillar, intro_caterpillar_rect)
                screen.blit(cat_text, cat_text_rect)
                screen.blit(caterpillar_text, caterpillar_text_rect)

                screen.blit(game_name, game_name_rect)
                screen.blit(message_text, message_text_rect)
            else:
                screen.blit(first_screen, first_screen_rect)
                display_score(score_value, 1)
                screen.blit(score_text, score_text_rect)
                screen.blit(restart_text, restart_text_rect)

        pygame.display.update()
        clock.tick(60)