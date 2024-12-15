import pygame
import gif_pygame
import screeninfo

class Settings:
    def __init__(self):
        self.WIDTH = screeninfo.get_monitors()[0].width
        self.HEIGHT = screeninfo.get_monitors()[0].height
        self.size_text_b = int(self.WIDTH * 0.01875)

        self.button_color = (50, 60, 50)
        pygame.init()

        self.display = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.icon = pygame.image.load('resources/images/icon_test2_p.png').convert()

        self.menu1 = pygame.image.load('resources/images/menu_p1.png').convert()
        self.menu2 = pygame.image.load('resources/images/menu_p2.png').convert()
        self.menu3 = pygame.image.load('resources/images/menu_p3.png').convert()
        self.menu4 = pygame.image.load('resources/images/menu_p4.png').convert()
        self.menu5 = pygame.image.load('resources/images/menu_p5.png').convert()
        self.gif = gif_pygame.load("resources/images/menu_g.gif")
        gif_pygame.transform.scale(self.gif, (self.WIDTH, self.HEIGHT))
        self.menu_list = [self.menu1, self.menu2, self.menu3, self.menu4, self.menu5]
        for i in range(len(self.menu_list)):
            self.menu_list[i] = pygame.transform.scale(self.menu_list[i], (self.WIDTH, self.HEIGHT))

        self.graph_dict = {0: False, 1: True, 2: False}
        self.d_dict = {0: False, 1: True, 2: False}
        self.fps_dict = {0: False, 1: True, 2: False}

        self.tank_dict = {0: True}
        self.lvl_dict = {0: True}
        self.clock = pygame.time.Clock()
        self.FPS = 60

        with open('resources/descriptions/ammunition.txt', encoding='utf-8') as f:
            self.ammo = list(map(lambda x: x[:-1], f.readlines()))
        with open('resources/descriptions/T-90M_descr.txt', encoding='utf-8') as f:
            self.T_90M_descr = list(map(lambda x: x[:-1], f.readlines()))
        with open('resources/descriptions/T-90M_TTH.txt', encoding='utf-8') as f:
            self.T_90M_TTH = list(map(lambda x: x[:-1], f.readlines()))
        with open('resources/descriptions/guide.txt', encoding='utf-8') as f:
            self.guide_descr = list(map(lambda x: x[:-1], f.readlines()))

        self.MAX_AMMO = 22
        self.APFSDS_COUNT = 0
        self.HE_COUNT = 0
        self.HEAT_COUNT = 0