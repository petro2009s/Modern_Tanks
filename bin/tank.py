import pygame
import sys
import math
from bin.text import Text
from bin.test_settings import TankSettings


class Tank:
    def __init__(self, settings, x, y, movement_angle, minimap_k, x_minimap, y_minimap):
        self.s = settings
        self.x = x
        self.y = y
        self.x_minimap = x_minimap
        self.y_minimap = y_minimap
        self.minimap_k = minimap_k
        self.sq = 0
        self.v = 0
        self.angle_of_view = 0
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
            self.s.display.fill((0, 0, 0))
            self.movement()
            self.draw_minimap(self.minimap_k, self.x_minimap, self.y_minimap)

            fps_count_text_bl.set_another_text(str(int(self.s.clock.get_fps())) + ' FPS')
            fps_count_text.set_another_text(str(int(self.s.clock.get_fps())) + ' FPS')
            fps_count_text_bl.draw(self.s.display)
            fps_count_text.draw(self.s.display)

            pygame.display.flip()
            self.s.clock.tick(self.s.FPS)

    def draw_minimap(self, minimap_k, x, y):
        self.s.map.draw(self.s.display, x, y, k=minimap_k, floor=self.s.floor, walls=self.s.wall)
        pygame.draw.circle(self.s.display, (255, 0, 00), (x + self.pos(k=minimap_k)[0], y + self.pos(k=minimap_k)[1]),
                           int(self.s.WIDTH * 0.006) // minimap_k)

        pygame.draw.line(self.s.display, (255, 0, 0), (x + self.pos(k=minimap_k)[0], y + self.pos(k=minimap_k)[1]),
                         (x + (self.x + self.sq * math.sin(self.movement_angle * 3.14 / 180)) // minimap_k,
                          y + (self.y - self.v * 0.5 * math.cos(self.movement_angle * 3.14 / 180)) // minimap_k))
        pygame.draw.line(self.s.display, (255, 255, 255), (x + self.pos(k=minimap_k)[0], y + self.pos(k=minimap_k)[1]),
                         (x + (self.x + self.v * 0.5 * math.sin(self.movement_angle * 3.14 / 180)) // minimap_k,
                          y + (self.y - self.v * 0.5 * math.cos(self.movement_angle * 3.14 / 180)) // minimap_k))
        pygame.draw.line(self.s.display, (0, 0, 255), (x + self.pos(k=minimap_k)[0], y + self.pos(k=minimap_k)[1]),
                         (x + (self.x + self.s.WIDTH * 0.05 * math.sin(self.angle_of_view * 3.14 / 180)) // minimap_k,
                          y + (self.y - self.s.WIDTH * 0.05 * math.cos(self.angle_of_view * 3.14 / 180)) // minimap_k))
        pygame.draw.line(self.s.display, (0, 255, 0), (x + self.pos(k=minimap_k)[0], y + self.pos(k=minimap_k)[1]),
                         (x + (self.x + self.s.WIDTH * 0.05 * math.sin(self.movement_angle * 3.14 / 180)) // minimap_k,
                          y + (self.y - self.s.WIDTH * 0.05 * math.cos(self.movement_angle * 3.14 / 180)) // minimap_k))

        image = pygame.transform.rotate(self.s.minimap_tank, -self.movement_angle)
        rect = image.get_rect()
        rect.center = (x + self.pos(k=minimap_k)[0],
                       y + self.pos(k=minimap_k)[1])
        self.s.display.blit(image, rect)

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
        self.sq = s
        dx = s * sin_a
        dy = s * cos_a

        # self.check_collisions(dx, dy)
        if dx != 0 or dy != 0:
            self.collisions(dx, dy)
            if self.stuck:
                v *= 0.8
        else:
            self.y -= dy
            self.x += dx
        # v = 0 if self.stuck else v
        self.v = v

        if self.v > self.s.min_speed_ad or self.v < 0:
            if keys[pygame.K_d]:
                self.movement_angle += min(self.v * 0.008, 7)
                self.v = self.v * 0.97

            elif keys[pygame.K_a]:
                self.movement_angle -= min(self.v * 0.008, 7)
                self.v = self.v * 0.97

    def check_collisions(self, dx, dy):
        self.stuck = False
        next_rect = self.tank_rect.copy()
        next_rect.move_ip(dx, dy)
        hits = next_rect.collidelistall(self.s.map.collision_walls)
        delta_x = 0
        delta_y = 0
        ty = 0
        if dy != 0:
            ty = self.side // 2 * abs(dy) / dy
        tx = 0
        if dx != 0:
            tx = self.side // 2 * abs(dx) / dx
        if len(hits) > 0:
            print(dx, dy)
            for i in hits:
                hit = self.s.map.collision_walls[i]
                if dx > 0:
                    delta_x += next_rect.right - hit.left
                else:
                    delta_x += hit.right - next_rect.left
                if dy > 0:
                    delta_y -= next_rect.top - hit.bottom
                else:
                    delta_y -= hit.top - next_rect.bottom
            # print(delta_y)
            if abs(delta_x - delta_y) < 10:
                dx = 0
                dy = 0
            elif delta_x > delta_y:
                dy = -delta_y
                dx = 0
                print(1, delta_x, delta_y)
                self.stuck = True
            elif delta_y > delta_x:
                print(2, delta_x, delta_y)
                dx = delta_x
                dy = 0
                self.stuck = True

                # self.stuck = True
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

        if self.check_wall((self.x + tx + dx) // self.s.tile_w, (self.y) // self.s.tile_h):
            if tx > 0:
                temp = ((self.x + tx + dx) // self.s.tile_w) * self.s.tile_w
            else:
                temp = ((self.x + tx + dx) // self.s.tile_w + 1) * self.s.tile_w
            self.x = temp - tx
            self.stuck = True

        if self.check_wall(self.x // self.s.tile_w, (self.y - dy - ty) // self.s.tile_h):
            if ty > 0:
                temp = ((self.y - dy - ty) // self.s.tile_h + 1) * self.s.tile_h
            else:
                temp = ((self.y - dy - ty) // self.s.tile_h) * self.s.tile_h
            self.y = temp + ty
            self.stuck = True
        if not self.check_wall((self.x + tx + dx) // self.s.tile_w, (self.y - ty - dy) // self.s.tile_h):
            self.y -= dy
            self.x += dx
            self.stuck = False

    def pos(self, k=1):
        return (self.x // k, self.y // k)


# #
# s = TankSettings()
# ex = Tank(s, 150, 150, 0, 1, 0, 0)
# ex.start()
