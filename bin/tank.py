import random

import pygame
import sys
import math
from bin.text import Text
from bin.test_settings import TankSettings
from bin.buttons import SelectButton, Button
from bin.damage import Damage

class Tank:
    def __init__(self, settings, x, y, movement_angle, minimap_k, x_minimap, y_minimap, apfsds_c=1, he_c=1, heat_c=1,
                 minimap_displaying=False):

        self.s = settings

        self.s.music_menu.stop()
        pygame.display.set_icon(self.s.icon)
        self.x = x
        self.y = y

        self.stab = False
        self.optic = False
        self.thermal = False
        self.zoom = False
        self.rangefinder_suo = False
        self.thermal_on = False
        self.lock = False
        self.lock_on = False
        self.extra_zoom = False
        self.ready = True
        self.block = False
        self.is_shot = False
        self.reload = False
        self.thermal_d = False
        self.menu = False
        self.is_sprite_depth = False
        self.death = False
        self.cause = ''

        self.s.background_sound.set_volume(self.s.volume_general / 100 * self.s.volume_music / 100)
        if self.s.volume_music == 0:
            self.s.background_sound.set_volume(self.s.volume_general / 100 * self.s.volume_sound / 100 * 0.5)
        self.s.background_sound.play(-1)

        self.x_minimap = x_minimap
        self.y_minimap = y_minimap
        self.minimap_k = minimap_k
        self.minimap_displaying = minimap_displaying

        self.apfsds_c, self.he_c, self.heat_c = apfsds_c, he_c, heat_c
        self.ammo_list = [self.apfsds_c, self.he_c, self.heat_c]
        self.ammo_list_text = ['БР', 'ОФ', 'КС']
        self.current_ammo = 0
        self.current_ammo_in_gun = 0
        self.current_shooted_ammo = None

        self.shot_timer = 0
        self.shot_time = 2
        self.reload_timer = 0
        self.reload_time = self.s.reload_time

        self.v = 0
        self.count_of_destroyed_targets = '0'
        self.count_of_targets = self.s.count_of_targets
        self.done = 'не выполнена'
        self.depth = '0000'
        self.depth_m = '0000'
        self.depth_sprite = '0000'
        self.true_depth = '0000'
        self.angle_of_view = 0
        self.horizontal = -self.s.HEIGHT * 0.085
        self.thermal_horizontal = -self.s.HEIGHT * 0.12
        self.thermal_horizontal_d = -self.s.HEIGHT * 0.02
        self.min_hor_thermal = -self.s.HEIGHT * 0.2
        self.min_hor_thermal_d = -self.s.HEIGHT * 0.06
        self.min_hor_optic = -self.s.HEIGHT * 0.15
        self.max_hor_thermal = self.s.HEIGHT * 0.5
        self.max_hor_thermal_d = self.s.HEIGHT * 0.15
        self.max_hor_optic = self.s.HEIGHT * 0.375
        self.lock_x = 0
        self.lock_y = 0
        self.type = 1
        self.tryaska = 0
        print(self.s.map.world_map, sep='\n')
        print(self.x, self.y)

        self.stuck = False
        self.side = min(int(self.s.WIDTH * 0.02), int(self.s.tile_w * 0.8))
        print(self.side)

        self.sky = pygame.Rect(self.s.WIDTH // 2 - self.s.HEIGHT // 2, 0, self.s.HEIGHT,
                               self.horizontal + self.s.HEIGHT // 2)
        self.sky_thermal = pygame.Rect(self.s.thermal_x + (self.s.WIDTH - self.s.thermal_base_width) // 2,
                                       self.s.thermal_y, self.s.thermal_width,
                                       self.thermal_horizontal + self.s.thermal_height // 2)
        self.sky_thermal_d = pygame.Rect(self.s.thermal_x_d,
                                         self.s.thermal_y_d_2, self.s.thermal_width,
                                         self.thermal_horizontal_d + self.s.thermal_height_d * 5 // 2)
        self.sky_thermal_color = (135 * (20 / self.s.max_t), 135 * (20 / self.s.max_t), 135 * (20 / self.s.max_t))
        self.floor_thermal_color = (45 * (20 / self.s.max_t), 45 * (20 / self.s.max_t), 45 * (20 / self.s.max_t))

        self.tank_rect = pygame.Rect(x, y, self.side, self.side)
        self.movement_angle = movement_angle
        self.walls = []
        self.damage = Damage(self)

    def start(self):
        pygame.display.set_icon(self.s.icon)
        print(sorted(self.s.map.world_map))
        show = True
        fps_count_text_bl = Text(self.s.WIDTH * 0.961, self.s.HEIGHT * 0.972, (0, 0, 0),
                                 str(int(self.s.clock.get_fps())) + ' FPS', int(self.s.WIDTH * 0.0104),
                                 is_topleft=True)
        fps_count_text = Text(self.s.WIDTH * 0.96, self.s.HEIGHT * 0.97, (200, 200, 200),
                              str(int(self.s.clock.get_fps())) + ' FPS', int(self.s.WIDTH * 0.0104),
                              is_topleft=True)
        optic_sight_button = SelectButton(self.s.optic_sight_x, self.s.optic_sight_y, self.s.optic_sight_w_r,
                                          self.s.optic_sight_h_r, 'Оптический прицел', font_size=20)
        thermal_sight_button = SelectButton(self.s.thermal_sight_x, self.s.thermal_sight_y, self.s.thermal_sight_w_r,
                                            self.s.thermal_sight_h_r, 'Тепловизор', font_size=20)
        suo_button = SelectButton(self.s.suo_x, self.s.suo_y, self.s.suo_w_r,
                                  self.s.suo_h_r, 'суо', font_size=20)
        depth_text4 = Text(self.s.thermal_x_d * 1.42, self.s.thermal_y_d_2 * 1.3937, (183, 183, 183),
                           self.depth_m[0], int(self.s.WIDTH * 0.008),
                           font_name='resources/fonts/depth_thermal_font.ttf'
                           )
        depth_text3 = Text(self.s.thermal_x_d * 1.385, self.s.thermal_y_d_2 * 1.3937, (183, 183, 183),
                           self.depth_m[1], int(self.s.WIDTH * 0.008),
                           font_name='resources/fonts/depth_thermal_font.ttf'
                           )
        depth_text2 = Text(self.s.thermal_x_d * 1.35, self.s.thermal_y_d_2 * 1.3937, (183, 183, 183),
                           self.depth_m[2], int(self.s.WIDTH * 0.008),
                           font_name='resources/fonts/depth_thermal_font.ttf'
                           )
        depth_text1 = Text(self.s.thermal_x_d * 1.319, self.s.thermal_y_d_2 * 1.3937, (183, 183, 183),
                           self.depth_m[3], int(self.s.WIDTH * 0.008),
                           font_name='resources/fonts/depth_thermal_font.ttf'
                           )
        ammo_text1 = Text(self.s.thermal_x_d * 1.165, self.s.thermal_y_d_2 * 1.3937, (183, 183, 183),
                          self.ammo_list_text[self.current_ammo][0], int(self.s.WIDTH * 0.008),
                          font_name='resources/fonts/depth_thermal_font.ttf'
                          )
        ammo_text2 = Text(self.s.thermal_x_d * 1.201, self.s.thermal_y_d_2 * 1.3937, (183, 183, 183),
                          self.ammo_list_text[self.current_ammo][1], int(self.s.WIDTH * 0.008),
                          font_name='resources/fonts/depth_thermal_font.ttf'
                          )
        ssu_text = Text(self.s.thermal_x_d * 1.12, self.s.thermal_y_d_2 * 1.393, (183, 183, 183),
                        'ССУ              ВКЛ', int(self.s.WIDTH * 0.006),
                        font_name='resources/fonts/depth_thermal_font.ttf'
                        )
        floor = pygame.Rect(self.s.thermal_x_d, 0, self.s.thermal_width,
                            self.s.HEIGHT)
        ready_text1 = Text(self.s.thermal_x_d * 1.0354, self.s.thermal_y_d_2 * 1.3937, (183, 183, 183),
                           'Г', int(self.s.WIDTH * 0.008),
                           font_name='resources/fonts/depth_thermal_font.ttf'
                           )
        ready_text2 = Text(self.s.thermal_x_d * 1.0687, self.s.thermal_y_d_2 * 1.3937, (183, 183, 183),
                           'О', int(self.s.WIDTH * 0.008),
                           font_name='resources/fonts/depth_thermal_font.ttf'
                           )
        ready_text3 = Text(self.s.thermal_x_d * 1.107, self.s.thermal_y_d_2 * 1.3937, (183, 183, 183),
                           'Т', int(self.s.WIDTH * 0.008),
                           font_name='resources/fonts/depth_thermal_font.ttf'
                           )
        weapon_text1 = Text(self.s.thermal_x_d * 1.474, self.s.thermal_y_d_2 * 1.3937, (183, 183, 183),
                           'О', int(self.s.WIDTH * 0.008),
                           font_name='resources/fonts/depth_thermal_font.ttf'
                           )
        weapon_text2 = Text(self.s.thermal_x_d * 1.507, self.s.thermal_y_d_2 * 1.3937, (183, 183, 183),
                            'С', int(self.s.WIDTH * 0.008),
                            font_name='resources/fonts/depth_thermal_font.ttf'
                            )
        weapon_text3 = Text(self.s.thermal_x_d * 1.544, self.s.thermal_y_d_2 * 1.3937, (183, 183, 183),
                            'Н', int(self.s.WIDTH * 0.008),
                            font_name='resources/fonts/depth_thermal_font.ttf'
                            )
        while show:

            self.movement_check()
            self.check_is_done()
            self.check_death()
            self.damage.check_mines()
            self.damage.check_drones()
            if self.menu:
                show = False
            optic_sight_button.check(pygame.mouse.get_pos())
            thermal_sight_button.check(pygame.mouse.get_pos())
            suo_button.check(pygame.mouse.get_pos())
            self.timer()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print(self.s.map.world_map, self.s.map.world_map_dict)
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.USEREVENT:
                    if event.button == optic_sight_button:

                        self.extra_zoom = False
                        self.thermal_d = False
                        self.optic_sight()
                        self.thermal_d = True
                        if self.menu:
                            show = False
                        print(1)
                        d = self.depth_m
                        depth_text1.set_another_text(d[0])
                        depth_text2.set_another_text(d[1])
                        depth_text3.set_another_text(d[2])
                        depth_text4.set_another_text(d[3])
                        if self.zoom:
                            self.sky = pygame.Rect(self.s.WIDTH // 2 - self.s.HEIGHT // 2, 0, self.s.HEIGHT,
                                                   3 * self.horizontal + self.s.HEIGHT // 2)
                            self.sky_thermal = pygame.Rect(
                                self.s.thermal_x + (self.s.WIDTH - self.s.thermal_base_width) // 2,
                                self.s.thermal_y,
                                self.s.thermal_width,
                                3 * self.thermal_horizontal + self.s.thermal_height // 2)
                            self.sky_thermal_d = pygame.Rect(self.s.thermal_x_d,
                                                             self.s.thermal_y_d_2, self.s.thermal_width,
                                                             3 * self.thermal_horizontal_d + self.s.thermal_height_d * 5 // 2)
                        elif self.extra_zoom:
                            self.sky = pygame.Rect(self.s.WIDTH // 2 - self.s.HEIGHT // 2, 0, self.s.HEIGHT,
                                                   6 * self.horizontal + self.s.HEIGHT // 2)
                            self.sky_thermal = pygame.Rect(
                                self.s.thermal_x + (self.s.WIDTH - self.s.thermal_base_width) // 2,
                                self.s.thermal_y,
                                self.s.thermal_width,
                                6 * self.thermal_horizontal + self.s.thermal_height // 2)
                            self.sky_thermal_d = pygame.Rect(self.s.thermal_x_d,
                                                             self.s.thermal_y_d_2, self.s.thermal_width,
                                                             6 * self.thermal_horizontal_d + self.s.thermal_height_d * 5 // 2)
                        else:
                            self.sky = pygame.Rect(self.s.WIDTH // 2 - self.s.HEIGHT // 2, 0, self.s.HEIGHT,
                                                   self.horizontal + self.s.HEIGHT // 2)
                            self.sky_thermal = pygame.Rect(
                                self.s.thermal_x + (self.s.WIDTH - self.s.thermal_base_width) // 2,
                                self.s.thermal_y,
                                self.s.thermal_width,
                                self.thermal_horizontal + self.s.thermal_height // 2)
                            self.sky_thermal_d = pygame.Rect(self.s.thermal_x_d,
                                                             self.s.thermal_y_d_2, self.s.thermal_width,
                                                             self.thermal_horizontal_d + self.s.thermal_height_d * 5 // 2)
                    elif event.button == thermal_sight_button:

                        self.thermal_d = False
                        self.thermal_sight()
                        self.thermal_d = True
                        d = self.depth_m
                        if self.menu:
                            show = False
                        depth_text1.set_another_text(d[0])
                        depth_text2.set_another_text(d[1])
                        depth_text3.set_another_text(d[2])
                        depth_text4.set_another_text(d[3])
                        ammo_text1.set_another_text(self.ammo_list_text[self.current_ammo][0])
                        ammo_text2.set_another_text(self.ammo_list_text[self.current_ammo][1])
                        print(2)
                        if self.zoom:
                            self.sky = pygame.Rect(self.s.WIDTH // 2 - self.s.HEIGHT // 2, 0, self.s.HEIGHT,
                                                   3 * self.horizontal + self.s.HEIGHT // 2)
                            self.sky_thermal = pygame.Rect(
                                self.s.thermal_x + (self.s.WIDTH - self.s.thermal_base_width) // 2,
                                self.s.thermal_y,
                                self.s.thermal_width,
                                3 * self.thermal_horizontal + self.s.thermal_height // 2)
                            self.sky_thermal_d = pygame.Rect(self.s.thermal_x_d,
                                                             self.s.thermal_y_d_2, self.s.thermal_width,
                                                             3 * self.thermal_horizontal_d + self.s.thermal_height_d * 5 // 2)
                        elif self.extra_zoom:
                            self.sky = pygame.Rect(self.s.WIDTH // 2 - self.s.HEIGHT // 2, 0, self.s.HEIGHT,
                                                   6 * self.horizontal + self.s.HEIGHT // 2)
                            self.sky_thermal = pygame.Rect(
                                self.s.thermal_x + (self.s.WIDTH - self.s.thermal_base_width) // 2,
                                self.s.thermal_y,
                                self.s.thermal_width,
                                6 * self.thermal_horizontal + self.s.thermal_height // 2)
                            self.sky_thermal_d = pygame.Rect(self.s.thermal_x_d,
                                                             self.s.thermal_y_d_2, self.s.thermal_width,
                                                             6 * self.thermal_horizontal_d + self.s.thermal_height_d * 5 // 2)
                        else:
                            self.sky = pygame.Rect(self.s.WIDTH // 2 - self.s.HEIGHT // 2, 0, self.s.HEIGHT,
                                                   self.horizontal + self.s.HEIGHT // 2)
                            self.sky_thermal = pygame.Rect(
                                self.s.thermal_x + (self.s.WIDTH - self.s.thermal_base_width) // 2,
                                self.s.thermal_y,
                                self.s.thermal_width,
                                self.thermal_horizontal + self.s.thermal_height // 2)
                            self.sky_thermal_d = pygame.Rect(self.s.thermal_x_d,
                                                             self.s.thermal_y_d_2, self.s.thermal_width,
                                                             self.thermal_horizontal_d + self.s.thermal_height_d * 5 // 2)
                    elif event.button == suo_button:
                        self.suo()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # show = False
                        self.s.display.blit(self.s.gunner_site2)
                        self.exit()

                    if event.key == pygame.K_e and self.rangefinder_suo:
                        d = self.rangefinder()
                        depth_text1.set_another_text(d[0])
                        depth_text2.set_another_text(d[1])
                        depth_text3.set_another_text(d[2])
                        depth_text4.set_another_text(d[3])
                    if event.key == pygame.K_z:
                        self.zoom = True if self.zoom is False else False
                        self.extra_zoom = False
                        if self.zoom:
                            self.sky = pygame.Rect(self.s.WIDTH // 2 - self.s.HEIGHT // 2, 0, self.s.HEIGHT,
                                                   3 * self.horizontal + self.s.HEIGHT // 2)
                            self.sky_thermal = pygame.Rect(
                                self.s.thermal_x + (self.s.WIDTH - self.s.thermal_base_width) // 2,
                                self.s.thermal_y,
                                self.s.thermal_width,
                                3 * self.thermal_horizontal + self.s.thermal_height // 2)
                            self.sky_thermal_d = pygame.Rect(self.s.thermal_x_d,
                                                             self.s.thermal_y_d_2, self.s.thermal_width,
                                                             3 * self.thermal_horizontal_d + self.s.thermal_height_d * 5 // 2)
                        else:
                            self.sky = pygame.Rect(self.s.WIDTH // 2 - self.s.HEIGHT // 2, 0, self.s.HEIGHT,
                                                   self.horizontal + self.s.HEIGHT // 2)
                            self.sky_thermal = pygame.Rect(
                                self.s.thermal_x + (self.s.WIDTH - self.s.thermal_base_width) // 2,
                                self.s.thermal_y,
                                self.s.thermal_width,
                                self.thermal_horizontal + self.s.thermal_height // 2)
                            self.sky_thermal_d = pygame.Rect(self.s.thermal_x_d,
                                                             self.s.thermal_y_d_2, self.s.thermal_width,
                                                             self.thermal_horizontal_d + self.s.thermal_height_d * 5 // 2)
                    if event.key == pygame.K_LSHIFT:
                        self.extra_zoom = True if self.extra_zoom is False else False
                        self.zoom = False
                        if self.extra_zoom:
                            self.sky = pygame.Rect(self.s.WIDTH // 2 - self.s.HEIGHT // 2, 0, self.s.HEIGHT,
                                                   6 * self.horizontal + self.s.HEIGHT // 2)
                            self.sky_thermal = pygame.Rect(
                                self.s.thermal_x + (self.s.WIDTH - self.s.thermal_base_width) // 2,
                                self.s.thermal_y,
                                self.s.thermal_width,
                                6 * self.thermal_horizontal + self.s.thermal_height // 2)
                            self.sky_thermal_d = pygame.Rect(self.s.thermal_x_d,
                                                             self.s.thermal_y_d_2, self.s.thermal_width,
                                                             6 * self.thermal_horizontal_d + self.s.thermal_height_d * 5 // 2)
                        else:
                            self.sky = pygame.Rect(self.s.WIDTH // 2 - self.s.HEIGHT // 2, 0, self.s.HEIGHT,
                                                   self.horizontal + self.s.HEIGHT // 2)
                            self.sky_thermal = pygame.Rect(
                                self.s.thermal_x + (self.s.WIDTH - self.s.thermal_base_width) // 2,
                                self.s.thermal_y,
                                self.s.thermal_width,
                                self.thermal_horizontal + self.s.thermal_height // 2)
                            self.sky_thermal_d = pygame.Rect(self.s.thermal_x_d,
                                                             self.s.thermal_y_d_2, self.s.thermal_width,
                                                             self.thermal_horizontal_d + self.s.thermal_height_d * 5 // 2)
                    self.ammo(event, [ammo_text1, ammo_text2])
                    if event.key == pygame.K_r and self.ready is False and self.is_shot is False and self.reload is False and \
                            self.ammo_list[self.current_ammo] > 0:
                        self.reload = True
                        self.block = True
                        print(self.ammo_list)
                        self.current_ammo_in_gun = int(str(self.current_ammo)[:])
                        print(self.ammo_list)

                optic_sight_button.handle_event(event)
                thermal_sight_button.handle_event(event)
                suo_button.handle_event(event)
            self.movement()
            # self.guidance()
            self.s.display.blit(self.s.gunner_site, (0, 0))
            if self.thermal_on:
                pygame.draw.rect(self.s.display, self.floor_thermal_color, floor)
                pygame.draw.rect(self.s.display, self.sky_thermal_color, self.sky_thermal_d)
                if self.zoom:
                    self.ray_casting(self.s.thermal_x_d,
                                     self.s.thermal_y_d, sight_type='4d')
                    temp = self.walls + [obj.object_locate(self) for obj in self.s.sprites.list_of_objects_thermal if not obj.death]
                    self.world(temp, self.s.thermal_sight_zoom_d,
                               (self.s.thermal_x_d, self.s.thermal_y_d_2))
                elif self.extra_zoom:
                    self.ray_casting(self.s.thermal_x_d,
                                     self.s.thermal_y_d, sight_type='4.5d')
                    temp = self.walls + [obj.object_locate(self) for obj in self.s.sprites.list_of_objects_thermal if not obj.death]
                    self.world(temp, self.s.thermal_sight_zoom_d,
                               (self.s.thermal_x_d, self.s.thermal_y_d_2))
                else:
                    self.ray_casting(self.s.thermal_x_d,
                                     self.s.thermal_y_d, sight_type='3d')
                    temp = self.walls + [obj.object_locate(self) for obj in self.s.sprites.list_of_objects_thermal if not obj.death]
                    self.world(temp, self.s.thermal_sight_d,
                               (self.s.thermal_x_d * 1.01, self.s.thermal_y_d_2))
                # optic_sight_button.draw(self.s.display)
                # thermal_sight_button.draw(self.s.display)
                # suo_button.draw(self.s.display)
                if self.zoom or self.extra_zoom:
                    depth_text1.draw(self.s.display)
                    depth_text2.draw(self.s.display)
                    depth_text3.draw(self.s.display)
                    depth_text4.draw(self.s.display)
                    ammo_text1.draw(self.s.display)
                    ammo_text2.draw(self.s.display)
                    weapon_text1.draw(self.s.display)
                    weapon_text2.draw(self.s.display)
                    weapon_text3.draw(self.s.display)
                    if self.ready:
                        ready_text1.draw(self.s.display)
                        ready_text2.draw(self.s.display)
                        ready_text3.draw(self.s.display)
                else:
                    ssu_text.draw(self.s.display)
            self.s.display.blit(self.s.gunner_site2)
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
        if self.minimap_displaying:
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

    def exit(self):
        pygame.display.set_icon(self.s.icon)
        exit_to_menu_button = Button(self.s.WIDTH * 0.33, self.s.HEIGHT * 0.51, self.s.WIDTH * 0.33, self.s.HEIGHT * 0.1, 'Выйти в меню', self.s.size_text_b, 'resources/images/button_inact.png',
                              'resources/images/button_active.png',
                              'resources/sounds/button_menu_sound.mp3')
        continue_button = Button(self.s.WIDTH * 0.33, self.s.HEIGHT * 0.32, self.s.WIDTH * 0.33, self.s.HEIGHT * 0.1, 'Продолжить', self.s.size_text_b, 'resources/images/button_inact.png',
                              'resources/images/button_active.png',
                              'resources/sounds/button_menu_sound.mp3')
        quit_button = Button(self.s.WIDTH * 0.33, self.s.HEIGHT * 0.69, self.s.WIDTH * 0.33, self.s.HEIGHT * 0.1,
                             'Выйти', self.s.size_text_b, 'resources/images/button_inact.png',
                             'resources/images/button_active.png',
                             'resources/sounds/button_menu_sound.mp3')
        guidence_text = Text(round(self.s.WIDTH * 0.7), round(self.s.HEIGHT * 0.3), (200, 200, 200), 'Управление:',
                    int(self.s.WIDTH * 0.01),
                    is_topleft=True)
        q_text = Text(self.s.WIDTH * 0.7, self.s.HEIGHT * 0.33, (200, 200, 200), 'Q - захват цели',
                    int(self.s.WIDTH * 0.01),
                    is_topleft=True)
        e_text = Text(self.s.WIDTH * 0.7, self.s.HEIGHT * 0.36, (200, 200, 200), 'E - замер дистанции',
                      int(self.s.WIDTH * 0.01),
                      is_topleft=True)
        r_text = Text(self.s.WIDTH * 0.7, self.s.HEIGHT * 0.39, (200, 200, 200), 'R - перезарядка',
                      int(self.s.WIDTH * 0.01),
                      is_topleft=True)
        lkm_text = Text(self.s.WIDTH * 0.7, self.s.HEIGHT * 0.42, (200, 200, 200), 'ЛКМ - выстрел',
                      int(self.s.WIDTH * 0.01),
                      is_topleft=True)
        background = pygame.Surface((self.s.WIDTH, self.s.HEIGHT))
        background.set_alpha(128)
        background.fill((1, 1, 1))
        background_text = pygame.Surface((self.s.WIDTH * 0.2, self.s.HEIGHT * 0.2))
        background_text.set_alpha(128)
        background_text.fill((37, 46, 37))
        self.s.display.blit(background, (0, 0))
        self.s.display.blit(background_text, (self.s.WIDTH * 0.68, self.s.HEIGHT * 0.28))
        show = True
        pygame.mouse.set_visible(True)
        while show:
            # self.s.display.blit(background, (0, 0))
            continue_button.check(pygame.mouse.get_pos())
            exit_to_menu_button.check(pygame.mouse.get_pos())
            quit_button.check(pygame.mouse.get_pos())
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.USEREVENT:
                    if event.button == continue_button:
                        show = False
                    elif event.button == quit_button:
                        pygame.quit()
                        sys.exit()
                    elif event.button == exit_to_menu_button:
                        self.s.music_menu.play(-1)
                        self.s.music_menu.set_volume(self.s.volume_general / 100 * self.s.volume_music / 100)
                        self.s.background_sound.stop()
                        self.s.reload_sound.stop()
                        self.s.shoot_sound.stop()
                        self.menu = True
                        show = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        show = False

                continue_button.handle_event(event, self.s.volume_sound * (self.s.volume_general / 100))
                exit_to_menu_button.handle_event(event, self.s.volume_sound * (self.s.volume_general / 100))
                quit_button.handle_event(event, self.s.volume_sound * (self.s.volume_general / 100))


            continue_button.draw(self.s.display)
            exit_to_menu_button.draw(self.s.display)
            quit_button.draw(self.s.display)
            guidence_text.draw(self.s.display)
            q_text.draw(self.s.display)
            e_text.draw(self.s.display)
            r_text.draw(self.s.display)
            lkm_text.draw(self.s.display)

            pygame.display.flip()
            self.s.clock.tick(self.s.FPS)
        pygame.mouse.set_visible(False)

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
        # print(self.is_sprite_depth, ((self.x - self.lock_x) ** 2 + (self.y - self.lock_y) ** 2) ** 0.5, float(self.depth))
        if int(((self.x - self.lock_x) ** 2 + (self.y - self.lock_y) ** 2) ** 0.5) > float(self.depth) * 1.006:
            self.lock = False
        if self.lock:
            if (self.x - self.lock_x > 0 and self.y - self.lock_y > 0) or (
                    self.x - self.lock_x > 0 and self.y - self.lock_y < 0):
                self.angle_of_view = self.lock_f(self.lock_x, self.lock_y) * 180 / 3.14 + 180
            else:
                print(self.lock_x, self.lock_y)
                self.angle_of_view = self.lock_f(self.lock_x, self.lock_y) * 180 / 3.14

        # if keys[pygame.K_RIGHT] and not self.lock:
        #     self.angle_of_view += self.s.tower_v * t
        #
        # elif keys[pygame.K_LEFT] and not self.lock:
        #     self.angle_of_view -= self.s.tower_v * t



        if keys[pygame.K_RIGHT] and not self.lock:
            self.angle_of_view += self.s.tower_v * t

        elif keys[pygame.K_LEFT] and not self.lock:
            self.angle_of_view -= self.s.tower_v * t
        elif keys[pygame.K_UP]:
            if self.block is False:
                self.horizontal = min(self.horizontal + self.s.vertical_v * t, self.max_hor_optic)
                self.thermal_horizontal = min(self.thermal_horizontal + self.s.vertical_v * t, self.max_hor_thermal)
                self.thermal_horizontal_d = min(self.thermal_horizontal_d + self.s.vertical_v * t, self.max_hor_thermal_d)
                if self.zoom:
                    self.sky = pygame.Rect(self.s.WIDTH // 2 - self.s.HEIGHT // 2, 0, self.s.HEIGHT,
                                           3 * self.horizontal + self.s.HEIGHT // 2)
                    self.sky_thermal = pygame.Rect(self.s.thermal_x + (self.s.WIDTH - self.s.thermal_base_width) // 2,
                                                   self.s.thermal_y, self.s.thermal_width,
                                                   3 * self.thermal_horizontal + self.s.thermal_height // 2)
                    self.sky_thermal_d = pygame.Rect(self.s.thermal_x_d,
                                                     self.s.thermal_y_d_2, self.s.thermal_width,
                                                     3 * self.thermal_horizontal_d / 2 + self.s.thermal_height_d // 2)

                elif self.extra_zoom:
                    self.sky = pygame.Rect(self.s.WIDTH // 2 - self.s.HEIGHT // 2, 0, self.s.HEIGHT,
                                           6 * self.horizontal + self.s.HEIGHT // 2)
                    self.sky_thermal = pygame.Rect(self.s.thermal_x + (self.s.WIDTH - self.s.thermal_base_width) // 2,
                                                   self.s.thermal_y, self.s.thermal_width,
                                                   6 * self.thermal_horizontal + self.s.thermal_height // 2)
                    self.sky_thermal_d = pygame.Rect(self.s.thermal_x_d,
                                                     self.s.thermal_y_d_2, self.s.thermal_width,
                                                     6 * self.thermal_horizontal_d / 2 + self.s.thermal_height_d // 2)
                else:
                    self.sky = pygame.Rect(self.s.WIDTH // 2 - self.s.HEIGHT // 2, 0, self.s.HEIGHT,
                                           self.horizontal + self.s.HEIGHT // 2)
                    self.sky_thermal = pygame.Rect(self.s.thermal_x + (self.s.WIDTH - self.s.thermal_base_width) // 2,
                                                   self.s.thermal_y, self.s.thermal_width,
                                                   self.thermal_horizontal + self.s.thermal_height // 2)
                    self.sky_thermal_d = pygame.Rect(self.s.thermal_x_d,
                                                     self.s.thermal_y_d_2, self.s.thermal_width,
                                                     self.thermal_horizontal_d / 2 + self.s.thermal_height_d // 2)
        elif keys[pygame.K_DOWN]:
            if self.block is False:
                self.horizontal = max(self.horizontal - self.s.vertical_v * t, self.min_hor_optic)
                self.thermal_horizontal = max(self.thermal_horizontal - self.s.vertical_v * t, self.min_hor_thermal)
                self.thermal_horizontal_d = max(self.thermal_horizontal_d - self.s.vertical_v * t, self.min_hor_thermal_d)
                if self.zoom:
                    self.sky = pygame.Rect(self.s.WIDTH // 2 - self.s.HEIGHT // 2, 0, self.s.HEIGHT,
                                           3 * self.horizontal + self.s.HEIGHT // 2)
                    self.sky_thermal = pygame.Rect(self.s.thermal_x + (self.s.WIDTH - self.s.thermal_base_width) // 2,
                                                   self.s.thermal_y, self.s.thermal_width,
                                                   3 * self.thermal_horizontal + self.s.thermal_height // 2)
                    self.sky_thermal_d = pygame.Rect(self.s.thermal_x_d,
                                                     self.s.thermal_y_d_2, self.s.thermal_width,
                                                     3 * self.thermal_horizontal_d + self.s.thermal_height_d * 5 // 2)
                elif self.extra_zoom:
                    self.sky = pygame.Rect(self.s.WIDTH // 2 - self.s.HEIGHT // 2, 0, self.s.HEIGHT,
                                           6 * self.horizontal + self.s.HEIGHT // 2)
                    self.sky_thermal = pygame.Rect(self.s.thermal_x + (self.s.WIDTH - self.s.thermal_base_width) // 2,
                                                   self.s.thermal_y, self.s.thermal_width,
                                                   6 * self.thermal_horizontal + self.s.thermal_height // 2)
                    self.sky_thermal_d = pygame.Rect(self.s.thermal_x_d,
                                                     self.s.thermal_y_d_2, self.s.thermal_width,
                                                     6 * self.thermal_horizontal_d + self.s.thermal_height_d * 5 // 2)
                else:
                    self.sky = pygame.Rect(self.s.WIDTH // 2 - self.s.HEIGHT // 2, 0, self.s.HEIGHT,
                                           self.horizontal + self.s.HEIGHT // 2)
                    self.sky_thermal = pygame.Rect(self.s.thermal_x + (self.s.WIDTH - self.s.thermal_base_width) // 2,
                                                   self.s.thermal_y, self.s.thermal_width,
                                                   self.s.thermal_height // 2 + self.thermal_horizontal)
                    self.sky_thermal_d = pygame.Rect(self.s.thermal_x_d,
                                                     self.s.thermal_y_d_2, self.s.thermal_width,
                                                     self.thermal_horizontal_d + self.s.thermal_height_d * 5 // 2)
        else:
            if pygame.mouse.get_focused() and not self.lock:
                dif_x = pygame.mouse.get_pos()[0] - self.s.WIDTH // 2
                dif_y = pygame.mouse.get_pos()[1] - self.s.HEIGHT // 2
                if self.block is False:
                    self.horizontal = min(self.horizontal + -dif_y * self.s.vertical_v * t / (self.s.WIDTH * 0.01), self.max_hor_optic)
                    self.thermal_horizontal = min(self.thermal_horizontal + -dif_y * self.s.vertical_v * t / (self.s.WIDTH * 0.01), self.max_hor_thermal)
                    self.thermal_horizontal_d = min(self.thermal_horizontal_d + -dif_y * self.s.vertical_v * t / (self.s.WIDTH * 0.01),
                                                    self.max_hor_thermal_d)
                    if self.zoom:
                        self.sky = pygame.Rect(self.s.WIDTH // 2 - self.s.HEIGHT // 2, 0, self.s.HEIGHT,
                                               3 * self.horizontal + self.s.HEIGHT // 2)
                        self.sky_thermal = pygame.Rect(
                            self.s.thermal_x + (self.s.WIDTH - self.s.thermal_base_width) // 2,
                            self.s.thermal_y, self.s.thermal_width,
                            3 * self.thermal_horizontal + self.s.thermal_height // 2)
                        self.sky_thermal_d = pygame.Rect(self.s.thermal_x_d,
                                                         self.s.thermal_y_d_2, self.s.thermal_width,
                                                         3 * self.thermal_horizontal_d / 2 + self.s.thermal_height_d // 2)

                    elif self.extra_zoom:
                        self.sky = pygame.Rect(self.s.WIDTH // 2 - self.s.HEIGHT // 2, 0, self.s.HEIGHT,
                                               6 * self.horizontal + self.s.HEIGHT // 2)
                        self.sky_thermal = pygame.Rect(
                            self.s.thermal_x + (self.s.WIDTH - self.s.thermal_base_width) // 2,
                            self.s.thermal_y, self.s.thermal_width,
                            6 * self.thermal_horizontal + self.s.thermal_height // 2)
                        self.sky_thermal_d = pygame.Rect(self.s.thermal_x_d,
                                                         self.s.thermal_y_d_2, self.s.thermal_width,
                                                         6 * self.thermal_horizontal_d / 2 + self.s.thermal_height_d // 2)
                    else:
                        self.sky = pygame.Rect(self.s.WIDTH // 2 - self.s.HEIGHT // 2, 0, self.s.HEIGHT,
                                               self.horizontal + self.s.HEIGHT // 2)
                        self.sky_thermal = pygame.Rect(
                            self.s.thermal_x + (self.s.WIDTH - self.s.thermal_base_width) // 2,
                            self.s.thermal_y, self.s.thermal_width,
                            self.thermal_horizontal + self.s.thermal_height // 2)
                        self.sky_thermal_d = pygame.Rect(self.s.thermal_x_d,
                                                         self.s.thermal_y_d_2, self.s.thermal_width,
                                                         self.thermal_horizontal_d / 2 + self.s.thermal_height_d // 2)
                pygame.mouse.set_pos((self.s.WIDTH // 2, self.s.HEIGHT // 2))
                self.angle_of_view += dif_x * self.s.tower_v * t / (self.s.WIDTH * 0.07)
        if self.type == 0:
            self.horizontal = self.tryaska
            self.thermal_horizontal = self.tryaska
            self.thermal_horizontal_d = self.tryaska
            self.type = 1
            if self.zoom:
                self.sky = pygame.Rect(self.s.WIDTH // 2 - self.s.HEIGHT // 2, 0, self.s.HEIGHT,
                                       3 * self.horizontal + self.s.HEIGHT // 2)
                self.sky_thermal = pygame.Rect(self.s.thermal_x + (self.s.WIDTH - self.s.thermal_base_width) // 2,
                                               self.s.thermal_y, self.s.thermal_width,
                                               3 * self.thermal_horizontal + self.s.thermal_height // 2)
                self.sky_thermal_d = pygame.Rect(self.s.thermal_x_d,
                                                 self.s.thermal_y_d_2, self.s.thermal_width,
                                                 3 * self.thermal_horizontal_d + self.s.thermal_height_d * 5 // 2)

            elif self.extra_zoom:
                self.sky = pygame.Rect(self.s.WIDTH // 2 - self.s.HEIGHT // 2, 0, self.s.HEIGHT,
                                       6 * self.horizontal + self.s.HEIGHT // 2)
                self.sky_thermal = pygame.Rect(self.s.thermal_x + (self.s.WIDTH - self.s.thermal_base_width) // 2,
                                               self.s.thermal_y, self.s.thermal_width,
                                               6 * self.thermal_horizontal + self.s.thermal_height // 2)
                self.sky_thermal_d = pygame.Rect(self.s.thermal_x_d,
                                                 self.s.thermal_y_d_2, self.s.thermal_width,
                                                 6 * self.thermal_horizontal_d + self.s.thermal_height_d * 5 // 2)
            else:
                self.sky = pygame.Rect(self.s.WIDTH // 2 - self.s.HEIGHT // 2, 0, self.s.HEIGHT,
                                       self.horizontal + self.s.HEIGHT // 2)
                self.sky_thermal = pygame.Rect(self.s.thermal_x + (self.s.WIDTH - self.s.thermal_base_width) // 2,
                                               self.s.thermal_y, self.s.thermal_width,
                                               self.thermal_horizontal + self.s.thermal_height // 2)
                self.sky_thermal_d = pygame.Rect(self.s.thermal_x_d,
                                                 self.s.thermal_y_d_2, self.s.thermal_width,
                                                 self.thermal_horizontal_d + self.s.thermal_height_d * 5 // 2)
        elif self.stab is False and self.v != 0 and self.type == 1:
            if abs(self.v) < self.s.max_speed_w * 0.1:
                self.tryaska = self.horizontal
                self.horizontal += random.randint(-int(self.s.HEIGHT * 0.005), int(self.s.HEIGHT * 0.005))
                self.thermal_horizontal = self.horizontal
                self.thermal_horizontal_d = self.horizontal
                self.type = 0
            elif abs(self.v) < self.s.max_speed_w * 0.3:
                self.tryaska = self.horizontal
                self.horizontal += random.randint(-int(self.s.HEIGHT * 0.01), int(self.s.HEIGHT * 0.01))
                self.thermal_horizontal = self.horizontal
                self.thermal_horizontal_d = self.horizontal
                self.type = 0
            elif abs(self.v) < self.s.max_speed_w * 0.5:
                self.tryaska = self.horizontal
                self.horizontal += random.randint(-int(self.s.HEIGHT * 0.02), int(self.s.HEIGHT * 0.02))
                self.thermal_horizontal = self.horizontal
                self.thermal_horizontal_d = self.horizontal
                self.type = 0
            elif abs(self.v) < self.s.max_speed_w * 0.7:
                self.tryaska = self.horizontal
                self.horizontal += random.randint(-int(self.s.HEIGHT * 0.025), int(self.s.HEIGHT * 0.025))
                self.thermal_horizontal = self.horizontal
                self.thermal_horizontal_d = self.horizontal
                self.type = 0
            elif abs(self.v) <= self.s.max_speed_w:
                self.tryaska = self.horizontal
                self.horizontal += random.randint(-int(self.s.HEIGHT * 0.03), int(self.s.HEIGHT * 0.03))
                self.thermal_horizontal = self.horizontal
                self.thermal_horizontal_d = self.horizontal
                self.type = 0

            if self.zoom:
                self.sky = pygame.Rect(self.s.WIDTH // 2 - self.s.HEIGHT // 2, 0, self.s.HEIGHT,
                                       3 * self.horizontal + self.s.HEIGHT // 2)
                self.sky_thermal = pygame.Rect(self.s.thermal_x + (self.s.WIDTH - self.s.thermal_base_width) // 2,
                                               self.s.thermal_y, self.s.thermal_width,
                                               3 * self.thermal_horizontal + self.s.thermal_height // 2)
                self.sky_thermal_d = pygame.Rect(self.s.thermal_x_d,
                                                 self.s.thermal_y_d_2, self.s.thermal_width,
                                                 3 * self.thermal_horizontal_d + self.s.thermal_height_d * 5 // 2)

            elif self.extra_zoom:
                self.sky = pygame.Rect(self.s.WIDTH // 2 - self.s.HEIGHT // 2, 0, self.s.HEIGHT,
                                       6 * self.horizontal + self.s.HEIGHT // 2)
                self.sky_thermal = pygame.Rect(self.s.thermal_x + (self.s.WIDTH - self.s.thermal_base_width) // 2,
                                               self.s.thermal_y, self.s.thermal_width,
                                               6 * self.thermal_horizontal + self.s.thermal_height // 2)
                self.sky_thermal_d = pygame.Rect(self.s.thermal_x_d,
                                                 self.s.thermal_y_d_2, self.s.thermal_width,
                                                 6 * self.thermal_horizontal_d + self.s.thermal_height_d * 5 // 2)
            else:
                self.sky = pygame.Rect(self.s.WIDTH // 2 - self.s.HEIGHT // 2, 0, self.s.HEIGHT,
                                       self.horizontal + self.s.HEIGHT // 2)
                self.sky_thermal = pygame.Rect(self.s.thermal_x + (self.s.WIDTH - self.s.thermal_base_width) // 2,
                                               self.s.thermal_y, self.s.thermal_width,
                                               self.thermal_horizontal + self.s.thermal_height // 2)
                self.sky_thermal_d = pygame.Rect(self.s.thermal_x_d,
                                                 self.s.thermal_y_d_2, self.s.thermal_width,
                                                 self.thermal_horizontal_d + self.s.thermal_height_d * 5 // 2)
        self.angle_of_view %= 360
        # if self.angle_of_view < 0:
        #     self.angle_of_view = 360 + self.angle_of_view

    def ammo(self, event, text):
        if event.key == pygame.K_1:
            self.current_ammo = 0
        elif event.key == pygame.K_2:
            self.current_ammo = 1
        elif event.key == pygame.K_3:
            self.current_ammo = 2
        if len(text) > 1:
            for i in range(len(text)):
                text[i].set_another_text(self.ammo_list_text[self.current_ammo][i])
        else:
            text[0].set_another_text(self.ammo_list_text[self.current_ammo])

    def suo(self):
        self.stab = True if self.stab is False else False
        self.rangefinder_suo = True if self.rangefinder_suo is False else False
        self.thermal_on = True if self.thermal_on is False else False
        self.lock_on = True if self.lock_on is False else False
        self.thermal_d = True if self.thermal_d is False else False

    def timer(self):
        if self.shot_timer >= self.shot_time:
            self.is_shot = False
            self.block = False
            self.current_shooted_ammo = None
            self.shot_timer = 0
        if self.reload_timer >= self.reload_time:
            self.reload = False
            self.block = False
            self.ready = True
            self.reload_timer = 0
        if self.is_shot:
            self.shot_timer += 1 / self.s.FPS
        if self.reload:
            self.reload_timer += 1 / self.s.FPS
    def mapping(self, a, b):
        return (a // self.s.tile_w) * self.s.tile_w, (b // self.s.tile_h) * self.s.tile_h

    def mapping_in_map(self, a, b):
        return (a // self.s.tile_w), (b // self.s.tile_h)

    def ray_casting(self, dr_x=0, dr_y=0, sight_type='1'):
        self.walls = []
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
                        # print(1)
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
                        # print(2)
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
                if int(texture) % 2 == 0:
                    # self.s.display.blit(wall_column,
                    #                     (dr_x + i * self.s.SCALE_optic,
                    #                      self.horizontal + dr_y + self.s.HEIGHT // 2 - proj_height // 2))
                    # self.s.display.blit(wall_column,
                    #                     (dr_x + i * self.s.SCALE_optic,
                    #                      self.horizontal + dr_y + self.s.HEIGHT // 2 - proj_height // 2 - proj_height))
                    pos1 = (dr_x + i * self.s.SCALE_optic,
                                         self.horizontal + dr_y + self.s.HEIGHT // 2 - proj_height // 2)
                    pos2 = (dr_x + i * self.s.SCALE_optic,
                                         self.horizontal + dr_y + self.s.HEIGHT // 2 - proj_height // 2 - proj_height)
                    self.walls.append((depth, wall_column, pos1))
                    self.walls.append((depth, wall_column, pos2))
                else:
                    # self.s.display.blit(wall_column,
                    #                     (dr_x + i * self.s.SCALE_optic,
                    #                      self.horizontal + dr_y + self.s.HEIGHT // 2 - proj_height // 2))
                    pos1 = (dr_x + i * self.s.SCALE_optic,
                                         self.horizontal + dr_y + self.s.HEIGHT // 2 - proj_height // 2)
                    self.walls.append((depth, wall_column, pos1))
                if int(cur_angle) == int(self.angle_of_view):
                    self.depth = str(depth)
                cur_angle += self.s.DELTA_ANGLE_optic
            # self.s.display.blit(self.s.optic_sight, (dr_x, dr_y))

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
                                                                      self.s.texture_w - offset * self.s.texture_scale,
                                                                      self.s.texture_h)
                else:
                    wall_column = self.s.textures[texture].subsurface(offset * self.s.texture_scale, 0,
                                                                      self.s.texture_scale, self.s.texture_h)
                wall_column = pygame.transform.scale(wall_column, (self.s.SCALE_optic_zoom, proj_height))

                if int(texture) % 2 == 0:
                    # self.s.display.blit(wall_column,
                    #                     (dr_x + i * self.s.SCALE_optic_zoom,
                    #                      3 * self.horizontal + dr_y + self.s.HEIGHT // 2 - proj_height // 2))
                    # self.s.display.blit(wall_column,
                    #                     (dr_x + i * self.s.SCALE_optic_zoom,
                    #                      3 * self.horizontal + dr_y + self.s.HEIGHT // 2 - proj_height // 2 - proj_height))
                    pos1 = (dr_x + i * self.s.SCALE_optic_zoom,
                                         3 * self.horizontal + dr_y + self.s.HEIGHT // 2 - proj_height // 2)
                    pos2 = (dr_x + i * self.s.SCALE_optic_zoom,
                                         3 * self.horizontal + dr_y + self.s.HEIGHT // 2 - proj_height // 2 - proj_height)
                    self.walls.append((depth, wall_column, pos1))
                    self.walls.append((depth, wall_column, pos2))
                else:
                    # self.s.display.blit(wall_column,
                    #                     (dr_x + i * self.s.SCALE_optic_zoom,
                    #                      3 * self.horizontal + dr_y + self.s.HEIGHT // 2 - proj_height // 2))
                    pos1 = (dr_x + i * self.s.SCALE_optic_zoom,
                            3 * self.horizontal + dr_y + self.s.HEIGHT // 2 - proj_height // 2)
                    self.walls.append((depth, wall_column, pos1))

                if int(cur_angle) == int(self.angle_of_view):
                    self.depth = str(depth)
                cur_angle += self.s.DELTA_ANGLE_optic_zoom
            # self.s.display.blit(self.s.optic_sight_zoom, (dr_x, dr_y))

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
                if int(texture) % 2 == 0:
                    # self.s.display.blit(wall_column,
                    #                     (dr_x + i * self.s.SCALE_thermal,
                    #                      self.thermal_horizontal + dr_y + self.s.thermal_height // 2 - proj_height // 2))
                    # self.s.display.blit(wall_column,
                    #                     (dr_x + i * self.s.SCALE_thermal,
                    #                      self.thermal_horizontal + dr_y + self.s.thermal_height // 2 - proj_height // 2 - proj_height))
                    pos1 = (dr_x + i * self.s.SCALE_thermal,
                                         self.thermal_horizontal + dr_y + self.s.thermal_height // 2 - proj_height // 2)
                    pos2 = (dr_x + i * self.s.SCALE_thermal,
                                         self.thermal_horizontal + dr_y + self.s.thermal_height // 2 - proj_height // 2 - proj_height)
                    self.walls.append((depth, wall_column, pos1))
                    self.walls.append((depth, wall_column, pos2))
                else:
                    # self.s.display.blit(wall_column,
                    #                     (dr_x + i * self.s.SCALE_thermal,
                    #                      self.thermal_horizontal + dr_y + self.s.thermal_height // 2 - proj_height // 2))
                    pos1 = (dr_x + i * self.s.SCALE_thermal,
                            self.thermal_horizontal + dr_y + self.s.thermal_height // 2 - proj_height // 2)
                    self.walls.append((depth, wall_column, pos1))
                if int(cur_angle) == int(self.angle_of_view):
                    self.depth = str(depth)
                cur_angle += self.s.DELTA_ANGLE_thermal
            # self.s.display.blit(self.s.thermal_sight, (dr_x, dr_y))

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
                if int(texture) % 2 == 0:
                    # self.s.display.blit(wall_column,
                    #                     (dr_x + i * self.s.SCALE_thermal,
                    #                      3 * self.thermal_horizontal + dr_y + self.s.thermal_height // 2 - proj_height // 2))
                    # self.s.display.blit(wall_column,
                    #                     (dr_x + i * self.s.SCALE_thermal,
                    #                      3 * self.thermal_horizontal + dr_y + self.s.thermal_height // 2 - proj_height // 2 - proj_height))
                    pos1 = (dr_x + i * self.s.SCALE_thermal,
                                         3 * self.thermal_horizontal + dr_y + self.s.thermal_height // 2 - proj_height // 2)
                    pos2 = (dr_x + i * self.s.SCALE_thermal,
                                         3 * self.thermal_horizontal + dr_y + self.s.thermal_height // 2 - proj_height // 2 - proj_height)
                    self.walls.append((depth, wall_column, pos1))
                    self.walls.append((depth, wall_column, pos2))
                else:
                    # self.s.display.blit(wall_column,
                    #                     (dr_x + i * self.s.SCALE_thermal,
                    #                      3 * self.thermal_horizontal + dr_y + self.s.thermal_height // 2 - proj_height // 2))
                    pos1 = (dr_x + i * self.s.SCALE_thermal,
                                          3 * self.thermal_horizontal + dr_y + self.s.thermal_height // 2 - proj_height // 2)
                    self.walls.append((depth, wall_column, pos1))
                if int(cur_angle) == int(self.angle_of_view):
                    self.depth = str(depth)
                cur_angle += self.s.DELTA_ANGLE_thermal_zoom
            # self.s.display.blit(self.s.thermal_sight_zoom, (dr_x, dr_y))

        elif sight_type == '4.5':
            x0, y0 = self.x, self.y
            xm, ym = self.mapping(x0, y0)
            cur_angle = self.angle_of_view - self.s.HALF_FOV_thermal_zoom_extra + 0.00001
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
                        texture_h = None
                        break
                    y += dy * self.s.tile_h
                depth, offset, texture = (depth_v, yv, texture_v) if depth_v < depth_h else (depth_h, xh, texture_h)
                offset = int(offset) % self.s.tile_w
                depth *= math.cos((self.angle_of_view - cur_angle) * 3.14 / 180)
                proj_height = min(int(self.s.PROJ_COEFF_thermal_zoom_extra / depth), 5 * self.s.thermal_height)
                if self.s.texture_scale + offset * self.s.texture_scale > self.s.texture_w:
                    wall_column = self.s.thermal_textures[texture][0].subsurface(offset * self.s.texture_scale, 0,
                                                                                 self.s.texture_w - offset * self.s.texture_scale,
                                                                                 self.s.texture_h)
                else:
                    wall_column = self.s.thermal_textures[texture][0].subsurface(offset * self.s.texture_scale, 0,
                                                                                 self.s.texture_scale, self.s.texture_h)
                wall_column = pygame.transform.scale(wall_column, (self.s.SCALE_thermal, proj_height))
                if int(texture) % 2 == 0:
                    self.s.display.blit(wall_column,
                                        (dr_x + i * self.s.SCALE_thermal,
                                         6 * self.thermal_horizontal + dr_y + self.s.thermal_height // 2 - proj_height // 2))
                    self.s.display.blit(wall_column,
                                        (dr_x + i * self.s.SCALE_thermal,
                                         6 * self.thermal_horizontal + dr_y + self.s.thermal_height // 2 - proj_height // 2 - proj_height))
                    pos1 = (dr_x + i * self.s.SCALE_thermal,
                                         6 * self.thermal_horizontal + dr_y + self.s.thermal_height // 2 - proj_height // 2)
                    pos2 = (dr_x + i * self.s.SCALE_thermal,
                                         6 * self.thermal_horizontal + dr_y + self.s.thermal_height // 2 - proj_height // 2 - proj_height)
                    self.walls.append((depth, wall_column, pos1))
                    self.walls.append((depth, wall_column, pos2))
                else:
                    self.s.display.blit(wall_column,
                                        (dr_x + i * self.s.SCALE_thermal,
                                             6 * self.thermal_horizontal + dr_y + self.s.thermal_height // 2 - proj_height // 2))
                    pos1 = (dr_x + i * self.s.SCALE_thermal,
                                             6 * self.thermal_horizontal + dr_y + self.s.thermal_height // 2 - proj_height // 2)
                    self.walls.append((depth, wall_column, pos1))
                if int(cur_angle) == int(self.angle_of_view):
                    self.depth = str(depth)
                cur_angle += self.s.DELTA_ANGLE_thermal_zoom_extra
            # self.s.display.blit(self.s.thermal_sight_zoom, (dr_x, dr_y))

        elif sight_type == '3d':
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
                        texture_h = None
                        break
                    y += dy * self.s.tile_h
                depth, offset, texture = (depth_v, yv, texture_v) if depth_v < depth_h else (depth_h, xh, texture_h)
                offset = int(offset) % self.s.tile_w
                depth *= math.cos((self.angle_of_view - cur_angle) * 3.14 / 180)
                proj_height = int(self.s.PROJ_COEFF_thermal_d / depth)
                if self.s.texture_scale + offset * self.s.texture_scale > self.s.texture_w:
                    wall_column = self.s.thermal_textures[texture][0].subsurface(offset * self.s.texture_scale, 0,
                                                                                 self.s.texture_w - offset * self.s.texture_scale,
                                                                                 self.s.texture_h)
                else:
                    wall_column = self.s.thermal_textures[texture][0].subsurface(offset * self.s.texture_scale, 0,
                                                                                 self.s.texture_scale, self.s.texture_h)
                wall_column = pygame.transform.scale(wall_column, (self.s.SCALE_thermal_d, proj_height))
                if int(texture) % 2 == 0:
                    # self.s.display.blit(wall_column,
                    #                     (dr_x + i * self.s.SCALE_thermal_d,
                    #                      self.thermal_horizontal_d + dr_y + self.s.thermal_height_d // 2 - proj_height // 2))
                    # self.s.display.blit(wall_column,
                    #                     (dr_x + i * self.s.SCALE_thermal_d,
                    #                      self.thermal_horizontal_d + dr_y + self.s.thermal_height_d // 2 - proj_height // 2 - proj_height))
                    pos1 = (dr_x + i * self.s.SCALE_thermal_d,
                                         self.thermal_horizontal_d + dr_y + self.s.thermal_height_d // 2 - proj_height // 2)
                    pos2 = (dr_x + i * self.s.SCALE_thermal_d,
                                         self.thermal_horizontal_d + dr_y + self.s.thermal_height_d // 2 - proj_height // 2 - proj_height)
                    self.walls.append((depth, wall_column, pos1))
                    self.walls.append((depth, wall_column, pos2))
                else:
                    # self.s.display.blit(wall_column,
                    #                     (dr_x + i * self.s.SCALE_thermal_d,
                    #                      self.thermal_horizontal_d + dr_y + self.s.thermal_height_d // 2 - proj_height // 2))
                    pos1 = (dr_x + i * self.s.SCALE_thermal_d,
                                         self.thermal_horizontal_d + dr_y + self.s.thermal_height_d // 2 - proj_height // 2)
                    self.walls.append((depth, wall_column, pos1))
                if int(cur_angle) == int(self.angle_of_view):
                    self.depth = str(depth)
                cur_angle += self.s.DELTA_ANGLE_thermal
            # self.s.display.blit(self.s.thermal_sight_d, (self.s.thermal_x_d * 1.01, self.s.thermal_y_d_2))

        elif sight_type == '4.5d':
            x0, y0 = self.x, self.y
            xm, ym = self.mapping(x0, y0)
            cur_angle = self.angle_of_view - self.s.HALF_FOV_thermal_zoom_extra + 0.00001
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
                        texture_h = None
                        break
                    y += dy * self.s.tile_h
                depth, offset, texture = (depth_v, yv, texture_v) if depth_v < depth_h else (depth_h, xh, texture_h)
                offset = int(offset) % self.s.tile_w
                depth *= math.cos((self.angle_of_view - cur_angle) * 3.14 / 180)
                proj_height = int(self.s.PROJ_COEFF_thermal_zoom_extra_d / depth)
                if self.s.texture_scale + offset * self.s.texture_scale > self.s.texture_w:
                    wall_column = self.s.thermal_textures[texture][0].subsurface(offset * self.s.texture_scale, 0,
                                                                                 self.s.texture_w - offset * self.s.texture_scale,
                                                                                 self.s.texture_h)
                else:
                    wall_column = self.s.thermal_textures[texture][0].subsurface(offset * self.s.texture_scale, 0,
                                                                                 self.s.texture_scale, self.s.texture_h)
                wall_column = pygame.transform.scale(wall_column, (self.s.SCALE_thermal_d, proj_height))
                if int(texture) % 2 == 0:
                    # self.s.display.blit(wall_column,
                    #                     (dr_x + i * self.s.SCALE_thermal_d,
                    #                      6 * self.thermal_horizontal_d + dr_y + self.s.thermal_height_d // 2 - proj_height // 2))
                    # self.s.display.blit(wall_column,
                    #                     (dr_x + i * self.s.SCALE_thermal_d,
                    #                      6 * self.thermal_horizontal_d + dr_y + self.s.thermal_height_d // 2 - proj_height // 2 - proj_height))
                    pos1 = (dr_x + i * self.s.SCALE_thermal_d,
                                         6 * self.thermal_horizontal_d + dr_y + self.s.thermal_height_d // 2 - proj_height // 2)
                    pos2 = (dr_x + i * self.s.SCALE_thermal_d,
                                         6 * self.thermal_horizontal_d + dr_y + self.s.thermal_height_d // 2 - proj_height // 2 - proj_height)
                    self.walls.append((depth, wall_column, pos1))
                    self.walls.append((depth, wall_column, pos2))
                else:
                    # self.s.display.blit(wall_column,
                    #                     (dr_x + i * self.s.SCALE_thermal_d,
                    #                      6 * self.thermal_horizontal_d + dr_y + self.s.thermal_height_d // 2 - proj_height // 2))
                    pos1 = (dr_x + i * self.s.SCALE_thermal_d,
                                         6 * self.thermal_horizontal_d + dr_y + self.s.thermal_height_d // 2 - proj_height // 2)
                    self.walls.append((depth, wall_column, pos1))
                if int(cur_angle) == int(self.angle_of_view):
                    self.depth = str(depth)
                cur_angle += self.s.DELTA_ANGLE_thermal_zoom_extra
            # self.s.display.blit(self.s.thermal_sight_zoom_d, (self.s.thermal_x_d, self.s.thermal_y_d_2))

        elif sight_type == '4d':
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
                        texture_h = None
                        break
                    y += dy * self.s.tile_h
                depth, offset, texture = (depth_v, yv, texture_v) if depth_v < depth_h else (depth_h, xh, texture_h)
                offset = int(offset) % self.s.tile_w
                depth *= math.cos((self.angle_of_view - cur_angle) * 3.14 / 180)
                proj_height = int(self.s.PROJ_COEFF_thermal_zoom_d / depth)
                if self.s.texture_scale + offset * self.s.texture_scale > self.s.texture_w:
                    wall_column = self.s.thermal_textures[texture][0].subsurface(offset * self.s.texture_scale, 0,
                                                                                 self.s.texture_w - offset * self.s.texture_scale,
                                                                                 self.s.texture_h)
                else:
                    wall_column = self.s.thermal_textures[texture][0].subsurface(offset * self.s.texture_scale, 0,
                                                                                 self.s.texture_scale, self.s.texture_h)
                wall_column = pygame.transform.scale(wall_column, (self.s.SCALE_thermal, proj_height))
                if int(texture) % 2 == 0:
                    # self.s.display.blit(wall_column,
                    #                     (dr_x + i * self.s.SCALE_thermal_d,
                    #                      3 * self.thermal_horizontal_d + dr_y + self.s.thermal_height_d // 2 - proj_height // 2))
                    # self.s.display.blit(wall_column,
                    #                     (dr_x + i * self.s.SCALE_thermal_d,
                    #                      3 * self.thermal_horizontal_d + dr_y + self.s.thermal_height_d // 2 - proj_height // 2 - proj_height))
                    pos1 = (dr_x + i * self.s.SCALE_thermal_d,
                                         3 * self.thermal_horizontal_d + dr_y + self.s.thermal_height_d // 2 - proj_height // 2)
                    pos2 = (dr_x + i * self.s.SCALE_thermal_d,
                                         3 * self.thermal_horizontal_d + dr_y + self.s.thermal_height_d // 2 - proj_height // 2 - proj_height)
                    self.walls.append((depth, wall_column, pos1))
                    self.walls.append((depth, wall_column, pos2))
                else:
                    self.s.display.blit(wall_column,
                                        (dr_x + i * self.s.SCALE_thermal_d,
                                         3 * self.thermal_horizontal_d + dr_y + self.s.thermal_height_d // 2 - proj_height // 2))
                    pos1 = (dr_x + i * self.s.SCALE_thermal_d,
                                         3 * self.thermal_horizontal_d + dr_y + self.s.thermal_height_d // 2 - proj_height // 2)
                    self.walls.append((depth, wall_column, pos1))
                if int(cur_angle) == int(self.angle_of_view):
                    self.depth = str(depth)
                cur_angle += self.s.DELTA_ANGLE_thermal_zoom
            # self.s.display.blit(self.s.thermal_sight_zoom_d, (self.s.thermal_x_d, self.s.thermal_y_d_2))

    def optic_sight(self):
        show = True
        pygame.display.set_icon(self.s.icon)
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
        black2 = pygame.Rect(0, 0, (self.s.WIDTH - self.s.HEIGHT) // 2,
                            self.s.HEIGHT)
        floor = pygame.Rect(self.s.WIDTH // 2 - self.s.HEIGHT // 2, 0, self.s.HEIGHT,
                            self.s.HEIGHT)
        ammo_text = Text(self.s.WIDTH * 0.48, self.s.HEIGHT * 0.98, (255, 0, 0),
                         self.ammo_list_text[self.current_ammo], int(self.s.WIDTH * 0.033),
                         font_name='resources/fonts/lcd_font.otf'
                         )
        self.optic = True
        if not self.zoom:
            self.sky = pygame.Rect(self.s.WIDTH // 2 - self.s.HEIGHT // 2, 0, self.s.HEIGHT,
                                   self.horizontal + self.s.HEIGHT // 2)
            self.sky_thermal = pygame.Rect(self.s.thermal_x + (self.s.WIDTH - self.s.thermal_base_width) // 2,
                                           self.s.thermal_y, self.s.thermal_width,
                                           self.thermal_horizontal + self.s.thermal_height // 2)
            self.sky_thermal_d = pygame.Rect(self.s.thermal_x_d,
                                             self.s.thermal_y_d_2, self.s.thermal_width,
                                             self.thermal_horizontal_d + self.s.thermal_height_d * 5 // 2)
        else:
            self.sky = pygame.Rect(self.s.WIDTH // 2 - self.s.HEIGHT // 2, 0, self.s.HEIGHT,
                                   3 * self.horizontal + self.s.HEIGHT // 2)
            self.sky_thermal = pygame.Rect(self.s.thermal_x + (self.s.WIDTH - self.s.thermal_base_width) // 2,
                                           self.s.thermal_y, self.s.thermal_width,
                                           3 * self.thermal_horizontal + self.s.thermal_height // 2)
            self.sky_thermal_d = pygame.Rect(self.s.thermal_x_d,
                                             self.s.thermal_y_d_2, self.s.thermal_width,
                                             3 * self.thermal_horizontal_d + self.s.thermal_height_d * 5 // 2)
        while show:

            self.movement_check()
            self.check_is_done()
            self.check_death()
            self.damage.check_mines()
            self.damage.check_drones()
            if self.menu:
                show = False
            self.s.display.fill((0, 0, 0))
            self.timer()
            pygame.draw.rect(self.s.display, (53, 104, 45), floor)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        print('escape')
                        show = False
                    if event.key == pygame.K_e and self.rangefinder_suo:
                        depth_text.set_another_text(self.rangefinder())
                    if event.key == pygame.K_z:
                        self.zoom = True if self.zoom is False else False
                        if self.zoom:
                            self.sky = pygame.Rect(self.s.WIDTH // 2 - self.s.HEIGHT // 2, 0, self.s.HEIGHT,
                                                   3 * self.horizontal + self.s.HEIGHT // 2)
                            self.sky_thermal = pygame.Rect(
                                self.s.thermal_x + (self.s.WIDTH - self.s.thermal_base_width) // 2,
                                self.s.thermal_y, self.s.thermal_width,
                                3 * self.thermal_horizontal + self.s.thermal_height // 2)
                            self.sky_thermal_d = pygame.Rect(self.s.thermal_x_d,
                                                             self.s.thermal_y_d_2, self.s.thermal_width,
                                                             3 * self.thermal_horizontal_d + self.s.thermal_height_d * 5 // 2)
                        else:
                            self.sky = pygame.Rect(self.s.WIDTH // 2 - self.s.HEIGHT // 2, 0, self.s.HEIGHT,
                                                   self.horizontal + self.s.HEIGHT // 2)
                            self.sky_thermal = pygame.Rect(
                                self.s.thermal_x + (self.s.WIDTH - self.s.thermal_base_width) // 2,
                                self.s.thermal_y, self.s.thermal_width,
                                self.thermal_horizontal + self.s.thermal_height // 2)
                            self.sky_thermal_d = pygame.Rect(self.s.thermal_x_d,
                                                             self.s.thermal_y_d_2, self.s.thermal_width,
                                                             self.thermal_horizontal_d + self.s.thermal_height_d * 5 // 2)
                    self.ammo(event, [ammo_text])
                    if event.key == pygame.K_r and self.ready is False and self.is_shot is False and self.reload is False and \
                            self.ammo_list[self.current_ammo] > 0:
                        self.s.reload_sound.set_volume(self.s.volume_general / 100 * self.s.volume_sound / 100)
                        self.s.reload_sound.play()
                        self.reload = True
                        self.block = True
                        self.current_ammo_in_gun = int(str(self.current_ammo)[:])
                        print(self.ammo_list)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_LEFT:
                        print(1)
                        if self.ready:
                            self.ammo_list[self.current_ammo] -= 1
                            self.ready = False
                            self.is_shot = True
                            self.block = True
                            self.s.shoot_sound.set_volume(self.s.volume_general / 100 * self.s.volume_sound / 100)
                            self.s.shoot_sound.play()

            self.movement()
            self.guidance()
            pygame.draw.rect(self.s.display, (135, 206, 235), self.sky)
            if not self.zoom:
                self.ray_casting(self.s.WIDTH // 2 - self.s.HEIGHT // 2, 0, sight_type='1')
                temp = self.walls + [obj.object_locate(self) for obj in self.s.sprites.list_of_objects if not obj.death]
                self.world(temp, self.s.optic_sight,
                           (self.s.WIDTH // 2 - self.s.HEIGHT // 2, 0))
            else:
                self.ray_casting(self.s.WIDTH // 2 - self.s.HEIGHT // 2, 0, sight_type='2')
                temp = self.walls + [obj.object_locate(self) for obj in self.s.sprites.list_of_objects if not obj.death]
                self.world(temp, self.s.optic_sight_zoom,
                           (self.s.WIDTH // 2 - self.s.HEIGHT // 2, 0))
            pygame.draw.rect(self.s.display, (0, 0, 0), black)
            pygame.draw.rect(self.s.display, (0, 0, 0), black2)
            self.draw_minimap(self.x_minimap, self.y_minimap)
            fps_count_text_bl.set_another_text(str(int(self.s.clock.get_fps())) + ' FPS')
            fps_count_text.set_another_text(str(int(self.s.clock.get_fps())) + ' FPS')
            fps_count_text_bl.draw(self.s.display)
            fps_count_text.draw(self.s.display)

            depth_text.draw(self.s.display)
            ammo_text.draw(self.s.display)

            pygame.display.flip()
            self.s.clock.tick(self.s.FPS)
        self.optic = False

    def check_is_done(self):
        if self.count_of_destroyed_targets >= self.count_of_targets:
            self.done = 'выполнена'
    def shot(self):
        pass

    def thermal_sight(self):
        show = True
        pygame.display.set_icon(self.s.icon)
        fps_count_text_bl = Text(self.s.WIDTH * 0.961, self.s.HEIGHT * 0.972, (0, 0, 0),
                                 str(int(self.s.clock.get_fps())) + ' FPS', int(self.s.WIDTH * 0.0104),
                                 is_topleft=True)
        fps_count_text = Text(self.s.WIDTH * 0.96, self.s.HEIGHT * 0.97, (200, 200, 200),
                              str(int(self.s.clock.get_fps())) + ' FPS', int(self.s.WIDTH * 0.0104),
                              is_topleft=True)

        depth_text1 = Text(self.s.WIDTH * 0.528, self.s.HEIGHT * 0.83, (183, 183, 183),
                           self.depth_m[0], int(self.s.WIDTH * 0.030),
                           font_name='resources/fonts/depth_thermal_font.ttf'
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
        ammo_text1 = Text(self.s.WIDTH * 0.377, self.s.HEIGHT * 0.8275, (183, 183, 183),
                          self.ammo_list_text[self.current_ammo][0], int(self.s.WIDTH * 0.030),
                          font_name='resources/fonts/depth_thermal_font.ttf'
                          )
        ammo_text2 = Text(self.s.WIDTH * 0.409, self.s.HEIGHT * 0.8275, (183, 183, 183),
                          self.ammo_list_text[self.current_ammo][1], int(self.s.WIDTH * 0.03),
                          font_name='resources/fonts/depth_thermal_font.ttf'
                          )
        ssu_text = Text(self.s.WIDTH * 0.324, self.s.HEIGHT * 0.823, (183, 183, 183),
                        'ССУ        ВКЛ', int(self.s.WIDTH * 0.028),
                        font_name='resources/fonts/depth_thermal_font.ttf'
                        )
        ready_text1 = Text(self.s.WIDTH * 0.25, self.s.HEIGHT * 0.828, (183, 183, 183),
                           'Г', int(self.s.WIDTH * 0.03),
                           font_name='resources/fonts/depth_thermal_font.ttf'
                           )
        ready_text2 = Text(self.s.WIDTH * 0.2846, self.s.HEIGHT * 0.828, (183, 183, 183),
                           'О', int(self.s.WIDTH * 0.03),
                           font_name='resources/fonts/depth_thermal_font.ttf'
                           )
        ready_text3 = Text(self.s.WIDTH * 0.3176, self.s.HEIGHT * 0.828, (183, 183, 183),
                           'Т', int(self.s.WIDTH * 0.03),
                           font_name='resources/fonts/depth_thermal_font.ttf'
                           )
        floor = pygame.Rect(self.s.thermal_x + (self.s.WIDTH - self.s.thermal_base_width) // 2, 0, self.s.thermal_width,
                            self.s.HEIGHT)
        black = pygame.Rect(self.s.thermal_x + (self.s.WIDTH - self.s.thermal_base_width) // 2, 0, self.s.thermal_width,
                            self.s.HEIGHT)
        z = pygame.Rect(self.s.thermal_x + self.s.thermal_base_width * 1.1, 0,
                        self.s.WIDTH - self.s.thermal_x - self.s.thermal_base_width,
                        self.s.HEIGHT)
        v = pygame.Rect(0, 0,
                        (self.s.WIDTH - self.s.thermal_base_width) // 2,
                        self.s.HEIGHT)
        weapon_text1 = Text(self.s.WIDTH * 0.682, self.s.HEIGHT * 0.828, (183, 183, 183),
                           'О', int(self.s.WIDTH * 0.03),
                           font_name='resources/fonts/depth_thermal_font.ttf'
                           )
        weapon_text2 = Text(self.s.WIDTH * 0.714, self.s.HEIGHT * 0.828, (183, 183, 183),
                            'С', int(self.s.WIDTH * 0.03),
                            font_name='resources/fonts/depth_thermal_font.ttf'
                            )
        weapon_text3 = Text(self.s.WIDTH * 0.7485, self.s.HEIGHT * 0.828, (183, 183, 183),
                            'Н', int(self.s.WIDTH * 0.03),
                            font_name='resources/fonts/depth_thermal_font.ttf'
                            )
        lock_rect = pygame.Rect(0, 0, self.s.WIDTH * 0.1, self.s.HEIGHT * 0.15)
        lock_rect.center = (self.s.WIDTH // 2, self.s.HEIGHT * 0.437)
        if not self.zoom:
            self.sky = pygame.Rect(self.s.WIDTH // 2 - self.s.HEIGHT // 2, 0, self.s.HEIGHT,
                                   self.horizontal + self.s.HEIGHT // 2)
            self.sky_thermal = pygame.Rect(self.s.thermal_x + (self.s.WIDTH - self.s.thermal_base_width) // 2,
                                           self.s.thermal_y, self.s.thermal_width,
                                           self.thermal_horizontal + self.s.thermal_height // 2)
            self.sky_thermal_d = pygame.Rect(self.s.thermal_x_d,
                                             self.s.thermal_y_d_2, self.s.thermal_width,
                                             self.thermal_horizontal_d + self.s.thermal_height_d * 5 // 2)

        else:
            self.sky = pygame.Rect(self.s.WIDTH // 2 - self.s.HEIGHT // 2, 0, self.s.HEIGHT,
                                   3 * self.horizontal + self.s.HEIGHT // 2)
            self.sky_thermal = pygame.Rect(self.s.thermal_x + (self.s.WIDTH - self.s.thermal_base_width) // 2,
                                           self.s.thermal_y, self.s.thermal_width,
                                           3 * self.thermal_horizontal + self.s.thermal_height // 2)
            self.sky_thermal_d = pygame.Rect(self.s.thermal_x_d,
                                             self.s.thermal_y_d_2, self.s.thermal_width,
                                             3 * self.thermal_horizontal_d + self.s.thermal_height_d * 5 // 2)
        self.thermal = True
        if self.menu:
            show = False
        while show:

            self.movement_check()
            self.check_is_done()
            self.check_death()
            self.damage.check_mines()
            self.damage.check_drones()
            if self.menu:
                show = False
            self.s.display.fill((150, 150, 150))
            self.timer()

            if self.thermal_on:
                pygame.draw.rect(self.s.display, self.floor_thermal_color, floor)
                pygame.draw.rect(self.s.display, self.sky_thermal_color, self.sky_thermal)
            else:
                pygame.draw.rect(self.s.display, (0, 0, 0), black)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        show = False
                    self.ammo(event, [ammo_text1, ammo_text2])
                    if event.key == pygame.K_e and self.rangefinder_suo:
                        d = self.rangefinder()
                        depth_text1.set_another_text(d[0])
                        depth_text2.set_another_text(d[1])
                        depth_text3.set_another_text(d[2])
                        depth_text4.set_another_text(d[3])
                    if event.key == pygame.K_z:

                        self.zoom = True if self.zoom is False else False
                        self.extra_zoom = False
                        if self.zoom:
                            self.sky = pygame.Rect(self.s.WIDTH // 2 - self.s.HEIGHT // 2, 0, self.s.HEIGHT,
                                                   3 * self.horizontal + self.s.HEIGHT // 2)
                            self.sky_thermal = pygame.Rect(
                                self.s.thermal_x + (self.s.WIDTH - self.s.thermal_base_width) // 2, self.s.thermal_y,
                                self.s.thermal_width,
                                3 * self.thermal_horizontal + self.s.thermal_height // 2)
                            self.sky_thermal_d = pygame.Rect(self.s.thermal_x_d,
                                                             self.s.thermal_y_d_2, self.s.thermal_width,
                                                             3 * self.thermal_horizontal_d + self.s.thermal_height_d * 5 // 2)
                        else:
                            self.sky = pygame.Rect(self.s.WIDTH // 2 - self.s.HEIGHT // 2, 0, self.s.HEIGHT,
                                                   self.horizontal + self.s.HEIGHT // 2)
                            self.sky_thermal = pygame.Rect(
                                self.s.thermal_x + (self.s.WIDTH - self.s.thermal_base_width) // 2, self.s.thermal_y,
                                self.s.thermal_width,
                                self.thermal_horizontal + self.s.thermal_height // 2)
                            self.sky_thermal_d = pygame.Rect(self.s.thermal_x_d,
                                                             self.s.thermal_y_d_2, self.s.thermal_width,
                                                             self.thermal_horizontal_d + self.s.thermal_height_d * 5 // 2)
                    if event.key == pygame.K_LSHIFT:
                        self.extra_zoom = True if self.extra_zoom is False else False
                        self.zoom = False
                        if self.extra_zoom:
                            self.sky = pygame.Rect(self.s.WIDTH // 2 - self.s.HEIGHT // 2, 0, self.s.HEIGHT,
                                                   6 * self.horizontal + self.s.HEIGHT // 2)
                            self.sky_thermal = pygame.Rect(
                                self.s.thermal_x + (self.s.WIDTH - self.s.thermal_base_width) // 2, self.s.thermal_y,
                                self.s.thermal_width,
                                6 * self.thermal_horizontal + self.s.thermal_height // 2)
                            self.sky_thermal_d = pygame.Rect(self.s.thermal_x_d,
                                                             self.s.thermal_y_d_2, self.s.thermal_width,
                                                             6 * self.thermal_horizontal_d + self.s.thermal_height_d * 5 // 2)
                        else:
                            self.sky = pygame.Rect(self.s.WIDTH // 2 - self.s.HEIGHT // 2, 0, self.s.HEIGHT,
                                                   self.horizontal + self.s.HEIGHT // 2)
                            self.sky_thermal = pygame.Rect(
                                self.s.thermal_x + (self.s.WIDTH - self.s.thermal_base_width) // 2, self.s.thermal_y,
                                self.s.thermal_width,
                                self.thermal_horizontal + self.s.thermal_height // 2)
                            self.sky_thermal_d = pygame.Rect(self.s.thermal_x_d,
                                                             self.s.thermal_y_d_2, self.s.thermal_width,
                                                             self.thermal_horizontal_d + self.s.thermal_height_d * 5 // 2)
                    if event.key == pygame.K_q and self.lock_on:
                        if self.is_sprite_depth:
                            self.true_depth = min(float(self.depth), float(self.depth_sprite))
                        else:
                            self.true_depth = float(self.depth)
                        self.lock_x = self.x + self.true_depth * math.cos(self.angle_of_view * 3.14 / 180)
                        self.lock_y = self.y + self.true_depth * math.sin(self.angle_of_view * 3.14 / 180)
                        self.lock = True if self.lock is False else False
                    if event.key == pygame.K_r and self.ready is False and self.is_shot is False and self.reload is False and self.ammo_list[self.current_ammo] > 0:
                        self.reload = True
                        self.block = True
                        self.current_ammo_in_gun = int(str(self.current_ammo)[:])
                        print(self.ammo_list)
                        self.s.reload_sound.set_volume(self.s.volume_general / 100 * self.s.volume_sound / 100)
                        self.s.reload_sound.play()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_LEFT:
                        print(1)
                        if self.ready:
                            self.ammo_list[self.current_ammo_in_gun] -= 1
                            self.current_shooted_ammo = int(str(self.current_ammo_in_gun)[:])
                            self.current_ammo_in_gun = None
                            self.ready = False
                            self.is_shot = True
                            self.block = True
                            self.s.shoot_sound.set_volume(self.s.volume_general / 100 * self.s.volume_sound / 100)
                            self.s.shoot_sound.play()


            self.movement()
            self.guidance()
            self.is_sprite_depth = False
            if self.thermal_on:
                if self.zoom:
                    self.ray_casting(self.s.thermal_x + (self.s.WIDTH - self.s.thermal_base_width) // 2,
                                     self.s.thermal_y, sight_type='4')
                    temp = self.walls + [obj.object_locate(self) for obj in self.s.sprites.list_of_objects_thermal if not obj.death]
                    self.world(temp, self.s.thermal_sight_zoom,
                               (self.s.thermal_x + (self.s.WIDTH - self.s.thermal_base_width) // 2,
                                self.s.thermal_y))
                elif self.extra_zoom:
                    self.ray_casting(self.s.thermal_x + (self.s.WIDTH - self.s.thermal_base_width) // 2,
                                     self.s.thermal_y, sight_type='4.5')
                    temp = self.walls + [obj.object_locate(self) for obj in self.s.sprites.list_of_objects_thermal if not obj.death]
                    self.world(temp, self.s.thermal_sight_zoom,
                               (self.s.thermal_x + (self.s.WIDTH - self.s.thermal_base_width) // 2,
                                self.s.thermal_y))
                else:
                    self.ray_casting(self.s.thermal_x + (self.s.WIDTH - self.s.thermal_base_width) // 2,
                                     self.s.thermal_y, sight_type='3')

                    temp = self.walls + [obj.object_locate(self) for obj in self.s.sprites.list_of_objects_thermal if not obj.death]
                    self.world(temp, self.s.thermal_sight, (self.s.thermal_x + (self.s.WIDTH - self.s.thermal_base_width) // 2,
                                     self.s.thermal_y))

                pygame.draw.rect(self.s.display, (150, 150, 150), z)
                pygame.draw.rect(self.s.display, (150, 150, 150), v)
            # if self.is_sprite_depth:
            #     self.true_depth = min(float(self.depth), float(self.depth_sprite))
            # else:
            #     self.true_depth = float(self.depth)
            self.s.display.blit(self.s.thermal_image, ((self.s.WIDTH - self.s.thermal_base_width) // 2, 0))

            self.draw_minimap(self.x_minimap, self.y_minimap)
            fps_count_text_bl.set_another_text(str(int(self.s.clock.get_fps())) + ' FPS')
            fps_count_text.set_another_text(str(int(self.s.clock.get_fps())) + ' FPS')
            fps_count_text_bl.draw(self.s.display)
            fps_count_text.draw(self.s.display)
            if self.thermal_on:
                if self.zoom or self.extra_zoom:
                    depth_text1.draw(self.s.display)
                    depth_text2.draw(self.s.display)
                    depth_text3.draw(self.s.display)
                    depth_text4.draw(self.s.display)
                    ammo_text1.draw(self.s.display)
                    ammo_text2.draw(self.s.display)
                    weapon_text1.draw(self.s.display)
                    weapon_text2.draw(self.s.display)
                    weapon_text3.draw(self.s.display)
                    if self.ready:
                        ready_text1.draw(self.s.display)
                        ready_text2.draw(self.s.display)
                        ready_text3.draw(self.s.display)
                    if self.lock:
                        pygame.draw.rect(self.s.display, (0, 0, 0), lock_rect, int(self.s.WIDTH * 0.004))
                else:
                    ssu_text.draw(self.s.display)
            pygame.display.flip()
            self.s.clock.tick(self.s.FPS)
        self.thermal = False

    def rangefinder(self):
        if self.is_sprite_depth:
            self.true_depth = min(float(self.depth), float(self.depth_sprite))
        else:
            self.true_depth = float(self.depth)
        depth = str(min(int(float(self.true_depth) * (7 / self.side)), 9999))
        depth = '0' * (4 - len(depth)) + depth
        self.depth_m = depth[:]
        return depth

    def lock_f(self, x, y):
        dx = self.x - x
        dy = self.y - y
        if dx != 0:
            return math.atan(dy / dx)
        else:
            return 3.14 / 2

    def check_wall(self, x, y):
        all_map = self.s.map.world_map | self.s.sprites.collision_set
        return (int(x), int(y)) in all_map

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

    def world(self, walls, mark, mark_pos):
        for i in sorted(walls, key=lambda x: x[0], reverse=True):
            if i[0]:
                obj = i[1]
                pos = i[2]
                self.s.display.blit(obj, pos)
        self.s.display.blit(mark, mark_pos)

    def movement_check(self):
        for i in self.s.sprites.list_of_objects:
            if i.type == 'bmp':
                i.bmp_movement(self)
        for i in self.s.sprites.list_of_objects_thermal:
            if i.type == 'bmp':
                i.bmp_movement(self)

    def check_death(self):
        if self.death:
            self.s.explode_sound.set_volume(self.s.volume_general / 100 * self.s.volume_sound / 100)
            self.s.explode_sound.play()
            death_text_bl = Text(self.s.WIDTH * 0.5028, self.s.HEIGHT * 0.1052, (0, 0, 0), 'Вас уничтожили!',
                         int(self.s.WIDTH * 0.052))
            death_text = Text(self.s.WIDTH * 0.5, self.s.HEIGHT * 0.1, (200, 200, 200), 'Вас уничтожили!',
                          int(self.s.WIDTH * 0.052))
            cause_text_bl = Text(self.s.WIDTH * 0.032, self.s.HEIGHT * 0.173, (0, 0, 0), f'Причина смерти: {self.cause}.', int(self.s.WIDTH * 0.025),
                      is_topleft=True)
            cause_text = Text(self.s.WIDTH * 0.03, self.s.HEIGHT * 0.17, (200, 200, 200), f'Причина смерти: {self.cause}.',
                   int(self.s.WIDTH * 0.025), is_topleft=True)
            done_text_bl = Text(self.s.WIDTH * 0.032, self.s.HEIGHT * 0.253, (0, 0, 0),
                                 f'Боевая задача {self.done}:', int(self.s.WIDTH * 0.025),
                                 is_topleft=True)
            done_text = Text(self.s.WIDTH * 0.03, self.s.HEIGHT * 0.25, (200, 200, 200),
                              f'Боевая задача {self.done}:',
                              int(self.s.WIDTH * 0.025), is_topleft=True)
            destroyed_targets_text_bl = Text(self.s.WIDTH * 0.072, self.s.HEIGHT * 0.333, (0, 0, 0),
                                f'Уничтожено целей: {self.count_of_destroyed_targets} из {self.count_of_targets}.', int(self.s.WIDTH * 0.025),
                                is_topleft=True)
            destroyed_targets_text = Text(self.s.WIDTH * 0.07, self.s.HEIGHT * 0.33, (200, 200, 200),
                             f'Уничтожено целей: {self.count_of_destroyed_targets} из {self.count_of_targets}.',
                             int(self.s.WIDTH * 0.025), is_topleft=True)
            fps_count_text_bl = Text(self.s.WIDTH * 0.961, self.s.HEIGHT * 0.972, (0, 0, 0),
                                     str(int(self.s.clock.get_fps())) + ' FPS', int(self.s.WIDTH * 0.0104),
                                     is_topleft=True)
            fps_count_text = Text(self.s.WIDTH * 0.96, self.s.HEIGHT * 0.97, (200, 200, 200),
                                  str(int(self.s.clock.get_fps())) + ' FPS', int(self.s.WIDTH * 0.0104),
                                  is_topleft=True)
            destroyed_text_bl = Text(self.s.WIDTH * 0.072, self.s.HEIGHT * 0.413, (0, 0, 0),
                                f'Техника потеряна.', int(self.s.WIDTH * 0.025),
                                is_topleft=True)
            destroyed_text = Text(self.s.WIDTH * 0.07, self.s.HEIGHT * 0.41, (200, 200, 200),
                                     f'Техника потеряна.', int(self.s.WIDTH * 0.025),
                                     is_topleft=True)
            pygame.display.set_icon(self.s.icon)
            exit_to_menu_button = Button(self.s.WIDTH * 0.58, self.s.HEIGHT * 0.83, self.s.WIDTH * 0.336, self.s.HEIGHT * 0.0925,
                              'Выйти в меню', self.s.size_text_b, 'resources/images/button_inact.png',
                              'resources/images/button_active.png',
                              'resources/sounds/button_menu_sound.mp3')

            quit_button = Button(self.s.WIDTH * 0.081, self.s.HEIGHT * 0.83, self.s.WIDTH * 0.336, self.s.HEIGHT * 0.0925,
                             'Выйти', self.s.size_text_b, 'resources/images/button_inact.png',
                             'resources/images/button_active.png',
                             'resources/sounds/button_menu_sound.mp3')

            background = pygame.Surface((self.s.WIDTH * 0.45, self.s.HEIGHT * 0.64))
            background.set_alpha(128)
            background.fill((50, 60, 50))
            # self.s.display.blit(background, (0, 0))
            # self.s.display.blit(background_text, (self.s.WIDTH * 0.68, self.s.HEIGHT * 0.28))
            show = True
            # pygame.mouse.set_visible(True)
            while show:
                # self.s.display.blit(background, (0, 0))
                exit_to_menu_button.check(pygame.mouse.get_pos())
                quit_button.check(pygame.mouse.get_pos())
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.USEREVENT:
                        if event.button == quit_button:
                            pygame.quit()
                            sys.exit()
                        elif event.button == exit_to_menu_button:
                            self.s.music_menu.play(-1)
                            self.s.music_menu.set_volume(self.s.volume_general / 100 * self.s.volume_music / 100)
                            self.s.background_sound.stop()
                            self.s.reload_sound.stop()
                            self.s.shoot_sound.stop()
                            self.menu = True
                            show = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.s.music_menu.play(-1)
                            self.s.music_menu.set_volume(self.s.volume_general / 100 * self.s.volume_music / 100)
                            self.s.background_sound.stop()
                            self.s.reload_sound.stop()
                            self.s.shoot_sound.stop()
                            self.menu = True
                            show = False

                    exit_to_menu_button.handle_event(event, self.s.volume_sound * (self.s.volume_general / 100))
                    quit_button.handle_event(event, self.s.volume_sound * (self.s.volume_general / 100))

                self.s.display.blit(self.s.destroyed_image, (0, 0))
                self.s.display.blit(background, (self.s.WIDTH * 0.026, self.s.HEIGHT * 0.16))
                exit_to_menu_button.draw(self.s.display)
                quit_button.draw(self.s.display)
                death_text_bl.draw(self.s.display)
                death_text.draw(self.s.display)
                cause_text_bl.draw(self.s.display)
                cause_text.draw(self.s.display)
                done_text_bl.draw(self.s.display)
                done_text.draw(self.s.display)
                destroyed_targets_text_bl.draw(self.s.display)
                destroyed_targets_text.draw(self.s.display)
                destroyed_text_bl.draw(self.s.display)
                destroyed_text.draw(self.s.display)

                fps_count_text_bl.set_another_text(str(int(self.s.clock.get_fps())) + ' FPS')
                fps_count_text.set_another_text(str(int(self.s.clock.get_fps())) + ' FPS')
                fps_count_text_bl.draw(self.s.display)
                fps_count_text.draw(self.s.display)
                if pygame.mouse.get_focused():
                    self.s.display.blit(self.s.cursor, pygame.mouse.get_pos())

                pygame.display.flip()
                self.s.clock.tick(self.s.FPS)
            # pygame.mouse.set_visible(False)
#
# s = TankSettings()
# ex = Tank(s, 120, 120, 0, 5, 0, 0)
# ex.start()
