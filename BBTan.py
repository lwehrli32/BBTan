import math
import pygame
from pygame.locals import *


class BBTan:

    def __init__(self):
        pygame.init()
        width, height = 640, 480
        self.screen = pygame.display.set_mode((width, height))
        self.balls_running = False
        self.ball_pos = [300, 428]

        # load game properties
        self.level = 1

        # load imgs
        self.ball = pygame.image.load("imgs/soccer_ball.png")
        self.ball = pygame.transform.scale(self.ball, (20, 20))

        # init starting balls
        mouse_pos = pygame.mouse.get_pos()
        self.balls = []
        self.balls.append([math.atan2(mouse_pos[1] - (self.ball_pos[1] + 32),
                                      mouse_pos[0] - (self.ball_pos[0] + 26)),
                           self.ball_pos[0] + 32, self.ball_pos[1] + 32, 10, 10])

        self.screen.blit(self.ball, (self.balls[0][1], self.balls[0][2]))
        print('ball location: ' + str(self.balls[0][1]) + ', ' + str(self.balls[0][2]))

    def play_game(self):
        game = True
        pygame.display.flip()
        while game:
            self.screen.fill(0)

            if self.balls_running:
                print('balls running. . .')
                # balls are hitting blocks
                balls_running = 0
                for ball in self.balls:
                    velx = math.cos(ball[0]) * 10
                    vely = math.sin(ball[0]) * 10

                    if ball[1] < 0 or ball[1] > 640:
                        ball[1] -= velx
                        ball[2] += vely
                    elif ball[2] > 480:
                        ball[1] += velx
                        ball[2] -= vely
                    else:
                        ball[1] += velx
                        ball[2] += vely

                    for b in self.balls:
                        self.screen.blit(self.ball, (b[1], b[2]))

                    if ball[2] > 0:
                        balls_running += 1
                    else:
                        pass

                if balls_running > 0:
                    # new level
                    self.level += 1
                    self.balls_running = False
            else:

                for ball in self.balls:
                    for b in self.balls:
                        self.screen.blit(self.ball, (b[1], b[2]))

            pygame.display.flip()

            # user selecting where to shoot
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not self.balls_running:
                        self.balls_running = True
                        mouse_pos = pygame.mouse.get_pos()
                        print('click location: ' + str(mouse_pos[0]) + ', ' + str(mouse_pos[1]))
