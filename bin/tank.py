import pygame
import sys
import math
from bin.text import Text

class Tank:
    def __init__(self, settings, x, y, movement_angle):
        self.s = settings
        self.x = x
        self.y = y
        self.v = 0
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

            for x, y in self.s.world_map:
                pygame.draw.rect(self.s.display, (50, 60, 50), (x, y, self.s.tile_w, self.s.tile_h), int(self.s.WIDTH * 0.002))
            fps_count_text_bl.set_another_text(str(int(self.s.clock.get_fps())) + ' FPS')
            fps_count_text.set_another_text(str(int(self.s.clock.get_fps())) + ' FPS')
            fps_count_text_bl.draw(self.s.display)
            fps_count_text.draw(self.s.display)

            pygame.display.flip()
            self.s.clock.tick(self.s.FPS)

    def movement(self):
        keys = pygame.key.get_pressed()
        t = 1 / self.s.FPS
        cos_a = math.cos(self.movement_angle * 3.14 / 180)
        sin_a = math.sin(self.movement_angle * 3.14 / 180)

        if keys[pygame.K_w]:
            self.v = max(min(self.v + self.s.a_w * t, self.s.max_speed_w), self.s.max_speed_s)
            s = int(self.v * t + (self.s.a_w * (t ** 2)) / 2)
            self.y -= s * cos_a
            self.x += s * sin_a


        elif keys[pygame.K_s]:
            self.v = max(min(self.v + self.s.a_s * t, self.s.max_speed_w), self.s.max_speed_s)
            s = int(self.v * t + (self.s.a_s * (t ** 2)) / 2)
            self.y -= s * cos_a
            self.x += s * sin_a

        else:
            if self.v > 0:
                s = round(self.v * t - (self.s.a_stop * (t ** 2)) / 2)
                self.v = max(self.v - self.s.a_stop * t, 0)
                self.y -= s * cos_a
                self.x += s * sin_a
            elif self.v < 0:
                s = round(self.v * t + (self.s.a_stop * (t ** 2)) / 2)
                self.v = min(self.v + self.s.a_stop * t, 0)
                self.y -= s * cos_a
                self.x += s * sin_a
        print(self.v)

        if self.v != 0:

            if keys[pygame.K_d]:
                self.movement_angle += self.v * 0.008
                self.v = self.v * 0.95

            elif keys[pygame.K_a]:
                self.movement_angle -= self.v * 0.008
                self.v = self.v * 0.95

    def pos(self):
        return (self.x, self.y)
