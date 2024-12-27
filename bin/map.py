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
                if char == '0':
                    self.world_map.add((i, j))
                    self.collision_walls.append(pygame.Rect(i * self.tile_w, j * self.tile_h, self.tile_w, self.tile_h))

    def draw(self, display, x0, y0, k=1, floor=None, walls=None):
        if floor:
            display.blit(floor, (x0, y0))
        for x, y in self.world_map:
            if walls:
                display.blit(walls, (x0 + x * self.tile_w // k, y0 + y * self.tile_h // k))
            else:
                pygame.draw.rect(display, self.color,
                             (x0 + x * self.tile_w // k, y0 + y * self.tile_h // k, self.tile_w // k, self.tile_h // k),
                             max(int(self.width) // k, 1))
