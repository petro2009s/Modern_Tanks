import math

import pygame.transform


class Sprite:
    def __init__(self, s):
        self.s = s
        self.sprite_types = {'bush_thermal': self.s.bush_sprite_thermal,
                             'bush': self.s.bush_sprite,
                             'bmp': self.s.test_sprite_v,
                             'bmp_thermal': self.s.test_sprite_v_thermal,
                             'tree_thermal': self.s.tree_sprite_thermal,
                             'tree': self.s.tree_sprite}
        self.list_of_objects_thermal = [
            SpriteObject(self.sprite_types['bush_thermal'], True, (45.1, 7.1), 0.7, 1, self.s, 5, self, 'oth'),
            SpriteObject(self.sprite_types['bush_thermal'], True, (47.1, 9.1), 0.7, 1, self.s, 5, self, 'oth'),
            SpriteObject(self.sprite_types['bmp_thermal'], False, (54, 17), 0.7, 1, self.s, 15, self, 'bmp', k=1.77, v=-0.03 * self.s.tile_w * self.s.FPS / 60, hp=100),
            SpriteObject(self.sprite_types['tree_thermal'], True, (50, 18), 0, 2, self.s, 5, self, 'oth')]
        self.list_of_objects = [
            SpriteObject(self.sprite_types['bush'], True, (45.1, 7.1), 0.7, 1, self.s, 5, self, 'oth'),
            SpriteObject(self.sprite_types['bush'], True, (47.1, 9.1), 0.7, 1, self.s, 5, self, 'oth'),
            SpriteObject(self.sprite_types['bmp'], False, (54, 17), 0.7, 1, self.s, 15, self, 'bmp', k=1.77, v=-0.03 * self.s.tile_w * self.s.FPS / 60, hp=100),
            SpriteObject(self.sprite_types['tree'], True, (50, 18), 0, 2, self.s, 5, self, 'oth')]
        self.collision_set = {(54, 17)}




