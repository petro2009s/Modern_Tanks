import sys

from bin.buttons import *
import pygame
import random
from bin.text import Text
from bin.settings import Settings
import gif_pygame


class Game:
    def __init__(self):
        pygame.init()
        self.s = Settings()
        pygame.display.set_caption('World of Modern Tanks')
        pygame.display.set_icon(self.s.icon)

    def start_game(self):
        show = True

        # menu_im = self.s.menu_list[random.randint(0, 4)]


        header_bl = Text(self.s.WIDTH // 2 + 4, round(self.s.HEIGHT * 0.1) + 4, (0, 0, 0), 'World of Modern Tanks', 70)
        header = Text(self.s.WIDTH // 2, round(self.s.HEIGHT * 0.1), (200, 200, 200), 'World of Modern Tanks', 70)

        play_button = Button(self.s.WIDTH // 2 - 323, 450, 645, 100, 'Играть', 'resources/images/button_inact.png',
                             'resources/images/button_active.png',
                             'resources/sounds/button_menu_sound.mp3')

        settings_button = Button(self.s.WIDTH // 2 - 323, 600, 645, 100, 'Настройки', 'resources/images/button_inact.png',
                                 'resources/images/button_active.png',
                                 'resources/sounds/button_menu_sound.mp3')

        quit_button = Button(self.s.WIDTH // 2 - 323, 750, 645, 100, 'Выйти', 'resources/images/button_inact.png',
                             'resources/images/button_active.png',
                             'resources/sounds/button_menu_sound.mp3')
        fps_count_text_bl = Text(self.s.WIDTH * 0.96 + 2, self.s.HEIGHT * 0.97 + 2, (0, 0, 0),
                                 str(int(self.s.clock.get_fps())) + ' FPS', 20,
                                 is_topleft=True)
        fps_count_text = Text(self.s.WIDTH * 0.96, self.s.HEIGHT * 0.97, (200, 200, 200),
                              str(int(self.s.clock.get_fps())) + ' FPS', 20,
                              is_topleft=True)
        while show:

            quit_button.check(pygame.mouse.get_pos())
            settings_button.check(pygame.mouse.get_pos())
            play_button.check(pygame.mouse.get_pos())

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.USEREVENT:
                    if event.button == quit_button:
                        pygame.quit()
                        sys.exit()
                    if event.button == settings_button:
                        self.settings_menu()
                    if event.button == play_button:
                        self.game_menu()

                play_button.handle_event(event)
                settings_button.handle_event(event)
                quit_button.handle_event(event)

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
            pygame.display.flip()
            self.s.clock.tick(self.s.FPS)

    def settings_menu(self):
        sett = True
        menu_im = self.s.menu_list[random.randint(0, 4)]

        header_bl = Text(self.s.WIDTH // 2 + 4, round(self.s.HEIGHT * 0.1) + 4, (0, 0, 0), 'Настройки графики', 60)
        header = Text(self.s.WIDTH // 2, round(self.s.HEIGHT * 0.1), (200, 200, 200), 'Настройки графики', 60)

        gr_text_bl = Text(self.s.WIDTH // 2 + 4, round(self.s.HEIGHT * 0.2) + 4, (0, 0, 0), 'Разрешение рендера', 48)
        gr_text = Text(self.s.WIDTH // 2, round(self.s.HEIGHT * 0.2), (200, 200, 200), 'Разрешение рендера', 48)

        d_text_bl = Text(self.s.WIDTH // 2 + 4, round(self.s.HEIGHT * 0.4) + 4, (0, 0, 0), 'Дальность прорисовки', 48)
        d_text = Text(self.s.WIDTH // 2, round(self.s.HEIGHT * 0.4), (200, 200, 200), 'Дальность прорисовки', 48)

        fps_text_bl = Text(self.s.WIDTH // 2 + 4, round(self.s.HEIGHT * 0.6) + 4, (0, 0, 0), 'Частота кадров', 48)
        fps_text = Text(self.s.WIDTH // 2, round(self.s.HEIGHT * 0.6), (200, 200, 200), 'Частота кадров', 48)

        back_button = Button(self.s.WIDTH // 2 - 323, 850, 645, 100, 'Назад', 'resources/images/button_inact.png',
                             'resources/images/button_active.png',
                             'resources/sounds/button_menu_sound.mp3')
        gr_low = SelectButton(510, self.s.HEIGHT * 0.23, 300, 150, 'Низкое', sound='resources/sounds/button_menu_sound.mp3')
        gr_mid = SelectButton(810, self.s.HEIGHT * 0.23, 300, 150, 'Среднее', sound='resources/sounds/button_menu_sound.mp3')
        gr_high = SelectButton(1110, self.s.HEIGHT * 0.23, 300, 150, 'Высокое', sound='resources/sounds/button_menu_sound.mp3')

        d_low = SelectButton(510, self.s.HEIGHT * 0.43, 300, 150, 'Низкая', sound='resources/sounds/button_menu_sound.mp3')
        d_mid = SelectButton(810, self.s.HEIGHT * 0.43, 300, 150, 'Средняя', sound='resources/sounds/button_menu_sound.mp3')
        d_high = SelectButton(1110, self.s.HEIGHT * 0.43, 300, 150, 'Высокая', sound='resources/sounds/button_menu_sound.mp3')

        fps_low = SelectButton(510, self.s.HEIGHT * 0.63, 300, 150, '30', sound='resources/sounds/button_menu_sound.mp3')
        fps_mid = SelectButton(810, self.s.HEIGHT * 0.63, 300, 150, '60', sound='resources/sounds/button_menu_sound.mp3')
        fps_high = SelectButton(1110, self.s.HEIGHT * 0.63, 300, 150, '90', sound='resources/sounds/button_menu_sound.mp3')

        gr_list = [gr_low, gr_mid, gr_high]
        d_list = [d_low, d_mid, d_high]
        fps_list = [fps_low, fps_mid, fps_high]

        fps_count_text_bl = Text(self.s.WIDTH * 0.96 + 2, self.s.HEIGHT * 0.97 + 2, (0, 0, 0), str(int(self.s.clock.get_fps())) + ' FPS', 20,
                              is_topleft=True)
        fps_count_text = Text(self.s.WIDTH * 0.96, self.s.HEIGHT * 0.97, (200, 200, 200), str(int(self.s.clock.get_fps())) + ' FPS', 20,
                              is_topleft=True)

        all_list = [back_button, gr_high, gr_low, gr_mid, d_high, d_low, d_mid, fps_high, fps_low, fps_mid, gr_text_bl,
                    gr_text, d_text_bl, d_text, fps_text_bl, fps_text, header_bl, header, fps_count_text_bl, fps_count_text]
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

            for i in fps_list:
                i.check(pygame.mouse.get_pos())

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

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

                back_button.handle_event(event)
                for i in gr_list:
                    i.handle_event(event)

                for i in d_list:
                    i.handle_event(event)

                for i in fps_list:
                    i.handle_event(event)

            self.s.display.blit(menu_im, (0, 0))
            fps_count_text_bl.set_another_text(str(int(self.s.clock.get_fps())) + ' FPS')
            fps_count_text.set_another_text(str(int(self.s.clock.get_fps())) + ' FPS')

            for i in all_list:
                i.draw(self.s.display)

            pygame.display.flip()
            self.s.clock.tick(self.s.FPS)

    def game_menu(self):
        gm = True

        APFSDS_COUNT = 0
        HE_COUNT = 0
        HEAT_COUNT = 0
        MAX_AMMO = 22
        CURRENT_AMMO = 0
        AMMO = 22

        menu_im = self.s.menu_list[random.randint(0, 4)]

        header_bl = Text(self.s.WIDTH // 2 + 4, round(self.s.HEIGHT * 0.05) + 4, (0, 0, 0), 'Игра', 60)
        header = Text(self.s.WIDTH // 2, round(self.s.HEIGHT * 0.05), (200, 200, 200), 'Игра', 60)

        t_bl = Text(round(self.s.WIDTH // 2 * 0.06) + 4, round(self.s.HEIGHT * 0.14) + 4, (0, 0, 0), 'Выбор техники', 48,
                    is_topleft=True)
        t = Text(round(self.s.WIDTH // 2 * 0.06), round(self.s.HEIGHT * 0.14), (200, 200, 200), 'Выбор техники', 48, is_topleft=True)

        lvl_bl = Text(round(self.s.WIDTH // 2 * 0.06) + 4, round(self.s.HEIGHT * 0.37) + 4, (0, 0, 0), 'Выбор уровня', 48,
                      is_topleft=True)
        lvl = Text(round(self.s.WIDTH // 2 * 0.06), round(self.s.HEIGHT * 0.37), (200, 200, 200), 'Выбор уровня', 48, is_topleft=True)

        am_bl = Text(round(self.s.WIDTH // 2 * 0.06) + 4, round(self.s.HEIGHT * 0.57) + 4, (0, 0, 0), 'Выбор боеприпасов', 48,
                     is_topleft=True)
        am = Text(round(self.s.WIDTH // 2 * 0.06), round(self.s.HEIGHT * 0.57), (200, 200, 200), 'Выбор боеприпасов', 48,
                  is_topleft=True)

        am_d = Text(round(self.s.WIDTH // 2 * 0.89) + 500, round(self.s.HEIGHT * 0.633), (200, 200, 200), 'Описание боеприпасов', 17)
        tank_descr = Text(round(self.s.WIDTH // 2 * 0.89) + 300, round(self.s.HEIGHT * 0.15), (200, 200, 200), 'Описание техники', 17)
        tank_tth = Text(round(self.s.WIDTH // 2 * 1.75), round(self.s.HEIGHT * 0.15), (200, 200, 200), 'ТТХ техники', 17)
        lvl_descr = Text(round(self.s.WIDTH // 2 * 0.89) + 300, round(self.s.HEIGHT * 0.4), (200, 200, 200), 'Описание уровня', 17)

        apfsds_txt = SelectButton(round(self.s.WIDTH // 2 * 0.1), round(self.s.HEIGHT * 0.63), w=160, h=45, w_r=176, h_r=80,
                                  text='БОПС', im='resources/images/apfsds.png', font_size=30)
        he_txt = SelectButton(round(self.s.WIDTH // 2 * 0.37), round(self.s.HEIGHT * 0.63), w=160, h=45, w_r=176, h_r=80,
                              text='ОФС', im='resources/images/he.png', font_size=30)
        heat_txt = SelectButton(round(self.s.WIDTH // 2 * 0.64), round(self.s.HEIGHT * 0.63), w=160, h=45, w_r=176, h_r=80,
                                text='КС', im='resources/images/heat.png', font_size=30)

        plus1 = Button(round(self.s.WIDTH // 2 * 0.07), round(self.s.HEIGHT * 0.725), 60, 60, '', 'resources/images/plus.png',
                       'resources/images/plus_act.png', 'resources/sounds/button_menu_sound.mp3')
        plus2 = Button(round(self.s.WIDTH // 2 * 0.34), round(self.s.HEIGHT * 0.725), 60, 60, '', 'resources/images/plus.png',
                       'resources/images/plus_act.png', 'resources/sounds/button_menu_sound.mp3')
        plus3 = Button(round(self.s.WIDTH // 2 * 0.61), round(self.s.HEIGHT * 0.725), 60, 60, '', 'resources/images/plus.png',
                       'resources/images/plus_act.png', 'resources/sounds/button_menu_sound.mp3')
        minus1 = Button(round(self.s.WIDTH // 2 * 0.25), round(self.s.HEIGHT * 0.725), 60, 60, '', 'resources/images/minus.png',
                        'resources/images/minus_act.png', 'resources/sounds/button_menu_sound.mp3')
        minus2 = Button(round(self.s.WIDTH // 2 * 0.52), round(self.s.HEIGHT * 0.725), 60, 60, '', 'resources/images/minus.png',
                        'resources/images/minus_act.png', 'resources/sounds/button_menu_sound.mp3')
        minus3 = Button(round(self.s.WIDTH // 2 * 0.79), round(self.s.HEIGHT * 0.725), 60, 60, '', 'resources/images/minus.png',
                        'resources/images/minus_act.png', 'resources/sounds/button_menu_sound.mp3')

        apfsds_count_txt = Text(round(self.s.WIDTH // 2 * 0.187), round(self.s.HEIGHT * 0.75), (200, 200, 200), str(APFSDS_COUNT), 32)
        apfsds_count_txt_bl = Text(round(self.s.WIDTH // 2 * 0.187) + 4, round(self.s.HEIGHT * 0.75) + 4, (0, 0, 0),
                                   str(APFSDS_COUNT), 32)
        he_count_txt = Text(round(self.s.WIDTH // 2 * 0.457), round(self.s.HEIGHT * 0.75), (200, 200, 200), str(HE_COUNT), 32)
        he_count_txt_bl = Text(round(self.s.WIDTH // 2 * 0.457) + 4, round(self.s.HEIGHT * 0.75) + 4, (0, 0, 0), str(HE_COUNT), 32)
        heat_count_txt = Text(round(self.s.WIDTH // 2 * 0.727), round(self.s.HEIGHT * 0.75), (200, 200, 200), str(HEAT_COUNT), 32)
        heat_count_txt_bl = Text(round(self.s.WIDTH // 2 * 0.727) + 4, round(self.s.HEIGHT * 0.75) + 4, (0, 0, 0), str(HEAT_COUNT),
                                 32)
        max_ammo_text_bl = Text(round(self.s.WIDTH // 2 * 0.457) + 4, round(self.s.HEIGHT * 0.8) + 4, (0, 0, 0), f'0/{str(MAX_AMMO)}',
                                32)
        max_ammo_text = Text(round(self.s.WIDTH // 2 * 0.457), round(self.s.HEIGHT * 0.8), (200, 200, 200), f'0/{str(MAX_AMMO)}', 32)

        back_button = Button(round(self.s.WIDTH // 2 * 0.5) - 323, 900, 645, 100, 'Назад', 'resources/images/button_inact.png',
                             'resources/images/button_active.png',
                             'resources/sounds/button_menu_sound.mp3')
        play_button = Button(round(self.s.WIDTH // 4 * 3) - 323, 900, 645, 100, 'Играть', 'resources/images/button_inact.png',
                             'resources/images/button_active.png',
                             'resources/sounds/button_menu_sound.mp3')
        tank1_button = SelectButton(round(self.s.WIDTH // 2 * 0.060), round(self.s.HEIGHT * 0.23), w=180, h=92, w_r=200, h_r=150,
                                    text='Т-90М', im='resources/images/T-90M_profile.png',
                                    sound='resources/sounds/button_menu_sound.mp3')
        guide_button = SelectButton(round(self.s.WIDTH // 2 * 0.060), round(self.s.HEIGHT * 0.43), w=64, h=100, w_r=200, h_r=150,
                                    text='Обучение', im='resources/images/guide.png',
                                    sound='resources/sounds/button_menu_sound.mp3')

        ammo_descr_list = []
        k = 0.63
        for i in self.s.ammo:
            temp = Text(round(self.s.WIDTH // 2 * 0.9), round(self.s.HEIGHT * k), (200, 200, 200), i, 15, (50, 60, 50),
                        is_topleft=True)
            k += 0.018
            ammo_descr_list.append(temp)

        tank_descr_list = []
        k2 = 0.17
        for i in self.s.T_90M_descr:
            temp = Text(round(self.s.WIDTH // 2 * 0.9), round(self.s.HEIGHT * k2), (200, 200, 200), i, 15, (50, 60, 50),
                        is_topleft=True)
            k2 += 0.0166
            tank_descr_list.append(temp)

        k3 = 0.17
        T_90M_TTH_list = []
        for i in self.s.T_90M_TTH:
            temp = Text(round(self.s.WIDTH // 2 * 1.5), round(self.s.HEIGHT * k3), (200, 200, 200), i, 15, (50, 60, 50),
                        is_topleft=True)
            k3 += 0.0167
            T_90M_TTH_list.append(temp)

        k4 = 0.43
        guide_list = []
        for i in self.s.guide_descr:
            temp = Text(round(self.s.WIDTH // 2 * 0.9), round(self.s.HEIGHT * k4), (200, 200, 200), i, 15, (50, 60, 50),
                        is_topleft=True)
            k4 += 0.0167
            guide_list.append(temp)

        tank_list = [tank1_button]
        lvl_list = [guide_button]

        rect = pygame.Rect(round(self.s.WIDTH // 2 * 0.89), round(self.s.HEIGHT * 0.14), 1100, 730)
        button_list = [back_button, tank1_button, guide_button, play_button, plus1, plus2, plus3, minus1, minus2,
                       minus3]

        fps_count_text_bl = Text(self.s.WIDTH * 0.96 + 2, self.s.HEIGHT * 0.97 + 2, (0, 0, 0),
                                 str(int(self.s.clock.get_fps())) + ' FPS', 20,
                                 is_topleft=True)
        fps_count_text = Text(self.s.WIDTH * 0.96, self.s.HEIGHT * 0.97, (200, 200, 200),
                              str(int(self.s.clock.get_fps())) + ' FPS', 20,
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
                    pygame.quit()
                    sys.exit()

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

                for i in button_list:
                    i.handle_event(event)

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

            pygame.display.flip()
            self.s.clock.tick(self.s.FPS)
