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
        self.stab = True
        self.x_minimap = x_minimap
        self.y_minimap = y_minimap
        self.minimap_k = minimap_k
        self.sq = 0
        self.v = 0
        self.angle_of_view = 0
        print(self.s.map.world_map, sep='\n')
        self.stuck = False
        self.side = int(self.s.WIDTH * 0.018)
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
            self.s.display.fill((200, 200, 200))
            self.movement()
            self.guidance()
            self.ray_casting()
            #  self.ray_casting2()
            self.draw_minimap(self.minimap_k, self.x_minimap, self.y_minimap)

            fps_count_text_bl.set_another_text(str(int(self.s.clock.get_fps())) + ' FPS')
            fps_count_text.set_another_text(str(int(self.s.clock.get_fps())) + ' FPS')
            fps_count_text_bl.draw(self.s.display)
            fps_count_text.draw(self.s.display)

            pygame.display.flip()
            self.s.clock.tick(self.s.FPS)

    def draw_minimap(self, minimap_k, x, y):
        self.s.map.draw(self.s.display, x, y, k=minimap_k)
        pygame.draw.circle(self.s.display, (255, 0, 00), (x + self.pos(k=minimap_k)[0], y + self.pos(k=minimap_k)[1]),
                           int(self.s.WIDTH * 0.006) // minimap_k)

        pygame.draw.line(self.s.display, (255, 0, 0), (x + self.pos(k=minimap_k)[0], y + self.pos(k=minimap_k)[1]),
                         (x + (self.x + self.sq * math.sin(self.movement_angle * 3.14 / 180)) // minimap_k,
                          y + (self.y - self.v * 0.5 * math.cos(self.movement_angle * 3.14 / 180)) // minimap_k))
        pygame.draw.line(self.s.display, (255, 255, 255), (x + self.pos(k=minimap_k)[0], y + self.pos(k=minimap_k)[1]),
                         (x + (self.x + self.v * 0.5 * math.sin(self.movement_angle * 3.14 / 180)) // minimap_k,
                          y + (self.y - self.v * 0.5 * math.cos(self.movement_angle * 3.14 / 180)) // minimap_k))
        pygame.draw.line(self.s.display, (0, 0, 255), (x + self.pos(k=minimap_k)[0], y + self.pos(k=minimap_k)[1]),
                         (x + (self.x // minimap_k + self.s.WIDTH * 0.05 * math.cos(self.angle_of_view * 3.14 / 180)),
                          y + (self.y // minimap_k - self.s.WIDTH * 0.05 * -math.sin(self.angle_of_view * 3.14 / 180))))
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
        s = (self.v * t + (a_cur * (t ** 2)) / 2)
        self.sq = s
        dx = s * sin_a
        dy = s * cos_a
        print(self.x, self.y)
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
                temp = min(self.v * 0.008, 7)
                self.movement_angle += temp
                self.v = self.v * 0.97
                if self.stab is False:
                    self.angle_of_view += temp
            elif keys[pygame.K_a]:
                temp = min(self.v * 0.008, 7)
                self.movement_angle -= temp
                self.v = self.v * 0.97
                if self.stab is False:
                    self.angle_of_view -= temp

    def guidance(self):
        keys = pygame.key.get_pressed()
        t = 1 / self.s.FPS

        if keys[pygame.K_RIGHT]:
            self.angle_of_view += self.s.tower_v * t

        elif keys[pygame.K_LEFT]:
            self.angle_of_view -= self.s.tower_v * t

    def mapping(self, a, b):
        return (a // self.s.tile_w) * self.s.tile_w, (b // self.s.tile_h) * self.s.tile_h

    def ray_casting(self):
        x0, y0 = self.x, self.y
        xm, ym = self.mapping(x0, y0)
        print(xm, ym)
        cur_angle = self.angle_of_view - self.s.HALF_FOV + 0.00001
        sin_a = math.sin(cur_angle * 3.14 / 180)
        cos_a = math.cos(cur_angle * 3.14 / 180)
        print(cur_angle, cos_a, sin_a)
        for i in range(self.s.NUM_RAYS):
            sin_a = math.sin(cur_angle * 3.14 / 180)
            cos_a = math.cos(cur_angle * 3.14 / 180)
            if cos_a >= 0:
                x = xm + self.s.tile_w
                dx = 1
            else:
                x = xm
                dx = -1
            for j in range(0, self.s.WIDTH, self.s.tile_w):
                depth_v = (x - x0) / cos_a
                y = y0 + depth_v * sin_a
                if (self.mapping(x + dx, y)[0] // 100, self.mapping(x + dx, y)[1] // 100) in self.s.map.world_map:
                    print(1)
                    break
                x += dx * self.s.tile_w

            if sin_a >= 0:
                y = ym + self.s.tile_h
                dy = 1
            else:
                y = ym
                dy = -1
            for j in range(0, self.s.HEIGHT, self.s.tile_h):
                depth_h = (y - y0) / sin_a
                x = x0 + depth_h * cos_a
                if (self.mapping(x, y + dy)[0] // 100, self.mapping(x, y + dy)[1] // 100) in self.s.map.world_map:
                    break
                y += dy * self.s.tile_h

            depth = depth_v if depth_v < depth_h else depth_h
            print(depth_v)
            depth *= math.cos((self.angle_of_view - cur_angle) * 3.14 / 180)
            proj_height = self.s.PROJ_COEFF / depth
            c = 255 / (1 + depth * depth * 0.0004)
            color = (int(c), int(c), int(c))
            pygame.draw.rect(self.s.display, color,
                             (i * self.s.SCALE, self.s.HEIGHT // 2 - proj_height // 2, self.s.SCALE, proj_height))
            cur_angle += self.s.DELTA_ANGLE

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
s = TankSettings()
ex = Tank(s, 150, 150, 90, 1, 0, 0)
ex.start()
