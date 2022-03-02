import math

import pygame
import random
from pygame.math import Vector2
from math import tan


class Smoke:

    def __init__(self, position):
        self.position = [p / 4 for p in position]
        self.alive = True
        self.rate_of_growth = 8
        self.rate_of_shrinkage = 0.5
        self.radius = random.randint(1, 3)
        self.max_radius = random.randint(5, 20)
        self.angle = random.randint(-180, -90) + random.randint(-15, 15)
        self.max_size = False
        self.spread = 0.8
        self.rise = 1.5
        self.alpha = random.randint(215, 255)
        self.color = random.choice([(255, 255, 255, self.alpha), (245, 255, 255, self.alpha)])
        self.speed = 25
        self.wind = -0
        self.direction = Vector2([random.randint(1, 10) / 100, random.randint(1, 10) / 100])
        self.direction.rotate_ip(self.angle)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.position, self.radius)

    def update(self, dt):
        dt = dt * self.speed
        if not self.max_size:
            self.position[0] += self.direction[0] * dt * self.speed * self.spread * 3
            self.position[1] += self.direction[1] * dt * self.speed * self.rise / 2
            self.radius += self.rate_of_growth * dt
            if self.radius >= self.max_radius:
                self.max_size = True
        else:
            self.position[0] += self.direction[0] * dt * self.speed * self.spread + self.wind
            self.position[1] += self.direction[1] * dt * self.speed * self.rise
            self.radius -= self.rate_of_shrinkage * dt
            #change rate of shrinkage
            if self.radius <= 1:
                self.alive = False
