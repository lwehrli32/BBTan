from random import randint
import pygame


class Block:

    def __init__(self, lives, x, y):
        self.lives = lives
        self.x = x
        self.y = y
        self.length = 57

        pink = (255, 102, 178)
        green = (0, 204, 102)
        orange = (255, 153, 51)
        purple = (153, 51, 255)
        colors = [pink, green, orange, purple]
        pos = randint(0, len(colors) - 1)
        self.color = colors[pos]

        self.font = pygame.font.SysFont("Arial", 20)

    def decrement_lives(self):
        self.lives -= 1

    def draw_block(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.length, self.length), 2)
        lives_text = self.font.render(str(self.lives), True, self.color)
        screen.blit(lives_text, (self.x + ((self.length / 2) - 5), (self.length / 2) - 10))
