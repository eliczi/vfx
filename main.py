import pygame
from polygon import Polygon
from circle import Circle
from line import Line
import time

world_size = (1600, 960)
display = pygame.display.set_mode(world_size)
screen = pygame.Surface(world_size).convert()
running = True
drawing_screen = pygame.Surface((world_size[0] / 4, world_size[1] / 4),
                                pygame.SRCALPHA).convert_alpha()
dest_surf = pygame.Surface((world_size[0], world_size[1]), pygame.SRCALPHA).convert_alpha()
WHITE = (255, 255, 255)


def resize_and_draw(surface, pixelated_surface, destination_surface):
    surface.blit(pygame.transform.scale(pixelated_surface, (world_size[0], world_size[1]), destination_surface),
                 (0, 0))


clock = pygame.time.Clock()
FPS = 300
points = [[600, 500], [670, 470], [750, 400], [660, 460]]
polygons = []
circles = []
lines = []


def explode(pos):
    line = Line(pos)
    lines.append(line)
    for _ in range(20):
        polygon = Polygon(pos)
        polygons.append(polygon)


prev_time = time.time()
time_now = 0
while running:
    now = time.time()
    dt = now - prev_time
    prev_time = now

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_ESCAPE]:
        running = False

    if pygame.mouse.get_pressed()[0] and pygame.time.get_ticks() - time_now > 250:
        time_now = pygame.time.get_ticks()
        pos = pygame.mouse.get_pos()
        explode(pos)

    screen.fill((0, 0, 0))
    drawing_screen.fill((0, 0, 0))

    for pol in lines:
        pol.update(dt)
        pol.draw(drawing_screen)
        if pol.alive is False:
            lines.remove(pol)
    for pol in polygons:
        pol.update(dt)
        pol.draw(drawing_screen)
        if pol.alive is False:
            polygons.remove(pol)

    resize_and_draw(screen, drawing_screen, dest_surf)
    #print(dt)
    display.blit(screen, (0, 0))
    pygame.display.flip()