class SpriteObject:
    def __init__(self, object, stat, pos, shift, scale, s, a1, sprites, type, k=1, v=0, hp=10):
        self.s = s
        self.sprites = sprites
        self.movement_angle = 1
        self.object = object
        self.stat = stat
        self.pos = self.x, self.y = pos[0] * self.s.tile_w, pos[1] * self.s.tile_h
        self.shift = shift
        self.scale = scale
        self.k = k
        self.hp = hp
        self.a1 = a1
        self.type = type
        self.v = v
        self.death = False
        if not stat:
            self.sprite_angles = [frozenset(range(i, i + 45)) for i in range(0, 360, 45)]
            self.sprite_pos = {angles: pos for angles, pos in zip(self.sprite_angles, self.object)}

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
                HALF_FOV = self.s.HALF_FOV_thermal_zoom
                drx, dry = (self.s.thermal_x + (self.s.WIDTH - self.s.thermal_base_width) // 2,
                            self.s.thermal_y)
                height = self.s.thermal_height
            elif tank.optic:
                DELTA_ANGLE = self.s.DELTA_ANGLE_optic_zoom
                PROJ_COEFF = self.s.PROJ_COEFF_optic_zoom
                horizontal = 3 * tank.horizontal
                SCALE = self.s.SCALE_optic
                height = self.s.HEIGHT
                HALF_FOV = self.s.HALF_FOV_optic_zoom
                drx, dry = (self.s.WIDTH // 2 - self.s.HEIGHT // 2, 0)
            elif tank.thermal_d:
                DELTA_ANGLE = self.s.DELTA_ANGLE_thermal_zoom
                PROJ_COEFF = self.s.PROJ_COEFF_thermal_zoom_d
                horizontal = 3 * tank.thermal_horizontal_d
                SCALE = self.s.SCALE_thermal_d
                HALF_FOV = self.s.HALF_FOV_thermal_zoom
                drx, dry = (self.s.thermal_x_d,
                            self.s.thermal_y_d)
                height = self.s.thermal_height_d
            else:
                return (False,)
        elif tank.extra_zoom:
            if tank.thermal:
                DELTA_ANGLE = self.s.DELTA_ANGLE_thermal_zoom_extra
                PROJ_COEFF = self.s.PROJ_COEFF_thermal_zoom_extra
                horizontal = 6 * tank.thermal_horizontal
                SCALE = self.s.SCALE_thermal
                height = self.s.thermal_height
                HALF_FOV = self.s.HALF_FOV_thermal_zoom_extra
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
                HALF_FOV = self.s.HALF_FOV_thermal_zoom_extra
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
                HALF_FOV = self.s.HALF_FOV_thermal
            elif tank.optic:
                DELTA_ANGLE = self.s.DELTA_ANGLE_optic
                PROJ_COEFF = self.s.PROJ_COEFF_optic
                horizontal = 1 * tank.horizontal
                SCALE = self.s.SCALE_optic
                height = self.s.HEIGHT
                drx, dry = (self.s.WIDTH // 2 - self.s.HEIGHT // 2, 0)
                HALF_FOV = self.s.HALF_FOV_optic
            elif tank.thermal_d:
                print(1)
                DELTA_ANGLE = self.s.DELTA_ANGLE_thermal
                PROJ_COEFF = self.s.PROJ_COEFF_thermal_d
                horizontal = 1 * tank.thermal_horizontal_d
                SCALE = self.s.SCALE_thermal_d
                drx, dry = (self.s.thermal_x_d,
                            self.s.thermal_y_d)
                height = self.s.thermal_height_d
                HALF_FOV = self.s.HALF_FOV_thermal
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
        dist *= math.cos(math.radians(HALF_FOV - current_ray * DELTA_ANGLE))
        fake_ray = current_ray + self.s.FAKE_RAYS
        if 0 <= fake_ray <= self.s.NUM_RAYS - 1 + 2 * self.s.FAKE_RAYS and dist < fake_walls[fake_ray][0]:

            proj_height = min(int(PROJ_COEFF / dist * self.scale), self.s.HEIGHT)

            half_proj_height = proj_height // 2
            shift = half_proj_height * self.shift
            if not self.stat:
                if theta < 0:
                    theta += 2 * math.pi
                theta = 360 - int(math.degrees(theta))
                for angles in self.sprite_angles:
                    if theta in angles:
                        self.object = self.sprite_pos[angles]
                        break

            sprite_pos = (
                drx + current_ray * SCALE - half_proj_height, horizontal + dry + height // 2 - half_proj_height + shift)
            # print(self.s.center_ray - self.a1 * (6 - HALF_FOV), current_ray, self.s.center_ray + self.a1 * (6 - HALF_FOV), self.s.center_ray - self.a1 * (6 - HALF_FOV) <= current_ray <= self.s.center_ray + self.a1 * (6 - HALF_FOV))
            if self.s.center_ray - self.a1 * (6 - HALF_FOV) <= current_ray <= self.s.center_ray + self.a1 * (6 - HALF_FOV):
                print('ffffff')
                print(int(tank.depth_m) * tank.side / 7, dist)
                if tank.horizontal + self.s.HEIGHT // 2 * 0.68 >= \
                    sprite_pos[1] and (
                    sprite_pos[1] + proj_height) >= tank.horizontal + self.s.HEIGHT // 2:
                    print(2)
                    tank.depth_sprite = str(dist)
                    tank.is_sprite_depth = True
                    # print('gjvtyzk', tank.thermal_horizontal)
                    print(tank.is_shot, tank.current_shooted_ammo)
                    if tank.is_shot and tank.current_shooted_ammo is not None:
                        print(3)

                        self.minus_hp(tank)
                        if self.hp <= 0:
                            self.death = True
                            if self.type == 'bmp':
                                tank.count_of_destroyed_targets = str(int(tank.count_of_destroyed_targets) + 1)
                        tank.current_shooted_ammo = None

                if tank.lock:
                    # print('ppppp', tank.thermal_horizontal)
                    # print(self.x + self.s.tile_w // 3, self.y - self.s.tile_h // 3, 12122121)
                    tank.lock_x, tank.lock_y = self.x + self.s.tile_w // 5 * self.k, self.y - self.s.tile_h // 2
            if self.movement_angle < 0:
                o = pygame.transform.flip(self.object, True, False)
                sprite = pygame.transform.scale(o, (proj_height * self.k, proj_height))
            else:
                sprite = pygame.transform.scale(self.object, (proj_height * self.k, proj_height))
            return (dist, sprite, sprite_pos)
        else:
            return (False,)

    def bmp_movement(self, tank):
        dx = self.v * self.movement_angle
        if dx != 0:
            if ((self.x + dx) // self.s.tile_w, self.y // self.s.tile_h) == (
            tank.x // self.s.tile_w, tank.y // self.s.tile_h):
                dx = 0
            if ((self.x + dx) // self.s.tile_w, self.y // self.s.tile_h) in self.s.map.world_map:
                self.movement_angle *= -1
            print(self.movement_angle)
            self.x += dx
            self.sprites.collision_set = {(self.x // self.s.tile_w, self.y // self.s.tile_h)}

    def minus_hp(self, tank):
        print(int(tank.depth_m) * tank.side / 7)
        if float(tank.depth_sprite) * 1.4 >= (int(tank.depth_m) + 1) * tank.side / 7 >= float(tank.depth_sprite) * 0.4:
            self.v = 0
            if self.type == 'bmp' or self.type == 'oth':
                if tank.current_shooted_ammo == 0:
                    self.hp -= 70
                elif tank.current_shooted_ammo == 1:
                    self.hp -= 100
                elif tank.current_shooted_ammo == 2:
                    self.hp -= 110

