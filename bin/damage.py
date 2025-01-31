import random


class Damage:
    def __init__(self, tank):
        # танк
        self.tank = tank
        # координаты зон с минами
        self.mine_coords = self.tank.s.mine_coords
        # координаты зон с FPV-дронами
        self.fpv_coords = self.tank.s.fpv_coords
        # счет времени для дронов
        self.fpv_time = self.tank.s.fpv_time
        self.fpv_timer = 0

    # проверка мин
    def check_mines(self):
        if (self.tank.x // self.tank.s.tile_w, self.tank.y // self.tank.s.tile_h) in self.mine_coords:
            p = random.randint(35, 100)
            if p > 60:
                self.tank.death = True
            if self.tank.death:
                self.tank.cause = 'наезд на мину'

    # проверка дронов
    def check_drones(self):
        if (self.tank.x // self.tank.s.tile_w, self.tank.y // self.tank.s.tile_h) in self.fpv_coords:
            if self.tank.v == 0:
                self.fpv_timer += 1 / self.tank.s.FPS
            elif self.tank.v != 0:
                self.fpv_timer = 0
            if self.fpv_timer >= 7:
                self.tank.s.fpv_sound.set_volume(self.tank.s.volume_general / 100 * self.tank.s.volume_music / 100)
                self.tank.s.fpv_sound.play()
        if self.fpv_timer > self.fpv_time:
            self.tank.death = True
            self.tank.cause = 'FPV-дрон'
