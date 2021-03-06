import math
import pygame
from random import randint

from Block import Block
from PowerUp import PowerUp
from Stats import Stats


class BBTan:

    def __init__(self):

        # load game properties
        self.level = 1
        self.max_blocks = 10
        self.balls_running = False
        self.balls_on_ground = False
        self.bottom = 430
        self.ball_velx = 0.75
        self.ball_vely = 0.75
        self.blocks = []
        self.balls = []
        self.width = 640
        self.height = 480
        self.ball_angle = 0
        self.balls_ran = 0
        self.ball_timer = 0
        self.ball_delay = 150
        self.stats = Stats()
        self.highscore = self.stats.read_score()
        self.powerups = []

        # index 0: lower number is left and higher number is right
        # index 1: lower number is up and higher number is down
        self.ball_pos = [300, self.bottom]

        # init pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.SysFont("Arial", 20)

        # render first block
        self.possible_block_positions = [0, 62, 124, 186, 248, 310, 372, 434, 496, 558]

        # get a random number of blocks
        self.add_new_row()

        # load imgs
        self.ball = pygame.image.load("imgs/soccer_ball.png")
        self.ball = pygame.transform.scale(self.ball, (20, 20))

        self.gameover = pygame.image.load("imgs/gameover.png")

        # init starting balls
        self.balls.append([0, self.ball_pos[0], self.ball_pos[1], 0, 0, 0])

        self.screen.blit(self.ball, (self.balls[0][1], self.balls[0][2]))

        pygame.display.flip()

    def add_new_row(self):
        total_num_blocks = randint(1, 8)
        taken_blocks = []
        num_blocks = 0

        pos = randint(0, len(self.possible_block_positions) - 1)
        taken_blocks.append(pos)
        new_powerup = PowerUp(self.screen, 0, self.possible_block_positions[pos] + 20, 25)
        self.powerups.append(new_powerup)

        while num_blocks < total_num_blocks:
            pos = randint(0, len(self.possible_block_positions) - 1)
            if not (pos in taken_blocks):
                block = Block(self.level * 2 if self.level % 10 == 0 else self.level,
                              self.possible_block_positions[pos], 0, color=(255, 0, 0) if self.level % 10 == 0 else None)
                self.blocks.append(block)
                taken_blocks.append(pos)
                num_blocks += 1

    def play_game(self):
        game = True

        while game:
            self.screen.fill((255, 255, 255))

            if self.balls_running:
                # balls are hitting blocks

                if pygame.time.get_ticks() - self.ball_timer > self.ball_delay and self.balls_ran < len(self.balls):
                    for ball in self.balls:
                        if ball[3] == 0 and ball[4] == 0 and ball[5] == 0:
                            ball[0] = self.ball_angle

                            # calc new velocities
                            if self.ball_angle < math.pi / 2:
                                ball[3] = self.ball_velx
                            else:
                                ball[3] = self.ball_velx * -1

                            ball[4] = self.ball_vely
                            ball[5] = 1
                            self.ball_timer = pygame.time.get_ticks()
                            self.balls_ran += 1
                            break

                # render balls
                balls_above_0 = 0
                for ball in self.balls:
                    velx = math.cos(ball[0]) * ball[3]
                    vely = math.sin(ball[0]) * ball[4]

                    ball[1] += velx
                    ball[2] += vely

                    if ball[1] > 620:
                        ball[3] = ball[3] * -1
                        ball[1] = 620
                    elif ball[1] < 0:
                        ball[3] = ball[3] * -1
                        ball[1] = 0
                    elif ball[2] < 0:
                        ball[4] = ball[4] * -1
                        ball[2] = 0
                    elif ball[2] > self.bottom:
                        if not self.balls_on_ground:
                            self.balls_on_ground = True
                            self.ball_pos[0] = ball[1]

                        ball[3] = 0
                        ball[4] = 0
                        ball[2] = self.bottom
                        ball[1] = self.ball_pos[0]

                    ball_rect = self.ball.get_rect()
                    ball_rect.x = ball[1]
                    ball_rect.y = ball[2]
                    bad_blocks = []
                    for block in self.blocks:
                        collision = False
                        block_rect = block.boundries
                        block_rect.x = block.x
                        block_rect.y = block.y
                        block_right = block.x + block.length
                        block_left = block.x
                        block_top = block.y
                        block_bottom = block.y + block.length
                        ball_left = ball_rect.x
                        ball_right = ball_rect.x + 20
                        ball_top = ball_rect.y
                        ball_bottom = ball_rect.y + 20

                        if block_left <= ball_right <= block_right and block_bottom >= ball_top >= block_top:
                            collision = True
                        if block_left <= ball_left <= block_right and block_bottom >= ball_top >= block_top:
                            collision = True
                        if block_left <= ball_right <= block_right and block_bottom >= ball_bottom >= block_top:
                            collision = True
                        if block_left <= ball_left <= block_right and block_bottom >= ball_bottom >= block_top:
                            collision = True

                        if ball_rect.colliderect(block_rect) and collision:
                            block.decrement_lives()

                            block_min_x = block.x
                            block_max_x = block.x + block.length
                            block_min_y = block.y
                            block_max_y = block.y + block.length
                            if block_min_y <= ball[2] <= block_max_y and (0 <= block_min_x - ball[1] <= 20):
                                ball[1] = block_min_x - 1
                                ball[3] = ball[3] * -1
                            elif block_min_y <= ball[2] <= block_max_y and (0 <= block_max_x - ball[1] <= 20):
                                ball[1] = block_max_x + 1
                                ball[3] = ball[3] * -1
                            elif block_min_x <= ball[1] <= block_max_x and (0 <= block_max_y - ball[2] <= 20):
                                ball[2] = block_max_y + 1
                                ball[4] = ball[4] * -1
                            elif block_min_x <= ball[1] <= block_max_x and (0 <= block_min_y - ball[2] <= 20):
                                ball[2] = block_min_y - 1
                                ball[4] = ball[4] * -1

                            # check if block is out of lives
                            if block.lives <= 0:
                                bad_blocks.append(block)
                    self.blocks = [b for b in self.blocks if (b not in bad_blocks)]

                    for powerup in self.powerups:
                        rect = powerup.img.get_rect()
                        rect.x = powerup.x
                        rect.y = powerup.y
                        if ball_rect.colliderect(rect):
                            powerup_type = powerup.powerup_type
                            if powerup_type == 0:
                                powerup.hit = True
                                powerup.show = False

                    #for b in self.balls:
                        #self.screen.blit(self.ball, (b[1], b[2]))

                    if ball[3] != 0 and ball[4] != 0 and ball[5] == 1:
                        balls_above_0 += 1

                if balls_above_0 == 0 and self.balls_ran == len(self.balls):
                    # new level
                    self.level += 1
                    self.balls_running = False
                    self.balls_ran = 0

                    #self.ball_velx = self.ball_velx + 0.15
                    #self.ball_vely = self.ball_vely + 0.15

                    for ball in self.balls:
                        ball[5] = 0

                    # move current blocks down
                    for block in self.blocks:
                        block.y = block.y + 62

                    bad_powerups = []
                    for powerup in self.powerups:
                        powerup.y = powerup.y + 62
                        if powerup.hit:
                            if powerup.powerup_type == 0:
                                self.balls.append([0, self.ball_pos[0], self.ball_pos[1], 0, 0, 0])
                            bad_powerups.append(powerup)

                    self.powerups = [p for p in self.powerups if (p not in bad_powerups)]

                    self.add_new_row()

            else:
                self.balls_on_ground = False

            # render blocks
            for block in self.blocks:
                block.draw_block(self.screen)

                if block.y >= self.bottom:
                    game = False

            # display balls
            for ball in self.balls:
                self.screen.blit(self.ball, (ball[1], ball[2]))

            # render power ups
            bad_powerups = []
            for powerup in self.powerups:
                if powerup.y >= self.bottom:
                    bad_powerups.append(powerup)
                    powerup.show = False

                if powerup.show:
                    self.screen.blit(powerup.img, (powerup.x, powerup.y))
            self.powerups = [p for p in self.powerups if (p not in bad_powerups)]

            # write level number
            level_text = self.font.render("Level: " + str(self.level), True, (0, 0, 0))
            self.screen.blit(level_text, ((self.screen.get_width() - level_text.get_width() - 20), 455))

            # draw bbtan
            bbtan_text = self.font.render("BBTAN", True, (0, 0, 0))
            self.screen.blit(bbtan_text, ((self.screen.get_width() / 2 - level_text.get_width() - 20), 455))

            # draw highscore
            high_score = self.font.render("High Score: " + str(self.highscore), True, (0, 0, 0))
            self.screen.blit(high_score, (20, 455))

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

                        self.ball_angle = math.atan2(mouse_pos[1] - self.balls[0][2], mouse_pos[0] - self.balls[0][1])
                        self.balls[0][0] = self.ball_angle

                        # calc new velocities
                        if self.ball_angle < math.pi / 2:
                            self.balls[0][3] = self.ball_velx
                        else:
                            self.balls[0][3] = self.ball_velx * -1

                        self.balls[0][4] = self.ball_vely
                        self.balls[0][5] = 1
                        self.ball_timer = pygame.time.get_ticks()
                        self.balls_ran += 1

        pygame.font.init()
        font = pygame.font.Font(None, 24)
        text = font.render("Score: " + str(self.level), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.centerx = self.screen.get_rect().centerx
        textRect.centery = self.screen.get_rect().centery + 24
        self.screen.blit(self.gameover, (0, 0))
        self.screen.blit(text, textRect)

        # record stats
        if self.level > self.highscore:
            self.stats.record_score(self.level)
        self.stats.calc_avg(self.level)

        self.ball_timer = pygame.time.get_ticks()
        while pygame.time.get_ticks() - self.ball_timer < 5000:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)
            pygame.display.flip()
