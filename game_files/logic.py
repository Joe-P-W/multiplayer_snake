import pygame
import sys
import time
import random
import json

from game_files.game_entities import Snake, Apple
from pygame_objects.boxes import InputBox, ButtonBox


def check_events(snake):
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if snake.direction != "right":
                    snake.direction = "left"
                    break
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if snake.direction != "left":
                    snake.direction = "right"
                    break
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if snake.direction != "up":
                    snake.direction = "down"
                    break
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                if snake.direction != "down":
                    snake.direction = "up"
                    break


def slow_time(snake_head, direction, squares):
    if snake_head[0] == 0 and direction == "left":
        time.sleep(0.2)
    elif snake_head[1] == 0 and direction == "up":
        time.sleep(0.2)
    elif snake_head[0] == squares - 1 and direction == "right":
        time.sleep(0.2)
    elif snake_head[1] == squares - 1 and direction == "down":
        time.sleep(0.2)
    else:
        time.sleep(0.15)


def main_loop(screen, resolution, squares, font):
    start_pos = [(squares / 2, squares / 2), (squares / 2, (squares / 2) + 1), (squares / 2, (squares / 2) + 2)]
    snake = Snake(start_pos, "up")
    score = 0

    apple_start = (random.randint(0, squares - 1), random.randint(0, squares - 1))
    while apple_start in start_pos:
        apple_start = (random.randint(0, squares - 1), random.randint(0, squares - 1))

    apple = Apple(apple_start)

    while True:

        slow_time(snake.segments[0], snake.direction, squares)
        check_events(snake)
        snake.move_snake(apple.pos)
        score = apple.check_if_eaten(snake.segments[0], score, snake.segments, squares)
        out_of_bounds = snake.check_out_of_bounds(squares)

        screen.fill((0, 0, 0))

        if not out_of_bounds:

            apple_pos = ((apple.pos[0] / squares) * resolution[0], (apple.pos[1] / squares) * resolution[0],
                         resolution[0] / squares, resolution[1] / squares)

            pygame.draw.rect(screen, (255, 0, 0), apple_pos)

            for segment in snake.segments:
                pos = ((segment[0] / squares) * resolution[0], (segment[1] / squares) * resolution[0],
                       resolution[0] / squares, resolution[1] / squares)

                pygame.draw.rect(screen, (255, 255, 255), pos)

            text = font.render(f'Score: {score}', False, (255, 0, 255))
            screen.blit(text, (resolution[0] - 150, 10))

        else:
            game_over(screen, squares, resolution, font, score)

        pygame.display.flip()


