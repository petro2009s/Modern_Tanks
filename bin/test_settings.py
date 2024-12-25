import pygame
from bin.map import Map

class TankSettings():
    def __init__(self):
        pygame.init()
        self.WIDTH = 1000
        self.HEIGHT = 1000
        self.display = pygame.display.set_mode((1000, 1000))
        self.a_w = 120
        self.a_s = -300
        self.a_stop = 300
        self.max_speed_w = 500
        self.max_speed_s = -60
        self.FPS = 60
        self.tile_w = 100
        self.tile_h = 100
        self.min_speed_ad = self.WIDTH * 0.5 * (self.FPS / 60) * 5 / 60
        self.clock = pygame.time.Clock()
        world_map = ['OOOOOOOOOO',
                    'O........O',
                    'O........O',
                    'O...O....O',
                    'O........O',
                    'O..O.....O',
                    'O........O',
                    'O........O',
                    'O........O',
                    'OOOOOOOOOO'
        ]
        self.tile_w = self.WIDTH * 0.1
        self.tile_h = self.HEIGHT * 0.1
        self.map = Map(world_map, self.tile_w, self.tile_h, self.WIDTH * 0.002)