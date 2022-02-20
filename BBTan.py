import math

import pygame
from pygame.locals import *


class BBTan:

    def __init__(self):
        pygame.init()
        width, height = 640, 480
        self.screen = pygame.display.set_mode((width, height))
        self.balls_running = True
        self.player_pos = [320, 50]

        # load imgs
        self.ball = pygame.image.load("imgs/soccer_ball.png")

        # init starting balls
        mouse_pos = pygame.mouse.get_pos()
        self.balls = []
        self.balls.append([math.atan2(mouse_pos[1] - (self.player_pos[1] + 32),
                                      mouse_pos[0] - (self.player_pos[0] + 26)),
                           self.player_pos[0] + 32, self.player_pos[1] + 32])

    def step(self):
        self.screen.fill(0)

        if self.balls_running:
            # balls are hitting blocks
            for ball in self.balls:
                velx = math.cos(ball[0]) * 10
                vely = math.sin(ball[0]) * 10
                ball[1] += velx
                ball[2] += vely

                for b in self.balls:
                    b1 = pygame.transform.rotate(arrow, 360-projectile[0]*57.29)
                    screen.blit()

        else:

            # user selecting where to shoot
            for event in pygame.event.get():
                if event == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self.balls.append([math.atan2(mouse_pos[1] - (self.player_pos[1] + 32),
                                                  mouse_pos[0] - (self.player_pos[0] + 26)),
                                       self.player_pos[0] + 32, self.player_pos[1] + 32])
