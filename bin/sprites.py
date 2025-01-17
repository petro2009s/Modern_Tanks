import math

import pygame.transform


class Sprite:
    def __init__(self, s):
        self.s = s
        self.sprite_types = {'bush_thermal': self.s.bush_sprite_thermal,
                             'bush': self.s.bush_sprite}
        self.list_of_objects_thermal = [SpriteObject(self.sprite_types['bush_thermal'], True, (45.1, 7.1), 0, 1, self.s),
                                        SpriteObject(self.sprite_types['bush_thermal'], True, (47.1, 9.1), 0, 1, self.s)]
        self.list_of_objects = [
            SpriteObject(self.sprite_types['bush'], True, (45.1, 7.1), 0, 1, self.s),
            SpriteObject(self.sprite_types['bush'], True, (47.1, 9.1), 0, 1, self.s)]


class SpriteObject:
    def __init__(self, object, stat, pos, shift, scale, s):
        self.s = s
        self.object = object
        self.stat = stat
        self.pos = self.x, self.y = pos[0] * self.s.tile_w, pos[1] * self.s.tile_h
        self.shift = shift
        self.scale = scale

    def object_locate(self, tank):
        fake_walls0 = [tank.walls[0] for i in range(self.s.FAKE_RAYS)]
        fake_walls1 = [tank.walls[-1] for i in range(self.s.FAKE_RAYS)]
        fake_walls = fake_walls0 + tank.walls + fake_walls1
        if tank.zoom:
            if tank.thermal:
                DELTA_ANGLE = self.s.DELTA_ANGLE_thermal_zoom
                PROJ_COEFF = self.s.PROJ_COEFF_thermal_zoom
                horizontal = 3 * tank.thermal_horizontal
                SCALE = self.s.SCALE_thermal
                drx, dry = (self.s.thermal_x + (self.s.WIDTH - self.s.thermal_base_width) // 2,
                                     self.s.thermal_y)
                height = self.s.thermal_height
            elif tank.optic:
                DELTA_ANGLE = self.s.DELTA_ANGLE_optic_zoom
                PROJ_COEFF = self.s.PROJ_COEFF_optic_zoom
                horizontal = 1 * tank.horizontal
                SCALE = self.s.SCALE_optic
                height = self.s.HEIGHT
                drx, dry = (self.s.WIDTH // 2 - self.s.HEIGHT // 2, 0)
            elif tank.thermal_d:
                DELTA_ANGLE = self.s.DELTA_ANGLE_thermal_zoom
                PROJ_COEFF = self.s.PROJ_COEFF_thermal_zoom_d
                horizontal = 3 * tank.thermal_horizontal_d
                SCALE = self.s.SCALE_thermal_d
                drx, dry = (self.s.thermal_x_d,
                            self.s.thermal_y_d)
                height = self.s.thermal_height_d
            else:
                return (False,)
        elif tank.extra_zoom:
            if tank.thermal:
                DELTA_ANGLE = self.s.DELTA_ANGLE_thermal_zoom_extra
                PROJ_COEFF = self.s.PROJ_COEFF_thermal_zoom_extra
                horizontal = 1 * tank.thermal_horizontal
                SCALE = self.s.SCALE_thermal
                height = self.s.thermal_height
                drx, dry = (self.s.thermal_x + (self.s.WIDTH - self.s.thermal_base_width) // 2,
                            self.s.thermal_y)
            elif tank.thermal_d:
                DELTA_ANGLE = self.s.DELTA_ANGLE_thermal_zoom_extra
                PROJ_COEFF = self.s.PROJ_COEFF_thermal_zoom_extra_d
                horizontal = 6 * tank.thermal_horizontal_d
                SCALE = self.s.SCALE_thermal_d
                drx, dry = (self.s.thermal_x_d,
                            self.s.thermal_y_d)
                height = self.s.thermal_height_d
            else:
                return (False,)
        else:
            if tank.thermal:
                DELTA_ANGLE = self.s.DELTA_ANGLE_thermal
                PROJ_COEFF = self.s.PROJ_COEFF_thermal
                horizontal = 1 * tank.thermal_horizontal
                SCALE = self.s.SCALE_thermal
                height = self.s.thermal_height
                drx, dry = (self.s.thermal_x + (self.s.WIDTH - self.s.thermal_base_width) // 2,
                            self.s.thermal_y)
            elif tank.optic:
                DELTA_ANGLE = self.s.DELTA_ANGLE_optic
                PROJ_COEFF = self.s.PROJ_COEFF_optic
                horizontal = 1 * tank.horizontal
                SCALE = self.s.SCALE_optic
                height = self.s.HEIGHT
                drx, dry = (self.s.WIDTH // 2 - self.s.HEIGHT // 2, 0)
            elif tank.thermal_d:
                print(1)
                DELTA_ANGLE = self.s.DELTA_ANGLE_thermal
                PROJ_COEFF = self.s.PROJ_COEFF_thermal_d
                horizontal = 1 * tank.thermal_horizontal_d
                SCALE = self.s.SCALE_thermal_d
                drx, dry = (self.s.thermal_x_d,
                                     self.s.thermal_y_d)
                height = self.s.thermal_height_d
            else:
                return (False,)
        dx, dy = self.x - tank.x, self.y - tank.y
        dist = math.sqrt(dx ** 2 + dy ** 2)
        theta = math.atan2(dy, dx)
        gamma = theta - tank.angle_of_view * 3.14 / 180
        #
        if dx > 0 and 180 <= tank.angle_of_view <= 360 or dx < 0 and dy < 0:
            gamma += 2 * math.pi
        # if (self.x - tank.x > 0 and self.y - tank.y > 0) or (
        #         self.x - tank.x > 0 and self.y - tank.y < 0):
        #     gamma += math.pi
        delta_rays = int(gamma / (DELTA_ANGLE * 3.14 / 180))
        current_ray = self.s.center_ray + delta_rays
        # dist *= math.cos(self.s.HALF_FOV_thermal - current_ray * self.s.DELTA_ANGLE_thermal)
        fake_ray = current_ray + self.s.FAKE_RAYS
        if 0 <= fake_ray <= self.s.NUM_RAYS - 1 + 2 * self.s.FAKE_RAYS and dist < fake_walls[fake_ray][0]:
            proj_height = min(int(PROJ_COEFF / dist * self.scale), self.s.HEIGHT)
            half_proj_height = proj_height // 2
            shift = half_proj_height * self.shift


            sprite_pos = (drx + current_ray * SCALE - half_proj_height, horizontal + dry + height // 2 - half_proj_height + shift)
            print(sprite_pos, drx, current_ray * SCALE)
            sprite = pygame.transform.scale(self.object, (proj_height, proj_height))
            return (dist, sprite, sprite_pos)
        else:
            return (False,)