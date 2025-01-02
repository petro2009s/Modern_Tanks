import math

import pygame
from bin.map import Map


class TankSettings():
    def __init__(self):
        pygame.init()
        self.WIDTH = 1000
        self.HEIGHT = 1000
        self.display = pygame.display.set_mode((1000, 1000))
        self.a_w = 200
        self.a_s = -300
        self.a_stop = 300
        self.max_speed_w = 500
        self.max_speed_s = -300
        self.FPS = 60
        self.tower_v = 50
        self.tile_w = 100
        self.tile_h = 100
        self.min_speed_ad = 200 * 10 / 60
        self.clock = pygame.time.Clock()
        world_map = ['0000000000',
                     '0........0',
                     '0........0',
                     '0..0000..0',
                     '0........0',
                     '0...11...0',
                     '0........0',
                     '0........0',
                     '0........0',
                     '0000000000'
                     ]
        world_map2 = ['00000000',
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
        world_map3 = ['000000000000000000000000000000000000000000000000000000000000000000000',
                      '0...................................................................0',
                      '0...................................................................0',
                      '0...0...............................................................0',
                      '0...................................................................0',
                      '0..0.................................0..............................0',
                      '0...................................................................0',
                      '0...0...............................................................0',
                      '0...................................................................0',
                      '0...................................................................0',
                      '0...................................................................0',
                      '0..............................00000................................0',
                      '0...............................000.................................0',
                      '0................................00.................................0',
                      '0...................................................................0',
                      '0...................................................................0',
                      '0...................................................................0',
                      '000000000000000000000000000000000000000000000000000000000000000000000'
                      ]
        self.tile_w = int(self.WIDTH * 0.1)
        self.tile_h = int(self.HEIGHT * 0.1)
        self.map = Map(world_map, self.tile_w, self.tile_h, self.WIDTH * 0.002)
        self.minimap_tank_base = pygame.image.load('resources/images/tank_minimap_base.png').convert_alpha()
        self.minimap_tank_tower_base = pygame.image.load('resources/images/tank_minimap_tower.png').convert_alpha()
        self.floor_base = pygame.image.load('resources/images/floor.png').convert()
        self.floor = pygame.transform.scale(self.floor_base,
                                            (self.tile_w * len(world_map[0]), self.tile_h * len(world_map)))
        self.wall_base = pygame.image.load('resources/images/wall.png').convert()
        self.wall = pygame.transform.scale(self.wall_base,
                                           (self.tile_w, self.tile_h))
        self.cursor_base = pygame.image.load('resources/images/cursor.png').convert_alpha()
        self.cursor = pygame.transform.scale(self.cursor_base, (self.WIDTH * 0.03125, self.WIDTH * 0.03125))
        self.minimap_tank_b = pygame.transform.scale(self.minimap_tank_base,
                                                     (self.WIDTH * 0.03125, self.WIDTH * 0.03365))
        self.minimap_tank_tower = pygame.transform.scale(self.minimap_tank_tower_base,
                                                         (self.WIDTH * 0.03125, self.WIDTH * 0.03365))
        self.minimap_k = 5
        self.FOV = 12
        self.HALF_FOV = self.FOV // 2
        self.NUM_RAYS = 150
        self.DELTA_ANGLE = self.FOV / self.NUM_RAYS
        self.DIST = self.NUM_RAYS / (2 * math.tan(self.HALF_FOV * 3.14 / 180))
        self.PROJ_COEFF = 0.4 * self.DIST * self.HEIGHT
        if self.HEIGHT % self.NUM_RAYS == 0:
            self.SCALE = self.HEIGHT // self.NUM_RAYS
        else:
            self.SCALE = self.HEIGHT / self.NUM_RAYS
        self.optic_sight_base = pygame.image.load('resources/images/sosna-u_optic.png').convert_alpha()
        self.optic_sight = pygame.transform.scale(self.optic_sight_base,
                                                  (self.HEIGHT, self.HEIGHT))
        self.gunner_site_base = pygame.image.load('resources/images/gunner_site.png').convert_alpha()
        self.gunner_site = pygame.transform.scale(self.gunner_site_base,
                                                  (self.WIDTH, self.HEIGHT))
        self.texture_w = 600
        self.texture_h = 600
        self.texture_scale = self.texture_w // self.tile_w
        self.texture_1_base = pygame.image.load('resources/images/wall.png').convert_alpha()
        self.texture_2_base = pygame.image.load('resources/images/floor.png').convert_alpha()
        self.textures = {'0': pygame.transform.scale(self.texture_1_base,
                                                     (self.texture_w, self.texture_h)),
                         '1': pygame.transform.scale(self.texture_2_base,
                                                     (self.texture_w, self.texture_h))}
        self.optic_sight_x = 200
        self.optic_sight_y = 200
        self.optic_sight_w_r = 100
        self.optic_sight_h_r = 100

        self.vertical_v = 30
