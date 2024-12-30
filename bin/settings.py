import pygame
import gif_pygame
import os
import screeninfo
from bin.bd import DBController
from bin.map import Map
import math

class Settings:
    def __init__(self):

        self.bd = DBController('resources/ModernTanksDB')
        # self.bd.clear()
        self.width_m = screeninfo.get_monitors()[0].width
        self.height_m = screeninfo.get_monitors()[0].height
        self.WIDTH = self.bd.select('size_table', 'width')[0][0]
        self.HEIGHT = self.bd.select('size_table', 'height')[0][0]
        if self.width_m < self.WIDTH or self.height_m < self.HEIGHT:
            self.WIDTH = self.width_m
            self.HEIGHT = self.height_m
            self.bd.update_to_db("size_table", "(width, height)", f"({self.WIDTH}, {self.HEIGHT})")
        self.size_text_b = int(self.WIDTH * 0.01875)
        self.size_list = pygame.display.list_modes()
        self.size_on_text = [self.WIDTH, self.HEIGHT]

        self.button_color = (50, 60, 50)
        pygame.init()
        self.display = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.icon = pygame.image.load('resources/images/icon_test2_p.png').convert()
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        if self.bd.select('full_table', '[on]')[0][0]:
            pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.FULLSCREEN)
        else:
            if self.width_m == self.WIDTH and self.height_m == self.HEIGHT:
                pygame.display.set_mode((self.WIDTH, self.HEIGHT - 40))
            else:
                pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        self.menu1 = pygame.image.load('resources/images/menu_p1.png').convert()
        self.menu2 = pygame.image.load('resources/images/menu_p2.png').convert()
        self.menu3 = pygame.image.load('resources/images/menu_p3.png').convert()
        self.menu4 = pygame.image.load('resources/images/menu_p4.png').convert()
        self.menu5 = pygame.image.load('resources/images/menu_p5.png').convert()
        self.gif = gif_pygame.load("resources/images/menu_g.gif")
        gif_pygame.transform.scale(self.gif, (self.WIDTH, self.HEIGHT))
        self.cursor_base = pygame.image.load('resources/images/cursor.png').convert_alpha()
        self.cursor = pygame.transform.scale(self.cursor_base, (self.WIDTH * 0.03125, self.WIDTH * 0.03125))
        self.menu_list = [self.menu1, self.menu2, self.menu3, self.menu4, self.menu5]
        for i in range(len(self.menu_list)):
            self.menu_list[i] = pygame.transform.scale(self.menu_list[i], (self.WIDTH, self.HEIGHT))

        self.music_menu = pygame.mixer.Sound("resources/sounds/music_menu.mp3")

        self.graph_dict = [self.bd.select('graph_table', 'low')[0][0], self.bd.select('graph_table', 'mid')[0][0],
                           self.bd.select('graph_table', 'high')[0][0]]
        self.d_dict = [self.bd.select('d_table', 'low')[0][0], self.bd.select('d_table', 'mid')[0][0],
                       self.bd.select('d_table', 'high')[0][0]]
        self.fps_dict = [self.bd.select('FPS_table', 'low')[0][0], self.bd.select('FPS_table', 'mid')[0][0],
                         self.bd.select('FPS_table', 'high')[0][0]]
        self.full_dict = [bool(self.display.get_flags() & pygame.FULLSCREEN),
                          not bool(self.display.get_flags() & pygame.FULLSCREEN)]
        self.volume_general = self.bd.select('volume_table', 'volume_general')[0][0]
        self.volume_music = self.bd.select('volume_table', 'volume_music')[0][0]
        self.volume_sound = self.bd.select('volume_table', 'volume_sound')[0][0]

        self.tank_dict = {0: True}
        self.lvl_dict = {0: True}
        self.clock = pygame.time.Clock()
        fps = self.bd.select('FPS_table', '*')[0]
        fps_dict = {0: 30, 1: 60, 2: 90}
        self.FPS = fps_dict[[i for i in range(3) if fps[i] == 1][0]]
        # self.FPS = 10000

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

        self.a_w = self.WIDTH * 0.12 * (self.FPS / 60)
        self.a_s = -self.WIDTH * 0.4 * (self.FPS / 60)
        self.a_stop = self.WIDTH * 0.4 * (self.FPS / 60)
        self.max_speed_w = self.WIDTH * 0.5 * (self.FPS / 60)
        self.max_speed_s = -self.WIDTH * 0.03 * (self.FPS / 60)
        self.min_speed_ad = self.WIDTH * 0.03 * (self.FPS / 60) * 10 / 60

        self.minimap_k = 5
        self.world_map = ['00000000',
                          '0......0',
                          '0......0',
                          '0...0..0',
                          '0......0',
                          '0..0.0.0',
                          '0......0',
                          '0...0..0',
                          '0......0',
                          '00000000'
                          ]
        self.tile_w = (self.WIDTH // len(self.world_map[0]))
        self.tile_h = (self.HEIGHT // len(self.world_map))
        self.map = Map(self.world_map, self.tile_w, self.tile_h, self.WIDTH * 0.002)
        self.minimap_tank_base = pygame.image.load('resources/images/tank_minimap.png').convert_alpha()
        self.minimap_tank = pygame.transform.scale(self.minimap_tank_base, (self.WIDTH * 0.0625 // self.minimap_k, self.WIDTH * 0.0625 // self.minimap_k))
        self.floor_base = pygame.image.load('resources/images/floor.png').convert()
        self.floor = pygame.transform.scale(self.floor_base, (self.tile_w * len(self.world_map[0]) // self.minimap_k, self.tile_h * len(self.world_map) // self.minimap_k))

        self.wall_base = pygame.image.load('resources/images/wall.png').convert()
        self.wall = pygame.transform.scale(self.wall_base,
                                           (self.tile_w // self.minimap_k, self.tile_h // self.minimap_k))
        self.tower_v = 20
        self.optic_scope_width = self.HEIGHT
        self.FOV = 12
        self.HALF_FOV = self.FOV // 2
        self.NUM_RAYS = 100
        self.DELTA_ANGLE = self.FOV / self.NUM_RAYS
        self.DIST = self.NUM_RAYS / (2 * math.tan(self.HALF_FOV * 3.14 / 180))
        self.PROJ_COEFF = 3 * self.DIST * self.tile_w
        self.SCALE = self.optic_scope_width // self.NUM_RAYS
    def update_db(self):
        self.bd.update_to_db("graph_table", "(low, mid, high)",
                             f"({self.graph_dict[0]}, {self.graph_dict[1]}, {self.graph_dict[2]})")
        self.bd.update_to_db("d_table", "(low, mid, high)", f"({self.d_dict[0]}, {self.d_dict[1]}, {self.d_dict[2]})")
        self.bd.update_to_db("FPS_table", "(low, mid, high)",
                             f"({self.fps_dict[0]}, {self.fps_dict[1]}, {self.fps_dict[2]})")
        self.bd.update_to_db("volume_table", "(volume_music, volume_sound, volume_general)",
                             f"({self.volume_music}, {self.volume_sound}, {self.volume_general})")
        self.bd.update_to_db("full_table", "([on], off)", f"({self.full_dict[0]}, {self.full_dict[1]})")
        self.bd.update_to_db("size_table", "(width, height)", f"({self.WIDTH}, {self.HEIGHT})")

    def update_size(self):
        gif_pygame.transform.scale(self.gif, (self.WIDTH, self.HEIGHT))
        for i in range(len(self.menu_list)):
            self.menu_list[i] = pygame.transform.scale(self.menu_list[i], (self.WIDTH, self.HEIGHT))
        self.cursor = pygame.transform.scale(self.cursor_base, (self.WIDTH * 0.03125, self.WIDTH * 0.03125))
        self.size_text_b = int(self.WIDTH * 0.01875)

        self.a_w = self.WIDTH * 0.12 * (self.FPS / 60)
        self.a_s = -self.WIDTH * 0.4 * (self.FPS / 60)
        self.a_stop = self.WIDTH * 0.4 * (self.FPS / 60)
        self.max_speed_w = self.WIDTH * 0.5 * (self.FPS / 60)
        self.max_speed_s = -self.WIDTH * 0.03 * (self.FPS / 60)
        self.min_speed_ad = self.WIDTH * 0.03 * (self.FPS / 60) * 10 / 60

        self.tile_w = (self.WIDTH // len(self.world_map[0]))
        self.tile_h = (self.HEIGHT // len(self.world_map))
        self.map = Map(self.world_map, self.tile_w, self.tile_h, self.WIDTH * 0.002)
        self.floor = pygame.transform.scale(self.floor_base,
                                            (self.tile_w * len(self.world_map[0]) // self.minimap_k, self.tile_h * len(self.world_map) // self.minimap_k))
        self.wall = pygame.transform.scale(self.wall_base,
                                           (self.tile_w // self.minimap_k, self.tile_h // self.minimap_k))

        self.minimap_tank = pygame.transform.scale(self.minimap_tank_base, (self.WIDTH * 0.0625 // self.minimap_k, self.WIDTH * 0.0625 // self.minimap_k))