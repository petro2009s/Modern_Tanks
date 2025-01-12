import sys

from bin.buttons import *
import pygame
import random
from bin.text import Text
from bin.settings import Settings
from bin.tank import Tank


class Game:
    def __init__(self):
        pygame.init()
        self.s = Settings()
        pygame.display.set_caption('World of Modern Tanks')
        pygame.display.set_icon(self.s.icon)
        pygame.mouse.set_visible(False)
        self.s.music_menu.play(-1)
        self.s.music_menu.set_volume(self.s.volume_general / 100 * self.s.volume_music / 100)

    def start_game(self, apply_sett=""):
        if apply_sett:
            self.settings_menu()
        show = True

        # menu_im = self.s.menu_list[random.randint(0, 4)]

        header_bl = Text(self.s.WIDTH * 0.5028, self.s.HEIGHT * 0.1052, (0, 0, 0), 'World of Modern Tanks',
                         int(self.s.WIDTH * 0.052))
        header = Text(self.s.WIDTH * 0.5, self.s.HEIGHT * 0.1, (200, 200, 200), 'World of Modern Tanks',
                      int(self.s.WIDTH * 0.052))

        play_button = Button(self.s.WIDTH * 0.33, self.s.HEIGHT * 0.32, self.s.WIDTH * 0.33, self.s.HEIGHT * 0.1,
                             'Играть', self.s.size_text_b, 'resources/images/button_inact.png',
                             'resources/images/button_active.png',
                             'resources/sounds/button_menu_sound.mp3')

        settings_button = Button(self.s.WIDTH * 0.33, self.s.HEIGHT * 0.51, self.s.WIDTH * 0.33, self.s.HEIGHT * 0.1,
                                 'Настройки', self.s.size_text_b, 'resources/images/button_inact.png',
                                 'resources/images/button_active.png',
                                 'resources/sounds/button_menu_sound.mp3')

        quit_button = Button(self.s.WIDTH * 0.33, self.s.HEIGHT * 0.69, self.s.WIDTH * 0.33, self.s.HEIGHT * 0.1,
                             'Выйти', self.s.size_text_b, 'resources/images/button_inact.png',
                             'resources/images/button_active.png',
                             'resources/sounds/button_menu_sound.mp3')
        fps_count_text_bl = Text(self.s.WIDTH * 0.961, self.s.HEIGHT * 0.972, (0, 0, 0),
                                 str(int(self.s.clock.get_fps())) + ' FPS', int(self.s.WIDTH * 0.0104),
                                 is_topleft=True)
        fps_count_text = Text(self.s.WIDTH * 0.96, self.s.HEIGHT * 0.97, (200, 200, 200),
                              str(int(self.s.clock.get_fps())) + ' FPS', int(self.s.WIDTH * 0.0104),
                              is_topleft=True)
        while show:

            quit_button.check(pygame.mouse.get_pos())
            settings_button.check(pygame.mouse.get_pos())
            play_button.check(pygame.mouse.get_pos())

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # self.s.update_db()
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.USEREVENT:
                    if event.button == quit_button:
                        # self.s.update_db()
                        pygame.quit()
                        sys.exit()
                    if event.button == settings_button:
                        self.settings_menu()
                    if event.button == play_button:
                        self.game_menu()

                play_button.handle_event(event, self.s.volume_sound * (self.s.volume_general / 100))
                settings_button.handle_event(event, self.s.volume_sound * (self.s.volume_general / 100))
                quit_button.handle_event(event, self.s.volume_sound * (self.s.volume_general / 100))

            # self.s.display.blit(menu_im, (0, 0))
            self.s.gif.render(self.s.display, (0, 0))
            play_button.draw(self.s.display)
            quit_button.draw(self.s.display)
            settings_button.draw(self.s.display)

            header_bl.draw(self.s.display)
            header.draw(self.s.display)

            fps_count_text.set_another_text(str(int(self.s.clock.get_fps())) + ' FPS')
            fps_count_text_bl.set_another_text(str(int(self.s.clock.get_fps())) + ' FPS')
            fps_count_text_bl.draw(self.s.display)
            fps_count_text.draw(self.s.display)

            if pygame.mouse.get_focused():
                self.s.display.blit(self.s.cursor, pygame.mouse.get_pos())
            pygame.display.flip()
            self.s.clock.tick(self.s.FPS)

    def settings_menu(self):
        sett = True
        menu_im = self.s.menu_list[random.randint(0, 4)]

        full_dict_temp = self.s.full_dict.copy()

        header_bl = Text(self.s.WIDTH * 0.354, self.s.HEIGHT * 0.104, (0, 0, 0), 'Настройки графики',
                         int(self.s.WIDTH * 0.03125))
        header = Text(self.s.WIDTH * 0.352, self.s.HEIGHT * 0.1, (200, 200, 200), 'Настройки графики',
                      int(self.s.WIDTH * 0.03125))

        volume_header_bl = Text(self.s.WIDTH * 0.778, self.s.HEIGHT * 0.104, (0, 0, 0), 'Настройки звука',
                                int(self.s.WIDTH * 0.03125))
        volume_header = Text(self.s.WIDTH * 0.776, self.s.HEIGHT * 0.1, (200, 200, 200), 'Настройки звука',
                             int(self.s.WIDTH * 0.03125))

        screen_text_bl = Text(self.s.WIDTH * 0.502, self.s.HEIGHT * 0.204, (0, 0, 0), 'Разрешение экрана',
                              int(self.s.WIDTH * 0.0208))
        screen_text = Text(self.s.WIDTH * 0.5, self.s.HEIGHT * 0.2, (200, 200, 200), 'Разрешение экрана',
                           int(self.s.WIDTH * 0.0208))

        fullscreen_text_bl = Text(self.s.WIDTH * 0.502, self.s.HEIGHT * 0.404, (0, 0, 0), 'Полноэкранный режим',
                                  int(self.s.WIDTH * 0.0208))
        fullscreen_text = Text(self.s.WIDTH * 0.5, self.s.HEIGHT * 0.4, (200, 200, 200), 'Полноэкранный режим',
                               int(self.s.WIDTH * 0.0208))

        gr_text_bl = Text(self.s.WIDTH * 0.198, self.s.HEIGHT * 0.204, (0, 0, 0), 'Разрешение рендера',
                          int(self.s.WIDTH * 0.0208))
        gr_text = Text(self.s.WIDTH * 0.196, self.s.HEIGHT * 0.2, (200, 200, 200), 'Разрешение рендера',
                       int(self.s.WIDTH * 0.0208))
        self.s.size_on_text = [self.s.WIDTH, self.s.HEIGHT]
        size_text_bl = Text(self.s.WIDTH * 0.502, self.s.HEIGHT * 0.304, (0, 0, 0),
                            "*".join(list(map(str, self.s.size_on_text))), int(self.s.WIDTH * 0.03125))
        size_text = Text(self.s.WIDTH * 0.5, self.s.HEIGHT * 0.3, (200, 200, 200),
                         "*".join(list(map(str, self.s.size_on_text))), int(self.s.WIDTH * 0.03125))
        d_text_bl = Text(self.s.WIDTH * 0.198, self.s.HEIGHT * 0.404, (0, 0, 0), 'Дальность прорисовки',
                         int(self.s.WIDTH * 0.0208))
        d_text = Text(self.s.WIDTH * 0.196, self.s.HEIGHT * 0.4, (200, 200, 200), 'Дальность прорисовки',
                      int(self.s.WIDTH * 0.0208))

        fps_text_bl = Text(self.s.WIDTH * 0.198, self.s.HEIGHT * 0.604, (0, 0, 0), 'Частота кадров',
                           int(self.s.WIDTH * 0.0208))
        fps_text = Text(self.s.WIDTH * 0.196, self.s.HEIGHT * 0.6, (200, 200, 200), 'Частота кадров',
                        int(self.s.WIDTH * 0.0208))

        general_text_bl = Text(self.s.WIDTH * 0.778, self.s.HEIGHT * 0.204, (0, 0, 0), 'Общая громкость',
                               int(self.s.WIDTH * 0.025))
        general_text = Text(self.s.WIDTH * 0.776, self.s.HEIGHT * 0.2, (200, 200, 200), 'Общая громкость',
                            int(self.s.WIDTH * 0.025))

        music_text_bl = Text(self.s.WIDTH * 0.778, self.s.HEIGHT * 0.404, (0, 0, 0), 'Громкость музыки',
                             int(self.s.WIDTH * 0.025))
        music_text = Text(self.s.WIDTH * 0.776, self.s.HEIGHT * 0.4, (200, 200, 200), 'Громкость музыки',
                          int(self.s.WIDTH * 0.025))

        sound_text_bl = Text(self.s.WIDTH * 0.778, self.s.HEIGHT * 0.604, (0, 0, 0), 'Громкость звуков',
                             int(self.s.WIDTH * 0.025))
        sound_text = Text(self.s.WIDTH * 0.776, self.s.HEIGHT * 0.6, (200, 200, 200), 'Громкость звуков',
                          int(self.s.WIDTH * 0.025))

        general_text_volume_bl = Text(self.s.WIDTH * 0.778, self.s.HEIGHT * 0.304, (0, 0, 0),
                                      str(self.s.volume_general), int(self.s.WIDTH * 0.0417))
        general_text_volume = Text(self.s.WIDTH * 0.776, self.s.HEIGHT * 0.3, (200, 200, 200),
                                   str(self.s.volume_general), int(self.s.WIDTH * 0.0417))

        music_text_volume_bl = Text(self.s.WIDTH * 0.778, self.s.HEIGHT * 0.504, (0, 0, 0), str(self.s.volume_music),
                                    int(self.s.WIDTH * 0.0417))
        music_text_volume = Text(self.s.WIDTH * 0.776, self.s.HEIGHT * 0.5, (200, 200, 200), str(self.s.volume_music),
                                 int(self.s.WIDTH * 0.0417))

        sound_text_volume_bl = Text(self.s.WIDTH * 0.778, self.s.HEIGHT * 0.704, (0, 0, 0), str(self.s.volume_sound),
                                    int(self.s.WIDTH * 0.0417))
        sound_text_volume = Text(self.s.WIDTH * 0.776, self.s.HEIGHT * 0.7, (200, 200, 200), str(self.s.volume_sound),
                                 int(self.s.WIDTH * 0.0417))

        apply_button = Button(self.s.WIDTH * 0.382, self.s.HEIGHT * 0.63, self.s.WIDTH * 0.234, self.s.HEIGHT * 0.139,
                              'Применить', self.s.size_text_b, 'resources/images/button_inact.png',
                              'resources/images/button_active.png',
                              'resources/sounds/button_menu_sound.mp3')

        back_button = Button(self.s.WIDTH * 0.33, self.s.HEIGHT * 0.833, self.s.WIDTH * 0.335, self.s.HEIGHT * 0.0925,
                             'Назад', self.s.size_text_b, 'resources/images/button_inact.png',
                             'resources/images/button_active.png',
                             'resources/sounds/button_menu_sound.mp3')

        gr_low = SelectButton(self.s.WIDTH * 0.041, self.s.HEIGHT * 0.23, int(self.s.WIDTH * 0.09),
                              self.s.HEIGHT * 0.139, 'Низкое', sound='resources/sounds/button_menu_sound.mp3',
                              font_size=int(self.s.size_text_b * 0.833))
        gr_mid = SelectButton(self.s.WIDTH * 0.138, self.s.HEIGHT * 0.23, int(self.s.WIDTH * 0.09),
                              self.s.HEIGHT * 0.139, 'Среднее', sound='resources/sounds/button_menu_sound.mp3',
                              font_size=int(self.s.size_text_b * 0.833))
        gr_high = SelectButton(self.s.WIDTH * 0.234, self.s.HEIGHT * 0.23, int(self.s.WIDTH * 0.09),
                               self.s.HEIGHT * 0.139, 'Высокое', sound='resources/sounds/button_menu_sound.mp3',
                               font_size=int(self.s.size_text_b * 0.833))

        d_low = SelectButton(self.s.WIDTH * 0.041, self.s.HEIGHT * 0.43, int(self.s.WIDTH * 0.09),
                             self.s.HEIGHT * 0.139, 'Низкая', sound='resources/sounds/button_menu_sound.mp3',
                             font_size=int(self.s.size_text_b * 0.833))
        d_mid = SelectButton(self.s.WIDTH * 0.138, self.s.HEIGHT * 0.43, int(self.s.WIDTH * 0.09),
                             self.s.HEIGHT * 0.139, 'Средняя', sound='resources/sounds/button_menu_sound.mp3',
                             font_size=int(self.s.size_text_b * 0.833))
        d_high = SelectButton(self.s.WIDTH * 0.234, self.s.HEIGHT * 0.43, int(self.s.WIDTH * 0.09),
                              self.s.HEIGHT * 0.139, 'Высокая', sound='resources/sounds/button_menu_sound.mp3',
                              font_size=int(self.s.size_text_b * 0.833))

        fps_low = SelectButton(self.s.WIDTH * 0.041, self.s.HEIGHT * 0.63, int(self.s.WIDTH * 0.09),
                               self.s.HEIGHT * 0.139, '30', sound='resources/sounds/button_menu_sound.mp3',
                               font_size=self.s.size_text_b)
        fps_mid = SelectButton(self.s.WIDTH * 0.138, self.s.HEIGHT * 0.63, int(self.s.WIDTH * 0.09),
                               self.s.HEIGHT * 0.139, '60', sound='resources/sounds/button_menu_sound.mp3',
                               font_size=self.s.size_text_b)
        fps_high = SelectButton(self.s.WIDTH * 0.234, self.s.HEIGHT * 0.63, int(self.s.WIDTH * 0.09),
                                self.s.HEIGHT * 0.139, '90', sound='resources/sounds/button_menu_sound.mp3',
                                font_size=self.s.size_text_b)

        full_on = SelectButton(self.s.WIDTH * 0.377, self.s.HEIGHT * 0.43, int(self.s.WIDTH * 0.1208),
                               self.s.HEIGHT * 0.139, 'Включить', sound='resources/sounds/button_menu_sound.mp3',
                               font_size=int(self.s.size_text_b * 0.833))
        full_off = SelectButton(self.s.WIDTH * 0.5026, self.s.HEIGHT * 0.43, int(self.s.WIDTH * 0.1208),
                                self.s.HEIGHT * 0.139, 'Выключить', sound='resources/sounds/button_menu_sound.mp3',
                                font_size=int(self.s.size_text_b * 0.833))

        plus_screen = Button(self.s.WIDTH * 0.377, self.s.HEIGHT * 0.263, self.s.WIDTH * 0.0417,
                             self.s.HEIGHT * 0.074, '', 1, 'resources/images/plus.png',
                             'resources/images/plus_act.png', 'resources/sounds/button_menu_sound.mp3')
        minus_screen = Button(self.s.WIDTH * 0.579, self.s.HEIGHT * 0.263, self.s.WIDTH * 0.0417,
                              self.s.HEIGHT * 0.074, '', 1, 'resources/images/minus.png',
                              'resources/images/minus_act.png', 'resources/sounds/button_menu_sound.mp3')

        plus_general = Button(self.s.WIDTH * 0.677, self.s.HEIGHT * 0.263, self.s.WIDTH * 0.0417,
                              self.s.HEIGHT * 0.074, '', 1, 'resources/images/plus.png',
                              'resources/images/plus_act.png', 'resources/sounds/button_menu_sound.mp3')
        minus_general = Button(self.s.WIDTH * 0.8333, self.s.HEIGHT * 0.263, self.s.WIDTH * 0.0417,
                               self.s.HEIGHT * 0.074, '', 1, 'resources/images/minus.png',
                               'resources/images/minus_act.png', 'resources/sounds/button_menu_sound.mp3')

        plus_music = Button(self.s.WIDTH * 0.677, self.s.HEIGHT * 0.463, self.s.WIDTH * 0.0417,
                            self.s.HEIGHT * 0.074, '', 1, 'resources/images/plus.png',
                            'resources/images/plus_act.png', 'resources/sounds/button_menu_sound.mp3')
        minus_music = Button(self.s.WIDTH * 0.8333, self.s.HEIGHT * 0.463, self.s.WIDTH * 0.0417,
                             self.s.HEIGHT * 0.074, '', 1, 'resources/images/minus.png',
                             'resources/images/minus_act.png', 'resources/sounds/button_menu_sound.mp3')

        plus_sound = Button(self.s.WIDTH * 0.677, self.s.HEIGHT * 0.663, self.s.WIDTH * 0.0417,
                            self.s.HEIGHT * 0.074, '', 1, 'resources/images/plus.png',
                            'resources/images/plus_act.png', 'resources/sounds/button_menu_sound.mp3')
        minus_sound = Button(self.s.WIDTH * 0.8333, self.s.HEIGHT * 0.663, self.s.WIDTH * 0.0417,
                             self.s.HEIGHT * 0.074, '', 1, 'resources/images/minus.png',
                             'resources/images/minus_act.png', 'resources/sounds/button_menu_sound.mp3')

        gr_list = [gr_low, gr_mid, gr_high]
        d_list = [d_low, d_mid, d_high]
        fps_list = [fps_low, fps_mid, fps_high]
        full_list = [full_on, full_off]
        button_list = [plus_music, minus_music, plus_sound, minus_sound, plus_general, minus_general, plus_screen,
                       minus_screen, apply_button]

        fps_count_text_bl = Text(self.s.WIDTH * 0.961, self.s.HEIGHT * 0.972, (0, 0, 0),
                                 str(int(self.s.clock.get_fps())) + ' FPS', int(self.s.WIDTH * 0.0104),
                                 is_topleft=True)
        fps_count_text = Text(self.s.WIDTH * 0.96, self.s.HEIGHT * 0.97, (200, 200, 200),
                              str(int(self.s.clock.get_fps())) + ' FPS', int(self.s.WIDTH * 0.0104),
                              is_topleft=True)

        all_list = [back_button, gr_high, gr_low, gr_mid, d_high, d_low, d_mid, fps_high, fps_low, fps_mid, gr_text_bl,
                    gr_text, d_text_bl, d_text, fps_text_bl, fps_text, header_bl, header, fps_count_text_bl,
                    fps_count_text,
                    plus_music, minus_music, plus_sound, minus_sound, volume_header_bl, volume_header, music_text_bl,
                    music_text, sound_text_bl, sound_text, music_text_volume_bl, music_text_volume,
                    sound_text_volume_bl,
                    sound_text_volume, general_text_bl, general_text, general_text_volume_bl, general_text_volume,
                    plus_general, minus_general, screen_text_bl, screen_text, fullscreen_text_bl, fullscreen_text,
                    plus_screen, minus_screen, size_text_bl, size_text, apply_button, full_on, full_off]
        set_list = ['low', 'mid', 'high']
        v = {'0': False, '1': True}
        while sett:
            back_button.check(pygame.mouse.get_pos())

            for i in range(3):
                gr_list[i].is_cl = self.s.graph_dict[i]

            for i in gr_list:
                i.check(pygame.mouse.get_pos())

            for i in range(3):
                d_list[i].is_cl = self.s.d_dict[i]

            for i in d_list:
                i.check(pygame.mouse.get_pos())

            for i in range(3):
                fps_list[i].is_cl = self.s.fps_dict[i]

            for i in full_list:
                i.check(pygame.mouse.get_pos())

            for i in range(2):
                full_list[i].is_cl = full_dict_temp[i]

            for i in fps_list:
                i.check(pygame.mouse.get_pos())

            for i in button_list:
                i.check(pygame.mouse.get_pos())

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # self.s.update_db()
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sett = False

                if event.type == pygame.USEREVENT:
                    if event.button == back_button:
                        sett = False

                    if event.button == gr_high:
                        self.s.graph_dict[1] = False
                        self.s.graph_dict[0] = False
                        self.s.graph_dict[2] = True

                    if event.button == gr_low:
                        self.s.graph_dict[1] = False
                        self.s.graph_dict[2] = False
                        self.s.graph_dict[0] = True

                    if event.button == gr_mid:
                        self.s.graph_dict[0] = False
                        self.s.graph_dict[2] = False
                        self.s.graph_dict[1] = True

                    if event.button == d_high:
                        self.s.d_dict[1] = False
                        self.s.d_dict[0] = False
                        self.s.d_dict[2] = True

                    if event.button == d_low:
                        self.s.d_dict[1] = False
                        self.s.d_dict[2] = False
                        self.s.d_dict[0] = True

                    if event.button == d_mid:
                        self.s.d_dict[0] = False
                        self.s.d_dict[2] = False
                        self.s.d_dict[1] = True

                    if event.button == fps_high:
                        self.s.fps_dict[1] = False
                        self.s.fps_dict[0] = False
                        self.s.fps_dict[2] = True
                        self.s.FPS = 90

                    if event.button == fps_low:
                        self.s.fps_dict[1] = False
                        self.s.fps_dict[2] = False
                        self.s.fps_dict[0] = True
                        self.s.FPS = 30

                    if event.button == fps_mid:
                        self.s.fps_dict[0] = False
                        self.s.fps_dict[2] = False
                        self.s.fps_dict[1] = True
                        self.s.FPS = 60

                    if event.button == full_on:
                        full_dict_temp[0] = True
                        full_dict_temp[1] = False

                    if event.button == full_off:
                        full_dict_temp[0] = False
                        full_dict_temp[1] = True

                    if event.button == plus_screen:
                        if self.s.size_list.index(tuple(self.s.size_on_text)) != 0:
                            self.s.size_on_text = list(
                                self.s.size_list[self.s.size_list.index(tuple(self.s.size_on_text)) - 1])
                            size_text.set_another_text("*".join(list(map(str, self.s.size_on_text))))
                            size_text_bl.set_another_text("*".join(list(map(str, self.s.size_on_text))))

                    if event.button == minus_screen:
                        if self.s.size_list.index(tuple(self.s.size_on_text)) + 1 != len(self.s.size_list):
                            self.s.size_on_text = list(
                                self.s.size_list[self.s.size_list.index(tuple(self.s.size_on_text)) + 1])
                            size_text.set_another_text("*".join(list(map(str, self.s.size_on_text))))
                            size_text_bl.set_another_text("*".join(list(map(str, self.s.size_on_text))))

                    if event.button == plus_general:
                        self.s.volume_general += 10 * (self.s.volume_general != 100)
                        self.s.music_menu.set_volume((self.s.volume_music / 100) * (self.s.volume_general / 100))
                        general_text_volume.set_another_text(str(self.s.volume_general))
                        general_text_volume_bl.set_another_text(str(self.s.volume_general))

                    if event.button == minus_general:
                        self.s.volume_general -= 10 * (self.s.volume_general != 0)
                        self.s.music_menu.set_volume((self.s.volume_music / 100) * (self.s.volume_general / 100))
                        general_text_volume.set_another_text(str(self.s.volume_general))
                        general_text_volume_bl.set_another_text(str(self.s.volume_general))

                    if event.button == plus_music:
                        self.s.volume_music += 10 * (self.s.volume_music != 100)
                        self.s.music_menu.set_volume((self.s.volume_music / 100) * (self.s.volume_general / 100))
                        music_text_volume.set_another_text(str(self.s.volume_music))
                        music_text_volume_bl.set_another_text(str(self.s.volume_music))

                    if event.button == minus_music:
                        self.s.volume_music -= 10 * (self.s.volume_music != 0)
                        self.s.music_menu.set_volume((self.s.volume_music / 100) * (self.s.volume_general / 100))
                        music_text_volume.set_another_text(str(self.s.volume_music))
                        music_text_volume_bl.set_another_text(str(self.s.volume_music))

                    if event.button == plus_sound:
                        self.s.volume_sound += 10 * (self.s.volume_sound != 100)
                        sound_text_volume.set_another_text(str(self.s.volume_sound))
                        sound_text_volume_bl.set_another_text(str(self.s.volume_sound))

                    if event.button == minus_sound:
                        self.s.volume_sound -= 10 * (self.s.volume_sound != 0)
                        sound_text_volume.set_another_text(str(self.s.volume_sound))
                        sound_text_volume_bl.set_another_text(str(self.s.volume_sound))

                    if event.button == apply_button:
                        if not ((self.s.width_m < self.s.size_on_text[0] or self.s.height_m < self.s.size_on_text[
                            1]) and full_dict_temp[1]):
                            self.s.WIDTH, self.s.HEIGHT = self.s.size_on_text
                            if full_dict_temp[0]:
                                pygame.display.set_mode((self.s.WIDTH, self.s.HEIGHT), pygame.FULLSCREEN)
                            else:
                                if self.s.width_m == self.s.WIDTH and self.s.height_m == self.s.HEIGHT:
                                    pygame.display.set_mode((self.s.WIDTH, self.s.HEIGHT - 40))
                                else:
                                    pygame.display.set_mode((self.s.WIDTH, self.s.HEIGHT))
                            self.s.full_dict = full_dict_temp
                            sett = False
                            self.s.update_size()
                            self.start_game("apply_set")

                back_button.handle_event(event, self.s.volume_sound * (self.s.volume_general / 100))

                for i in gr_list:
                    i.handle_event(event, self.s.volume_sound * (self.s.volume_general / 100))

                for i in d_list:
                    i.handle_event(event, self.s.volume_sound * (self.s.volume_general / 100))

                for i in fps_list:
                    i.handle_event(event, self.s.volume_sound * (self.s.volume_general / 100))

                for i in full_list:
                    i.handle_event(event, self.s.volume_sound * (self.s.volume_general / 100))

                for i in button_list:
                    i.handle_event(event, self.s.volume_sound * (self.s.volume_general / 100))

            self.s.display.blit(menu_im, (0, 0))
            fps_count_text_bl.set_another_text(str(int(self.s.clock.get_fps())) + ' FPS')
            fps_count_text.set_another_text(str(int(self.s.clock.get_fps())) + ' FPS')

            for i in all_list:
                i.draw(self.s.display)

            if pygame.mouse.get_focused():
                self.s.display.blit(self.s.cursor, pygame.mouse.get_pos())
            pygame.display.flip()
            self.s.clock.tick(self.s.FPS)
        self.s.update_db()
    def game_menu(self):
        gm = True

        APFSDS_COUNT = 0
        HE_COUNT = 0
        HEAT_COUNT = 0
        MAX_AMMO = 22
        CURRENT_AMMO = 0
        AMMO = 22

        menu_im = self.s.menu_list[random.randint(0, 4)]

        header_bl = Text(self.s.WIDTH * 0.502, self.s.HEIGHT * 0.053, (0, 0, 0), 'Игра', int(self.s.WIDTH * 0.03125))
        header = Text(self.s.WIDTH * 0.5, self.s.HEIGHT * 0.05, (200, 200, 200), 'Игра', int(self.s.WIDTH * 0.03125))

        t_bl = Text(self.s.WIDTH * 0.032, self.s.HEIGHT * 0.144, (0, 0, 0), 'Выбор техники', int(self.s.WIDTH * 0.025),
                    is_topleft=True)
        t = Text(self.s.WIDTH * 0.03, self.s.HEIGHT * 0.14, (200, 200, 200), 'Выбор техники', int(self.s.WIDTH * 0.025),
                 is_topleft=True)

        lvl_bl = Text(self.s.WIDTH * 0.032, self.s.HEIGHT * 0.373, (0, 0, 0), 'Выбор уровня', int(self.s.WIDTH * 0.025),
                      is_topleft=True)
        lvl = Text(self.s.WIDTH * 0.03, self.s.HEIGHT * 0.37, (200, 200, 200), 'Выбор уровня',
                   int(self.s.WIDTH * 0.025), is_topleft=True)

        am_bl = Text(self.s.WIDTH * 0.032, self.s.HEIGHT * 0.573, (0, 0, 0), 'Выбор боеприпасов',
                     int(self.s.WIDTH * 0.025),
                     is_topleft=True)
        am = Text(self.s.WIDTH * 0.03, self.s.HEIGHT * 0.57, (200, 200, 200), 'Выбор боеприпасов',
                  int(self.s.WIDTH * 0.025),
                  is_topleft=True)

        am_d = Text(self.s.WIDTH * 0.705, self.s.HEIGHT * 0.633, (200, 200, 200), 'Описание боеприпасов',
                    int(self.s.WIDTH * 0.009))
        tank_descr = Text(self.s.WIDTH * 0.60125, self.s.HEIGHT * 0.15, (200, 200, 200), 'Описание техники',
                          int(self.s.WIDTH * 0.009))
        tank_tth = Text(self.s.WIDTH * 0.875, self.s.HEIGHT * 0.15, (200, 200, 200), 'ТТХ техники',
                        int(self.s.WIDTH * 0.009))
        lvl_descr = Text(self.s.WIDTH * 0.60125, self.s.HEIGHT * 0.4, (200, 200, 200), 'Описание уровня',
                         int(self.s.WIDTH * 0.009))

        apfsds_txt = SelectButton(self.s.WIDTH * 0.05, self.s.HEIGHT * 0.63, w=self.s.WIDTH * 0.083,
                                  h=self.s.HEIGHT * 0.042, w_r=self.s.WIDTH * 0.092, h_r=self.s.HEIGHT * 0.074,
                                  text='БОПС', im='resources/images/apfsds.png', font_size=self.s.size_text_b)
        he_txt = SelectButton(self.s.WIDTH * 0.185, self.s.HEIGHT * 0.63, w=self.s.WIDTH * 0.083,
                              h=self.s.HEIGHT * 0.042, w_r=self.s.WIDTH * 0.092, h_r=self.s.HEIGHT * 0.074,
                              text='ОФС', im='resources/images/he.png', font_size=self.s.size_text_b)
        heat_txt = SelectButton(self.s.WIDTH * 0.32, self.s.HEIGHT * 0.63, w=self.s.WIDTH * 0.083,
                                h=self.s.HEIGHT * 0.042, w_r=self.s.WIDTH * 0.092, h_r=self.s.HEIGHT * 0.074,
                                text='КС', im='resources/images/heat.png', font_size=self.s.size_text_b)

        plus1 = Button(round(self.s.WIDTH // 2 * 0.07), round(self.s.HEIGHT * 0.725), self.s.WIDTH * 0.03125,
                       self.s.HEIGHT * 0.055, '', 1, 'resources/images/plus.png',
                       'resources/images/plus_act.png', 'resources/sounds/button_menu_sound.mp3')
        plus2 = Button(round(self.s.WIDTH // 2 * 0.34), round(self.s.HEIGHT * 0.725), self.s.WIDTH * 0.03125,
                       self.s.HEIGHT * 0.055, '', 1, 'resources/images/plus.png',
                       'resources/images/plus_act.png', 'resources/sounds/button_menu_sound.mp3')
        plus3 = Button(round(self.s.WIDTH // 2 * 0.61), round(self.s.HEIGHT * 0.725), self.s.WIDTH * 0.03125,
                       self.s.HEIGHT * 0.055, '', 1, 'resources/images/plus.png',
                       'resources/images/plus_act.png', 'resources/sounds/button_menu_sound.mp3')
        minus1 = Button(round(self.s.WIDTH // 2 * 0.25), round(self.s.HEIGHT * 0.725), self.s.WIDTH * 0.03125,
                        self.s.HEIGHT * 0.055, '', 1, 'resources/images/minus.png',
                        'resources/images/minus_act.png', 'resources/sounds/button_menu_sound.mp3')
        minus2 = Button(round(self.s.WIDTH // 2 * 0.52), round(self.s.HEIGHT * 0.725), self.s.WIDTH * 0.03125,
                        self.s.HEIGHT * 0.055, '', 1, 'resources/images/minus.png',
                        'resources/images/minus_act.png', 'resources/sounds/button_menu_sound.mp3')
        minus3 = Button(round(self.s.WIDTH // 2 * 0.79), round(self.s.HEIGHT * 0.725), self.s.WIDTH * 0.03125,
                        self.s.HEIGHT * 0.055, '', 1, 'resources/images/minus.png',
                        'resources/images/minus_act.png', 'resources/sounds/button_menu_sound.mp3')

        apfsds_count_txt = Text(round(self.s.WIDTH // 2 * 0.187), round(self.s.HEIGHT * 0.75), (200, 200, 200),
                                str(APFSDS_COUNT), int(self.s.WIDTH * 0.016))
        apfsds_count_txt_bl = Text(self.s.WIDTH * 0.0955, self.s.HEIGHT * 0.754, (0, 0, 0),
                                   str(APFSDS_COUNT), int(self.s.WIDTH * 0.016))
        he_count_txt = Text(round(self.s.WIDTH // 2 * 0.457), round(self.s.HEIGHT * 0.75), (200, 200, 200),
                            str(HE_COUNT), int(self.s.WIDTH * 0.016))
        he_count_txt_bl = Text(self.s.WIDTH * 0.2305, round(self.s.HEIGHT * 0.753), (0, 0, 0), str(HE_COUNT),
                               int(self.s.WIDTH * 0.016))
        heat_count_txt = Text(round(self.s.WIDTH // 2 * 0.727), round(self.s.HEIGHT * 0.75), (200, 200, 200),
                              str(HEAT_COUNT), int(self.s.WIDTH * 0.016))
        heat_count_txt_bl = Text(self.s.WIDTH * 0.365, round(self.s.HEIGHT * 0.753), (0, 0, 0), str(HEAT_COUNT),
                                 int(self.s.WIDTH * 0.016))
        max_ammo_text_bl = Text(self.s.WIDTH * 0.2305, round(self.s.HEIGHT * 0.803), (0, 0, 0), f'0/{str(MAX_AMMO)}',
                                int(self.s.WIDTH * 0.016))
        max_ammo_text = Text(round(self.s.WIDTH // 2 * 0.457), round(self.s.HEIGHT * 0.8), (200, 200, 200),
                             f'0/{str(MAX_AMMO)}', int(self.s.WIDTH * 0.016))

        back_button = Button(self.s.WIDTH * 0.081, self.s.HEIGHT * 0.83, self.s.WIDTH * 0.336, self.s.HEIGHT * 0.0925,
                             'Назад', self.s.size_text_b, 'resources/images/button_inact.png',
                             'resources/images/button_active.png',
                             'resources/sounds/button_menu_sound.mp3')

        play_button = Button(self.s.WIDTH * 0.58, self.s.HEIGHT * 0.83, self.s.WIDTH * 0.336, self.s.HEIGHT * 0.0925,
                             'Играть', self.s.size_text_b, 'resources/images/button_inact.png',
                             'resources/images/button_active.png',
                             'resources/sounds/button_menu_sound.mp3')
        tank1_button = SelectButton(round(self.s.WIDTH // 2 * 0.060), round(self.s.HEIGHT * 0.23),
                                    w=self.s.WIDTH * 0.09375, h=self.s.HEIGHT * 0.085, w_r=self.s.WIDTH * 0.104,
                                    h_r=self.s.HEIGHT * 0.139,
                                    text='Т-90М', im='resources/images/T-90M_profile.png',
                                    sound='resources/sounds/button_menu_sound.mp3',
                                    font_size=self.s.size_text_b)
        guide_button = SelectButton(round(self.s.WIDTH // 2 * 0.060), round(self.s.HEIGHT * 0.43),
                                    w=self.s.WIDTH * 0.033, h=self.s.HEIGHT * 0.0925, w_r=self.s.WIDTH * 0.104,
                                    h_r=self.s.HEIGHT * 0.139,
                                    text='Обучение', im='resources/images/guide.png',
                                    sound='resources/sounds/button_menu_sound.mp3',
                                    font_size=self.s.size_text_b)

        ammo_descr_list = []
        k = 0.63
        for i in self.s.ammo:
            temp = Text(round(self.s.WIDTH // 2 * 0.9), round(self.s.HEIGHT * k), (200, 200, 200), i,
                        int(self.s.WIDTH * 0.0078), (50, 60, 50),
                        is_topleft=True)
            k += 0.018
            ammo_descr_list.append(temp)

        tank_descr_list = []
        k2 = 0.17
        for i in self.s.T_90M_descr:
            temp = Text(round(self.s.WIDTH // 2 * 0.9), round(self.s.HEIGHT * k2), (200, 200, 200), i,
                        int(self.s.WIDTH * 0.0078), (50, 60, 50),
                        is_topleft=True)
            k2 += 0.0166
            tank_descr_list.append(temp)

        k3 = 0.17
        T_90M_TTH_list = []
        for i in self.s.T_90M_TTH:
            temp = Text(round(self.s.WIDTH // 2 * 1.5), round(self.s.HEIGHT * k3), (200, 200, 200), i,
                        int(self.s.WIDTH * 0.0078), (50, 60, 50),
                        is_topleft=True)
            k3 += 0.0167
            T_90M_TTH_list.append(temp)

        k4 = 0.43
        guide_list = []
        for i in self.s.guide_descr:
            temp = Text(round(self.s.WIDTH // 2 * 0.9), round(self.s.HEIGHT * k4), (200, 200, 200), i,
                        int(self.s.WIDTH * 0.0078), (50, 60, 50),
                        is_topleft=True)
            k4 += 0.0167
            guide_list.append(temp)

        tank_list = [tank1_button]
        lvl_list = [guide_button]

        rect = pygame.Rect(round(self.s.WIDTH // 2 * 0.89), round(self.s.HEIGHT * 0.14), self.s.WIDTH * 0.573,
                           self.s.HEIGHT * 0.676)
        button_list = [back_button, tank1_button, guide_button, play_button, plus1, plus2, plus3, minus1, minus2,
                       minus3]

        fps_count_text_bl = Text(self.s.WIDTH * 0.961, self.s.HEIGHT * 0.972, (0, 0, 0),
                                 str(int(self.s.clock.get_fps())) + ' FPS', int(self.s.WIDTH * 0.0104),
                                 is_topleft=True)
        fps_count_text = Text(self.s.WIDTH * 0.96, self.s.HEIGHT * 0.97, (200, 200, 200),
                              str(int(self.s.clock.get_fps())) + ' FPS', int(self.s.WIDTH * 0.0104),
                              is_topleft=True)

        text_list = [header_bl, header, t_bl, t, lvl_bl, lvl, am_bl, am, apfsds_txt, heat_txt, he_txt,
                     apfsds_count_txt_bl, fps_count_text_bl, fps_count_text,
                     apfsds_count_txt, he_count_txt_bl, he_count_txt, heat_count_txt_bl, heat_count_txt,
                     max_ammo_text_bl, max_ammo_text]

        while gm:

            apfsds_txt.is_cl = True
            he_txt.is_cl = True
            heat_txt.is_cl = True

            fps_count_text_bl.set_another_text(str(int(self.s.clock.get_fps())) + ' FPS')
            fps_count_text.set_another_text(str(int(self.s.clock.get_fps())) + ' FPS')

            self.s.display.blit(menu_im, (0, 0))
            for i in range(len(tank_list)):
                tank_list[i].is_cl = self.s.tank_dict[i]
            for i in range(len(lvl_list)):
                lvl_list[i].is_cl = self.s.lvl_dict[i]

            for i in button_list:
                i.check(pygame.mouse.get_pos())

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.s.update_db()
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        gm = False

                if event.type == pygame.USEREVENT:
                    if event.button == back_button:
                        gm = False

                    if event.button == plus1:
                        if MAX_AMMO > 0:
                            APFSDS_COUNT += 1
                            MAX_AMMO -= 1
                            CURRENT_AMMO += 1
                            apfsds_count_txt.set_another_text(str(APFSDS_COUNT))
                            apfsds_count_txt_bl.set_another_text(str(APFSDS_COUNT))
                            max_ammo_text_bl.set_another_text(f'{str(CURRENT_AMMO)}/{str(AMMO)}')
                            max_ammo_text.set_another_text(f'{str(CURRENT_AMMO)}/{str(AMMO)}')

                    elif event.button == plus2:
                        if MAX_AMMO > 0:
                            HE_COUNT += 1
                            MAX_AMMO -= 1
                            CURRENT_AMMO += 1
                            he_count_txt.set_another_text(str(HE_COUNT))
                            he_count_txt_bl.set_another_text(str(HE_COUNT))
                            max_ammo_text_bl.set_another_text(f'{str(CURRENT_AMMO)}/{str(AMMO)}')
                            max_ammo_text.set_another_text(f'{str(CURRENT_AMMO)}/{str(AMMO)}')


                    elif event.button == plus3:
                        if MAX_AMMO > 0:
                            HEAT_COUNT += 1
                            MAX_AMMO -= 1
                            CURRENT_AMMO += 1
                            heat_count_txt.set_another_text(str(HEAT_COUNT))
                            heat_count_txt_bl.set_another_text(str(HEAT_COUNT))
                            max_ammo_text_bl.set_another_text(f'{str(CURRENT_AMMO)}/{str(AMMO)}')
                            max_ammo_text.set_another_text(f'{str(CURRENT_AMMO)}/{str(AMMO)}')

                    if event.button == minus1:
                        if APFSDS_COUNT > 0:
                            APFSDS_COUNT -= 1
                            MAX_AMMO += 1
                            CURRENT_AMMO -= 1
                            apfsds_count_txt.set_another_text(str(APFSDS_COUNT))
                            apfsds_count_txt_bl.set_another_text(str(APFSDS_COUNT))
                            max_ammo_text_bl.set_another_text(f'{str(CURRENT_AMMO)}/{str(AMMO)}')
                            max_ammo_text.set_another_text(f'{str(CURRENT_AMMO)}/{str(AMMO)}')
                    elif event.button == minus2:
                        if HE_COUNT > 0:
                            HE_COUNT -= 1
                            MAX_AMMO += 1
                            CURRENT_AMMO -= 1
                            he_count_txt.set_another_text(str(HE_COUNT))
                            he_count_txt_bl.set_another_text(str(HE_COUNT))
                            max_ammo_text_bl.set_another_text(f'{str(CURRENT_AMMO)}/{str(AMMO)}')
                            max_ammo_text.set_another_text(f'{str(CURRENT_AMMO)}/{str(AMMO)}')

                    elif event.button == minus3:
                        if HEAT_COUNT > 0:
                            HEAT_COUNT -= 1
                            MAX_AMMO += 1
                            CURRENT_AMMO -= 1
                            heat_count_txt.set_another_text(str(HEAT_COUNT))
                            heat_count_txt_bl.set_another_text(str(HEAT_COUNT))
                            max_ammo_text_bl.set_another_text(f'{str(CURRENT_AMMO)}/{str(AMMO)}')
                            max_ammo_text.set_another_text(f'{str(CURRENT_AMMO)}/{str(AMMO)}')

                    if event.button == play_button:
                        print(APFSDS_COUNT, HE_COUNT, HEAT_COUNT)
                        print([i for i, j in self.s.tank_dict.items() if j][0])
                        print([i for i, j in self.s.lvl_dict.items() if j][0])
                        self.play()

                for i in button_list:
                    i.handle_event(event, self.s.volume_sound * (self.s.volume_general / 100))

            for i in button_list:
                i.draw(self.s.display)

            for i in text_list:
                i.draw(self.s.display)

            pygame.draw.rect(self.s.display, (50, 60, 50), rect)
            for i in ammo_descr_list:
                i.draw(self.s.display)
            for i in tank_descr_list:
                i.draw(self.s.display)
            for i in T_90M_TTH_list:
                i.draw(self.s.display)
            for i in guide_list:
                i.draw(self.s.display)
            am_d.draw(self.s.display)
            tank_descr.draw(self.s.display)
            tank_tth.draw(self.s.display)
            lvl_descr.draw(self.s.display)

            if pygame.mouse.get_focused():
                self.s.display.blit(self.s.cursor, pygame.mouse.get_pos())
            pygame.display.flip()
            self.s.clock.tick(self.s.FPS)

    def play(self):
        print(self.s.WIDTH // 2, self.s.HEIGHT // 2)
        tank = Tank(self.s, self.s.map_width // 2, self.s.map_height // 2, 0, self.s.minimap_k, 0, 0)
        tank.start()
