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

    cat_surface = pygame.image.load(os.path.join(os.path.dirname(__file__), "image/pixil-frame-0.png"))
    cat_surface = pygame.transform.scale(cat_surface, (80, 110))
    cat_rect = cat_surface.get_rect(center=(150, -100))
    cat_gravity = 0

    grass_surface = pygame.image.load(os.path.join(os.path.dirname(__file__), "image/grass.png"))
    grass_surface = pygame.transform.scale(grass_surface, (800, 135))
    grass_rect = grass_surface.get_rect(topleft=(0, 340))

    screen = pygame.display.set_mode((800, 450))

    pygame.display.set_caption("pixel cat")
    background_color = (171, 216, 255)

    # intro screen
    first_screen = pygame.image.load(os.path.join(os.path.dirname(__file__), "image/screen.png"))
    first_screen = pygame.transform.scale(first_screen, (1100, 650))
    first_screen_rect = first_screen.get_rect(center=(390, 230))

    game_name = font_100.render("pixel cat", False, (0, 0, 0))
    game_name_rect = game_name.get_rect(center=(410, 70))

    message_text = font_30.render("to  start press    LEFT  SHIFT ", False, (74, 171, 134))
    message_text_rect = message_text.get_rect(center=(400, 405))

    score_text = font_100.render("game over", False, 15)
    score_text_rect = score_text.get_rect(center=(400, 70))

    restart_text = font_30.render("to  start again  press   LEFT  SHIFT", False, (74, 171, 134))
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
                    if event.key == pygame.K_SPACE and cat_rect.bottom >= 340:
                        cat_gravity = -23
            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_LSHIFT:
                    game_active = True
                    score_value = 0
                    flower_rect.left = 800
            if event.type == timer_flowers and game_active:
                obstacle_rect_list.append(flower_surface.get_rect(bottomright=(randint(825, 1000), 340)))

        screen.fill(background_color)
        if game_active:
            display_score(score_value, 0)

            cat_gravity += 1
            cat_rect.y += cat_gravity

            if cat_rect.bottom >= 340:
                cat_rect.bottom = 340

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