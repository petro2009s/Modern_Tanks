import pygame
import sys
import math
from bin.text import Text
from bin.test_settings import TankSettings
from bin.buttons import SelectButton


class Tank:
    def __init__(self, settings, x, y, movement_angle, minimap_k, x_minimap, y_minimap):
        self.s = settings

        self.x = x
        self.y = y

        self.stab = True
        self.optic = False
        self.thermal = False
        self.zoom = False

        self.x_minimap = x_minimap
        self.y_minimap = y_minimap
        self.minimap_k = minimap_k

        self.v = 0
        self.depth = '0000'
        self.depth_m = '0000'
        self.angle_of_view = 0
        self.horizontal = 0
        self.thermal_horizontal = self.s.HEIGHT * -0.02
        print(self.s.map.world_map, sep='\n')
        print(self.x, self.y)

        self.stuck = False
        self.side = min(int(self.s.WIDTH * 0.02), int(self.s.tile_w * 0.8))
        print(self.side)

        self.sky = pygame.Rect(self.s.WIDTH // 2 - self.s.HEIGHT // 2, 0, self.s.HEIGHT,
                               self.horizontal + self.s.HEIGHT // 2)
        self.sky_thermal = pygame.Rect(self.s.thermal_x + (self.s.WIDTH - self.s.thermal_base_width) // 2, self.s.thermal_y, self.s.thermal_width,
                               self.thermal_horizontal + self.s.thermal_height // 2)
        self.sky_thermal_color = (135 * (20 / self.s.max_t), 135 * (20 / self.s.max_t), 135 * (20 / self.s.max_t))
        self.floor_thermal_color = (45 * (20 / self.s.max_t), 45 * (20 / self.s.max_t), 45 * (20 / self.s.max_t))

        self.tank_rect = pygame.Rect(x, y, self.side, self.side)
        self.movement_angle = movement_angle

    def start(self):
        print(sorted(self.s.map.world_map))
        show = True
        fps_count_text_bl = Text(self.s.WIDTH * 0.961, self.s.HEIGHT * 0.972, (0, 0, 0),
                                 str(int(self.s.clock.get_fps())) + ' FPS', int(self.s.WIDTH * 0.0104),
                                 is_topleft=True)
        fps_count_text = Text(self.s.WIDTH * 0.96, self.s.HEIGHT * 0.97, (200, 200, 200),
                              str(int(self.s.clock.get_fps())) + ' FPS', int(self.s.WIDTH * 0.0104),
                              is_topleft=True)
        optic_sight_button = SelectButton(self.s.optic_sight_x, self.s.optic_sight_y, self.s.optic_sight_w_r,
                                          self.s.optic_sight_h_r, 'прицел', font_size=20)
        thermal_sight_button = SelectButton(self.s.thermal_sight_x, self.s.thermal_sight_y, self.s.thermal_sight_w_r,
                                          self.s.thermal_sight_h_r, 'прицел', font_size=20)
        while show:
            optic_sight_button.check(pygame.mouse.get_pos())
            thermal_sight_button.check(pygame.mouse.get_pos())
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print(self.s.map.world_map, self.s.map.world_map_dict)
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.USEREVENT:
                    if event.button == optic_sight_button:
                        self.optic_sight()
                        print(1)
                    elif event.button == thermal_sight_button:
                        self.thermal_sight()
                        print(2)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        print('escape')
                        show = False
                optic_sight_button.handle_event(event)
                thermal_sight_button.handle_event(event)
            self.movement()
            self.guidance()
            self.s.display.blit(self.s.gunner_site, (0, 0))
            optic_sight_button.draw(self.s.display)
            thermal_sight_button.draw(self.s.display)
            self.draw_minimap(self.x_minimap, self.y_minimap)

            fps_count_text_bl.set_another_text(str(int(self.s.clock.get_fps())) + ' FPS')
            fps_count_text.set_another_text(str(int(self.s.clock.get_fps())) + ' FPS')
            fps_count_text_bl.draw(self.s.display)
            fps_count_text.draw(self.s.display)
            if pygame.mouse.get_focused():
                self.s.display.blit(self.s.cursor, pygame.mouse.get_pos())
            pygame.display.flip()
            self.s.clock.tick(self.s.FPS)

    def draw_minimap(self, x, y):
        self.s.map.draw(self.s.display, x, y, k=self.s.minimap_k)
        pygame.draw.circle(self.s.display, (255, 0, 00),
                           (x + self.pos(k=self.s.minimap_k)[0], y + self.pos(k=self.s.minimap_k)[1]),
                           int(self.s.WIDTH * 0.006) // self.s.minimap_k)

        pygame.draw.line(self.s.display, (255, 0, 0),
                         (x + self.pos(k=self.s.minimap_k)[0], y + self.pos(k=self.s.minimap_k)[1]),
                         (x + (self.x + self.sq * math.sin(self.movement_angle * 3.14 / 180)) // self.s.minimap_k,
                          y + (self.y - self.v * 0.5 * math.cos(self.movement_angle * 3.14 / 180)) // self.s.minimap_k))
        pygame.draw.line(self.s.display, (255, 255, 255),
                         (x + self.pos(k=self.s.minimap_k)[0], y + self.pos(k=self.s.minimap_k)[1]),
                         (x + (self.x + self.v * 0.5 * math.sin(self.movement_angle * 3.14 / 180)) // self.s.minimap_k,
                          y + (self.y - self.v * 0.5 * math.cos(self.movement_angle * 3.14 / 180)) // self.s.minimap_k))
        pygame.draw.line(self.s.display, (0, 0, 255),
                         (x + self.pos(k=self.s.minimap_k)[0], y + self.pos(k=self.s.minimap_k)[1]),
                         (x + (self.x // self.s.minimap_k + self.s.WIDTH * 0.05 * math.cos(
                             self.angle_of_view * 3.14 / 180)),
                          y + (self.y // self.s.minimap_k + self.s.WIDTH * 0.05 * math.sin(
                              self.angle_of_view * 3.14 / 180))))
        pygame.draw.line(self.s.display, (0, 255, 0),
                         (x + self.pos(k=self.s.minimap_k)[0], y + self.pos(k=self.s.minimap_k)[1]),
                         (x + (self.x + self.s.WIDTH * 0.05 * math.sin(
                             self.movement_angle * 3.14 / 180)) // self.s.minimap_k,
                          y + (self.y - self.s.WIDTH * 0.05 * math.cos(
                              self.movement_angle * 3.14 / 180)) // self.s.minimap_k))

        image = pygame.transform.rotate(self.s.minimap_tank_b, -self.movement_angle)
        rect = image.get_rect()
        rect.center = (x + self.pos(k=self.s.minimap_k)[0],
                       y + self.pos(k=self.s.minimap_k)[1])
        self.s.display.blit(image, rect)
        image = pygame.transform.rotate(self.s.minimap_tank_tower, 270 - self.angle_of_view)
        rect2 = image.get_rect()
        rect2.center = (x + self.pos(k=self.s.minimap_k)[0],
                        y + self.pos(k=self.s.minimap_k)[1])
        self.s.display.blit(image, rect2)

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

        elif keys[pygame.K_UP]:
            self.horizontal += self.s.vertical_v * t
            self.thermal_horizontal += self.s.vertical_v * t
            if not self.zoom:
                self.sky = pygame.Rect(self.s.WIDTH // 2 - self.s.HEIGHT // 2, 0, self.s.HEIGHT,
                                   self.horizontal + self.s.HEIGHT // 2)
                self.sky_thermal = pygame.Rect(self.s.thermal_x + (self.s.WIDTH - self.s.thermal_base_width) // 2,
                                               self.s.thermal_y, self.s.thermal_width,
                                               self.thermal_horizontal + self.s.thermal_height // 2 )
            else:
                self.sky = pygame.Rect(self.s.WIDTH // 2 - self.s.HEIGHT // 2, 0, self.s.HEIGHT,
                                       3 * self.horizontal + self.s.HEIGHT // 2)
                self.sky_thermal = pygame.Rect(self.s.thermal_x + (self.s.WIDTH - self.s.thermal_base_width) // 2,
                                               self.s.thermal_y, self.s.thermal_width,
                                               3 * self.thermal_horizontal + self.s.thermal_height // 2)
        elif keys[pygame.K_DOWN]:
            self.horizontal -= self.s.vertical_v * t
            self.thermal_horizontal -= self.s.vertical_v * t
            if not self.zoom:
                self.sky = pygame.Rect(self.s.WIDTH // 2 - self.s.HEIGHT // 2, 0, self.s.HEIGHT,
                                   self.horizontal + self.s.HEIGHT // 2)
                self.sky_thermal = pygame.Rect(self.s.thermal_x + (self.s.WIDTH - self.s.thermal_base_width) // 2,
                                               self.s.thermal_y, self.s.thermal_width,
                                               self.s.thermal_height // 2 + self.thermal_horizontal)
            else:
                self.sky = pygame.Rect(self.s.WIDTH // 2 - self.s.HEIGHT // 2, 0, self.s.HEIGHT,
                                       3 * self.horizontal + self.s.HEIGHT // 2)
                self.sky_thermal = pygame.Rect(self.s.thermal_x + (self.s.WIDTH - self.s.thermal_base_width) // 2,
                                               self.s.thermal_y, self.s.thermal_width,
                                               3 * self.thermal_horizontal + self.s.thermal_height // 2)
    def mapping(self, a, b):
        return (a // self.s.tile_w) * self.s.tile_w, (b // self.s.tile_h) * self.s.tile_h

    def mapping_in_map(self, a, b):
        return (a // self.s.tile_w), (b // self.s.tile_h)

    def ray_casting(self, dr_x=0, dr_y=0, sight_type='1'):
        if sight_type == '1':
            x0, y0 = self.x, self.y
            xm, ym = self.mapping(x0, y0)
            cur_angle = self.angle_of_view - self.s.HALF_FOV_optic + 0.00001
            for i in range(self.s.NUM_RAYS):
                sin_a = math.sin(cur_angle * 3.14 / 180)
                cos_a = math.cos(cur_angle * 3.14 / 180)
                if cos_a >= 0:
                    x = xm + self.s.tile_w
                    dx = 1
                else:
                    x = xm
                    dx = -1
                for j in range(0, self.s.map_width, self.s.tile_w):
                    depth_v = (x - x0) / cos_a
                    yv = y0 + depth_v * sin_a
                    temp = self.mapping_in_map(x + dx, yv)
                    # print(x + dx, yv)

                    if temp in self.s.map.world_map:
                        texture_v = self.s.map.world_map_dict[temp]

                        break
                    if x > self.s.map_width:
                        print(1)
                        texture_v = None
                        break
                    x += dx * self.s.tile_w

                if sin_a >= 0:
                    y = ym + self.s.tile_h
                    dy = 1
                else:
                    y = ym
                    dy = -1
                for j in range(0, self.s.map_height, self.s.tile_h):
                    depth_h = (y - y0) / sin_a
                    xh = x0 + depth_h * cos_a
                    temp2 = self.mapping_in_map(xh, y + dy)
                    if temp2 in self.s.map.world_map:
                        texture_h = self.s.map.world_map_dict[temp2]
                        break
                    if y > self.s.map_height:
                        print(2)
                        texture_h = None
                        break
                    y += dy * self.s.tile_h
                depth, offset, texture = (depth_v, yv, texture_v) if depth_v < depth_h else (depth_h, xh, texture_h)
                offset = round(offset) % self.s.tile_w
                depth *= math.cos((self.angle_of_view - cur_angle) * 3.14 / 180)
                proj_height = min(int(self.s.PROJ_COEFF_optic / depth), 5 * self.s.HEIGHT)
                if self.s.texture_scale + offset * self.s.texture_scale > self.s.texture_w:
                    wall_column = self.s.textures[texture].subsurface(offset * self.s.texture_scale, 0,
                                                                      self.s.texture_w - offset * self.s.texture_scale,
                                                                      self.s.texture_h)
                else:
                    wall_column = self.s.textures[texture].subsurface(offset * self.s.texture_scale, 0,
                                                                      self.s.texture_scale, self.s.texture_h)
                wall_column = pygame.transform.scale(wall_column, (self.s.SCALE_optic, proj_height))
                self.s.display.blit(wall_column,
                                    (dr_x + i * self.s.SCALE_optic,
                                     self.horizontal + dr_y + self.s.HEIGHT // 2 - proj_height // 2))

                if int(cur_angle) == int(self.angle_of_view):
                    self.depth = str(depth)
                cur_angle += self.s.DELTA_ANGLE_optic
            self.s.display.blit(self.s.optic_sight, (dr_x, dr_y))
        elif sight_type == '2':
            x0, y0 = self.x, self.y
            xm, ym = self.mapping(x0, y0)
            cur_angle = self.angle_of_view - self.s.HALF_FOV_optic_zoom + 0.00001
            for i in range(self.s.NUM_RAYS):
                sin_a = math.sin(cur_angle * 3.14 / 180)
                cos_a = math.cos(cur_angle * 3.14 / 180)
                if cos_a >= 0:
                    x = xm + self.s.tile_w
                    dx = 1
                else:
                    x = xm
                    dx = -1
                for j in range(0, self.s.map_width, self.s.tile_w):
                    depth_v = (x - x0) / cos_a
                    yv = y0 + depth_v * sin_a
                    temp = self.mapping_in_map(x + dx, yv)
                    # print(x + dx, yv)

                    if temp in self.s.map.world_map:
                        texture_v = self.s.map.world_map_dict[temp]

                        break
                    if x > self.s.map_width:
                        print(1)
                        texture_v = None
                        break
                    x += dx * self.s.tile_w

                if sin_a >= 0:
                    y = ym + self.s.tile_h
                    dy = 1
                else:
                    y = ym
                    dy = -1
                for j in range(0, self.s.map_height, self.s.tile_h):
                    depth_h = (y - y0) / sin_a
                    xh = x0 + depth_h * cos_a
                    temp2 = self.mapping_in_map(xh, y + dy)
                    if temp2 in self.s.map.world_map:
                        texture_h = self.s.map.world_map_dict[temp2]
                        break
                    if y > self.s.map_height:
                        print(2)
                        texture_h = None
                        break
                    y += dy * self.s.tile_h
                depth, offset, texture = (depth_v, yv, texture_v) if depth_v < depth_h else (depth_h, xh, texture_h)
                offset = round(offset) % self.s.tile_w
                depth *= math.cos((self.angle_of_view - cur_angle) * 3.14 / 180)
                proj_height = min(int(self.s.PROJ_COEFF_optic_zoom / depth), 5 * self.s.HEIGHT)
                if self.s.texture_scale + offset * self.s.texture_scale > self.s.texture_w:
                    wall_column = self.s.textures[texture].subsurface(offset * self.s.texture_scale, 0,
                                                                      self.s.texture_w - offset * self.s.texture_scale, self.s.texture_h)
                else:
                    wall_column = self.s.textures[texture].subsurface(offset * self.s.texture_scale, 0,
                                                                      self.s.texture_scale, self.s.texture_h)
                wall_column = pygame.transform.scale(wall_column, (self.s.SCALE_optic_zoom, proj_height))
                self.s.display.blit(wall_column,
                                    (dr_x + i * self.s.SCALE_optic_zoom,
                                     3 * self.horizontal + dr_y + self.s.HEIGHT // 2 - proj_height // 2))

                if int(cur_angle) == int(self.angle_of_view):
                    self.depth = str(depth)
                cur_angle += self.s.DELTA_ANGLE_optic_zoom
            self.s.display.blit(self.s.optic_sight_zoom, (dr_x, dr_y))

        elif sight_type == '3':
            x0, y0 = self.x, self.y
            xm, ym = self.mapping(x0, y0)
            cur_angle = self.angle_of_view - self.s.HALF_FOV_thermal + 0.00001
            for i in range(self.s.NUM_RAYS):
                sin_a = math.sin(cur_angle * 3.14 / 180)
                cos_a = math.cos(cur_angle * 3.14 / 180)
                if cos_a >= 0:
                    x = xm + self.s.tile_w
                    dx = 1
                else:
                    x = xm
                    dx = -1
                for j in range(0, self.s.map_width, self.s.tile_w):
                    depth_v = (x - x0) / cos_a
                    yv = y0 + depth_v * sin_a
                    temp = self.mapping_in_map(x + dx, yv)
                    # print(x + dx, yv)

                    if temp in self.s.map.world_map:
                        texture_v = self.s.map.world_map_dict[temp]

                        break
                    if x > self.s.map_width:
                        print(1)
                        texture_v = None
                        break
                    x += dx * self.s.tile_w

                if sin_a >= 0:
                    y = ym + self.s.tile_h
                    dy = 1
                else:
                    y = ym
                    dy = -1
                for j in range(0, self.s.map_height, self.s.tile_h):
                    depth_h = (y - y0) / sin_a
                    xh = x0 + depth_h * cos_a
                    temp2 = self.mapping_in_map(xh, y + dy)
                    if temp2 in self.s.map.world_map:
                        texture_h = self.s.map.world_map_dict[temp2]
                        break
                    if y > self.s.map_height:
                        print(2)
                        texture_h = None
                        break
                    y += dy * self.s.tile_h
                depth, offset, texture = (depth_v, yv, texture_v) if depth_v < depth_h else (depth_h, xh, texture_h)
                offset = int(offset) % self.s.tile_w
                depth *= math.cos((self.angle_of_view - cur_angle) * 3.14 / 180)
                proj_height = min(int(self.s.PROJ_COEFF_thermal / depth), 5 * self.s.thermal_height)
                if self.s.texture_scale + offset * self.s.texture_scale > self.s.texture_w:
                    wall_column = self.s.thermal_textures[texture][0].subsurface(offset * self.s.texture_scale, 0,
                                                                      self.s.texture_w - offset * self.s.texture_scale,
                                                                      self.s.texture_h)
                else:
                    wall_column = self.s.thermal_textures[texture][0].subsurface(offset * self.s.texture_scale, 0,
                                                                      self.s.texture_scale, self.s.texture_h)
                wall_column = pygame.transform.scale(wall_column, (self.s.SCALE_thermal, proj_height))
                self.s.display.blit(wall_column,
                                    (dr_x + i * self.s.SCALE_thermal,
                                     self.thermal_horizontal + dr_y + self.s.thermal_height // 2 - proj_height // 2))

                if int(cur_angle) == int(self.angle_of_view):
                    self.depth = str(depth)
                cur_angle += self.s.DELTA_ANGLE_thermal
            self.s.display.blit(self.s.thermal_sight, (dr_x, dr_y))

        elif sight_type == '4':
            x0, y0 = self.x, self.y
            xm, ym = self.mapping(x0, y0)
            cur_angle = self.angle_of_view - self.s.HALF_FOV_thermal_zoom + 0.00001
            for i in range(self.s.NUM_RAYS):
                sin_a = math.sin(cur_angle * 3.14 / 180)
                cos_a = math.cos(cur_angle * 3.14 / 180)
                if cos_a >= 0:
                    x = xm + self.s.tile_w
                    dx = 1
                else:
                    x = xm
                    dx = -1
                for j in range(0, self.s.map_width, self.s.tile_w):
                    depth_v = (x - x0) / cos_a
                    yv = y0 + depth_v * sin_a
                    temp = self.mapping_in_map(x + dx, yv)
                    # print(x + dx, yv)

                    if temp in self.s.map.world_map:
                        texture_v = self.s.map.world_map_dict[temp]

                        break
                    if x > self.s.map_width:
                        print(1)
                        texture_v = None
                        break
                    x += dx * self.s.tile_w

                if sin_a >= 0:
                    y = ym + self.s.tile_h
                    dy = 1
                else:
                    y = ym
                    dy = -1
                for j in range(0, self.s.map_height, self.s.tile_h):
                    depth_h = (y - y0) / sin_a
                    xh = x0 + depth_h * cos_a
                    temp2 = self.mapping_in_map(xh, y + dy)
                    if temp2 in self.s.map.world_map:
                        texture_h = self.s.map.world_map_dict[temp2]
                        break
                    if y > self.s.map_height:
                        print(2)
                        texture_h = None
                        break
                    y += dy * self.s.tile_h
                depth, offset, texture = (depth_v, yv, texture_v) if depth_v < depth_h else (depth_h, xh, texture_h)
                offset = int(offset) % self.s.tile_w
                depth *= math.cos((self.angle_of_view - cur_angle) * 3.14 / 180)
                proj_height = min(int(self.s.PROJ_COEFF_thermal_zoom / depth), 5 * self.s.thermal_height)
                if self.s.texture_scale + offset * self.s.texture_scale > self.s.texture_w:
                    wall_column = self.s.thermal_textures[texture][0].subsurface(offset * self.s.texture_scale, 0,
                                                                      self.s.texture_w - offset * self.s.texture_scale,
                                                                      self.s.texture_h)
                else:
                    wall_column = self.s.thermal_textures[texture][0].subsurface(offset * self.s.texture_scale, 0,
                                                                      self.s.texture_scale, self.s.texture_h)
                wall_column = pygame.transform.scale(wall_column, (self.s.SCALE_thermal, proj_height))
                self.s.display.blit(wall_column,
                                    (dr_x + i * self.s.SCALE_thermal,
                                     3 * self.thermal_horizontal + dr_y + self.s.thermal_height // 2 - proj_height // 2))

                if int(cur_angle) == int(self.angle_of_view):
                    self.depth = str(depth)
                cur_angle += self.s.DELTA_ANGLE_thermal_zoom
            self.s.display.blit(self.s.thermal_sight_zoom, (dr_x, dr_y))

    def optic_sight(self):
        show = True
        fps_count_text_bl = Text(self.s.WIDTH * 0.961, self.s.HEIGHT * 0.972, (0, 0, 0),
                                 str(int(self.s.clock.get_fps())) + ' FPS', int(self.s.WIDTH * 0.0104),
                                 is_topleft=True)
        fps_count_text = Text(self.s.WIDTH * 0.96, self.s.HEIGHT * 0.97, (200, 200, 200),
                              str(int(self.s.clock.get_fps())) + ' FPS', int(self.s.WIDTH * 0.0104),
                              is_topleft=True)
        depth_text = Text(self.s.WIDTH * 0.5, self.s.HEIGHT * 0.916, (255, 0, 0),
                          self.depth_m, int(self.s.WIDTH * 0.033), font_name='resources/fonts/lcd_font.otf'
                          )
        black = pygame.Rect(self.s.WIDTH // 2 + self.s.HEIGHT // 2, 0, self.s.HEIGHT // 2,
                            self.s.HEIGHT)
        floor = pygame.Rect(self.s.WIDTH // 2 - self.s.HEIGHT // 2, 0, self.s.HEIGHT,
                            self.s.HEIGHT)
        self.optic = True
        if not self.zoom:
            self.sky = pygame.Rect(self.s.WIDTH // 2 - self.s.HEIGHT // 2, 0, self.s.HEIGHT,
                                   self.horizontal + self.s.HEIGHT // 2)
            self.sky_thermal = pygame.Rect(self.s.thermal_x + (self.s.WIDTH - self.s.thermal_base_width) // 2,
                                           self.s.thermal_y, self.s.thermal_width,
                                           self.thermal_horizontal + self.s.thermal_height // 2)
        else:
            self.sky = pygame.Rect(self.s.WIDTH // 2 - self.s.HEIGHT // 2, 0, self.s.HEIGHT,
                                   3 * self.horizontal + self.s.HEIGHT // 2)
            self.sky_thermal = pygame.Rect(self.s.thermal_x + (self.s.WIDTH - self.s.thermal_base_width) // 2,
                                           self.s.thermal_y, self.s.thermal_width,
                                           3 * self.thermal_horizontal + self.s.thermal_height // 2)
        while show:
            self.s.display.fill((0, 0, 0))
            pygame.draw.rect(self.s.display, (53, 104, 45), floor)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        print('escape')
                        show = False
                    if event.key == pygame.K_e:
                        depth_text.set_another_text(self.rangefinder())
                    if event.key == pygame.K_z:
                        self.zoom = True if self.zoom is False else False
                        if self.zoom:
                            self.sky = pygame.Rect(self.s.WIDTH // 2 - self.s.HEIGHT // 2, 0, self.s.HEIGHT,
                                                   3 * self.horizontal + self.s.HEIGHT // 2)
                        else:
                            self.sky = pygame.Rect(self.s.WIDTH // 2 - self.s.HEIGHT // 2, 0, self.s.HEIGHT,
                                                   self.horizontal + self.s.HEIGHT // 2)
            self.movement()
            self.guidance()
            pygame.draw.rect(self.s.display, (135, 206, 235), self.sky)
            if not self.zoom:
                self.ray_casting(self.s.WIDTH // 2 - self.s.HEIGHT // 2, 0, sight_type='1')
            else:
                self.ray_casting(self.s.WIDTH // 2 - self.s.HEIGHT // 2, 0, sight_type='2')
            pygame.draw.rect(self.s.display, (0, 0, 0), black)
            self.draw_minimap(self.x_minimap, self.y_minimap)
            fps_count_text_bl.set_another_text(str(int(self.s.clock.get_fps())) + ' FPS')
            fps_count_text.set_another_text(str(int(self.s.clock.get_fps())) + ' FPS')
            fps_count_text_bl.draw(self.s.display)
            fps_count_text.draw(self.s.display)
            depth_text.draw(self.s.display)

            pygame.display.flip()
            self.s.clock.tick(self.s.FPS)
        self.optic = False

    def thermal_sight(self):
        show = True
        fps_count_text_bl = Text(self.s.WIDTH * 0.961, self.s.HEIGHT * 0.972, (0, 0, 0),
                                 str(int(self.s.clock.get_fps())) + ' FPS', int(self.s.WIDTH * 0.0104),
                                 is_topleft=True)
        fps_count_text = Text(self.s.WIDTH * 0.96, self.s.HEIGHT * 0.97, (200, 200, 200),
                              str(int(self.s.clock.get_fps())) + ' FPS', int(self.s.WIDTH * 0.0104),
                              is_topleft=True)
        depth_text1 = Text(self.s.WIDTH * 0.528, self.s.HEIGHT * 0.83, (183, 183, 183),
                          self.depth_m[0], int(self.s.WIDTH * 0.030), font_name='resources/fonts/depth_thermal_font.ttf'
                          )
        depth_text2 = Text(self.s.WIDTH * 0.56, self.s.HEIGHT * 0.83, (183, 183, 183),
                           self.depth_m[1], int(self.s.WIDTH * 0.03),
                           font_name='resources/fonts/depth_thermal_font.ttf'
                           )
        depth_text3 = Text(self.s.WIDTH * 0.594, self.s.HEIGHT * 0.83, (183, 183, 183),
                           self.depth_m[2], int(self.s.WIDTH * 0.03),
                           font_name='resources/fonts/depth_thermal_font.ttf'
                           )
        depth_text4 = Text(self.s.WIDTH * 0.6285, self.s.HEIGHT * 0.83, (183, 183, 183),
                           self.depth_m[3], int(self.s.WIDTH * 0.03),
                           font_name='resources/fonts/depth_thermal_font.ttf'
                           )
        ssu_text = Text(self.s.WIDTH * 0.274, self.s.HEIGHT * 0.823, (183, 183, 183),
                           'ССУ', int(self.s.WIDTH * 0.028),
                           font_name='resources/fonts/depth_thermal_font.ttf'
                           )
        floor = pygame.Rect(self.s.thermal_x + (self.s.WIDTH - self.s.thermal_base_width) // 2, 0, self.s.thermal_width,
                            self.s.HEIGHT)
        z = pygame.Rect(self.s.thermal_x + self.s.thermal_base_width * 1.1, 0, self.s.WIDTH - self.s.thermal_x - self.s.thermal_base_width,
                            self.s.HEIGHT)
        if not self.zoom:
            self.sky = pygame.Rect(self.s.WIDTH // 2 - self.s.HEIGHT // 2, 0, self.s.HEIGHT,
                                   self.horizontal + self.s.HEIGHT // 2)
            self.sky_thermal = pygame.Rect(self.s.thermal_x + (self.s.WIDTH - self.s.thermal_base_width) // 2,
                                           self.s.thermal_y, self.s.thermal_width,
                                           self.thermal_horizontal + self.s.thermal_height // 2)
        else:
            self.sky = pygame.Rect(self.s.WIDTH // 2 - self.s.HEIGHT // 2, 0, self.s.HEIGHT,
                                   3 * self.horizontal + self.s.HEIGHT // 2)
            self.sky_thermal = pygame.Rect(self.s.thermal_x + (self.s.WIDTH - self.s.thermal_base_width) // 2,
                                           self.s.thermal_y, self.s.thermal_width,
                                           3 * self.thermal_horizontal + self.s.thermal_height // 2)
        self.thermal = True
        while show:
            self.s.display.fill((150, 150, 150))
            pygame.draw.rect(self.s.display, self.floor_thermal_color, floor)
            pygame.draw.rect(self.s.display, self.sky_thermal_color, self.sky_thermal)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        show = False
                    if event.key == pygame.K_e:
                        d = self.rangefinder()
                        depth_text1.set_another_text(d[0])
                        depth_text2.set_another_text(d[1])
                        depth_text3.set_another_text(d[2])
                        depth_text4.set_another_text(d[3])
                    if event.key == pygame.K_z:
                        self.zoom = True if self.zoom is False else False
                        if self.zoom:
                            self.sky = pygame.Rect(self.s.WIDTH // 2 - self.s.HEIGHT // 2, 0, self.s.HEIGHT,
                                                   3 * self.horizontal + self.s.HEIGHT // 2)
                            self.sky_thermal = pygame.Rect(self.s.thermal_x + (self.s.WIDTH - self.s.thermal_base_width) // 2, self.s.thermal_y, self.s.thermal_width,
                               3 * self.thermal_horizontal + self.s.thermal_height // 2)
                        else:
                            self.sky = pygame.Rect(self.s.WIDTH // 2 - self.s.HEIGHT // 2, 0, self.s.HEIGHT,
                                                   self.horizontal + self.s.HEIGHT // 2)
                            self.sky_thermal = pygame.Rect(
                                self.s.thermal_x + (self.s.WIDTH - self.s.thermal_base_width) // 2, self.s.thermal_y,
                                self.s.thermal_width,
                                self.thermal_horizontal + self.s.thermal_height // 2)
            self.movement()
            self.guidance()
            if not self.zoom:
                self.ray_casting(self.s.thermal_x + (self.s.WIDTH - self.s.thermal_base_width) // 2, self.s.thermal_y, sight_type='3')
            else:
                self.ray_casting(self.s.thermal_x + (self.s.WIDTH - self.s.thermal_base_width) // 2, self.s.thermal_y, sight_type='4')

            pygame.draw.rect(self.s.display, (150, 150, 150), z)
            self.s.display.blit(self.s.thermal_image, ((self.s.WIDTH - self.s.thermal_base_width) // 2, 0))

            self.draw_minimap(self.x_minimap, self.y_minimap)
            fps_count_text_bl.set_another_text(str(int(self.s.clock.get_fps())) + ' FPS')
            fps_count_text.set_another_text(str(int(self.s.clock.get_fps())) + ' FPS')
            fps_count_text_bl.draw(self.s.display)
            fps_count_text.draw(self.s.display)
            if self.zoom:
                depth_text1.draw(self.s.display)
                depth_text2.draw(self.s.display)
                depth_text3.draw(self.s.display)
                depth_text4.draw(self.s.display)
            else:
                ssu_text.draw(self.s.display)
            pygame.display.flip()
            self.s.clock.tick(self.s.FPS)
        self.thermal = False

    def rangefinder(self):
        depth = str(min(int(float(self.depth) * (7 / self.side)), 9999))
        depth = '0' * (4 - len(depth)) + depth
        self.depth_m = depth
        return depth

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

#
# s = TankSettings()
# ex = Tank(s, 120, 120, 0, 5, 0, 0)
# ex.start()
