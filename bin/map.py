import pygame


class Map:
    def __init__(self, mini_map, tile_w, tile_h, width=0, color=(50, 60, 50)):
        # миникарта
        self.mini_map = mini_map
        self.world_map = set()
        self.world_map_dict = {}
        # параметры миникарты
        self.tile_w = tile_w
        self.tile_h = tile_h
        self.width = width
        self.color = color
        # словарь и множество с координатами стен
        for j, row in enumerate(self.mini_map):
            for i, char in enumerate(row):
                if char != '.':
                    self.world_map.add((i, j))
                if char == '1':
                    self.world_map_dict[(i, j)] = '1'
                elif char == '3':
                    self.world_map_dict[(i, j)] = '3'
                elif char == '2':
                    self.world_map_dict[(i, j)] = '2'
                elif char == '5':
                    self.world_map_dict[(i, j)] = '5'
                elif char == '7':
                    self.world_map_dict[(i, j)] = '7'
                elif char == '9':
                    self.world_map_dict[(i, j)] = '9'
    # отображение миникарты
    def draw(self, display, x0, y0, k=1, floor=None, walls=None):
        if floor:
            display.blit(floor, (x0, y0))
        for x, y in self.world_map:
            if walls:
                display.blit(walls, (x0 + x * self.tile_w // k, y0 + y * self.tile_h // k))
            else:
                pygame.draw.rect(display, self.color,
                                 (x0 + x * self.tile_w // k, y0 + y * self.tile_h // k, self.tile_w // k,
                                  self.tile_h // k),
                                 max(int(self.width) // k, 1))
