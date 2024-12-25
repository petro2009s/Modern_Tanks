import pygame
import sys
import math
from bin.text import Text
from bin.test_settings import TankSettings

class Tank:
    def __init__(self, settings, x, y, movement_angle):
        self.s = settings
        self.x = x
        self.y = y
        self.v = 0
        self.side = int(self.s.WIDTH * 0.015)
        self.tank_rect = pygame.Rect(x, y, self.side, self.side)
        self.movement_angle = movement_angle

    def start(self):
        show = True
        fps_count_text_bl = Text(self.s.WIDTH * 0.961, self.s.HEIGHT * 0.972, (0, 0, 0),
                                 str(int(self.s.clock.get_fps())) + ' FPS', int(self.s.WIDTH * 0.0104),
                                 is_topleft=True)
        fps_count_text = Text(self.s.WIDTH * 0.96, self.s.HEIGHT * 0.97, (200, 200, 200),
                              str(int(self.s.clock.get_fps())) + ' FPS', int(self.s.WIDTH * 0.0104),
                              is_topleft=True)
        while show:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.s.display.fill((50, 100, 255))
            self.movement()
            pygame.draw.circle(self.s.display, (255, 0, 00), self.pos(), int(self.s.WIDTH * 0.006))
            pygame.draw.line(self.s.display, (255, 0, 0), self.pos(),
                             (self.x + self.v * 0.5 * math.sin(self.movement_angle * 3.14 / 180),
                              self.y - self.v * 0.5 * math.cos(self.movement_angle * 3.14 / 180)))

            self.s.map.draw(self.s.display)
            fps_count_text_bl.set_another_text(str(int(self.s.clock.get_fps())) + ' FPS')
            fps_count_text.set_another_text(str(int(self.s.clock.get_fps())) + ' FPS')
            fps_count_text_bl.draw(self.s.display)
            fps_count_text.draw(self.s.display)

            pygame.display.flip()
            self.s.clock.tick(self.s.FPS)

    def movement(self):
        keys = pygame.key.get_pressed()
        self.tank_rect.center = self.x, self.y
        t = 1 / self.s.FPS
        cos_a = math.cos(self.movement_angle * 3.14 / 180)
        sin_a = math.sin(self.movement_angle * 3.14 / 180)
        a_cur = 0
        v = 0
        if keys[pygame.K_w]:
            v = max(min(self.v + self.s.a_w * t, self.s.max_speed_w), self.s.max_speed_s)
            a_cur = self.s.a_w

        elif keys[pygame.K_s]:
            v = max(min(self.v + self.s.a_s * t, self.s.max_speed_w), self.s.max_speed_s)
            a_cur = self.s.a_s
        else:
            if self.v > 0:
                v = max(self.v - self.s.a_stop * t, 0)
                a_cur = -self.s.a_stop
            elif self.v < 0:
                v = min(self.v + self.s.a_stop * t, 0)
                a_cur = self.s.a_stop
        s = round(self.v * t + (a_cur * (t ** 2)) / 2)
        dx = s * sin_a
        dy = s * cos_a

        # self.check_collisions(dx, dy)
        if dx != 0 or dy != 0:
            self.collisions(dx, dy)
        else:
            self.y -= dy
            self.x += dx
        self.v = v

        if self.v > self.s.min_speed_ad or self.v < 0:
            if keys[pygame.K_d]:
                self.movement_angle += min(self.v * 0.008, 7)
                self.v = self.v * 0.95

            elif keys[pygame.K_a]:
                self.movement_angle -= min(self.v * 0.008, 7)
                self.v = self.v * 0.95

    def check_collisions(self, dx, dy):
        next_rect = self.tank_rect.copy()
        next_rect.move_ip(dx, dy)
        hits = next_rect.collidelistall(self.s.map.collision_walls)
        if len(hits) > 0:
            delta_x = 0
            delta_y = 0
            for i in hits:
                hit = self.s.map.collision_walls[i]
                if dx > 0:
                    delta_x += next_rect.right - hit.left
                else:
                    delta_x += hit.right - next_rect.left
                if dy > 0:
                    delta_y += next_rect.bottom - hit.top
                else:
                    delta_y += hit.bottom - next_rect.top
            print(delta_x, delta_y)
            if abs(delta_x - delta_y) < 10:
                dx = 0
                dy = 0
            elif delta_y > delta_x:
                dx = 0
            elif delta_x > delta_y:
                dy = 0
        self.x += dx
        self.y -= dy

    def check_wall(self, x, y):

        return (x, y) in self.s.map.world_map
    def collisions(self, dx, dy):
        print(0.5, self.x, self.y, dx, dy)
        # if not self.check_wall((self.x + dx) // self.s.tile_w, (self.y + dy) // self.s.tile_h):
        #     self.y -= dy
        #     self.x += dx
        #     print(1, self.x, self.y)
        if self.check_wall(self.x // self.s.tile_w, self.y // self.s.tile_h):
            print(2)
            self.y += dy
            self.x -= dx
        elif not self.check_wall(self.x // self.s.tile_w, self.y // self.s.tile_h):
            self.y -= dy
            self.x += dx
            print(2.5)
        elif self.check_wall((self.x + dx) // self.s.tile_w, self.y // self.s.tile_h):
            self.y -= dy
            print(3)

        elif self.check_wall(self.x // self.s.tile_w, (self.y - dy) // self.s.tile_h):
            print(4)
            print(dy)
            self.x += dx




    def pos(self):
        return (self.x, self.y)


# s = TankSettings()
# ex = Tank(s, 150, 150, 0)
# ex.start()