import pygame

WIDTH = 1920
HEIGHT = 1080

button_color = (50, 60, 50)

icon = pygame.image.load('images/icon_test2_p.png')

menu1 = pygame.image.load('images/menu_p1.png')
menu2 = pygame.image.load('images/menu_p2.png')
menu3 = pygame.image.load('images/menu_p3.png')
menu4 = pygame.image.load('images/menu_p4.png')
menu5 = pygame.image.load('images/menu_p5.png')
menu_list = [menu1, menu2, menu3, menu4, menu5]

display = pygame.display.set_mode((WIDTH, HEIGHT))

graph_dict = {0: False, 1: True, 2: False}
d_dict = {0: False, 1: True, 2: False}

clock = pygame.time.Clock()