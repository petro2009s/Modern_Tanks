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
        if (self.width_m < self.WIDTH or self.height_m < self.HEIGHT) and self.bd.select('full_table', 'off')[0][0]:
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


        self.minimap_k = 5
        self.world_map = ['00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
                          '0...................................................................................................0',
                          '0....0...........0000.................1.............................................................0',
                          '0...0................................11.............................................................0',
                          '0...................................1111............................................................0',
                          '0..0...............010...............11.............................................................0',
                          '0...................................................................................................0',
                          '0...0...........00..................................................................................0',
                          '0....0..............................................................................................0',
                          '0...................................................................................................0',
                          '0..........1111.....................................................................................0',
                          '0...................................................................................................0',
                          '0...................................................................................................0',
                          '0...................................................................................................0',
                          '0...................................................................................................0',
                          '0...................................................................................................0',
                          '0...................................................................................................0',
                          '0..........1111.....................................................................................0',
                          '0...................................................................................................0',
                          '0...................................................................................................0',
                          '0...................................................................................................0',
                          '0...................................................................................................0',
                          '0...................................................................................................0',
                          '0...................................................................................................0',
                          '0..........1111.....................................................................................0',
                          '0...................................................................................................0',
                          '0...................................................................................................0',
                          '0...................................................................................................0',
                          '0...................................................................................................0',
                          '0...................................................................................................0',
                          '0...................................................................................................0',
                          '0...................................................................................................0',
                          '0...................................................................................................0',
                          '0...................................................................................................0',
                          '0...................................................................................................0',
                          '0...................................................................................................0',
                          '0...................................................................................................0',
                          '0..........1111.....................................................................................0',
                          '0...................................................................................................0',
                          '0...................................................................................................0',
                          '0...................................................................................................0',
                          '0...................................................................................................0',
                          '0...................................................................................................0',
                          '0...................................................................................................0',
                          '0...................................................................................................0',
                          '0...................................................................................................0',
                          '0...................................................................................................0',
                          '0...................................................................................................0',
                          '0...................................................................................................0',
                          '0...................................................................................................0',
                          '0..........1111.....................................................................................0',
                          '0...................................................................................................0',
                          '0...................................................................................................0',
                          '0...................................................................................................0',
                          '0...................................................................................................0',
                          '0...................................................................................................0',
                          '0...................................................................................................0',
                          '0...................................................................................................0',
                          '0...................................................................................................0',
                          '0...................................................................................................0',
                          '0...................................................................................................0',
                          '0...................................................................................................0',
                          '0...................................................................................................0',
                          '0..........1111.....................................................................................0',
                          '0...................................................................................................0',
                          '0...................................................................................................0',
                          '0...................................................................................................0',
                          '0...................................................................................................0',
                          '0...................................................................................................0',
                          '0...................................................................................................0',
                          '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
                          ]
        self.world_map2 = ['0000000000000000',
                          '0..............0',
                          '0.......0000...0',
                          '0...0.....11...0',
                          '0..............0',
                          '0..............0',
                          '0.....11.......0',
                          '0..............0',
                          '0..............0',
                          '0000000000000000']


        self.tile_w = (self.WIDTH // len(self.world_map[0]))
        self.tile_h = (self.WIDTH // len(self.world_map[0]))
        self.map_width = self.tile_w * len(self.world_map[0])
        self.map_height = self.tile_h * len(self.world_map)
        self.map = Map(self.world_map, self.tile_w, self.tile_h, self.WIDTH * 0.002)
        self.minimap_tank_base = pygame.image.load('resources/images/tank_minimap_base.png').convert_alpha()
        self.minimap_tank_tower_base = pygame.image.load('resources/images/tank_minimap_tower.png').convert_alpha()
        self.minimap_tank_b = pygame.transform.scale(self.minimap_tank_base,
                                                     (self.WIDTH * 0.0625 // self.minimap_k, self.WIDTH * 0.0625 // self.minimap_k))
        self.minimap_tank_tower = pygame.transform.scale(self.minimap_tank_tower_base,
                                                         (self.WIDTH * 0.0625 // self.minimap_k, self.WIDTH * 0.0625 // self.minimap_k))

        self.side = min(int(self.WIDTH * 0.02), int(self.tile_w * 0.8))
        self.a_w = self.WIDTH * 0.05 * (self.FPS / 60) * (7 / self.side)
        self.a_s = -self.WIDTH * 0.1 * (self.FPS / 60) * (7 / self.side)
        self.a_stop = self.WIDTH * 0.1 * (self.FPS / 60) * (7 / self.side)
        self.max_speed_w = self.WIDTH * 0.2 * (self.FPS / 60) * (7 / self.side)
        self.max_speed_s = -self.WIDTH * 0.01 * (self.FPS / 60) * (7 / self.side)
        self.min_speed_ad = self.WIDTH * 0.01 * (self.FPS / 60) * 10 / 60 * (7 / self.side)

        self.tower_v = 20
        self.vertical_v = 30

        self.optic_scope_width = self.HEIGHT
        self.FOV_optic = 12
        self.HALF_FOV_optic = self.FOV_optic // 2
        self.NUM_RAYS = 150
        self.DELTA_ANGLE_optic = self.FOV_optic / self.NUM_RAYS
        self.DIST_optic = self.NUM_RAYS / (2 * math.tan(self.HALF_FOV_optic * 3.14 / 180))
        self.PROJ_COEFF_optic = 70 * self.HEIGHT

        if self.optic_scope_width % self.NUM_RAYS == 0:
            self.SCALE_optic = self.optic_scope_width // self.NUM_RAYS
        else:
            self.SCALE_optic = int(self.optic_scope_width / self.NUM_RAYS) + 1

        self.FOV_optic_zoom = 4
        self.HALF_FOV_optic_zoom = self.FOV_optic_zoom // 2
        self.DELTA_ANGLE_optic_zoom = self.FOV_optic_zoom / self.NUM_RAYS
        self.DIST_optic_zoom = self.NUM_RAYS / (2 * math.tan(self.HALF_FOV_optic_zoom * 3.14 / 180))
        self.PROJ_COEFF_optic_zoom = 210 * self.HEIGHT
        print(self.PROJ_COEFF_optic_zoom)
        if self.optic_scope_width % self.NUM_RAYS == 0:
            self.SCALE_optic_zoom = self.optic_scope_width // self.NUM_RAYS
        else:
            self.SCALE_optic_zoom = int(self.optic_scope_width / self.NUM_RAYS) + 1

        self.optic_sight_base = pygame.image.load('resources/images/sosna-u_optic.png').convert_alpha()
        self.optic_sight = pygame.transform.scale(self.optic_sight_base,
                                                  (self.HEIGHT, self.HEIGHT))

        self.optic_sight_zoom_base = pygame.image.load('resources/images/sosna-u_optic_zoom.png').convert_alpha()
        self.optic_sight_zoom = pygame.transform.scale(self.optic_sight_zoom_base,
                                                  (self.HEIGHT, self.HEIGHT))
        self.gunner_site_base = pygame.image.load('resources/images/gunner_site.png').convert_alpha()
        self.gunner_site = pygame.transform.scale(self.gunner_site_base,
                                                  (self.WIDTH, self.HEIGHT))
        self.texture_w = self.WIDTH * 0.6
        self.texture_h = self.WIDTH * 0.6
        self.texture_scale = self.texture_w // self.tile_w
        self.texture_1_base = pygame.image.load('resources/images/forest.png').convert_alpha()
        self.texture_2_base = pygame.image.load('resources/images/building.png').convert_alpha()
        self.textures = {'0': pygame.transform.scale(self.texture_1_base,
                                                     (self.texture_w, self.texture_h)),
                         '1': pygame.transform.scale(self.texture_2_base,
                                                     (self.texture_w, self.texture_h))}
        self.thermal_textures = {'0': (pygame.transform.scale(self.texture_1_base,
                                                              (self.texture_w, self.texture_h)), 30),
                                 '1': (pygame.transform.scale(self.texture_2_base,
                                                              (self.texture_w, self.texture_h)), 20)}
        for i, j in self.thermal_textures.items():
            thermal_texture(j[0], 20, 50)
        self.optic_sight_x = 0.5 * self.WIDTH
        self.optic_sight_y = 0.1 * self.WIDTH
        self.optic_sight_w_r = 0.2 * self.WIDTH
        self.optic_sight_h_r = 0.2 * self.WIDTH

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

        self.tile_w = (self.WIDTH // len(self.world_map[0]))
        self.tile_h = (self.WIDTH // len(self.world_map[0]))
        self.side = min(int(self.WIDTH * 0.02), int(self.tile_w * 0.8))
        self.a_w = self.WIDTH * 0.05 * (self.FPS / 60) * (7 / self.side)
        self.a_s = -self.WIDTH * 0.1 * (self.FPS / 60) * (7 / self.side)
        self.a_stop = self.WIDTH * 0.1 * (self.FPS / 60) * (7 / self.side)
        self.max_speed_w = self.WIDTH * 0.2 * (self.FPS / 60) * (7 / self.side)
        self.max_speed_s = -self.WIDTH * 0.01 * (self.FPS / 60) * (7 / self.side)
        self.min_speed_ad = self.WIDTH * 0.01 * (self.FPS / 60) * 10 / 60 * (7 / self.side)


        self.map = Map(self.world_map, self.tile_w, self.tile_h, self.WIDTH * 0.002)
        self.minimap_tank_b = pygame.transform.scale(self.minimap_tank_base,
                                                     (self.WIDTH * 0.0625 // self.minimap_k,
                                                      self.WIDTH * 0.0625 // self.minimap_k))
        self.minimap_tank_tower = pygame.transform.scale(self.minimap_tank_tower_base,
                                                         (self.WIDTH * 0.0625 // self.minimap_k,
                                                          self.WIDTH * 0.0625 // self.minimap_k))

        self.map_width = self.tile_w * len(self.world_map[0])
        self.map_height = self.tile_h * len(self.world_map)
        self.gunner_site = pygame.transform.scale(self.gunner_site_base,
                                                  (self.WIDTH, self.HEIGHT))
        self.texture_w = self.WIDTH * 0.6
        self.texture_h = self.WIDTH * 0.6
        self.texture_scale = self.texture_w // self.tile_w
        self.textures = {'0': pygame.transform.scale(self.texture_1_base,
                                                     (self.texture_w, self.texture_h)),
                         '1': pygame.transform.scale(self.texture_2_base,
                                                     (self.texture_w, self.texture_h))}
        self.optic_sight_x = 0.5 * self.WIDTH
        self.optic_sight_y = 0.1 * self.WIDTH
        self.optic_sight_w_r = 0.2 * self.WIDTH
        self.optic_sight_h_r = 0.2 * self.WIDTH

        self.optic_scope_width = self.HEIGHT
        self.PROJ_COEFF_optic = 70 * self.HEIGHT

        if self.optic_scope_width % self.NUM_RAYS == 0:
            self.SCALE_optic = self.optic_scope_width // self.NUM_RAYS
        else:
            self.SCALE_optic = int(self.optic_scope_width / self.NUM_RAYS) + 1

        self.PROJ_COEFF_optic_zoom = 210 * self.HEIGHT
        if self.optic_scope_width % self.NUM_RAYS == 0:
            self.SCALE_optic_zoom = self.optic_scope_width // self.NUM_RAYS
        else:
            self.SCALE_optic_zoom = int(self.optic_scope_width / self.NUM_RAYS) + 1

        self.optic_sight = pygame.transform.scale(self.optic_sight_base,
                                                  (self.HEIGHT, self.HEIGHT))

        self.optic_sight_zoom = pygame.transform.scale(self.optic_sight_zoom_base,
                                                  (self.HEIGHT, self.HEIGHT))


def thermal_texture(surface, t, max_t):
    w, h = surface.get_size()
    for x in range(w):
        for y in range(h):
            a = surface.get_at((x, y))[3]
            r, g, b = surface.get_at((x, y))[0:3]
            color = min(r, g, b)
            color *= abs(t / max_t)
            color = max(max(color, 0), 5)
            surface.set_at((x, y), pygame.Color(color, color, color, a))