def game_over(screen, squares, resolution, font, score):
    with open("game_files/high_scores.json", "r") as in_file:
        high_scores = json.load(in_file)

    high_scores.sort(reverse=True)
    if score > high_scores[-1]:
        high_scores.append(score)
        high_scores.sort(reverse=True)
        if len(high_scores) > 5:
            high_scores.pop()

        with open("game_files/high_scores.json", "w") as out_file:
            json.dump(high_scores, out_file)

    for i in range(500):
        text = font.render("Game Over", False, (0, 255, 0))
        score_text = font.render(f"Your score: {score}", False, (0, 255, 0))
        high_score = font.render(f"High score: {high_scores[0]}", False, (0, 255, 0))
        textRect = text.get_rect()
        scoreRect = score_text.get_rect()
        highRect = score_text.get_rect()
        textRect.center = (resolution[0] // 2, resolution[1] // 2)
        scoreRect.center = (resolution[0] // 2, (resolution[1] // 2) + 50)
        highRect.center = (resolution[0] // 2, (resolution[1] // 2) + 100)
        screen.blit(text, textRect)
        screen.blit(score_text, scoreRect)
        screen.blit(high_score, highRect)
        pygame.display.flip()
        time.sleep(0.01)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()

        if i == 499:
            main_menu(screen, squares, resolution, font)


def main_menu(screen, squares, resolution, font):
    play_button = (resolution[0] / 2 - 75, resolution[1] - 550, 150, 50)
    play_button_rect = pygame.Rect(play_button)
    high_scores = (resolution[0] / 2 - 75, resolution[1] - 400, 150, 50)
    high_scores_button_rect = pygame.Rect(high_scores)
    multiplayer_button = (resolution[0] / 2 - 75, resolution[1] - 250, 150, 50)
    multiplayer_button_rect = pygame.Rect(multiplayer_button)
    quit_button = (resolution[0] / 2 - 75, resolution[1] - 100, 150, 50)
    quit_button_button_rect = pygame.Rect(quit_button)
    while True:
        time.sleep(0.1)
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (255, 100, 0), play_button)
        pygame.draw.rect(screen, (255, 100, 0), high_scores)
        pygame.draw.rect(screen, (255, 100, 0), multiplayer_button)
        pygame.draw.rect(screen, (255, 100, 0), quit_button)
        play_text = font.render("Play", False, (0, 255, 0))
        score_text = font.render("High Scores", False, (0, 255, 0))
        multiplayer_text = font.render("Multiplayer", False, (0, 255, 0))
        quit_text = font.render("Quit", False, (0, 255, 0))
        playRect = play_text.get_rect()
        scoreRect = score_text.get_rect()
        multiplayerRect = multiplayer_text.get_rect()
        quitRect = quit_text.get_rect()
        playRect.center = (resolution[0] / 2, resolution[1] - 525)
        scoreRect.center = (resolution[0] / 2, resolution[1] - 375)
        multiplayerRect.center = (resolution[0] / 2, resolution[1] - 225)
        quitRect.center = (resolution[0] / 2, resolution[1] - 75)
        screen.blit(play_text, playRect)
        screen.blit(score_text, scoreRect)
        screen.blit(multiplayer_text, multiplayerRect)
        screen.blit(quit_text, quitRect)
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:

                    if quit_button_button_rect.collidepoint(event.pos):
                        sys.exit()
                    elif play_button_rect.collidepoint(event.pos):
                        main_loop(screen, resolution, squares, font)
                    elif multiplayer_button_rect.collidepoint(event.pos):
                        multiplayer_menu(screen, squares, resolution, font)
                    elif high_scores_button_rect.collidepoint(event.pos):
                        high_score_menu(screen, squares, resolution, font)

        pygame.display.flip()


def multiplayer_game(screen, squares, resolution, font, ip_address, port):
    print("foo")
    print(ip_address)
    print(port)


def multiplayer_menu(screen, squares, resolution, font):
    clock = pygame.time.Clock()
    title = font.render("Input IP & Port of Server you wish to connect to.", False, (0, 255, 0))
    ip_address_box = InputBox(50, 200, 100, 50, font, "IP Address")
    port_input_box = InputBox(50, 350, 100, 50, font, "Port")
    main_menu_button = ButtonBox(
        450, 550, 150, 50, "Main Menu", font,
        (255, 100, 0), (0, 255, 0), main_menu, args=(screen, squares, resolution, font)
    )
    enter_button = ButtonBox(
        300, 300, 150, 50, "Enter", font, (255, 100, 0), (0, 255, 0),
        multiplayer_game, args=(screen, squares, resolution, font, ip_address_box.value, port_input_box.value)
    )
    boxes = (ip_address_box, port_input_box, main_menu_button, enter_button)
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            for box in boxes:
                box.handle_event(event)

        for box in [ip_address_box, port_input_box]:
            box.update()

        screen.fill((0, 0, 0))
        screen.blit(title, (45, 0))
        for box in boxes:
            box.draw(screen)

        pygame.display.flip()
        clock.tick(30)


def high_score_menu(screen, squares, resolution, font):
    with open("game_files/high_scores.json", "r") as in_file:
        high_scores = json.load(in_file)
    while True:
        screen.fill((0, 0, 0))
        for i in range(len(high_scores)):
            high_score = font.render(f"{i + 1}: {high_scores[i]}", False, (0, 255, 0))
            highRect = high_score.get_rect()
            highRect.center = (resolution[0] / 2, 30 + i * (resolution[1] / 6))
            screen.blit(high_score, highRect)
        menu_button = (resolution[0] / 2 - 75, resolution[1] - 100, 150, 50)
        menu_button_rect = pygame.Rect(menu_button)
        pygame.draw.rect(screen, (255, 100, 0), menu_button)
        menu_text = font.render("Main Menu", False, (0, 255, 0))
        menuRect = menu_text.get_rect()
        menuRect.center = (resolution[0] / 2, resolution[1] - 75)
        screen.blit(menu_text, menuRect)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if menu_button_rect.collidepoint(event.pos):
                        main_menu(screen, squares, resolution, font)

        pygame.display.flip()
        time.sleep(0.01)
