import pygame
import random
import math


class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.life = None  # how long should particle live(frames)


class Fire(Particle):
    def __init__(self, pos):
        super().__init__(pos[0] / 4, pos[1] / 4)
        self.color = ((255, 255, 0),
                      (255, 173, 51),
                      (247, 117, 33),
                      (191, 74, 46),
                      (115, 61, 56),
                      (61, 38, 48))
        self.max_life = random.randint(6, 13)
        self.alive = True
        self.life = self.max_life
        self.radius = random.randint(0, 4)
        self.spread = random.randint(-2, 2)  # spread
        self.rise = random.randint(-2, 0)  # rise
        self.angle = random.randint(0, 360)
        self.i = int(((self.life - 1) / self.max_life) * 6)  # color index
        self.alpha = None
        self.draw_x = self.x
        self.draw_y = self.y

    def update(self, dt):  # change some constants to acquire different effect
        if random.randint(1, 4) == 2:
            if self.angle > 360:  # Angle
                self.angle = 0
            self.life -= 1
            if self.life == 0:
                self.alive = False
            self.i = int((self.life / self.max_life) * 6)
            self.y -= 2.7  # rise
            self.x += 0  # wind
            if not random.randint(0, 5):
                self.radius += 0.5  # circle radius, set to 10 for big bang
            self.draw_x, self.draw_y = self.x, self.y
            self.draw_x += self.spread * (5 - self.i)
            self.draw_y += self.rise * (5 - self.i)
            self.alpha = 255
            if self.life < self.max_life / 4:
                self.alpha = int((self.life / self.max_life) * 255)

    def draw(self, surface):
        alpha = 255
        pygame.draw.circle(surface,
                           self.color[self.i] + (alpha,),
                           (self.draw_x, self.draw_y),
                           self.radius, 0)
        if self.i == 0:
            pygame.draw.circle(surface,
                               (0, 0, 0, 0),
                               (self.draw_x + random.randint(-1, 1),
                                self.draw_y - 4),
                               self.radius * (((self.max_life - self.life) / self.max_life) / 0.88), 0)
        else:
            pygame.draw.circle(surface,
                               self.color[self.i - 1] + (alpha,),
                               (self.draw_x + random.randint(-1, 1), self.draw_y - 3),
                               self.radius / 1.5, 0)
