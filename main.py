import pygame
import os
from sys import exit
from random import randint


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
        score = test_font.render("score is  " + str(score_value), False, "paleturquoise")
        score_rect = score.get_rect(center=(250, 245))
        screen.blit(score, score_rect)
    else:
        score = font.render("score: " + str(score_value), True, (74, 171, 134))
        screen.blit(score, (160, 50))


if __name__ == '__main__':
    pygame.init()

    clock = pygame.time.Clock()
    game_active = False

    font = pygame.font.Font(os.path.join(os.path.dirname(__file__), "font/ddd.otf"), 50)
    test_font = pygame.font.Font(os.path.join(os.path.dirname(__file__), "font/pizza.TTF"), 30)
    test2_font = pygame.font.Font(os.path.join(os.path.dirname(__file__), "font/pizza.TTF"), 20)

    flower_surface = pygame.image.load(os.path.join(os.path.dirname(__file__), "image/flower.png"))
    flower_surface = pygame.transform.rotozoom(flower_surface, 0, 1.5)
    flower_rect = flower_surface.get_rect(bottomright=(400, 250))

    obstacle_rect_list = []

    cat_surface = pygame.image.load(os.path.join(os.path.dirname(__file__), "image/pixil-frame-0.png"))
    cat_rect = cat_surface.get_rect(topleft=(70, 200))
    cat_gravity = 0

    grass_surface = pygame.image.load(os.path.join(os.path.dirname(__file__), "image/grass.png"))
    grass_rect = grass_surface.get_rect(topleft=(0, 250))

    screen = pygame.display.set_mode((500, 300))

    pygame.display.set_caption("pixel cat")
    background_color = "paleturquoise"

    # intro screen
    first_screen = pygame.image.load(os.path.join(os.path.dirname(__file__), "image/screen.png"))
    first_screen = pygame.transform.scale2x(first_screen)
    first_screen_rect = first_screen.get_rect(topleft=(-110, -50))

    game_name = font.render("pixel cat", False, (0, 0, 0))
    game_name_rect = game_name.get_rect(center=(250, 50))

    message_text = test_font.render("to  start press   LSHIFT ", False, (74, 171, 134))
    message_text_rect = message_text.get_rect(center=(250, 265))

    score_text = font.render("game over", False, 15)
    score_text_rect = score_text.get_rect(center=(250, 50))

    restart_text = test2_font.render("to  start again  press  LSHIFT", False, (74, 171, 134))
    restart_text_rect = restart_text.get_rect(center=(250, 275))

    timer_flowers = pygame.USEREVENT + 1
    pygame.time.set_timer(timer_flowers, 1000)

    score_value = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if game_active:
                # if event.type == pygame.MOUSEMOTION:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and cat_rect.bottom >= 250:
                        cat_gravity = -20
            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_LSHIFT:
                    game_active = True
                    score_value = 0
                    flower_rect.left = 500
            if event.type == timer_flowers and game_active:
                obstacle_rect_list.append(flower_surface.get_rect(bottomright=(randint(625, 800), 250)))

        screen.fill(background_color)
        if game_active:
            display_score(score_value, 0)

            cat_gravity += 1
            cat_rect.y += cat_gravity

            if cat_rect.bottom >= 250:
                cat_rect.bottom = 250

            screen.blit(flower_surface, flower_rect)
            screen.blit(cat_surface, cat_rect)
            screen.blit(grass_surface, grass_rect)

            obstacle_rect_list, score_value = obstacle(obstacle_rect_list, score_value)

            game_active = collisions(cat_rect, obstacle_rect_list)
        else:
            screen.blit(first_screen, first_screen_rect)
            obstacle_rect_list.clear()

            if score_value == 0:
                screen.blit(game_name, game_name_rect)
                screen.blit(message_text, message_text_rect)
            else:
                display_score(score_value, 1)
                screen.blit(score_text, score_text_rect)
                screen.blit(restart_text, restart_text_rect)

        pygame.display.update()
        clock.tick(60)