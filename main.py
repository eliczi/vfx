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
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)
text_surface = my_font.render('a - attack, r - atack ready, f - fire, s - smoke', False, (255, 255, 255))


def resize_and_draw(surface, pixelated_surface, destination_surface):
    surface.blit(pygame.transform.scale(pixelated_surface, (world_size[0], world_size[1]), destination_surface),
                 (0, 0))


clock = pygame.time.Clock()
FPS = 60
particles = []


def hit(pos):
    line = Line(pos)
    particles.append(line)
    for _ in range(20):
        polygon = Polygon(pos)
        particles.append(polygon)


def smoke_effect(pos):
    for _ in range(40):
        smoke_particle = Smoke(pos)
        particles.append(smoke_particle)


def atack_rdy(pos):
    line = AttackReady(pos, None)
    particles.append(line)


def fire(pos):
    for _ in range(20):
        particles.append(Fire(pos))


def cooldown(timer, value):
    return pygame.time.get_ticks() - timer > value


prev_time = time.time()
time_now = 0
x, y = 0, 0
effect = 'smoke'
cd_time = 0 #cooldown
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
    if pressed[pygame.K_s]:
        effect = 'smoke'
    if pressed[pygame.K_a]:
        effect = 'attack'
    if pressed[pygame.K_r]:
        effect = 'attack_ready'
    if pressed[pygame.K_f]:
        effect = 'fire'

    if pygame.mouse.get_pressed()[0] and cooldown(time_now, cd_time):
        time_now = pygame.time.get_ticks()
        pos = pygame.mouse.get_pos()
        if effect == 'fire':
            fire(pos)
            cd_time = 0
        elif effect == 'smoke':
            smoke_effect(pos)
            cd_time = 50
        elif effect == 'attack_ready':
            atack_rdy(pos)
            cd_time = 500
        elif effect == 'attack':
            hit(pos)
            cd_time = 350

    drawing_screen.fill((0, 0, 0))
    for p in particles:
        p.update(dt)
        p.draw(drawing_screen)
        if not p.alive:
            particles.remove(p)



    screen.fill('black')
    resize_and_draw(screen, drawing_screen, dest_surf)
    screen.blit(text_surface, (0, 0))
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
