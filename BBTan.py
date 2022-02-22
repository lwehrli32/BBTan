import math
import pygame
from random import randint

from Block import Block


class BBTan:

    def __init__(self):

        # load game properties
        self.level = 1
        self.max_blocks = 10
        self.balls_running = False
        self.bottom = 430
        self.ball_velx = 0.5
        self.ball_vely = 0.5
        self.blocks = []
        self.balls = []
        self.width = 640
        self.height = 480

        # index 0: lower number is left and higher number is right
        # index 1: lower number is up and higher number is down
        self.ball_pos = [300, self.bottom]

        # init pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.SysFont("Arial", 20)

        # render first block
        self.possible_block_positions = [0, 62, 124, 186, 248, 310, 372, 434, 496, 558]
        self.taken_blocks = []
        num_blocks = randint(1, 10)

        for b in range(num_blocks):
            if not (b in self.taken_blocks):
                pos = randint(0, len(self.possible_block_positions) - 1)
                block = Block(self.level, self.possible_block_positions[pos], 0)
                self.blocks.append(block)
                self.taken_blocks.append(pos)

        # load imgs
        self.ball = pygame.image.load("imgs/soccer_ball.png")
        self.ball = pygame.transform.scale(self.ball, (20, 20))

        # init starting balls
        self.balls.append([0, self.ball_pos[0], self.ball_pos[1], 0, 0])

        self.screen.blit(self.ball, (self.balls[0][1], self.balls[0][2]))

        pygame.display.flip()

    def play_game(self):
        game = True

        while game:
            self.screen.fill((255, 255, 255))

            if self.balls_running:
                # balls are hitting blocks

                # render blocks
                for block in self.blocks:
                    block.draw_block(self.screen)

                # render balls
                balls_above_0 = 0
                for ball in self.balls:
                    velx = math.cos(ball[0]) * ball[3]
                    vely = math.sin(ball[0]) * ball[4]

                    ball[1] += velx
                    ball[2] += vely

                    if ball[1] < 0 or ball[1] > 620:
                        ball[3] = ball[3] * -1
                    elif ball[2] < 0:
                        ball[4] = ball[4] * -1
                    elif ball[2] > self.bottom:
                        ball[3] = 0
                        ball[4] = 0
                        ball[2] = self.bottom

                    for b in self.balls:
                        self.screen.blit(self.ball, (b[1], b[2]))

                    if ball[3] != 0 and ball[4] != 0:
                        balls_above_0 += 1

                if balls_above_0 == 0:
                    # new level
                    self.level += 1
                    self.balls_running = False
                    print('new level!')

            # render blocks
            for block in self.blocks:
                block.draw_block(self.screen)

            # display balls
            for ball in self.balls:
                self.screen.blit(self.ball, (ball[1], ball[2]))

            # write level number
            level_text = self.font.render("Level: " + str(self.level), True, (0, 0, 0))
            self.screen.blit(level_text, ((self.screen.get_width() - level_text.get_width() - 20), 455))

            # draw bbtan
            bbtan_text = self.font.render("BBTAN", True, (0, 0, 0))
            self.screen.blit(bbtan_text, (20, 455))

            # draw baseline
            pygame.draw.line(self.screen, (0, 0, 0), (0, 450), (self.width, 450))

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

                        for ball in self.balls:
                            ball_angle = math.atan2(mouse_pos[1] - ball[2],
                                                    mouse_pos[0] - ball[1])

                            ball[0] = ball_angle

                            # calc new velocities
                            if ball_angle < math.pi / 2:
                                ball[3] = self.ball_velx
                            else:
                                ball[3] = self.ball_velx * -1

                            ball[4] = self.ball_vely
