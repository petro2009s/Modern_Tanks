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
        print(self.s.map.world_map, sep='\n')
        self.stuck = False
        self.side = int(self.s.WIDTH * 0.016)
        print(self.side)
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
            pygame.draw.rect(self.s.display, (50, 50, 50),
                             (self.tank_rect.x, self.tank_rect.y, self.tank_rect.width, self.tank_rect.height))
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

        # self.check(dx, dy)
        if dx != 0 or dy != 0:
            self.collisions(dx, dy)
            if self.stuck:
                v = 0
        else:
            self.y -= dy
            self.x += dx
        # v = 0 if self.stuck else v
        self.v = v

        if self.v > self.s.min_speed_ad or self.v < 0:
            if keys[pygame.K_d]:
                self.movement_angle += min(self.v * 0.008, 7)
                self.v = self.v * 0.95

            elif keys[pygame.K_a]:
                self.movement_angle -= min(self.v * 0.008, 7)
                self.v = self.v * 0.95

    def check_collisions(self, dx, dy):
        self.stuck = False
        next_rect = self.tank_rect.copy()
        next_rect.move_ip(dx, dy)
        hits = next_rect.collidelistall(self.s.map.collision_walls)
        delta_x = 0
        delta_y = 0
        if len(hits) > 0:
            print(dx, dy)
            for i in hits:
                hit = self.s.map.collision_walls[i]
                if dx > 0:
                    delta_x += next_rect.right - hit.left
                else:
                    delta_x += hit.right - next_rect.left
                if dy > 0:
                    delta_y -= next_rect.bottom - hit.top
                else:

                    delta_y += hit.bottom - next_rect.top
            # print(delta_y)
            if abs(delta_x - delta_y) < 10:
                dx = 0
                dy = 0
            elif delta_x > delta_y:
                dy = 0
                print(1, delta_x, delta_y)
            # self.stuck = True
            elif delta_y > delta_x:
                print(2, delta_x, delta_y)
                dx = 0

                # self.stuck = True
        self.x += dx
        self.y -= dy

    def check(self, dx, dy):
        self.stuck = False
        print()
        if dx != 0:
            delta_x = (self.side // 2) * abs(dx) / dx
            if self.check_wall((self.x + dx + delta_x) // self.s.tile_w, (self.y + delta_x) // self.s.tile_h):
                dx = 0
                print(1.5)
                self.stuck = True
            if self.check_wall((self.x + dx + delta_x) // self.s.tile_w, (self.y - delta_x) // self.s.tile_h):
                dx = 0
                print(2.5)
                self.stuck = True
        if dy != 0:
            delta_y = (self.side // 2) * abs(dy) / dy
            print((self.y - delta_y + dy), self.y)
            if self.check_wall((self.x + delta_y) // self.s.tile_w, (self.y - delta_y + dy) // self.s.tile_h):
                self.stuck = True
                print(1)
                dy = 0
            if self.check_wall((self.x - delta_y) // self.s.tile_w, (self.y + dy - delta_y) // self.s.tile_h):
                print(2)
                dy = 0
        self.x += dx
        self.y -= dy

    def check_wall(self, x, y):
        return (int(x), int(y)) in self.s.map.world_map

    def collisions(self, dx, dy):
        self.stuck = False
        ty = 0
        if dy != 0:
            ty = self.side // 2 * abs(dy) / dy
        tx = 0
        if dx != 0:
            tx = self.side // 2 * abs(dx) / dx

        if self.check_wall((self.x + tx + dx) // self.s.tile_w, (self.y - ty) // self.s.tile_h):
            print(((self.x + tx + dx) // self.s.tile_w + 1) * self.s.tile_w)
            if tx > 0:
                temp = ((self.x + tx + dx) // self.s.tile_w) * self.s.tile_w
            else:
                temp = ((self.x + tx + dx) // self.s.tile_w + 1) * self.s.tile_w
            self.x += temp - self.x - tx
            self.stuck = True
            print(3)

        if self.check_wall((self.x + tx) // self.s.tile_w, (self.y - dy - ty) // self.s.tile_h):
            print(4)
            if ty > 0:
                temp = ((self.y - dy - ty) // self.s.tile_h + 1) * self.s.tile_h
                print(((self.y - dy - ty) // self.s.tile_h) * self.s.tile_h)
            else:
                print(((self.y - dy - ty) // self.s.tile_h) * self.s.tile_h)
                temp = ((self.y - dy - ty) // self.s.tile_h) * self.s.tile_h
            print(dy)
            print(-temp + self.y - ty)

            self.y -= -temp + self.y - ty

            self.stuck = True
        if not self.check_wall((self.x + tx + dx) // self.s.tile_w, (self.y - ty - dy) // self.s.tile_h):
            self.y -= dy
            self.x += dx
            self.stuck = False
           # print(2.5, ((self.x + tx), (self.y - ty)))

    def pos(self):
        return (self.x, self.y)


# s = TankSettings()
# ex = Tank(s, 150, 150, 0)
# ex.start()
