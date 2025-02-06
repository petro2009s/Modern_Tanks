import pygame
import gif_pygame
import os
import screeninfo
import threading
from bin.bd import DBController
from bin.map import Map
from bin.sprites import Sprite
from bin.text import Text
import math


class Settings:
    def __init__(self):
        #
        self.bd = DBController('resources/ModernTanksDB')
        #
        self.monitors = screeninfo.get_monitors()
        self.monitor = int(self.bd.select('monitor_table', 'id')[0][0])
        self.monitor_on_text = self.monitor
        self.width_m = self.monitors[self.monitor].width
        self.height_m = self.monitors[self.monitor].height
        self.WIDTH = self.bd.select('size_table', 'width')[0][0]
        self.HEIGHT = self.bd.select('size_table', 'height')[0][0]
        if (self.width_m < self.WIDTH or self.height_m < self.HEIGHT) and self.bd.select('full_table', 'off')[0][0]:
            self.WIDTH = self.width_m
            self.HEIGHT = self.height_m
            self.bd.update_to_db("size_table", "(width, height)", f"({self.WIDTH}, {self.HEIGHT})")
        self.size_list = list(filter(lambda x: x[0] / x[1] == 16 / 9, pygame.display.list_modes(display=self.monitor)))
        #
        self.size_text_b = int(self.WIDTH * 0.01875)
        self.size_on_text = [self.WIDTH, self.HEIGHT]
        #
        self.button_color = (50, 60, 50)
        #
        pygame.init()
        pygame.event.set_grab(True)
        self.display = pygame.display.set_mode((self.WIDTH, self.HEIGHT), display=self.monitor)
        self.icon = pygame.image.load('resources/images/menu/icon_test2_p.png').convert()
        os.environ['SDL_VIDEO_CENTERED'] = '1'

        if self.bd.select('full_table', '[on]')[0][0]:
            pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.FULLSCREEN, display=self.monitor)
        else:
            if self.width_m == self.WIDTH and self.height_m == self.HEIGHT:
                pygame.display.set_mode((self.WIDTH, self.HEIGHT - 40), display=self.monitor)
            else:
                pygame.display.set_mode((self.WIDTH, self.HEIGHT), display=self.monitor)
        self.clock = pygame.time.Clock()
        #
        fps = self.bd.select('FPS_table', '*')[0]
        fps_dict = {0: 30, 1: 60, 2: 90}
        self.FPS = fps_dict[[i for i in range(3) if fps[i] == 1][0]]
        #
        self.count_point = 3
        self.load_timer = 1
        self.show = True
        self.thread = threading.Thread(target=self.load, args=())
        self.thread.start()
        #
        self.menu1 = pygame.image.load('resources/images/menu/menu_p1.png').convert()
        self.menu2 = pygame.image.load('resources/images/menu/menu_p2.png').convert()
        self.menu3 = pygame.image.load('resources/images/menu/menu_p3.png').convert()
        self.menu4 = pygame.image.load('resources/images/menu/menu_p4.png').convert()
        self.menu5 = pygame.image.load('resources/images/menu/menu_p5.png').convert()
        self.destroyed_image = pygame.image.load('resources/images/menu/destroyed.png').convert_alpha()
        self.destroyed_image = pygame.transform.scale(self.destroyed_image, (self.WIDTH, self.HEIGHT))
        self.gif = gif_pygame.load("resources/images/menu/menu_g.gif")
        gif_pygame.transform.scale(self.gif, (self.WIDTH, self.HEIGHT))
        self.menu_list = [self.menu1, self.menu2, self.menu3, self.menu4, self.menu5]
        for i in range(len(self.menu_list)):
            self.menu_list[i] = pygame.transform.scale(self.menu_list[i], (self.WIDTH, self.HEIGHT))
        #
        self.cursor_base = pygame.image.load('resources/images/menu/cursor.png').convert_alpha()
        self.cursor = pygame.transform.scale(self.cursor_base, (self.WIDTH * 0.03125, self.WIDTH * 0.03125))
        #
        self.music_menu = pygame.mixer.Sound("resources/sounds/music_menu.mp3")
        self.shoot_sound = pygame.mixer.Sound("resources/sounds/shoot1.mp3")
        self.reload_sound = pygame.mixer.Sound("resources/sounds/reload.mp3")
        self.background_sound = pygame.mixer.Sound("resources/sounds/background.mp3")
        self.explode_sound = pygame.mixer.Sound("resources/sounds/explode.mp3")
        self.fpv_sound = pygame.mixer.Sound("resources/sounds/drone.mp3")
        self.win_sound = pygame.mixer.Sound("resources/sounds/win.mp3")
        self.lose_sound = pygame.mixer.Sound("resources/sounds/lose2.mp3")
        #
        self.graph_dict = [self.bd.select('graph_table', 'low')[0][0], self.bd.select('graph_table', 'mid')[0][0],
                           self.bd.select('graph_table', 'high')[0][0]]
        self.minimap_dict = [self.bd.select('minimap_table', '[on]')[0][0],
                             self.bd.select('minimap_table', 'off')[0][0]]
        self.fps_dict = [self.bd.select('FPS_table', 'low')[0][0], self.bd.select('FPS_table', 'mid')[0][0],
                         self.bd.select('FPS_table', 'high')[0][0]]
        self.full_dict = [bool(self.display.get_flags() & pygame.FULLSCREEN),
                          not bool(self.display.get_flags() & pygame.FULLSCREEN)]

        self.volume_general = self.bd.select('volume_table', 'volume_general')[0][0]
        self.volume_music = self.bd.select('volume_table', 'volume_music')[0][0]
        self.volume_sound = self.bd.select('volume_table', 'volume_sound')[0][0]

        self.tank_dict = {0: True}
        self.lvl_dict = {0: True, 1: False, 2: False}
        #
        with open('resources/descriptions/ammunition.txt', encoding='utf-8') as f:
            self.ammo = list(map(lambda x: x[:-1], f.readlines()))
        with open('resources/descriptions/T-90M_descr.txt', encoding='utf-8') as f:
            self.T_90M_descr = list(map(lambda x: x[:-1], f.readlines()))
        with open('resources/descriptions/T-90M_TTH.txt', encoding='utf-8') as f:
            self.T_90M_TTH = list(map(lambda x: x[:-1], f.readlines()))
        with open('resources/descriptions/guide.txt', encoding='utf-8') as f:
            self.guide_descr = list(map(lambda x: x[:-1], f.readlines()))
        with open('resources/descriptions/mission_1_descr.txt', encoding='utf-8') as f:
            self.mission1_descr = list(map(lambda x: x[:-1], f.readlines()))
        with open('resources/descriptions/mission_2_descr.txt', encoding='utf-8') as f:
            self.mission2_descr = list(map(lambda x: x[:-1], f.readlines()))
        with open('resources/descriptions/help.txt', encoding='utf-8') as f:
            self.help_level_list = list(map(str.rstrip, f.readlines()))
            self.help_level_descr = [[]]
            for i in self.help_level_list:
                if i:
                    self.help_level_descr[-1].append(i)
                else:
                    self.help_level_descr.append([])
        #
        with open('resources/maps/test_map.txt', encoding='utf-8') as f:
            self.world_map = list(map(lambda x: x[:-1], f.readlines()))
        with open('resources/maps/guide_map.txt', encoding='utf-8') as f:
            self.guide_map = list(map(lambda x: x[:-1], f.readlines()))
        with open('resources/maps/mission1_map.txt', encoding='utf-8') as f:
            self.mission1_map = list(map(lambda x: x[:-1], f.readlines()))
        with open('resources/maps/mission2_map.txt', encoding='utf-8') as f:
            self.mission2_map = list(map(lambda x: x[:-1], f.readlines()))
        #
        self.tile_w = (self.WIDTH // len(self.world_map[0]))
        self.tile_h = (self.WIDTH // len(self.world_map[0]))
        self.map_width = self.tile_w * len(self.world_map[0])
        self.map_height = self.tile_h * len(self.world_map)
        self.map = Map(self.world_map, self.tile_w, self.tile_h, self.WIDTH * 0.002)
        self.minimap_k = 5
        #
        self.minimap_tank_base = pygame.image.load('resources/images/tank/tank_minimap_base.png').convert_alpha()
        self.minimap_tank_tower_base = pygame.image.load('resources/images/tank/tank_minimap_tower.png').convert_alpha()
        self.minimap_tank_base_scope = pygame.image.load('resources/images/tank/tank_minimap_base.png').convert_alpha()
        self.minimap_tank_tower_scope = pygame.image.load(
            'resources/images/tank/tank_minimap_tower.png').convert_alpha()

        thermal_texture(self.minimap_tank_base_scope, 50, 60)
        thermal_texture(self.minimap_tank_tower_scope, 50, 60)

        self.minimap_tank_b = pygame.transform.scale(self.minimap_tank_base,
                                                     (self.WIDTH * 0.0625 // self.minimap_k,
                                                      self.WIDTH * 0.0625 // self.minimap_k))
        self.minimap_tank_tower = pygame.transform.scale(self.minimap_tank_tower_base,
                                                         (self.WIDTH * 0.0625 // self.minimap_k,
                                                          self.WIDTH * 0.0625 // self.minimap_k))
        self.minimap_tank_b_scope = pygame.transform.scale(self.minimap_tank_base_scope,
                                                           (self.WIDTH * 0.0625 / 1.5,
                                                            self.WIDTH * 0.0625 / 1.5))
        self.minimap_tank_tower_scope = pygame.transform.scale(self.minimap_tank_tower_scope,
                                                               (self.WIDTH * 0.062 / 1.5,
                                                                self.WIDTH * 0.062 / 1.5))
        #
        self.side = min(int(self.WIDTH * 0.02), int(self.tile_w * 0.8))
        self.a_w = self.WIDTH * 0.05 * (self.FPS / 60) * (7 / self.side)
        self.a_s = -self.WIDTH * 0.1 * (self.FPS / 60) * (7 / self.side)
        self.a_stop = self.WIDTH * 0.1 * (self.FPS / 60) * (7 / self.side)
        self.max_speed_w = self.WIDTH * 0.2 * (self.FPS / 60) * (7 / self.side)
        self.max_speed_s = -self.WIDTH * 0.01 * (self.FPS / 60) * (7 / self.side)
        self.min_speed_ad = self.WIDTH * 0.01 * (self.FPS / 60) * 10 / 60 * (7 / self.side)
        #
        self.tower_v = 30
        self.vertical_v = 50
        #
        self.optic_scope_width = self.HEIGHT
        self.FOV_optic = 12
        self.HALF_FOV_optic = self.FOV_optic // 2
        self.NUM_RAYS = 125 + 75 * self.graph_dict.index(1)
        self.DELTA_ANGLE_optic = self.FOV_optic / self.NUM_RAYS
        self.DIST_optic = self.NUM_RAYS / (2 * math.tan(self.HALF_FOV_optic * 3.14 / 180))
        self.PROJ_COEFF_optic = 70 * self.HEIGHT

        if self.optic_scope_width % self.NUM_RAYS == 0:
            self.SCALE_optic = self.optic_scope_width // self.NUM_RAYS
        else:
            self.SCALE_optic = int(self.optic_scope_width / self.NUM_RAYS) + 1
        #
        self.FOV_optic_zoom = 4
        self.HALF_FOV_optic_zoom = self.FOV_optic_zoom // 2
        self.DELTA_ANGLE_optic_zoom = self.FOV_optic_zoom / self.NUM_RAYS
        self.DIST_optic_zoom = self.NUM_RAYS / (2 * math.tan(self.HALF_FOV_optic_zoom * 3.14 / 180))
        self.PROJ_COEFF_optic_zoom = 210 * self.HEIGHT

        if self.optic_scope_width % self.NUM_RAYS == 0:
            self.SCALE_optic_zoom = self.optic_scope_width // self.NUM_RAYS
        else:
            self.SCALE_optic_zoom = int(self.optic_scope_width / self.NUM_RAYS) + 1
        #
        self.optic_sight_base = pygame.image.load('resources/images/scopes/sosna-u_optic.png').convert_alpha()
        self.optic_sight = pygame.transform.scale(self.optic_sight_base,
                                                  (self.HEIGHT, self.HEIGHT))

        self.optic_sight_zoom_base = pygame.image.load('resources/images/scopes/sosna-u_optic_zoom.png').convert_alpha()
        self.optic_sight_zoom = pygame.transform.scale(self.optic_sight_zoom_base,
                                                       (self.HEIGHT, self.HEIGHT))
        #
        self.gunner_site_base = pygame.image.load('resources/images/tank/gunner_site.png').convert_alpha()
        self.gunner_site = pygame.transform.scale(self.gunner_site_base,
                                                  (self.WIDTH, self.HEIGHT))
        self.gunner_site_base2 = pygame.image.load('resources/images/tank/gunner_site2.png').convert_alpha()
        self.gunner_site2 = pygame.transform.scale(self.gunner_site_base2,
                                                   (self.WIDTH, self.HEIGHT))
        #
        self.max_t = 80
        #
        self.texture_w = self.WIDTH * 0.6 * 1.44
        self.texture_h = self.WIDTH * 0.6

        self.texture_scale = self.texture_w // self.tile_w if self.texture_w % self.tile_w == 0 else self.texture_w // self.tile_w + 1
        #
        self.texture_1_base = pygame.image.load('resources/images/textures/forest.png').convert_alpha()
        self.texture_2_base = pygame.image.load('resources/images/textures/building.png').convert_alpha()
        self.texture_5_base = pygame.image.load('resources/images/textures/building1.png').convert_alpha()
        self.texture_7_base = pygame.image.load('resources/images/textures/building2.png').convert_alpha()
        self.texture_9_base = pygame.image.load('resources/images/textures/building3.png').convert_alpha()

        self.textures = {'3': pygame.transform.scale(self.texture_1_base,
                                                     (self.texture_w, self.texture_h)),
                         '1': pygame.transform.scale(self.texture_2_base,
                                                     (self.texture_w, self.texture_h)),
                         '2': pygame.transform.scale(self.texture_2_base,
                                                     (self.texture_w, self.texture_h)),
                         '5': pygame.transform.scale(self.texture_5_base,
                                                     (self.texture_w, self.texture_h)),
                         '7': pygame.transform.scale(self.texture_7_base,
                                                     (self.texture_w, self.texture_h)),
                         '9': pygame.transform.scale(self.texture_9_base,
                                                     (self.texture_w, self.texture_h)),
                         }
        #
        self.thermal_textures = {'3': (pygame.transform.scale(self.texture_1_base,
                                                              (self.texture_w, self.texture_h)), 30),
                                 '1': (pygame.transform.scale(self.texture_2_base,
                                                              (self.texture_w, self.texture_h)), 20),
                                 '2': (pygame.transform.scale(self.texture_2_base,
                                                              (self.texture_w, self.texture_h)), 40),
                                 '5': (pygame.transform.scale(self.texture_5_base,
                                                              (self.texture_w, self.texture_h)), 40),
                                 '7': (pygame.transform.scale(self.texture_7_base,
                                                              (self.texture_w, self.texture_h)), 40),
                                 '9': (pygame.transform.scale(self.texture_9_base,
                                                              (self.texture_w, self.texture_h)), 50),

                                 }
        for i, j in self.thermal_textures.items():
            thermal_texture(j[0], j[1], self.max_t)
        #
        self.optic_sight_x = 0.5 * self.WIDTH
        self.optic_sight_y = 0.1 * self.WIDTH
        self.optic_sight_w_r = 0.2 * self.WIDTH
        self.optic_sight_h_r = 0.2 * self.WIDTH
        #
        self.thermal_sight_h_r = 0.13 * self.WIDTH
        self.thermal_sight_w_r = 0.2 * self.WIDTH
        self.thermal_sight_x = 0.22 * self.WIDTH
        self.thermal_sight_y = 0.25 * self.WIDTH
        #
        self.thermal_base = pygame.image.load('resources/images/tank/sosna-thermal_base.png').convert_alpha()
        self.thermal_image = pygame.transform.scale(self.thermal_base,
                                                    (self.HEIGHT * 1.225, self.HEIGHT))

        self.thermal_base_width = self.HEIGHT * 1.225
        self.thermal_width = self.HEIGHT * 1.225 / 13.4 * 11.15
        self.thermal_height = self.HEIGHT / 14.2 * 11
        self.thermal_x = self.HEIGHT / 13.4 * 1.4
        self.thermal_y = self.HEIGHT / 14.2 * 1.57
        #
        self.FOV_thermal = 9
        self.HALF_FOV_thermal = self.FOV_thermal / 2
        self.DELTA_ANGLE_thermal = self.FOV_thermal / self.NUM_RAYS
        self.DIST_thermal = self.NUM_RAYS / (2 * math.tan(self.HALF_FOV_thermal * 3.14 / 180))
        self.PROJ_COEFF_thermal = 95 * self.thermal_height

        if self.thermal_width % self.NUM_RAYS == 0:
            self.SCALE_thermal = self.thermal_width // self.NUM_RAYS
        else:
            self.SCALE_thermal = int(self.thermal_width // self.NUM_RAYS) + 1
        #
        self.FOV_thermal_zoom = 3
        self.HALF_FOV_thermal_zoom = self.FOV_thermal_zoom / 2
        self.DELTA_ANGLE_thermal_zoom = self.FOV_thermal_zoom / self.NUM_RAYS
        self.DIST_thermal_zoom = self.NUM_RAYS / (2 * math.tan(self.HALF_FOV_thermal_zoom * 3.14 / 180))
        self.PROJ_COEFF_thermal_zoom = 285 * self.thermal_height
        #
        self.thermal_sight_base = pygame.image.load('resources/images/scopes/sosna_u_thermal.png').convert_alpha()
        self.thermal_sight = pygame.transform.scale(self.thermal_sight_base,
                                                    (self.thermal_width, self.thermal_height))
        self.thermal_sight_zoom_base = pygame.image.load(
            'resources/images/scopes/sosna-u_thermal_zoom.png').convert_alpha()
        self.thermal_sight_zoom = pygame.transform.scale(self.thermal_sight_zoom_base,
                                                         (self.thermal_width, self.thermal_height))
        #
        self.FOV_thermal_zoom_extra = 1.5
        self.HALF_FOV_thermal_zoom_extra = self.FOV_thermal_zoom_extra / 2
        self.DELTA_ANGLE_thermal_zoom_extra = self.FOV_thermal_zoom_extra / self.NUM_RAYS
        self.DIST_thermal_zoom_extra = self.NUM_RAYS / (2 * math.tan(self.HALF_FOV_thermal_zoom_extra * 3.14 / 180))
        self.PROJ_COEFF_thermal_zoom_extra = 570 * self.thermal_height
        #
        self.suo_x = self.WIDTH * 0.83
        self.suo_y = self.WIDTH * 0.39
        self.suo_w_r = self.WIDTH * 0.14
        self.suo_h_r = self.WIDTH * 0.1
        #
        self.thermal_width_d = self.WIDTH * 5 / 37
        self.thermal_height_d = self.HEIGHT * 0.8 / 20.5

        self.PROJ_COEFF_thermal_d = 30 * self.thermal_height
        self.PROJ_COEFF_thermal_zoom_extra_d = 180 * self.thermal_height
        self.PROJ_COEFF_thermal_zoom_d = 90 * self.thermal_height

        if self.thermal_width_d % self.NUM_RAYS == 0:
            self.SCALE_thermal_d = self.thermal_width_d // self.NUM_RAYS
        else:
            self.SCALE_thermal_d = int(self.thermal_width_d // self.NUM_RAYS) + 1
        #
        self.thermal_x_d = self.WIDTH * 9.1 / 37
        self.thermal_y_d = self.HEIGHT * 11 / 20.5
        self.thermal_y_d_2 = self.HEIGHT * 9.4 / 20.5
        #
        self.thermal_sight_d = pygame.transform.scale(self.thermal_sight_base,
                                                      (self.thermal_width / 4, self.thermal_height / 4))
        self.thermal_sight_zoom_d = pygame.transform.scale(self.thermal_sight_zoom_base,
                                                           (self.thermal_width / 4, self.thermal_height / 4))
        #
        self.test_sprite = pygame.image.load('resources/sprites/bush.png').convert_alpha()
        self.test_sprite2 = pygame.image.load('resources/sprites/bush1.png').convert_alpha()
        self.test_sprite3 = pygame.image.load('resources/sprites/bush2.png').convert_alpha()
        self.test_sprite4 = pygame.image.load('resources/sprites/bush3.png').convert_alpha()

        self.bush_sprite2 = pygame.transform.scale(self.test_sprite, (self.WIDTH * 0.4, self.WIDTH * 0.4))
        self.bush_sprite_thermal2 = pygame.transform.scale(self.test_sprite2, (self.WIDTH * 0.4, self.WIDTH * 0.4))
        thermal_texture(self.bush_sprite_thermal2, 20, 50)

        self.bush_sprite3 = pygame.transform.scale(self.test_sprite, (self.WIDTH * 0.4, self.WIDTH * 0.4))
        self.bush_sprite_thermal3 = pygame.transform.scale(self.test_sprite3, (self.WIDTH * 0.4, self.WIDTH * 0.4))
        thermal_texture(self.bush_sprite_thermal3, 20, 50)

        self.bush_sprite4 = pygame.transform.scale(self.test_sprite, (self.WIDTH * 0.4, self.WIDTH * 0.4))
        self.bush_sprite_thermal4 = pygame.transform.scale(self.test_sprite4, (self.WIDTH * 0.4, self.WIDTH * 0.4))
        thermal_texture(self.bush_sprite_thermal4, 20, 50)

        self.bush_sprite = pygame.transform.scale(self.test_sprite, (self.WIDTH * 0.4, self.WIDTH * 0.4))
        self.bush_sprite_thermal = pygame.transform.scale(self.test_sprite, (self.WIDTH * 0.4, self.WIDTH * 0.4))
        thermal_texture(self.bush_sprite_thermal, 20, self.max_t)

        self.tree_sprite = pygame.image.load('resources/sprites/tree.png').convert_alpha()
        self.tree_sprite_thermal = pygame.transform.scale(self.tree_sprite, (self.WIDTH * 0.4, self.WIDTH * 0.4))
        thermal_texture(self.tree_sprite_thermal, 20, self.max_t)
        #
        self.center_ray = self.NUM_RAYS // 2 - 1
        self.FAKE_RAYS = int(self.NUM_RAYS * 2)
        #
        self.test_sprite_v = [pygame.image.load(f'resources/sprites/bmp_sprite/{i * 45}.png').convert_alpha() for i in
                              range(8)]
        self.test_sprite_v_thermal = [pygame.image.load(f'resources/sprites/bmp_sprite/{i * 45}.png').convert_alpha()
                                      for i in range(8)]
        for i in self.test_sprite_v_thermal:
            thermal_texture(i, 80, 80)

        self.tank_sprite = [
            pygame.image.load(f'resources/sprites/tank_sprite/tank{str((i * 45 + 90) % 360)}_p.png').convert_alpha() for
            i in
            range(8)]
        self.tank_sprite_thermal = [
            pygame.image.load(f'resources/sprites/tank_sprite/tank{str((i * 45 + 90) % 360)}_p.png').convert_alpha()
            for i in range(8)]
        for i in self.tank_sprite_thermal:
            thermal_texture(i, 80, 80)

        self.mrap_sprite = [
            pygame.image.load(f'resources/sprites/mrap_sprite/mrap_{str((i * 45 + 90) % 360)}_p.png').convert_alpha() for
            i in
            range(8)]
        self.mrap_sprite_thermal = [
            pygame.image.load(f'resources/sprites/mrap_sprite/mrap_{str((i * 45 + 90) % 360)}_p.png').convert_alpha()
            for i in range(8)]
        for i in self.mrap_sprite_thermal:
            thermal_texture(i, 80, 80)

        #
        self.mine_coords = {(55, 20), (56, 21), (55, 21), (57, 25), (50, 60)}
        self.fpv_coords = set([(i, j) for j in range(len(self.world_map) // 2) for i in range(len(self.world_map[0]))])
        self.rpg_coords = (0, 0)
        #
        self.fpv_time = 10

        self.rpg_time = 10
        #
        self.reload_time = 6
        #
        self.task_1 = ''
        self.task_2 = ''
        #
        self.count_of_targets = ''
        #
        self.start_point = (self.map_width // 9, self.map_height // 1.1)
        self.end_point = [(i, j) for j in range(int((self.map_height // 1.1) // self.tile_h),
                                                int((self.map_height // 1) // self.tile_h)) for i in
                          range(int((self.map_width // 12) // self.tile_w), int((self.map_width // 7) // self.tile_w))]
        #
        self.shot_anim = [pygame.image.load(f'resources/sprites/explode1_sprite/frame_{str(i + 1)}.png').convert_alpha()
                          for i in
                          range(3)]
        self.shot_anim_thermal = [
            pygame.image.load(f'resources/sprites/explode1_sprite/frame_{str(i + 1)}.png').convert_alpha() for i in
            range(3)]
        for i in self.shot_anim_thermal:
            thermal_texture(i, 200, self.max_t)
        #
        self.shot_anim_time = 0.3
        self.shot_frames = int(self.shot_anim_time * self.FPS)
        self.shot_frames_delta = max(self.shot_frames // 3, 1)
        self.shot_frames = int(self.shot_frames_delta * 3)
        #
        self.shot_he_anim = [
            pygame.image.load(f'resources/sprites/explode2_sprite/frame_{str(i + 1)}.png').convert_alpha()
            for i in
            range(5)]
        self.shot_he_anim_thermal = [
            pygame.image.load(f'resources/sprites/explode2_sprite/frame_{str(i + 1)}.png').convert_alpha() for i in
            range(5)]
        for i in self.shot_he_anim_thermal:
            thermal_texture(i, 200, self.max_t)
        #
        self.shot_he_anim_time = 0.4
        self.shot_he_frames = int(self.shot_he_anim_time * self.FPS)
        self.shot_he_frames_delta = max(self.shot_he_frames // 5, 1)
        self.shot_he_frames = int(self.shot_he_frames_delta * 5)
        #
        self.shot_smog_anim = [
            pygame.image.load(f'resources/sprites/smog_sprite/frame_{str(i + 1)}.png').convert_alpha()
            for i in
            range(10)]
        self.shot_smog_anim_thermal = [
            pygame.image.load(f'resources/sprites/smog_sprite/frame_{str(i + 1)}.png').convert_alpha() for i in
            range(10)]
        for i in self.shot_smog_anim_thermal:
            thermal_texture(i, 100, self.max_t)
        #
        self.shot_smog_anim_time = 0.3
        self.shot_smog_frames = int(self.shot_smog_anim_time * self.FPS)
        self.shot_smog_frames_delta = max(self.shot_smog_frames // 10, 1)
        self.shot_smog_frames = int(self.shot_smog_frames_delta * 10)
        #
        self.bmp_death_anim = [
            pygame.image.load(f'resources/sprites/big_explode_sprite/frame_{str(i + 1)}.png').convert_alpha()
            for i in
            range(14)]
        self.bmp_death_anim_thermal = [
            pygame.image.load(f'resources/sprites/big_explode_sprite/frame_{str(i + 1)}.png').convert_alpha() for i in
            range(14)]
        for i in self.bmp_death_anim_thermal:
            thermal_texture(i, 100, self.max_t)
        #
        self.bmp_death_anim_time = 0.8
        self.bmp_death_frames = int(self.bmp_death_anim_time * self.FPS)
        self.bmp_death_frames_delta = max(self.bmp_death_frames // 14, 1)
        self.bmp_death_frames = int(self.bmp_death_frames_delta * 14)
        #
        self.sprite_types = {'bush_thermal': self.bush_sprite_thermal,
                             'bush': self.bush_sprite,
                             'bmp': self.test_sprite_v,
                             'bmp_thermal': self.test_sprite_v_thermal,
                             'tree_thermal': self.tree_sprite_thermal,
                             'tree': self.tree_sprite,
                             'tank': self.tank_sprite,
                             'tank_thermal': self.tank_sprite_thermal,
                             'bush1': self.bush_sprite2,
                             'bush2': self.bush_sprite3,
                             'bush3': self.bush_sprite4,
                             'bush1_thermal': self.bush_sprite_thermal2,
                             'bush2_thermal': self.bush_sprite_thermal3,
                             'bush3_thermal': self.bush_sprite_thermal4
                             }
        #
        self.ammo_v = {0: 1500, 1: 670, 2: 800}
        #
        self.show = False
        self.thread.join()

    #
    def set_lvl(self):
        self.show = True
        self.thread = threading.Thread(target=self.load, args=())
        self.thread.start()
        if self.lvl_dict[0]:
            self.tile_w = (self.WIDTH // len(self.guide_map[0]))
            self.tile_h = (self.WIDTH // len(self.guide_map[0]))
            self.map_width = self.tile_w * len(self.guide_map[0])
            self.map_height = self.tile_h * len(self.guide_map)
            self.map = Map(self.guide_map, self.tile_w, self.tile_h, self.WIDTH * 0.002)
            self.texture_scale = self.texture_w // self.tile_w if self.texture_w % self.tile_w == 0 else self.texture_w // self.tile_w + 1

            self.start_point = (self.map_width // 9, self.map_height // 1.1)
            self.end_point = [(i, j) for j in range(56, 70) for i in
                              range(0, 20)]
            self.mine_coords1 = set([(i, j) for j in range(1, 15) for i in range(len(self.guide_map[0]) // 2)])
            self.mine_coords2 = set([(i, j) for j in range(32, 50) for i in range(len(self.guide_map[0]) // 4)])
            self.mine_coords3 = set([(i, j) for j in range(47, 100) for i in
                                     range(int(len(self.guide_map[0]) * 0.7), len(self.guide_map[0]))])
            self.fpv_coords = set([(i, j) for j in range(1, 51) for i in range(len(self.guide_map[0]))])
            self.fpv_coords2 = set(
                [(i, j) for j in range(51, 100) for i in range(len(self.guide_map[0]) // 2, len(self.guide_map[0]))])

            self.mine_coords = self.mine_coords1 | self.mine_coords2 | self.mine_coords3
            self.fpv_coords = self.fpv_coords | self.fpv_coords2
            self.task2_1 = 'пройти обучение.'
            self.task1_1 = 'уничтожить БМП и уехать'
            self.task1_2 = 'на начальную точку.'
            self.tank_sprite = [
                pygame.image.load(f'resources/sprites/tank_sprite/tank{str((i * 45 + 90) % 360)}_p.png').convert_alpha()
                for
                i in
                range(8)]
            self.tank_sprite_thermal = [
                pygame.image.load(f'resources/sprites/tank_sprite/tank{str((i * 45 + 90) % 360)}_p.png').convert_alpha()
                for i in range(8)]
            for i in self.tank_sprite_thermal:
                thermal_texture(i, 80, 80)
            self.sprite_types = {'bush_thermal': self.bush_sprite_thermal,
                                 'bush': self.bush_sprite,
                                 'bmp': self.test_sprite_v,
                                 'bmp_thermal': self.test_sprite_v_thermal,
                                 'tree_thermal': self.tree_sprite_thermal,
                                 'tree': self.tree_sprite,
                                 'tank': self.tank_sprite,
                                 'tank_thermal': self.tank_sprite_thermal,
                                 'bush1': self.bush_sprite2,
                                 'bush2': self.bush_sprite3,
                                 'bush3': self.bush_sprite4,
                                 'bush1_thermal': self.bush_sprite_thermal2,
                                 'bush2_thermal': self.bush_sprite_thermal3,
                                 'bush3_thermal': self.bush_sprite_thermal4
                                 }
            self.count_of_targets = '2'

            self.sprites = Sprite(self)

        elif self.lvl_dict[1]:
            self.tile_w = (self.WIDTH // len(self.mission1_map[0]))
            self.tile_h = (self.WIDTH // len(self.mission1_map[0]))
            self.map_width = self.tile_w * len(self.mission1_map[0])
            self.map_height = self.tile_h * len(self.mission1_map)
            self.map = Map(self.mission1_map, self.tile_w, self.tile_h, self.WIDTH * 0.002)
            self.texture_scale = self.texture_w // self.tile_w if self.texture_w % self.tile_w == 0 else self.texture_w // self.tile_w + 1

            self.start_point = (self.map_width // 9, self.map_height // 1.05)
            self.end_point = [(i, j) for j in range(122, 157) for i in
                              range(129, 154)]
            self.mine_coords1 = set([(i, j) for j in range(1, 15) for i in range(len(self.mission1_map[0]) // 2)])
            self.mine_coords2 = set([(i, j) for j in range(32, 50) for i in range(len(self.mission1_map[0]) // 4)])
            self.mine_coords3 = set([(i, j) for j in range(47, 100) for i in
                                     range(int(len(self.mission1_map[0]) * 0.7), len(self.mission1_map[0]))])
            self.fpv_coords = set([(i, j) for j in range(1, 105) for i in range(len(self.mission1_map[0]))])

            self.mine_coords = self.mine_coords1 | self.mine_coords2 | self.mine_coords3
            self.mine_coords = set()
            self.task1_1 = 'уничтожить колонну техники, пока она не покинула'
            self.task1_2 = 'карту, и уехать к низким зданиям на юго-востоке.'
            self.count_of_targets = '3'
            self.tank_sprite = [
                pygame.image.load(f'resources/sprites/tank_sprite/tank{str(i * 45)}_p.png').convert_alpha()
                for
                i in
                range(8)]
            self.tank_sprite_thermal = [
                pygame.image.load(f'resources/sprites/tank_sprite/tank{str(i * 45)}_p.png').convert_alpha()
                for i in range(8)]
            for i in self.tank_sprite_thermal:
                thermal_texture(i, 80, 80)
            self.sprite_types = {'bush_thermal': self.bush_sprite_thermal,
                                 'bush': self.bush_sprite,
                                 'bmp': self.test_sprite_v,
                                 'bmp_thermal': self.test_sprite_v_thermal,
                                 'tree_thermal': self.tree_sprite_thermal,
                                 'tree': self.tree_sprite,
                                 'tank': self.tank_sprite,
                                 'tank_thermal': self.tank_sprite_thermal,
                                 'bush1': self.bush_sprite2,
                                 'bush2': self.bush_sprite3,
                                 'bush3': self.bush_sprite4,
                                 'bush1_thermal': self.bush_sprite_thermal2,
                                 'bush2_thermal': self.bush_sprite_thermal3,
                                 'bush3_thermal': self.bush_sprite_thermal4
                                 }
            self.sprites = Sprite(self)

        elif self.lvl_dict[2]:
            self.tile_w = (self.WIDTH // len(self.mission2_map[0]))
            self.tile_h = (self.WIDTH // len(self.mission2_map[0]))
            self.map_width = self.tile_w * len(self.mission2_map[0])
            self.map_height = self.tile_h * len(self.mission2_map)
            self.map = Map(self.mission2_map, self.tile_w, self.tile_h, self.WIDTH * 0.002)
            self.texture_scale = self.texture_w // self.tile_w if self.texture_w % self.tile_w == 0 else self.texture_w // self.tile_w + 1

            self.start_point = (self.tile_w * 5, self.tile_h * 50)
            self.end_point = [(i, j) for j in range(0, 7) for i in
                              range(0, 54)]
            self.rpg_coords = [(i, j) for j in range(0, 52) for i in
                              range(10, 18)]
            self.mine_coords1 = set()
            self.mine_coords2 = set()
            self.mine_coords3 = set()
            self.fpv_coords = set()

            self.mine_coords = self.mine_coords1 | self.mine_coords2 | self.mine_coords3
            self.mine_coords = set()
            self.task1_1 = 'уничтожить всю технику и'
            self.task1_2 = 'уехать из города.'
            self.count_of_targets = '3'
            self.tank_sprite = [
                pygame.image.load(f'resources/sprites/tank_sprite/tank{str(i * 45)}_p.png').convert_alpha()
                for
                i in
                range(8)]
            self.tank_sprite_thermal = [
                pygame.image.load(f'resources/sprites/tank_sprite/tank{str(i * 45)}_p.png').convert_alpha()
                for i in range(8)]
            for i in self.tank_sprite_thermal:
                thermal_texture(i, 80, 80)
            self.sprite_types = {'bush_thermal': self.bush_sprite_thermal,
                                 'bush': self.bush_sprite,
                                 'bmp': self.test_sprite_v,
                                 'bmp_thermal': self.test_sprite_v_thermal,
                                 'tree_thermal': self.tree_sprite_thermal,
                                 'tree': self.tree_sprite,
                                 'tank': self.tank_sprite,
                                 'tank_thermal': self.tank_sprite_thermal,
                                 'bush1': self.bush_sprite2,
                                 'bush2': self.bush_sprite3,
                                 'bush3': self.bush_sprite4,
                                 'bush1_thermal': self.bush_sprite_thermal2,
                                 'bush2_thermal': self.bush_sprite_thermal3,
                                 'bush3_thermal': self.bush_sprite_thermal4,
                                 'mrap_thermal': self.mrap_sprite_thermal,
                                 'mrap': self.mrap_sprite
                                 }
            self.sprites = Sprite(self)
        self.show = False
        self.thread.join()
    #
    def graph_set(self, n):
        self.show = True
        self.thread = threading.Thread(target=self.load, args=())
        self.thread.start()
        self.NUM_RAYS = n
        self.DELTA_ANGLE_optic = self.FOV_optic / self.NUM_RAYS
        self.DIST_optic = self.NUM_RAYS / (2 * math.tan(self.HALF_FOV_optic * 3.14 / 180))
        if self.optic_scope_width % self.NUM_RAYS == 0:
            self.SCALE_optic = self.optic_scope_width // self.NUM_RAYS
        else:
            self.SCALE_optic = int(self.optic_scope_width / self.NUM_RAYS) + 1
        self.DELTA_ANGLE_optic_zoom = self.FOV_optic_zoom / self.NUM_RAYS
        self.DIST_optic_zoom = self.NUM_RAYS / (2 * math.tan(self.HALF_FOV_optic_zoom * 3.14 / 180))
        if self.optic_scope_width % self.NUM_RAYS == 0:
            self.SCALE_optic_zoom = self.optic_scope_width // self.NUM_RAYS
        else:
            self.SCALE_optic_zoom = int(self.optic_scope_width / self.NUM_RAYS) + 1
        self.DELTA_ANGLE_thermal = self.FOV_thermal / self.NUM_RAYS
        self.DIST_thermal = self.NUM_RAYS / (2 * math.tan(self.HALF_FOV_thermal * 3.14 / 180))
        if self.thermal_width % self.NUM_RAYS == 0:
            self.SCALE_thermal = self.thermal_width // self.NUM_RAYS
        else:
            self.SCALE_thermal = int(self.thermal_width // self.NUM_RAYS) + 1
        self.DELTA_ANGLE_thermal_zoom = self.FOV_thermal_zoom / self.NUM_RAYS
        self.DIST_thermal_zoom = self.NUM_RAYS / (2 * math.tan(self.HALF_FOV_thermal_zoom * 3.14 / 180))
        self.DELTA_ANGLE_thermal_zoom_extra = self.FOV_thermal_zoom_extra / self.NUM_RAYS
        self.DIST_thermal_zoom_extra = self.NUM_RAYS / (2 * math.tan(self.HALF_FOV_thermal_zoom_extra * 3.14 / 180))
        if self.thermal_width_d % self.NUM_RAYS == 0:
            self.SCALE_thermal_d = self.thermal_width_d // self.NUM_RAYS
        else:
            self.SCALE_thermal_d = int(self.thermal_width_d // self.NUM_RAYS) + 1
        self.show = False
        self.thread.join()

    #
    def update_db(self):
        self.show = True
        self.thread = threading.Thread(target=self.load, args=())
        self.thread.start()
        self.bd.update_to_db("graph_table", "(low, mid, high)",
                             f"({self.graph_dict[0]}, {self.graph_dict[1]}, {self.graph_dict[2]})")
        self.bd.update_to_db("minimap_table", "([on], off)", f"({self.minimap_dict[0]}, {self.minimap_dict[1]})")
        self.bd.update_to_db("FPS_table", "(low, mid, high)",
                             f"({self.fps_dict[0]}, {self.fps_dict[1]}, {self.fps_dict[2]})")
        self.bd.update_to_db("volume_table", "(volume_music, volume_sound, volume_general)",
                             f"({self.volume_music}, {self.volume_sound}, {self.volume_general})")
        self.bd.update_to_db("full_table", "([on], off)", f"({self.full_dict[0]}, {self.full_dict[1]})")
        self.bd.update_to_db("size_table", "(width, height)", f"({self.WIDTH}, {self.HEIGHT})")
        self.bd.update_to_db("monitor_table", "id", f"{self.monitor}")
        self.show = False
        self.thread.join()

    #
    def update_size(self):
        self.show = True
        self.thread = threading.Thread(target=self.load, args=())
        self.thread.start()

        gif_pygame.transform.scale(self.gif, (self.WIDTH, self.HEIGHT))
        for i in range(len(self.menu_list)):
            self.menu_list[i] = pygame.transform.scale(self.menu_list[i], (self.WIDTH, self.HEIGHT))
        self.destroyed_image = pygame.transform.scale(self.destroyed_image, (self.WIDTH, self.HEIGHT))
        self.gunner_site = pygame.transform.scale(self.gunner_site_base,
                                                  (self.WIDTH, self.HEIGHT))

        self.cursor = pygame.transform.scale(self.cursor_base, (self.WIDTH * 0.03125, self.WIDTH * 0.03125))
        self.size_text_b = int(self.WIDTH * 0.01875)

        self.side = min(int(self.WIDTH * 0.02), int(self.tile_w * 0.8))
        self.a_w = self.WIDTH * 0.05 * (self.FPS / 60) * (7 / self.side)
        self.a_s = -self.WIDTH * 0.1 * (self.FPS / 60) * (7 / self.side)
        self.a_stop = self.WIDTH * 0.1 * (self.FPS / 60) * (7 / self.side)
        self.max_speed_w = self.WIDTH * 0.2 * (self.FPS / 60) * (7 / self.side)
        self.max_speed_s = -self.WIDTH * 0.01 * (self.FPS / 60) * (7 / self.side)
        self.min_speed_ad = self.WIDTH * 0.01 * (self.FPS / 60) * 10 / 60 * (7 / self.side)

        self.show = False
        self.thread.join()

        self.set_lvl()

        self.show = True
        self.thread = threading.Thread(target=self.load, args=())
        self.thread.start()

        self.minimap_tank_b = pygame.transform.scale(self.minimap_tank_base,
                                                     (self.WIDTH * 0.0625 // self.minimap_k,
                                                      self.WIDTH * 0.0625 // self.minimap_k))
        self.minimap_tank_tower = pygame.transform.scale(self.minimap_tank_tower_base,
                                                         (self.WIDTH * 0.0625 // self.minimap_k,
                                                          self.WIDTH * 0.0625 // self.minimap_k))

        self.minimap_tank_b_scope = pygame.transform.scale(self.minimap_tank_base,
                                                           (self.WIDTH * 0.0625 / 1.5,
                                                            self.WIDTH * 0.0625 / 1.5))
        self.minimap_tank_tower_scope = pygame.transform.scale(self.minimap_tank_tower_base,
                                                               (self.WIDTH * 0.062 / 1.5,
                                                                self.WIDTH * 0.062 / 1.5))

        self.texture_w = self.WIDTH * 0.6 * 1.44
        self.texture_h = self.WIDTH * 0.6
        self.texture_scale = self.texture_w // self.tile_w
        self.textures = {'3': pygame.transform.scale(self.texture_1_base,
                                                     (self.texture_w, self.texture_h)),
                         '1': pygame.transform.scale(self.texture_2_base,
                                                     (self.texture_w, self.texture_h)),
                         '2': pygame.transform.scale(self.texture_2_base,
                                                     (self.texture_w, self.texture_h)),
                         '5': pygame.transform.scale(self.texture_5_base,
                                                     (self.texture_w, self.texture_h)),
                         '7': pygame.transform.scale(self.texture_7_base,
                                                     (self.texture_w, self.texture_h)),
                         '9': pygame.transform.scale(self.texture_9_base,
                                                     (self.texture_w, self.texture_h)),
                         }
        self.thermal_textures = {'3': (pygame.transform.scale(self.texture_1_base,
                                                              (self.texture_w, self.texture_h)), 30),
                                 '1': (pygame.transform.scale(self.texture_2_base,
                                                              (self.texture_w, self.texture_h)), 20),
                                 '2': (pygame.transform.scale(self.texture_2_base,
                                                              (self.texture_w, self.texture_h)), 40),
                                 '5': (pygame.transform.scale(self.texture_5_base,
                                                              (self.texture_w, self.texture_h)), 40),
                                 '7': (pygame.transform.scale(self.texture_7_base,
                                                              (self.texture_w, self.texture_h)), 40),
                                 '9': (pygame.transform.scale(self.texture_9_base,
                                                              (self.texture_w, self.texture_h)), 50),

                                 }
        for i, j in self.thermal_textures.items():
            thermal_texture(j[0], j[1], self.max_t)

        self.optic_sight_x = 0.5 * self.WIDTH
        self.optic_sight_y = 0.1 * self.WIDTH
        self.optic_sight_w_r = 0.2 * self.WIDTH
        self.optic_sight_h_r = 0.2 * self.WIDTH
        self.optic_scope_width = self.HEIGHT

        self.thermal_sight_h_r = 0.13 * self.WIDTH
        self.thermal_sight_w_r = 0.2 * self.WIDTH
        self.thermal_sight_x = 0.22 * self.WIDTH
        self.thermal_sight_y = 0.25 * self.WIDTH

        self.PROJ_COEFF_optic = 70 * self.HEIGHT
        if self.optic_scope_width % self.NUM_RAYS == 0:
            self.SCALE_optic = self.optic_scope_width // self.NUM_RAYS
        else:
            self.SCALE_optic = int(self.optic_scope_width / self.NUM_RAYS) + 1

        self.PROJ_COEFF_optic_zoom = 210 * self.HEIGHT
        if self.optic_scope_width % self.NUM_RAYS == 0:
            self.SCALE_optic_zoom = self.optic_scope_width // self.NUM_RAYS
        else:
            self.SCALE_optic_zoom = int(self.optic_scope_width / self.NUM_RAYS) + 1

        self.optic_sight = pygame.transform.scale(self.optic_sight_base,
                                                  (self.HEIGHT, self.HEIGHT))
        self.optic_sight_zoom = pygame.transform.scale(self.optic_sight_zoom_base,
                                                       (self.HEIGHT, self.HEIGHT))

        self.thermal_image = pygame.transform.scale(self.thermal_base,
                                                    (self.HEIGHT * 1.225, self.HEIGHT))
        self.thermal_sight = pygame.transform.scale(self.thermal_sight_base,
                                                    (self.thermal_width, self.thermal_height))
        self.thermal_sight_zoom = pygame.transform.scale(self.thermal_sight_zoom_base,
                                                         (self.thermal_width, self.thermal_height))

        self.thermal_base_width = self.HEIGHT * 1.225
        self.thermal_width = self.HEIGHT * 1.225 / 13.4 * 11.15
        self.thermal_height = self.HEIGHT / 14.2 * 11

        self.PROJ_COEFF_thermal = 95 * self.thermal_height
        if self.thermal_width % self.NUM_RAYS == 0:
            self.SCALE_thermal = self.thermal_width // self.NUM_RAYS
        else:
            self.SCALE_thermal = int(self.thermal_width // self.NUM_RAYS) + 1
        self.thermal_x = self.HEIGHT / 13.4 * 1.4
        self.thermal_y = self.HEIGHT / 14.2 * 1.57

        self.PROJ_COEFF_thermal_zoom = 285 * self.thermal_height

        self.DIST_thermal_zoom_extra = self.NUM_RAYS / (2 * math.tan(self.HALF_FOV_thermal_zoom_extra * 3.14 / 180))
        self.PROJ_COEFF_thermal_zoom_extra = 570 * self.thermal_height

        self.suo_x = self.WIDTH * 0.83
        self.suo_y = self.WIDTH * 0.39
        self.suo_w_r = self.WIDTH * 0.14
        self.suo_h_r = self.WIDTH * 0.1
        self.suo_x = self.WIDTH * 0.83
        self.suo_y = self.WIDTH * 0.39
        self.suo_w_r = self.WIDTH * 0.14
        self.suo_h_r = self.WIDTH * 0.1

        self.thermal_width_d = self.WIDTH * 5 / 37
        self.thermal_height_d = self.HEIGHT * 0.8 / 20.5

        self.PROJ_COEFF_thermal_d = 30 * self.thermal_height
        self.PROJ_COEFF_thermal_zoom_extra_d = 180 * self.thermal_height
        self.PROJ_COEFF_thermal_zoom_d = 90 * self.thermal_height
        if self.thermal_width_d % self.NUM_RAYS == 0:
            self.SCALE_thermal_d = self.thermal_width_d // self.NUM_RAYS
        else:
            self.SCALE_thermal_d = int(self.thermal_width_d // self.NUM_RAYS) + 1
        self.thermal_x_d = self.WIDTH * 9.1 / 37
        self.thermal_y_d = self.HEIGHT * 11 / 20.5
        self.thermal_y_d_2 = self.HEIGHT * 9.4 / 20.5
        self.thermal_sight_d = pygame.transform.scale(self.thermal_sight_base,
                                                      (self.thermal_width / 4, self.thermal_height / 4))
        self.thermal_sight_zoom_d = pygame.transform.scale(self.thermal_sight_zoom_base,
                                                           (self.thermal_width / 4, self.thermal_height / 4))
        self.gunner_site2 = pygame.transform.scale(self.gunner_site_base2,
                                                   (self.WIDTH, self.HEIGHT))

        self.bush_sprite = pygame.transform.scale(self.test_sprite, (self.WIDTH * 0.4, self.WIDTH * 0.4))
        self.bush_sprite_thermal = pygame.transform.scale(self.test_sprite, (self.WIDTH * 0.4, self.WIDTH * 0.4))
        thermal_texture(self.bush_sprite_thermal, 20, 50)

        self.bush_sprite2 = pygame.transform.scale(self.test_sprite, (self.WIDTH * 0.4, self.WIDTH * 0.4))
        self.bush_sprite_thermal2 = pygame.transform.scale(self.test_sprite2, (self.WIDTH * 0.4, self.WIDTH * 0.4))
        thermal_texture(self.bush_sprite_thermal2, 20, 50)

        self.bush_sprite3 = pygame.transform.scale(self.test_sprite, (self.WIDTH * 0.4, self.WIDTH * 0.4))
        self.bush_sprite_thermal3 = pygame.transform.scale(self.test_sprite3, (self.WIDTH * 0.4, self.WIDTH * 0.4))
        thermal_texture(self.bush_sprite_thermal3, 20, 50)

        self.bush_sprite4 = pygame.transform.scale(self.test_sprite, (self.WIDTH * 0.4, self.WIDTH * 0.4))
        self.bush_sprite_thermal4 = pygame.transform.scale(self.test_sprite4, (self.WIDTH * 0.4, self.WIDTH * 0.4))
        thermal_texture(self.bush_sprite_thermal4, 20, 50)

        self.center_ray = self.NUM_RAYS // 2 - 1
        self.FAKE_RAYS = int(self.NUM_RAYS * 4)

        self.test_sprite_v = [pygame.image.load(f'resources/sprites/bmp_sprite/{i * 45}.png').convert_alpha() for i in
                              range(8)]
        self.test_sprite_v_thermal = [pygame.image.load(f'resources/sprites/bmp_sprite/{i * 45}.png').convert_alpha()
                                      for i in range(8)]
        for i in self.test_sprite_v_thermal:
            thermal_texture(i, 60, 60)

        self.shot_frames = int(self.shot_anim_time * self.FPS)
        self.shot_frames_delta = max(self.shot_frames // 3, 1)

        self.shot_he_frames = int(self.shot_he_anim_time * self.FPS)
        self.shot_he_frames_delta = max(self.shot_he_frames // 5, 1)
        self.shot_he_frames = int(self.shot_he_frames_delta * 5)

        self.shot_smog_frames = int(self.shot_smog_anim_time * self.FPS)
        self.shot_smog_frames_delta = max(self.shot_smog_frames // 10, 1)
        self.shot_smog_frames = int(self.shot_smog_frames_delta * 10)

        self.sprites = Sprite(self)

        self.show = False
        self.thread.join()

    def update_size2(self):
        self.size_text_b = int(self.WIDTH * 0.01875)
        #
        self.show = True
        self.thread = threading.Thread(target=self.load, args=())
        self.thread.start()
        #
        self.destroyed_image = pygame.transform.scale(self.destroyed_image, (self.WIDTH, self.HEIGHT))
        gif_pygame.transform.scale(self.gif, (self.WIDTH, self.HEIGHT))
        for i in range(len(self.menu_list)):
            self.menu_list[i] = pygame.transform.scale(self.menu_list[i], (self.WIDTH, self.HEIGHT))
        #
        self.cursor = pygame.transform.scale(self.cursor_base, (self.WIDTH * 0.03125, self.WIDTH * 0.03125))
        #
        self.set_lvl()

        self.minimap_tank_b = pygame.transform.scale(self.minimap_tank_base,
                                                     (self.WIDTH * 0.0625 // self.minimap_k,
                                                      self.WIDTH * 0.0625 // self.minimap_k))
        self.minimap_tank_tower = pygame.transform.scale(self.minimap_tank_tower_base,
                                                         (self.WIDTH * 0.0625 // self.minimap_k,
                                                          self.WIDTH * 0.0625 // self.minimap_k))
        self.minimap_tank_b_scope = pygame.transform.scale(self.minimap_tank_base_scope,
                                                           (self.WIDTH * 0.0625 / 1.5,
                                                            self.WIDTH * 0.0625 / 1.5))
        self.minimap_tank_tower_scope = pygame.transform.scale(self.minimap_tank_tower_scope,
                                                               (self.WIDTH * 0.062 / 1.5,
                                                                self.WIDTH * 0.062 / 1.5))
        #
        self.side = min(int(self.WIDTH * 0.02), int(self.tile_w * 0.8))
        self.a_w = self.WIDTH * 0.05 * (self.FPS / 60) * (7 / self.side)
        self.a_s = -self.WIDTH * 0.1 * (self.FPS / 60) * (7 / self.side)
        self.a_stop = self.WIDTH * 0.1 * (self.FPS / 60) * (7 / self.side)
        self.max_speed_w = self.WIDTH * 0.2 * (self.FPS / 60) * (7 / self.side)
        self.max_speed_s = -self.WIDTH * 0.01 * (self.FPS / 60) * (7 / self.side)
        self.min_speed_ad = self.WIDTH * 0.01 * (self.FPS / 60) * 10 / 60 * (7 / self.side)
        #
        self.optic_scope_width = self.HEIGHT
        self.NUM_RAYS = 125 + 75 * self.graph_dict.index(1)
        self.DELTA_ANGLE_optic = self.FOV_optic / self.NUM_RAYS
        self.DIST_optic = self.NUM_RAYS / (2 * math.tan(self.HALF_FOV_optic * 3.14 / 180))
        self.PROJ_COEFF_optic = 70 * self.HEIGHT

        if self.optic_scope_width % self.NUM_RAYS == 0:
            self.SCALE_optic = self.optic_scope_width // self.NUM_RAYS
        else:
            self.SCALE_optic = int(self.optic_scope_width / self.NUM_RAYS) + 1
        #
        self.DELTA_ANGLE_optic_zoom = self.FOV_optic_zoom / self.NUM_RAYS
        self.DIST_optic_zoom = self.NUM_RAYS / (2 * math.tan(self.HALF_FOV_optic_zoom * 3.14 / 180))
        self.PROJ_COEFF_optic_zoom = 210 * self.HEIGHT

        if self.optic_scope_width % self.NUM_RAYS == 0:
            self.SCALE_optic_zoom = self.optic_scope_width // self.NUM_RAYS
        else:
            self.SCALE_optic_zoom = int(self.optic_scope_width / self.NUM_RAYS) + 1
        #
        self.optic_sight = pygame.transform.scale(self.optic_sight_base,
                                                  (self.HEIGHT, self.HEIGHT))

        self.optic_sight_zoom = pygame.transform.scale(self.optic_sight_zoom_base,
                                                       (self.HEIGHT, self.HEIGHT))
        #
        self.gunner_site = pygame.transform.scale(self.gunner_site_base,
                                                  (self.WIDTH, self.HEIGHT))
        self.gunner_site2 = pygame.transform.scale(self.gunner_site_base2,
                                                   (self.WIDTH, self.HEIGHT))
        #
        self.texture_w = self.WIDTH * 0.6 * 1.44
        self.texture_h = self.WIDTH * 0.6

        self.texture_scale = self.texture_w // self.tile_w if self.texture_w % self.tile_w == 0 else self.texture_w // self.tile_w + 1
        #
        self.textures = {'3': pygame.transform.scale(self.texture_1_base,
                                                     (self.texture_w, self.texture_h)),
                         '1': pygame.transform.scale(self.texture_2_base,
                                                     (self.texture_w, self.texture_h)),
                         '2': pygame.transform.scale(self.texture_2_base,
                                                     (self.texture_w, self.texture_h)),
                         '5': pygame.transform.scale(self.texture_5_base,
                                                     (self.texture_w, self.texture_h)),
                         '7': pygame.transform.scale(self.texture_7_base,
                                                     (self.texture_w, self.texture_h)),
                         '9': pygame.transform.scale(self.texture_9_base,
                                                     (self.texture_w, self.texture_h)),
                         }
        #
        self.thermal_textures = {'3': (pygame.transform.scale(self.texture_1_base,
                                                              (self.texture_w, self.texture_h)), 30),
                                 '1': (pygame.transform.scale(self.texture_2_base,
                                                              (self.texture_w, self.texture_h)), 20),
                                 '2': (pygame.transform.scale(self.texture_2_base,
                                                              (self.texture_w, self.texture_h)), 40),
                                 '5': (pygame.transform.scale(self.texture_5_base,
                                                              (self.texture_w, self.texture_h)), 40),
                                 '7': (pygame.transform.scale(self.texture_7_base,
                                                              (self.texture_w, self.texture_h)), 40),
                                 '9': (pygame.transform.scale(self.texture_9_base,
                                                              (self.texture_w, self.texture_h)), 50),

                                 }
        for i, j in self.thermal_textures.items():
            thermal_texture(j[0], j[1], self.max_t)
        #
        self.optic_sight_x = 0.5 * self.WIDTH
        self.optic_sight_y = 0.1 * self.WIDTH
        self.optic_sight_w_r = 0.2 * self.WIDTH
        self.optic_sight_h_r = 0.2 * self.WIDTH
        #
        self.thermal_sight_h_r = 0.13 * self.WIDTH
        self.thermal_sight_w_r = 0.2 * self.WIDTH
        self.thermal_sight_x = 0.22 * self.WIDTH
        self.thermal_sight_y = 0.25 * self.WIDTH
        #
        self.thermal_image = pygame.transform.scale(self.thermal_base,
                                                    (self.HEIGHT * 1.225, self.HEIGHT))

        self.thermal_base_width = self.HEIGHT * 1.225
        self.thermal_width = self.HEIGHT * 1.225 / 13.4 * 11.15
        self.thermal_height = self.HEIGHT / 14.2 * 11
        self.thermal_x = self.HEIGHT / 13.4 * 1.4
        self.thermal_y = self.HEIGHT / 14.2 * 1.57
        #
        self.DELTA_ANGLE_thermal = self.FOV_thermal / self.NUM_RAYS
        self.DIST_thermal = self.NUM_RAYS / (2 * math.tan(self.HALF_FOV_thermal * 3.14 / 180))
        self.PROJ_COEFF_thermal = 95 * self.thermal_height

        if self.thermal_width % self.NUM_RAYS == 0:
            self.SCALE_thermal = self.thermal_width // self.NUM_RAYS
        else:
            self.SCALE_thermal = int(self.thermal_width // self.NUM_RAYS) + 1
        #
        self.DELTA_ANGLE_thermal_zoom = self.FOV_thermal_zoom / self.NUM_RAYS
        self.DIST_thermal_zoom = self.NUM_RAYS / (2 * math.tan(self.HALF_FOV_thermal_zoom * 3.14 / 180))
        self.PROJ_COEFF_thermal_zoom = 285 * self.thermal_height
        #
        self.thermal_sight = pygame.transform.scale(self.thermal_sight_base,
                                                    (self.thermal_width, self.thermal_height))

        self.thermal_sight_zoom = pygame.transform.scale(self.thermal_sight_zoom_base,
                                                         (self.thermal_width, self.thermal_height))
        #
        self.DELTA_ANGLE_thermal_zoom_extra = self.FOV_thermal_zoom_extra / self.NUM_RAYS
        self.DIST_thermal_zoom_extra = self.NUM_RAYS / (2 * math.tan(self.HALF_FOV_thermal_zoom_extra * 3.14 / 180))
        self.PROJ_COEFF_thermal_zoom_extra = 570 * self.thermal_height
        #
        self.suo_x = self.WIDTH * 0.83
        self.suo_y = self.WIDTH * 0.39
        self.suo_w_r = self.WIDTH * 0.14
        self.suo_h_r = self.WIDTH * 0.1
        #
        self.thermal_width_d = self.WIDTH * 5 / 37
        self.thermal_height_d = self.HEIGHT * 0.8 / 20.5

        self.PROJ_COEFF_thermal_d = 30 * self.thermal_height
        self.PROJ_COEFF_thermal_zoom_extra_d = 180 * self.thermal_height
        self.PROJ_COEFF_thermal_zoom_d = 90 * self.thermal_height

        if self.thermal_width_d % self.NUM_RAYS == 0:
            self.SCALE_thermal_d = self.thermal_width_d // self.NUM_RAYS
        else:
            self.SCALE_thermal_d = int(self.thermal_width_d // self.NUM_RAYS) + 1
        #
        self.thermal_x_d = self.WIDTH * 9.1 / 37
        self.thermal_y_d = self.HEIGHT * 11 / 20.5
        self.thermal_y_d_2 = self.HEIGHT * 9.4 / 20.5
        #
        self.thermal_sight_d = pygame.transform.scale(self.thermal_sight_base,
                                                      (self.thermal_width / 4, self.thermal_height / 4))
        self.thermal_sight_zoom_d = pygame.transform.scale(self.thermal_sight_zoom_base,
                                                           (self.thermal_width / 4, self.thermal_height / 4))
        #
        self.bush_sprite2 = pygame.transform.scale(self.test_sprite, (self.WIDTH * 0.4, self.WIDTH * 0.4))
        self.bush_sprite_thermal2 = pygame.transform.scale(self.test_sprite2, (self.WIDTH * 0.4, self.WIDTH * 0.4))
        thermal_texture(self.bush_sprite_thermal2, 20, 50)

        self.bush_sprite3 = pygame.transform.scale(self.test_sprite, (self.WIDTH * 0.4, self.WIDTH * 0.4))
        self.bush_sprite_thermal3 = pygame.transform.scale(self.test_sprite3, (self.WIDTH * 0.4, self.WIDTH * 0.4))
        thermal_texture(self.bush_sprite_thermal3, 20, 50)

        self.bush_sprite4 = pygame.transform.scale(self.test_sprite, (self.WIDTH * 0.4, self.WIDTH * 0.4))
        self.bush_sprite_thermal4 = pygame.transform.scale(self.test_sprite4, (self.WIDTH * 0.4, self.WIDTH * 0.4))
        thermal_texture(self.bush_sprite_thermal4, 20, 50)

        self.bush_sprite = pygame.transform.scale(self.test_sprite, (self.WIDTH * 0.4, self.WIDTH * 0.4))
        self.bush_sprite_thermal = pygame.transform.scale(self.test_sprite, (self.WIDTH * 0.4, self.WIDTH * 0.4))
        thermal_texture(self.bush_sprite_thermal, 20, self.max_t)

        self.tree_sprite_thermal = pygame.transform.scale(self.tree_sprite, (self.WIDTH * 0.4, self.WIDTH * 0.4))
        thermal_texture(self.tree_sprite_thermal, 20, self.max_t)
        #
        self.center_ray = self.NUM_RAYS // 2 - 1
        self.FAKE_RAYS = int(self.NUM_RAYS * 2)
        #
        self.shot_frames = int(self.shot_anim_time * self.FPS)
        self.shot_frames_delta = max(self.shot_frames // 3, 1)
        self.shot_frames = int(self.shot_frames_delta * 3)
        #
        self.shot_he_frames = int(self.shot_he_anim_time * self.FPS)
        self.shot_he_frames_delta = max(self.shot_he_frames // 5, 1)
        self.shot_he_frames = int(self.shot_he_frames_delta * 5)
        #
        self.shot_smog_frames = int(self.shot_smog_anim_time * self.FPS)
        self.shot_smog_frames_delta = max(self.shot_smog_frames // 10, 1)
        self.shot_smog_frames = int(self.shot_smog_frames_delta * 10)
        #
        self.bmp_death_frames = int(self.bmp_death_anim_time * self.FPS)
        self.bmp_death_frames_delta = max(self.bmp_death_frames // 14, 1)
        self.bmp_death_frames = int(self.bmp_death_frames_delta * 14)
        #
        self.sprite_types = {'bush_thermal': self.bush_sprite_thermal,
                             'bush': self.bush_sprite,
                             'bmp': self.test_sprite_v,
                             'bmp_thermal': self.test_sprite_v_thermal,
                             'tree_thermal': self.tree_sprite_thermal,
                             'tree': self.tree_sprite,
                             'tank': self.tank_sprite,
                             'tank_thermal': self.tank_sprite_thermal,
                             'bush1': self.bush_sprite2,
                             'bush2': self.bush_sprite3,
                             'bush3': self.bush_sprite4,
                             'bush1_thermal': self.bush_sprite_thermal2,
                             'bush2_thermal': self.bush_sprite_thermal3,
                             'bush3_thermal': self.bush_sprite_thermal4
                             }
        #
        self.show = False
        self.thread.join()

    #
    def update_sprites(self):
        self.show = True
        self.thread = threading.Thread(target=self.load, args=())
        self.thread.start()

        self.sprites = Sprite(self)

        self.show = False
        self.thread.join()

    #
    def load(self):
        while self.show:
            if self.load_timer >= 1:
                background = pygame.Surface((self.WIDTH, self.HEIGHT))
                background.fill((50, 60, 50))
                self.display.blit(background, (0, 0))
                load_bl = Text(self.WIDTH * 0.5028, self.HEIGHT * 0.5046, (0, 0, 0),
                               'Загрузка' + "." * self.count_point,
                               int(self.WIDTH * 0.052))
                load = Text(self.WIDTH * 0.5, self.HEIGHT * 0.5, (200, 200, 200), 'Загрузка' + "." * self.count_point,
                            int(self.WIDTH * 0.052))
                load_bl.draw(self.display)
                load.draw(self.display)
                self.count_point = 0 if self.count_point == 3 else self.count_point + 1
                self.load_timer = 0
            self.load_timer += 1 / (int(self.clock.get_fps()) + self.FPS * (int(self.clock.get_fps()) == 0))
            pygame.display.flip()
            self.clock.tick(self.FPS)
        self.load_timer = 1


def thermal_texture(surface, t, max_t):
    w, h = surface.get_size()
    for x in range(w):
        for y in range(h):
            a = surface.get_at((x, y))[3]
            r, g, b = surface.get_at((x, y))[0:3]
            color = min(r, g, b)
            color *= abs(t / max_t)
            color = min(max(max(color, 0), 5), 255)
            surface.set_at((x, y), pygame.Color(int(color), int(color), int(color), a))
