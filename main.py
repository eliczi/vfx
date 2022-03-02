import pygame
from polygon import Polygon
from circle import Circle
from smoke import Smoke
from line import Line
from line2 import Line2
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
FPS = 30
points = [[600, 500], [670, 470], [750, 400], [660, 460]]
polygons = []
circles = []
lines = []
smoke = []


def hit(pos):
    line = Line(pos)
    lines.append(line)
    for _ in range(20):
        polygon = Polygon(pos)
        polygons.append(polygon)


def explode(pos):
    line = Line2(pos)
    lines.append(line)



prev_time = time.time()
time_now = 0
image = pygame.transform.scale(pygame.image.load('orc.png').convert_alpha(), (640, 640))
mud = pygame.transform.scale(pygame.image.load('mud.png', ).convert_alpha(), (320, 320))
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
    if pressed[pygame.K_ESCAPE]:
        running = False
    if pressed[pygame.K_w]:
        y -= 10
    if pressed[pygame.K_s]:
        y += 10
    if pressed[pygame.K_a]:
        x -= 10
    if pressed[pygame.K_d]:
        x += 10

    if pygame.mouse.get_pressed()[0] and pygame.time.get_ticks() - time_now > 200:
        time_now = pygame.time.get_ticks()
        pos = pygame.mouse.get_pos()
        explode(pos)

    drawing_screen.fill((0, 0, 0))

    for s in lines:
        s.update(dt)
        s.draw(drawing_screen)
        if not s.alive:
            lines.remove(s)

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
