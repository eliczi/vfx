import random
import pygame
from polygon import Polygon
import math
from pygame.math import Vector2

class Line:
    alpha = 255
    color = (255, 255, 255, alpha)

    def __init__(self, center):
        self.points = [[], [], [], []]  # 4 points
        self.center = [point / 4 for point in center]  # center of polygon
        self.length = random.randint(75,100)  # longer diagonal
        self.angle = random.randint(-180, 180)
        self.perpendicular_straight = random.randint(2, 3)  # shorter diagonal
        self.create_polygon()
        self.alive = True
        self.dir = None
        self.speed = random.randint(1, 3)
        self.factor = random.choice([-1, 1])
        self.calculate_direction()
        self.decay_factor = 0.05
        self.delta = 0.008 * 25

    
    def create_polygon(self):  # it's a mess
        x = self.center[0] + self.length * math.cos(math.radians(self.angle))
        y = self.center[1] + self.length * math.sin(math.radians(self.angle))
        self.points[0] = Vector2([x, y])
        x = self.center[0] - self.length * math.cos(math.radians(self.angle))
        y = self.center[1] - self.length * math.sin(math.radians(self.angle))
        self.points[1] = Vector2([x, y])
        x1, x2 = self.points[0][0], self.points[1][0]
        y1, y2 = self.points[0][1], self.points[1][1]
        x3, y3 = self.center
        B = Vector2(y1 - y2, x2 - x1)
        B.normalize_ip()
        x, y = Vector2(x3, y3) + self.perpendicular_straight * B
        self.points[2] = Vector2([x, y])
        # self.points[2] = Vector2([x + random.randint(1, 3), y + random.randint(1, 3)])
        x, y = Vector2(x3, y3) - self.perpendicular_straight * B
        self.points[3] = Vector2([x, y])
        # self.points[3] = Vector2([x + random.randint(1, 3), y + random.randint(1, 3)])
        self.points[1], self.points[2] = self.points[2], self.points[1]

    def calculate_direction(self):
        self.dir = pygame.math.Vector2(self.points[2] - self.points[0])
        self.dir.normalize_ip()
        self.dir.scale_to_length(self.speed)
        self.dir = self.dir * self.factor


    def draw(self, surface):
        if self.alive:
            pygame.draw.polygon(surface, self.color, self.points, width=0)

    def new_points(self, factor):
        self.points[0] = self.points[0] + (self.points[2] - self.points[0]) * factor
        self.points[1] = self.points[1] + (self.points[2] - self.points[1]) * factor
        self.points[3] = self.points[3] + (self.points[2] - self.points[3]) * factor

    def rotate(self, angle):
        for vector in self.points:
            vector.rotate_ip(angle)

    def update_position(self):
        for point in range(len(self.points)):
            for i in range(2):
                self.points[point][i] += self.dir[i] * self.delta

    def update_decay_factor(self):
        self.decay_factor -= 0.008

    def update_speed(self):
        self.speed -= 0.02
        if self.speed <= 0:
            self.alive = False

    def update(self, dt):
        self.new_points(self.decay_factor)
        self.update_position()
        self.update_speed()
        self.calculate_direction()
        # self.update_decay_factor()