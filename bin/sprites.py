import math

import pygame.transform


class Sprite:
    def __init__(self, s):
        # настройки
        self.s = s
        # типы спрайтов
        self.sprite_types = self.s.sprite_types
        # списки со всеми спрайтами на карте
        self.list_of_objects_thermal = self.s.list_of_objects_thermal
        self.list_of_objects = self.s.list_of_objects
        self.all_list = self.list_of_objects + self.list_of_objects_thermal
        # коллизии
        self.collision_set = {}
        for i in self.list_of_objects:
            if i.type != 'oth':
                self.collision_set[i.num] = i.coords


class SpriteObject:
    def __init__(self, object, stat, pos, shift, scale, s, a1, sprites, type, num, k=1, v=0, hp=10, death_anim=None):
        # настройки и спрайты
        self.s = s
        self.sprites = sprites
        # тип, номер и хп
        self.num = num
        self.type = type
        self.hp = hp
        # координаты спрайта
        self.pos = self.x, self.y = pos[0] * self.s.tile_w, pos[1] * self.s.tile_h
        self.coords = pos
        # направление движения и скорость
        self.movement_angle = 1
        self.v = v
        # параметры отображения спрайта
        self.object = object
        self.stat = stat
        self.shift = shift
        self.scale = scale
        self.k = k
        self.a1 = a1
        # переменные для анимаций и смерти
        self.death = False
        self.is_death_anim = None
        self.death_anim_counter = None
        # параметры отображения объемного спрайта
        if not stat:
            self.sprite_angles = [frozenset(range(i, i + 45)) for i in range(0, 360, 45)]
            self.sprite_pos = {angles: pos for angles, pos in zip(self.sprite_angles, self.object)}
        # анимация смерти
        if death_anim:
            if self.type == 'bmp':
                self.is_death_anim = False
                self.death_anim_counter = 1

    # отображение спрайта
    def object_locate(self, tank):
        if not self.death:
            # параметры отображения
            fake_walls0 = [tank.walls[0] for i in range(self.s.FAKE_RAYS)]
            fake_walls1 = [tank.walls[-1] for i in range(self.s.FAKE_RAYS)]
            fake_walls = fake_walls0 + tank.walls + fake_walls1
            DELTA_ANGLE, PROJ_COEFF, horizontal, SCALE, HALF_FOV, drx, dry, height, k = self.all_current_parametres(
                tank)

            dx, dy = self.x - tank.x, self.y - tank.y
            dist = math.sqrt(dx ** 2 + dy ** 2)
            theta = math.atan2(dy, dx)
            gamma = theta - tank.angle_of_view * 3.14 / 180

            if dx > 0 and 180 <= tank.angle_of_view <= 360 or dx < 0 and dy < 0:
                gamma += 2 * math.pi

            delta_rays = int(gamma / (DELTA_ANGLE * 3.14 / 180))
            current_ray = self.s.center_ray + delta_rays

            dist *= math.cos(math.radians(HALF_FOV - current_ray * DELTA_ANGLE))

            fake_ray = current_ray + self.s.FAKE_RAYS
            # проверка на наличие в кадре
            if 0 <= fake_ray <= self.s.NUM_RAYS - 1 + 2 * self.s.FAKE_RAYS and dist < fake_walls[fake_ray][0]:
                #
                proj_height = min(int(PROJ_COEFF / dist * self.scale), 5 * self.s.HEIGHT)
                half_proj_height = proj_height // 2

                shift = half_proj_height * self.shift
                # объемный спрайт
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
                        drx + current_ray * SCALE - half_proj_height * self.k,
                        horizontal + dry + height // 2 - half_proj_height + shift)
                    # проверка того, что перекрестие на спрайте
                    if (self.s.center_ray - self.a1 * (7 - HALF_FOV) * proj_height * self.k / 300) <= current_ray <= (
                            self.s.center_ray + self.a1 * (7 - HALF_FOV) * proj_height * self.k / 300):
                        if self.s.HEIGHT // 2 * k - horizontal >= \
                                sprite_pos[1] and (
                                sprite_pos[1] + proj_height) >= (self.s.HEIGHT // 2 * k - horizontal):

                            tank.depth_sprite = str(dist)
                            tank.is_sprite_depth = True
                            # выстрел по спрайту
                            if tank.current_shooted_ammo is not None and tank.shot_anim is True:
                                self.minus_hp(tank)
                                self.check_death(tank)
                                tank.current_shooted_ammo = None
                        # захват спрайта
                        if tank.lock:
                            tank.lock_x, tank.lock_y = self.x, self.y
                    # проверка направления движения
                    if self.movement_angle < 0:
                        o = pygame.transform.flip(self.object, True, False)
                        sprite = pygame.transform.scale(o, (proj_height * self.k, proj_height))
                    else:
                        sprite = pygame.transform.scale(self.object, (proj_height * self.k, proj_height))
                # анимация смерти
                else:
                    self.check_death_anim()

                    sprite = self.death_anim(tank)
                    self.death_anim_counter += 1

                    if sprite == False:
                        return (False,)

                    sprite_pos = (
                        drx + current_ray * SCALE - half_proj_height * 2.07 * 2,
                        horizontal + dry + height // 2 - half_proj_height * 2)
                    sprite = pygame.transform.scale(sprite, (proj_height * 2.07 * 2, proj_height * 2))
                # возвращение кортежа с параметрами спрайта
                return (dist, sprite, sprite_pos)
        return (False,)

    # движение бмп
    def bmp_movement(self, tank):
        if self.v != 0:
            dx = self.v * self.movement_angle

            if dx != 0:
                if ((self.x + dx) // self.s.tile_w, self.y // self.s.tile_h) == (
                        tank.x // self.s.tile_w, tank.y // self.s.tile_h):
                    dx = 0
                if ((self.x + dx) // self.s.tile_w, self.y // self.s.tile_h) in self.s.map.world_map:
                    self.movement_angle *= -1
                self.x += dx
                self.sprites.collision_set[self.num] = (self.x // self.s.tile_w, self.y // self.s.tile_h)

    # проверка анимации смерти
    def check_death_anim(self):
        for i in range(len(self.sprites.all_list)):
            if self.sprites.all_list[i].num == self.num:
                if self.sprites.all_list[i].death_anim_counter > self.s.bmp_death_frames:
                    self.sprites.all_list[i].is_death_anim = False
                    self.sprites.all_list[i].death = True
                    self.sprites.all_list[i].death_anim_counter = 0

    # анимация смерти
    def death_anim(self, tank):
        for i in range(len(self.sprites.all_list)):
            if self.sprites.all_list[i].num == self.num:
                if self.sprites.all_list[i].is_death_anim:
                    if self.sprites.all_list[i].death_anim_counter % self.s.bmp_death_frames_delta == 0:
                        if tank.thermal or tank.thermal_d:
                            return self.s.bmp_death_anim_thermal[
                                self.sprites.all_list[i].death_anim_counter // self.s.bmp_death_frames_delta - 1]
                        else:
                            return self.s.bmp_death_anim[
                                self.sprites.all_list[i].death_anim_counter // self.s.bmp_death_frames_delta - 1]

        return False

    # попадание по спрайту
    def minus_hp(self, tank):
        if float(tank.depth_sprite) * 1.4 >= (int(tank.depth_m) + 1) * tank.side / 7 >= float(tank.depth_sprite) * 0.4:
            for i in range(len(self.sprites.all_list)):
                if self.sprites.all_list[i].num == self.num:
                    self.sprites.all_list[i].v = 0
                    if self.sprites.all_list[i].type == 'bmp' or self.sprites.all_list[i].type == 'oth':
                        if tank.current_shooted_ammo == 0:
                            self.sprites.all_list[i].hp -= 70
                        elif tank.current_shooted_ammo == 1:
                            self.sprites.all_list[i].hp -= 100
                        elif tank.current_shooted_ammo == 2:
                            self.sprites.all_list[i].hp -= 110

    # проверка смерти спрайта
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

    # все основные параметры танка
    def all_current_parametres(self, tank):
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
                return (DELTA_ANGLE, PROJ_COEFF, horizontal, SCALE, HALF_FOV, drx, dry, height, k)

            elif tank.optic:
                DELTA_ANGLE = self.s.DELTA_ANGLE_optic_zoom
                PROJ_COEFF = self.s.PROJ_COEFF_optic_zoom
                horizontal = 3 * tank.horizontal
                SCALE = self.s.SCALE_optic
                height = self.s.HEIGHT
                HALF_FOV = self.s.HALF_FOV_optic_zoom
                drx, dry = (self.s.WIDTH // 2 - self.s.NUM_RAYS * self.s.SCALE_optic_zoom // 2, 0)
                k = 0.95
                return (DELTA_ANGLE, PROJ_COEFF, horizontal, SCALE, HALF_FOV, drx, dry, height, k)

            elif tank.thermal_d:
                DELTA_ANGLE = self.s.DELTA_ANGLE_thermal_zoom
                PROJ_COEFF = self.s.PROJ_COEFF_thermal_zoom_d
                horizontal = 3 * tank.thermal_horizontal_d
                SCALE = self.s.SCALE_thermal_d
                HALF_FOV = self.s.HALF_FOV_thermal_zoom
                drx, dry = (
                    self.s.thermal_x_d * 1.008 + self.s.thermal_width_d / 2 - self.s.NUM_RAYS * self.s.SCALE_thermal_d / 2,
                    self.s.thermal_y_d)
                height = self.s.thermal_height_d
                k = 0.6
                return (DELTA_ANGLE, PROJ_COEFF, horizontal, SCALE, HALF_FOV, drx, dry, height, k)

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
                return (DELTA_ANGLE, PROJ_COEFF, horizontal, SCALE, HALF_FOV, drx, dry, height, k)

            elif tank.thermal_d:
                DELTA_ANGLE = self.s.DELTA_ANGLE_thermal_zoom_extra
                PROJ_COEFF = self.s.PROJ_COEFF_thermal_zoom_extra_d
                horizontal = 6 * tank.thermal_horizontal_d
                SCALE = self.s.SCALE_thermal_d
                drx, dry = (
                    self.s.thermal_x_d * 1.008 + self.s.thermal_width_d / 2 - self.s.NUM_RAYS * self.s.SCALE_thermal_d / 2,
                    self.s.thermal_y_d)
                height = self.s.thermal_height_d
                HALF_FOV = self.s.HALF_FOV_thermal_zoom_extra
                k = 0.6
                return (DELTA_ANGLE, PROJ_COEFF, horizontal, SCALE, HALF_FOV, drx, dry, height, k)
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
                return (DELTA_ANGLE, PROJ_COEFF, horizontal, SCALE, HALF_FOV, drx, dry, height, k)

            elif tank.optic:
                DELTA_ANGLE = self.s.DELTA_ANGLE_optic
                PROJ_COEFF = self.s.PROJ_COEFF_optic
                horizontal = 1 * tank.horizontal
                SCALE = self.s.SCALE_optic
                height = self.s.HEIGHT
                drx, dry = (self.s.WIDTH // 2 - self.s.NUM_RAYS * self.s.SCALE_optic // 2, 0)
                HALF_FOV = self.s.HALF_FOV_optic
                k = 0.95
                return (DELTA_ANGLE, PROJ_COEFF, horizontal, SCALE, HALF_FOV, drx, dry, height, k)

            elif tank.thermal_d:
                DELTA_ANGLE = self.s.DELTA_ANGLE_thermal
                PROJ_COEFF = self.s.PROJ_COEFF_thermal_d
                horizontal = 1 * tank.thermal_horizontal_d
                SCALE = self.s.SCALE_thermal_d
                drx, dry = (
                    self.s.thermal_x_d * 1.008 + self.s.thermal_width_d / 2 - self.s.NUM_RAYS * self.s.SCALE_thermal_d / 2,
                    self.s.thermal_y_d)
                height = self.s.thermal_height_d
                HALF_FOV = self.s.HALF_FOV_thermal
                k = 0.6
                return (DELTA_ANGLE, PROJ_COEFF, horizontal, SCALE, HALF_FOV, drx, dry, height, k)
            else:
                return (False,)
