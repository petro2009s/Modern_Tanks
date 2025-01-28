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
            SpriteObject(self.sprite_types['bush_thermal'], True, (45.1, 7.1), 0.7, 1, self.s, 3, self, 'oth', 0),
            SpriteObject(self.sprite_types['bush_thermal'], True, (47.1, 9.1), 0.7, 1, self.s, 3, self, 'oth', 1),
            SpriteObject(self.sprite_types['bmp_thermal'], False, (54, 17), 0.7, 1, self.s, 6, self, 'bmp', 2, k=1.77, v=-0.03 * self.s.tile_w * self.s.FPS / 60, hp=100, death_anim=True),
            SpriteObject(self.sprite_types['tree_thermal'], True, (50, 18), 0, 2, self.s, 3, self, 'oth', 3)]
        self.list_of_objects = [
            SpriteObject(self.sprite_types['bush'], True, (45.1, 7.1), 0.7, 1, self.s, 3, self, 'oth', 0),
            SpriteObject(self.sprite_types['bush'], True, (47.1, 9.1), 0.7, 1, self.s, 3, self, 'oth', 1),
            SpriteObject(self.sprite_types['bmp'], False, (54, 17), 0.7, 1, self.s, 6, self, 'bmp',  2, k=1.77, v=-0.03 * self.s.tile_w * self.s.FPS / 60, hp=100, death_anim=True),
            SpriteObject(self.sprite_types['tree'], True, (50, 18), 0, 2, self.s, 3, self, 'oth', 3)]
        self.all_list = self.list_of_objects + self.list_of_objects_thermal
        self.collision_set = {(54, 17)}




