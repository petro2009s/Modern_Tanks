import pygame

WIDTH = 1920
HEIGHT = 1080

button_color = (50, 60, 50)
pygame.init()

display = pygame.display.set_mode((WIDTH, HEIGHT))
icon = pygame.image.load('resources/images/icon_test2_p.png').convert()

menu1 = pygame.image.load('resources/images/menu_p1.png').convert()
menu2 = pygame.image.load('resources/images/menu_p2.png').convert()
menu3 = pygame.image.load('resources/images/menu_p3.png').convert()
menu4 = pygame.image.load('resources/images/menu_p4.png').convert()
menu5 = pygame.image.load('resources/images/menu_p5.png').convert()
menu_list = [menu1, menu2, menu3, menu4, menu5]

graph_dict = {0: False, 1: True, 2: False}
d_dict = {0: False, 1: True, 2: False}
fps_dict = {0: False, 1: True, 2: False}

tank_dict = {0: True}
lvl_dict = {0: True}
clock = pygame.time.Clock()
FPS = 60

with (open('resources/descriptions/he.txt', encoding='utf-8') as f,
      open('resources/descriptions/apfsds.txt', encoding='utf-8') as f2,
      open('resources/descriptions/heat.txt', encoding='utf-8') as f3):
    HE = list(map(lambda x: x[:-1], f.readlines()))
    APFSDS = list(map(lambda x: x[:-1], f2.readlines()))
    HEAT = list(map(lambda x: x[:-1], f3.readlines()))
with open('resources/descriptions/ammunition.txt', encoding='utf-8') as f:
    ammo = list(map(lambda x: x[:-1], f.readlines()))
with open('resources/descriptions/T-90M_descr.txt', encoding='utf-8') as f:
    T_90M_descr = list(map(lambda x: x[:-1], f.readlines()))
with open('resources/descriptions/T-90M_TTH.txt', encoding='utf-8') as f:
    T_90M_TTH = list(map(lambda x: x[:-1], f.readlines()))
with open('resources/descriptions/guide.txt', encoding='utf-8') as f:
    guide_descr = list(map(lambda x: x[:-1], f.readlines()))

MAX_AMMO = 22
APFSDS_COUNT = 0
HE_COUNT = 0
HEAT_COUNT = 0
