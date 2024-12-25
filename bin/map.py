import pygame


class Map:
    def __init__(self, mini_map, tile_w, tile_h, width=0, color=(50, 60, 50)):
        self.mini_map = mini_map
        self.world_map = set()
        self.tile_w = tile_w
        self.tile_h = tile_h
        self.width = width
        self.color = color
        self.collision_walls = []
        for j, row in enumerate(self.mini_map):
            for i, char in enumerate(row):
                if char == 'O':
                    self.world_map.add((i, j))
                    self.collision_walls.append(pygame.Rect(i * self.tile_w, j * self.tile_h, self.tile_w, self.tile_h))


    def draw(self, display):
        for x, y in self.world_map:
            pygame.draw.rect(display, self.color, (x * self.tile_w, y * self.tile_h, self.tile_w, self.tile_h),
                             int(self.width))