class SpriteObject:
    def __init__(self, object, stat, pos, shift, scale, s, a1, sprites, type, num, k=1, v=0, hp=10, death_anim=None):
        self.s = s
        self.sprites = sprites
        self.num = num
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
        self.is_death_anim = None
        self.death_anim_counter = None
        if not stat:
            self.sprite_angles = [frozenset(range(i, i + 45)) for i in range(0, 360, 45)]
            self.sprite_pos = {angles: pos for angles, pos in zip(self.sprite_angles, self.object)}
        if death_anim:
            if self.type == 'bmp':
                self.is_death_anim = False
                self.death_anim_counter = 1

    def object_locate(self, tank):
        if not self.death:
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
                    drx, dry = ((self.s.WIDTH - self.s.NUM_RAYS * self.s.SCALE_thermal) // 2,
                                self.s.thermal_y)
                    height = self.s.thermal_height
                    k = 0.6
                elif tank.optic:
                    DELTA_ANGLE = self.s.DELTA_ANGLE_optic_zoom
                    PROJ_COEFF = self.s.PROJ_COEFF_optic_zoom
                    horizontal = 3 * tank.horizontal
                    SCALE = self.s.SCALE_optic
                    height = self.s.HEIGHT
                    HALF_FOV = self.s.HALF_FOV_optic_zoom
                    drx, dry = (self.s.WIDTH // 2 - self.s.NUM_RAYS * self.s.SCALE_optic_zoom // 2, 0)
                    k = 0.8
                elif tank.thermal_d:
                    DELTA_ANGLE = self.s.DELTA_ANGLE_thermal_zoom
                    PROJ_COEFF = self.s.PROJ_COEFF_thermal_zoom_d
                    horizontal = 3 * tank.thermal_horizontal_d
                    SCALE = self.s.SCALE_thermal_d
                    HALF_FOV = self.s.HALF_FOV_thermal_zoom
                    drx, dry = (self.s.thermal_x_d * 0.75,
                                self.s.thermal_y_d)
                    height = self.s.thermal_height_d
                    k = 0.6
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
                    drx, dry = ((self.s.WIDTH - self.s.NUM_RAYS * self.s.SCALE_thermal) // 2,
                                self.s.thermal_y)
                    k = 0.6
                elif tank.thermal_d:
                    DELTA_ANGLE = self.s.DELTA_ANGLE_thermal_zoom_extra
                    PROJ_COEFF = self.s.PROJ_COEFF_thermal_zoom_extra_d
                    horizontal = 6 * tank.thermal_horizontal_d
                    SCALE = self.s.SCALE_thermal_d
                    drx, dry = (self.s.thermal_x_d * 0.75,
                                self.s.thermal_y_d)
                    height = self.s.thermal_height_d
                    HALF_FOV = self.s.HALF_FOV_thermal_zoom_extra
                    k = 0.6
                else:
                    return (False,)
            else:
                if tank.thermal:
                    DELTA_ANGLE = self.s.DELTA_ANGLE_thermal
                    PROJ_COEFF = self.s.PROJ_COEFF_thermal
                    horizontal = 1 * tank.thermal_horizontal
                    SCALE = self.s.SCALE_thermal
                    height = self.s.thermal_height
                    drx, dry = ((self.s.WIDTH - self.s.NUM_RAYS * self.s.SCALE_thermal) // 2,
                                self.s.thermal_y)
                    HALF_FOV = self.s.HALF_FOV_thermal
                    k = 0.6
                elif tank.optic:
                    DELTA_ANGLE = self.s.DELTA_ANGLE_optic
                    PROJ_COEFF = self.s.PROJ_COEFF_optic
                    horizontal = 1 * tank.horizontal
                    SCALE = self.s.SCALE_optic
                    height = self.s.HEIGHT
                    drx, dry = (self.s.WIDTH // 2 - self.s.NUM_RAYS * self.s.SCALE_optic // 2, 0)
                    HALF_FOV = self.s.HALF_FOV_optic
                    k = 0.8
                elif tank.thermal_d:
                    # print(1)
                    DELTA_ANGLE = self.s.DELTA_ANGLE_thermal
                    PROJ_COEFF = self.s.PROJ_COEFF_thermal_d
                    horizontal = 1 * tank.thermal_horizontal_d
                    SCALE = self.s.SCALE_thermal_d
                    drx, dry = (self.s.thermal_x_d * 0.75,
                                self.s.thermal_y_d)
                    height = self.s.thermal_height_d
                    HALF_FOV = self.s.HALF_FOV_thermal
                    k = 0.6
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
            # print(delta_rays)
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
                if not self.is_death_anim:
                    sprite_pos = (
                        drx + current_ray * SCALE - half_proj_height * self.k, horizontal + dry + height // 2 - half_proj_height + shift)

                    # print(self.s.center_ray - self.a1 * (6 - HALF_FOV), current_ray, self.s.center_ray + self.a1 * (6 - HALF_FOV), self.s.center_ray - self.a1 * (6 - HALF_FOV) <= current_ray <= self.s.center_ray + self.a1 * (6 - HALF_FOV))

                    if (self.s.center_ray - self.a1 * (7 - HALF_FOV)) <= current_ray <= (self.s.center_ray + self.a1 * (7 - HALF_FOV)) * 0.93:
                        print('ffffff')
                        # print(horizontal)
                        if self.s.HEIGHT // 2 * k - horizontal >= \
                            sprite_pos[1] and (
                            sprite_pos[1] + proj_height) >= (self.s.HEIGHT // 2 * k - horizontal):
                            print(2)
                            tank.depth_sprite = str(dist)
                            tank.is_sprite_depth = True
                            # print('gjvtyzk', tank.thermal_horizontal)
                            # print(tank.is_shot, tank.current_shooted_ammo)
                            if tank.is_shot and tank.current_shooted_ammo is not None:
                                print(3)

                                self.minus_hp(tank)
                                self.check_death(tank)
                                tank.current_shooted_ammo = None

                        if tank.lock:
                            # print('ppppp', tank.thermal_horizontal)
                            # print(self.x + self.s.tile_w // 3, self.y - self.s.tile_h // 3, 12122121)
                            tank.lock_x, tank.lock_y = self.x, self.y
                    if self.movement_angle < 0:
                        o = pygame.transform.flip(self.object, True, False)
                        sprite = pygame.transform.scale(o, (proj_height * self.k, proj_height))
                    else:
                        sprite = pygame.transform.scale(self.object, (proj_height * self.k, proj_height))
                else:
                    self.check_death_anim()
                    sprite = self.death_anim(tank)
                    self.death_anim_counter += 1
                    if sprite == False:
                        return (False, )
                    sprite_pos = (
                        drx + current_ray * SCALE - half_proj_height * 2.07 * 2,
                        horizontal + dry + height // 2 - half_proj_height * 2)
                    sprite = pygame.transform.scale(sprite, (proj_height * 2.07 * 2, proj_height * 2))
                return (dist, sprite, sprite_pos)
            else:
                return (False,)
        else:
            return (False,)

    def bmp_movement(self, tank):
        if self.v != 0:
            dx = self.v * self.movement_angle
            if dx != 0:
                if ((self.x + dx) // self.s.tile_w, self.y // self.s.tile_h) == (
                tank.x // self.s.tile_w, tank.y // self.s.tile_h):
                    dx = 0
                if ((self.x + dx) // self.s.tile_w, self.y // self.s.tile_h) in self.s.map.world_map:
                    self.movement_angle *= -1
                # print(self.movement_angle)
                self.x += dx
                self.sprites.collision_set = {(self.x // self.s.tile_w, self.y // self.s.tile_h)}

    def check_death_anim(self):
        if self.death_anim_counter > self.s.bmp_death_frames:
            self.is_death_anim = False
            self.death = True
            self.death_anim_counter = 0

    def death_anim(self, tank):
        if self.is_death_anim:
            if self.death_anim_counter % self.s.bmp_death_frames_delta == 0:
                if tank.thermal or tank.thermal_d:
                    return self.s.bmp_death_anim_thermal[self.death_anim_counter // self.s.bmp_death_frames_delta - 1]
                else:
                    return self.s.bmp_death_anim[self.death_anim_counter // self.s.bmp_death_frames_delta - 1]

        return False
    def minus_hp(self, tank):
        # print(int(tank.depth_m) * tank.side / 7)
        if float(tank.depth_sprite) * 1.4 >= (int(tank.depth_m) + 1) * tank.side / 7 >= float(tank.depth_sprite) * 0.4:
            for i in range(len(self.sprites.all_list)):
                if self.sprites.all_list[i].num == self.num:
                    self.sprites.all_list[i].v = 0
                    print(5555)
                    if self.sprites.all_list[i].type == 'bmp' or self.sprites.all_list[i].type == 'oth':
                        if tank.current_shooted_ammo == 0:
                            self.sprites.all_list[i].hp -= 70
                        elif tank.current_shooted_ammo == 1:
                            self.sprites.all_list[i].hp -= 100
                        elif tank.current_shooted_ammo == 2:
                            self.sprites.all_list[i].hp -= 110

    def check_death(self, tank):
        for i in range(len(self.sprites.all_list)):
            if self.sprites.all_list[i].hp <= 0:
                if self.sprites.all_list[i].type != 'bmp':
                    self.sprites.all_list[i].death = True
                else:
                    self.sprites.all_list[i].is_death_anim = True
                if self.sprites.all_list[i].type == 'bmp':
                    tank.count_of_destroyed_targets = str(float(tank.count_of_destroyed_targets) + 0.5)
        tank.count_of_destroyed_targets = str(int(float(tank.count_of_destroyed_targets)))


