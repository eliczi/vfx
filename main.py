import pygame
from polygon import Polygon
from circle import Circle
from smoke import Smoke
from fire import Fire
from line import Line
from attack_ready import AttackReady
import time

world_size = (1200, 600)
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
FPS = 60
polygons = []
circles = []
lines = []
smoke = []
fires = []


def hit(pos):
    line = Line(pos)
    lines.append(line)
    for _ in range(20):
        polygon = Polygon(pos)
        polygons.append(polygon)


def smoke_effect(pos):
    for _ in range(40):
        smoke_particle = Smoke(pos)
        smoke.append(smoke_particle)


def explode(pos):
    line = AttackReady(pos, None)
    lines.append(line)


def fire(pos):
    for _ in range(20):
        fires.append(Fire(pos))


def cooldown(timer, value):
    return pygame.time.get_ticks() - timer > value


prev_time = time.time()
time_now = 0
x, y = 0, 0
czas = 0
while running:
    now = time.time()
    dt = now - prev_time
    prev_time = now

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    pressed = pygame.key.get_pressed()
    effect = 'smoke'
    if pressed[pygame.K_ESCAPE]:
        running = False
    if pressed[pygame.K_s]:
        effect = 'smoke'
    if pressed[pygame.K_a]:
        effect = 'attack'
    if pressed[pygame.K_r]:
        effect = 'attack_ready'

    if pygame.mouse.get_pressed()[0] and cooldown(time_now, 0):
        time_now = pygame.time.get_ticks()
        pos = pygame.mouse.get_pos()
        fire(pos)

    drawing_screen.fill((0, 0, 0))
    for s in fires:
        s.update(dt)
        s.draw(drawing_screen)
        if not s.alive:
            fires.remove(s)

    for s in smoke:
        s.update(dt)
        s.draw(drawing_screen)
        if not s.alive:
            smoke.remove(s)
    for s in lines:
        s.update(dt)
        s.draw(drawing_screen)
        if not s.alive:
            lines.remove(s)
    for s in polygons:
        s.update(dt)
        s.draw(drawing_screen)
        if not s.alive:
            polygons.remove(s)

    screen.fill('black')
    resize_and_draw(screen, drawing_screen, dest_surf)
    display.blit(screen, (0, 0))
    pygame.display.flip()

# masking
# mask = pygame.mask.from_surface(mud)
# sur = mask.to_surface()
# sur.set_colorkey((255, 255, 255))
#
# surface = image.copy()
# surface.blit(sur, (200, 150))
# surface.set_colorkey((255, 255, 255))
#
# new_surf = pygame.Surface((320, 320)).convert_alpha()
# new_surf.blit(surface, (-200, -150))
# new_surf.set_colorkey((0, 0,0))
# pygame.draw.rect(screen, (255, 255, 255), (0, 0, 320, 320))
#
#
# screen.blit(image, (600, 100))
# screen.blit(new_surf, (x, y))
