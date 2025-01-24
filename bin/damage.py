import pygame
import random

class Damage:
    def __init__(self, tank):
        self.tank = tank
        self.mine_coords = self.tank.s.mine_coords
        self.fpv_coords = self.tank.s.fpv_coords
        self.fpv_time = self.tank.s.fpv_time
        self.fpv_timer = 0
    def check_mines(self):
        # print((self.tank.x // self.tank.s.tile_w, self.tank.y // self.tank.s.tile_h))
        if (self.tank.x // self.tank.s.tile_w, self.tank.y // self.tank.s.tile_h) in self.mine_coords:
            p = random.randint(35, 100)
            if p > 60:
                self.tank.death = True
            if self.tank.death:
                self.tank.cause = 'наезд на мину'
            # print(self.tank.death)
    def check_drones(self):
        print((self.tank.x // self.tank.s.tile_w, self.tank.y // self.tank.s.tile_h) in self.fpv_coords, self.fpv_timer)
        if (self.tank.x // self.tank.s.tile_w, self.tank.y // self.tank.s.tile_h) in self.fpv_coords:
            if self.tank.v == 0:
                self.fpv_timer += 1 / self.tank.s.FPS
            elif self.tank.v != 0:
                self.fpv_timer = 0

        if self.fpv_timer > self.fpv_time:
            self.tank.death = True
            self.tank.cause = 'FPV-дрон'