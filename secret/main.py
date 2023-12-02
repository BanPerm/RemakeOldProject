import pygame
import json
import math

pygame.init()

#Définir taille écran
screen_height = 720
screen_width = 1080

# Gestion temps et FPS
mainClock = pygame.time.Clock()
FPS = 144

# Initialisation fenetre
screen = pygame.display.set_mode((screen_width, screen_height))

# Affichage des fps pour optimisation
def fps_counter():
    font2 = pygame.font.SysFont("comicsans", 15, bold=False, italic=False)
    fps = mainClock.get_fps()  # Utiliser get_fps() au lieu de mainClock
    fps_t = font2.render(f'fps:{fps}', 1, (255, 255, 0))
    screen.blit(fps_t, (20, 50))

def draw3D():
    wx = [0, 0]
    wy = [0, 0]
    wz = [0, 0]

    angle = player.a * (math.pi / 180)
    cos = math.cos(angle)
    sin = math.sin(angle)
    # Create 2 points
    x1 = 40 - player.x
    y1 = 10 - player.y
    x2 = 40 - player.x
    y2 = 290 - player.y

    # Position du monde en x
    wx[0] = x1 * cos - y1 * sin
    wx[1] = x2 * cos - y2 * sin

    # Position du monde en y
    wy[0] = y1 * cos + x1 * sin
    wy[1] = y2 * cos + x2 * sin

    # Position du monde en z
    wz[0] = 0 - player.z - ((player.l * wy[0]) / 32)
    wz[1] = 0 - player.z - ((player.l * wy[1]) / 32)

    # Screen positions
    wx[0] = wx[0] * 200 / wz[0] + (screen_width // 2)
    wy[0] = wy[0] * 200 / wz[0] + (screen_height // 2)
    wx[1] = wx[1] * 200 / wz[1] + (screen_width // 2)
    wy[1] = wy[1] * 200 / wz[1] + (screen_height // 2)

    pygame.draw.line(screen, (255, 255, 255), (wx[0], wy[0]), (wx[1], wy[1]), 2)

###########################Player###########################
class Player():
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z =z
        self.a = 0
        self.l = 0

    def reset_angle(self):
        if self.a<0:
            self.a+=360
        elif self.a>359:
            self.a -=360

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_q]:
            if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:self.l -= 1
            else:self.a -= 4;self.reset_angle()

        if keys[pygame.K_d]:
            if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:self.l += 1
            else:self.a += 4;self.reset_angle()

        dx = math.sin(math.radians(self.a)) * 1
        dy = math.cos(math.radians(self.a)) * 1

        if keys[pygame.K_z]:
            if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:self.z -= 4
            else:self.x += dx;self.y += dy

        if keys[pygame.K_s]:
            if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:self.z += 4
            else:self.x -= dx;self.y -= dy


player = Player(70,110,20)


def game():
    running = True
    while running:
        screen.fill((0, 60, 130))
        draw3D()

        fps_counter()
        player.move()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                pygame.sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                #if event.key == pygame.K_q:


        pygame.display.update()
        mainClock.tick(144)

game()

pygame.quit()