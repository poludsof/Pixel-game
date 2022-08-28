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
        score_rect = score.get_rect(center=(400, 385))
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
    flower_surface = pygame.transform.scale(flower_surface, (50, 70))
    flower_rect = flower_surface.get_rect(bottomright=(400, 250))

    obstacle_rect_list = []

    caterpillar_surface = pygame.image.load(os.path.join(os.path.dirname(__file__), "image/caterpillar.png"))
    caterpillar_surface = pygame.transform.scale(caterpillar_surface, (130, 35))
    caterpillar_rect = caterpillar_surface.get_rect(center=(150, -100))
    caterpillar_gravity = 0

    #caterpillar_move = pygame.image.load(os.path.join(os.path.dirname(__file__), "image/caterpillar_moves.png"))
    #caterpillar_move = pygame.transform.scale(caterpillar_move, (130, 50))
    #caterpillar_move_rect = caterpillar_surface.get_rect(center=(150, 310))
    #player_index = 0

    grass_surface = pygame.image.load(os.path.join(os.path.dirname(__file__), "image/grass.png"))
    grass_surface = pygame.transform.scale(grass_surface, (800, 135))
    grass_rect = grass_surface.get_rect(topleft=(0, 340))

    screen = pygame.display.set_mode((800, 450))

    pygame.display.set_caption("pixel caterpillar")
    background_color = (171, 216, 255)

    # intro screen
    first_screen = pygame.image.load(os.path.join(os.path.dirname(__file__), "image/screen.png"))
    first_screen = pygame.transform.scale(first_screen, (800, 455))
    first_screen_rect = first_screen.get_rect(center=(400, 225))

    game_name = font_70.render("pixel caterpillar", False, (0, 0, 0))
    game_name_rect = game_name.get_rect(center=(410, 70))

    message_text = font_30.render("to  start press    LEFT  SHIFT ", False, (0, 0, 0))
    message_text_rect = message_text.get_rect(center=(400, 405))

    score_text = font_70.render("game over", False, 15)
    score_text_rect = score_text.get_rect(center=(400, 70))

    final_screen = pygame.image.load(os.path.join(os.path.dirname(__file__), "image/final.png"))
    final_screen = pygame.transform.scale(final_screen, (800, 455))
    final_screen_rect = first_screen.get_rect(center=(400, 225))
    restart_text = font_30.render("to  start again  press   LEFT  SHIFT", False, (0, 0, 0))
    restart_text_rect = restart_text.get_rect(center=(400, 425))

    timer_flowers = pygame.USEREVENT + 1
    pygame.time.set_timer(timer_flowers, 1100)

    score_value = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if game_active:
                # if event.type == pygame.MOUSEMOTION:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and caterpillar_rect.bottom >= 340:
                        caterpillar_gravity = -25
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

            caterpillar_gravity += 1
            caterpillar_rect.y += caterpillar_gravity

            if caterpillar_rect.bottom >= 340:
                caterpillar_rect.bottom = 340

            screen.blit(flower_surface, flower_rect)
            screen.blit(caterpillar_surface, caterpillar_rect)
            screen.blit(grass_surface, grass_rect)

            obstacle_rect_list, score_value = obstacle(obstacle_rect_list, score_value)

            game_active = collisions(caterpillar_rect, obstacle_rect_list)
        else:
            obstacle_rect_list.clear()

            if score_value == 0:
                screen.blit(first_screen, first_screen_rect)
                screen.blit(game_name, game_name_rect)
                screen.blit(message_text, message_text_rect)
            else:
                screen.blit(final_screen, final_screen_rect)
                display_score(score_value, 1)
                screen.blit(score_text, score_text_rect)
                screen.blit(restart_text, restart_text_rect)

        pygame.display.update()
        clock.tick(60)