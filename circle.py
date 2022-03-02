import pygame
import random


class Circle:
    color = (255, 255, 255)

    def __init__(self, center):
        self.center = [point / 4 for point in center]
        self.radius = 1
        self.mini_radius = 1
        self.max_radius = random.randint(50, 75)
        self.alive = True
        self.speed = 1.5

    def draw(self, surface):
        if self.alive:
            pygame.draw.circle(surface, self.color, self.center, self.radius, 2)
            pygame.draw.circle(surface, self.color, self.center, self.mini_radius, 2)

    def update(self, dt=1):
        self.radius += 2 * dt * 45 * self.speed
        self.mini_radius += 0.75 * dt * 45 * self.speed
        if self.radius > self.max_radius or self.speed <=0:
            self.alive = False
        self.speed -= dt
