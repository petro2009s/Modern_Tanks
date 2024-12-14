import sys

from bin.buttons import *
import pygame
import random
from bin.text import Text


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('World of Modern Tanks')
        pygame.display.set_icon(icon)

    def start_game(self):
        show = True

        menu_im = menu_list[random.randint(0, 4)]

        header_bl = Text(WIDTH // 2 + 4, round(HEIGHT * 0.1) + 4, (0, 0, 0), 'World of Modern Tanks', 70)
        header = Text(WIDTH // 2, round(HEIGHT * 0.1), (200, 200, 200), 'World of Modern Tanks', 70)

        play_button = Button(WIDTH // 2 - 323, 450, 645, 100, 'Играть', 'resources/images/button_inact.png',
                             'resources/images/button_active.png',
                             'resources/sounds/button_menu_sound.mp3')

        settings_button = Button(WIDTH // 2 - 323, 600, 645, 100, 'Настройки', 'resources/images/button_inact.png',
                                 'resources/images/button_active.png',
                                 'resources/sounds/button_menu_sound.mp3')

        quit_button = Button(WIDTH // 2 - 323, 750, 645, 100, 'Выйти', 'resources/images/button_inact.png',
                             'resources/images/button_active.png',
                             'resources/sounds/button_menu_sound.mp3')
        fps_count_text = Text(WIDTH * 0.96, HEIGHT * 0.97, (0, 0, 0), str(int(clock.get_fps())) + ' FPS', 20,
                              is_topleft=True)
        while show:
            quit_button.check(pygame.mouse.get_pos())
            settings_button.check(pygame.mouse.get_pos())
            play_button.check(pygame.mouse.get_pos())
            # fps_count_text.create_text(str(int(clock.get_fps())))

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

            display.blit(menu_im, (0, 0))

            play_button.draw(display)
            quit_button.draw(display)
            settings_button.draw(display)

            header_bl.draw(display)
            header.draw(display)

            fps_count_text.draw_fps(display, int(clock.get_fps()))
            # fps_count_text.set_another_text(str(int(clock.get_fps())) + ' FPS')
            # fps_count_text.draw(display)
            pygame.display.flip()
            clock.tick(FPS)

    def settings_menu(self):
        global FPS
        sett = True
        menu_im = menu_list[random.randint(0, 4)]

        header_bl = Text(WIDTH // 2 + 4, round(HEIGHT * 0.1) + 4, (0, 0, 0), 'Настройки графики', 60)
        header = Text(WIDTH // 2, round(HEIGHT * 0.1), (200, 200, 200), 'Настройки графики', 60)

        gr_text_bl = Text(WIDTH // 2 + 4, round(HEIGHT * 0.2) + 4, (0, 0, 0), 'Разрешение рендера', 48)
        gr_text = Text(WIDTH // 2, round(HEIGHT * 0.2), (200, 200, 200), 'Разрешение рендера', 48)

        d_text_bl = Text(WIDTH // 2 + 4, round(HEIGHT * 0.4) + 4, (0, 0, 0), 'Дальность прорисовки', 48)
        d_text = Text(WIDTH // 2, round(HEIGHT * 0.4), (200, 200, 200), 'Дальность прорисовки', 48)

        fps_text_bl = Text(WIDTH // 2 + 4, round(HEIGHT * 0.6) + 4, (0, 0, 0), 'Частота кадров', 48)
        fps_text = Text(WIDTH // 2, round(HEIGHT * 0.6), (200, 200, 200), 'Частота кадров', 48)

        back_button = Button(WIDTH // 2 - 323, 850, 645, 100, 'Назад', 'resources/images/button_inact.png',
                             'resources/images/button_active.png',
                             'resources/sounds/button_menu_sound.mp3')
        gr_low = SelectButton(510, HEIGHT * 0.23, 300, 150, 'Низкое', sound='resources/sounds/button_menu_sound.mp3')
        gr_mid = SelectButton(810, HEIGHT * 0.23, 300, 150, 'Среднее', sound='resources/sounds/button_menu_sound.mp3')
        gr_high = SelectButton(1110, HEIGHT * 0.23, 300, 150, 'Высокое', sound='resources/sounds/button_menu_sound.mp3')

        d_low = SelectButton(510, HEIGHT * 0.43, 300, 150, 'Низкая', sound='resources/sounds/button_menu_sound.mp3')
        d_mid = SelectButton(810, HEIGHT * 0.43, 300, 150, 'Средняя', sound='resources/sounds/button_menu_sound.mp3')
        d_high = SelectButton(1110, HEIGHT * 0.43, 300, 150, 'Высокая', sound='resources/sounds/button_menu_sound.mp3')

        fps_low = SelectButton(510, HEIGHT * 0.63, 300, 150, '30', sound='resources/sounds/button_menu_sound.mp3')
        fps_mid = SelectButton(810, HEIGHT * 0.63, 300, 150, '60', sound='resources/sounds/button_menu_sound.mp3')
        fps_high = SelectButton(1110, HEIGHT * 0.63, 300, 150, '90', sound='resources/sounds/button_menu_sound.mp3')

        gr_list = [gr_low, gr_mid, gr_high]
        d_list = [d_low, d_mid, d_high]
        fps_list = [fps_low, fps_mid, fps_high]

        fps_count_text = Text(WIDTH * 0.96, HEIGHT * 0.97, (0, 0, 0), str(int(clock.get_fps())) + ' FPS', 20,
                              is_topleft=True)

        all_list = [back_button, gr_high, gr_low, gr_mid, d_high, d_low, d_mid, fps_high, fps_low, fps_mid, gr_text_bl,
                    gr_text, d_text_bl, d_text, fps_text_bl, fps_text, header_bl, header, fps_count_text]
        while sett:
            back_button.check(pygame.mouse.get_pos())

            for i in range(3):
                gr_list[i].is_cl = graph_dict[i]

            for i in gr_list:
                i.check(pygame.mouse.get_pos())

            for i in range(3):
                d_list[i].is_cl = d_dict[i]

            for i in d_list:
                i.check(pygame.mouse.get_pos())

            for i in range(3):
                fps_list[i].is_cl = fps_dict[i]

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
                        graph_dict[1] = False
                        graph_dict[0] = False
                        graph_dict[2] = True

                    if event.button == gr_low:
                        graph_dict[1] = False
                        graph_dict[2] = False
                        graph_dict[0] = True

                    if event.button == gr_mid:
                        graph_dict[0] = False
                        graph_dict[2] = False
                        graph_dict[1] = True

                    if event.button == d_high:
                        d_dict[1] = False
                        d_dict[0] = False
                        d_dict[2] = True

                    if event.button == d_low:
                        d_dict[1] = False
                        d_dict[2] = False
                        d_dict[0] = True

                    if event.button == d_mid:
                        d_dict[0] = False
                        d_dict[2] = False
                        d_dict[1] = True

                    if event.button == fps_high:
                        fps_dict[1] = False
                        fps_dict[0] = False
                        fps_dict[2] = True
                        FPS = 90

                    if event.button == fps_low:
                        fps_dict[1] = False
                        fps_dict[2] = False
                        fps_dict[0] = True
                        FPS = 30

                    if event.button == fps_mid:
                        fps_dict[0] = False
                        fps_dict[2] = False
                        fps_dict[1] = True
                        FPS = 60

                back_button.handle_event(event)
                for i in gr_list:
                    i.handle_event(event)

                for i in d_list:
                    i.handle_event(event)

                for i in fps_list:
                    i.handle_event(event)

            display.blit(menu_im, (0, 0))

            fps_count_text.set_another_text(str(int(clock.get_fps())) + ' FPS')

            for i in all_list:
                i.draw(display)

            pygame.display.flip()
            clock.tick(FPS)

    def game_menu(self):
        global FPS
        gm = True

        APFSDS_COUNT = 0
        HE_COUNT = 0
        HEAT_COUNT = 0
        MAX_AMMO = 22
        CURRENT_AMMO = 0
        AMMO = 22

        menu_im = menu_list[random.randint(0, 4)]

        header_bl = Text(WIDTH // 2 + 4, round(HEIGHT * 0.05) + 4, (0, 0, 0), 'Игра', 60)
        header = Text(WIDTH // 2, round(HEIGHT * 0.05), (200, 200, 200), 'Игра', 60)

        t_bl = Text(round(WIDTH // 2 * 0.06) + 4, round(HEIGHT * 0.14) + 4, (0, 0, 0), 'Выбор техники', 48,
                    is_topleft=True)
        t = Text(round(WIDTH // 2 * 0.06), round(HEIGHT * 0.14), (200, 200, 200), 'Выбор техники', 48, is_topleft=True)

        lvl_bl = Text(round(WIDTH // 2 * 0.06) + 4, round(HEIGHT * 0.37) + 4, (0, 0, 0), 'Выбор уровня', 48,
                      is_topleft=True)
        lvl = Text(round(WIDTH // 2 * 0.06), round(HEIGHT * 0.37), (200, 200, 200), 'Выбор уровня', 48, is_topleft=True)

        am_bl = Text(round(WIDTH // 2 * 0.06) + 4, round(HEIGHT * 0.57) + 4, (0, 0, 0), 'Выбор боеприпасов', 48,
                     is_topleft=True)
        am = Text(round(WIDTH // 2 * 0.06), round(HEIGHT * 0.57), (200, 200, 200), 'Выбор боеприпасов', 48,
                  is_topleft=True)

        am_d = Text(round(WIDTH // 2 * 0.89) + 500, round(HEIGHT * 0.633), (200, 200, 200), 'Описание боеприпасов', 17)
        tank_descr = Text(round(WIDTH // 2 * 0.89) + 300, round(HEIGHT * 0.15), (200, 200, 200), 'Описание техники', 17)
        tank_tth = Text(round(WIDTH // 2 * 1.75), round(HEIGHT * 0.15), (200, 200, 200), 'ТТХ техники', 17)
        lvl_descr = Text(round(WIDTH // 2 * 0.89) + 300, round(HEIGHT * 0.4), (200, 200, 200), 'Описание уровня', 17)

        apfsds_txt = SelectButton(round(WIDTH // 2 * 0.1), round(HEIGHT * 0.63), w=160, h=45, w_r=176, h_r=80,
                                  text='БОПС', im='resources/images/apfsds.png', font_size=30)
        he_txt = SelectButton(round(WIDTH // 2 * 0.37), round(HEIGHT * 0.63), w=160, h=45, w_r=176, h_r=80,
                              text='ОФС', im='resources/images/he.png', font_size=30)
        heat_txt = SelectButton(round(WIDTH // 2 * 0.64), round(HEIGHT * 0.63), w=160, h=45, w_r=176, h_r=80,
                                text='КС', im='resources/images/heat.png', font_size=30)

        plus1 = Button(round(WIDTH // 2 * 0.07), round(HEIGHT * 0.725), 60, 60, '', 'resources/images/plus.png',
                       'resources/images/plus_act.png', 'resources/sounds/button_menu_sound.mp3')
        plus2 = Button(round(WIDTH // 2 * 0.34), round(HEIGHT * 0.725), 60, 60, '', 'resources/images/plus.png',
                       'resources/images/plus_act.png', 'resources/sounds/button_menu_sound.mp3')
        plus3 = Button(round(WIDTH // 2 * 0.61), round(HEIGHT * 0.725), 60, 60, '', 'resources/images/plus.png',
                       'resources/images/plus_act.png', 'resources/sounds/button_menu_sound.mp3')
        minus1 = Button(round(WIDTH // 2 * 0.25), round(HEIGHT * 0.725), 60, 60, '', 'resources/images/minus.png',
                        'resources/images/minus_act.png', 'resources/sounds/button_menu_sound.mp3')
        minus2 = Button(round(WIDTH // 2 * 0.52), round(HEIGHT * 0.725), 60, 60, '', 'resources/images/minus.png',
                        'resources/images/minus_act.png', 'resources/sounds/button_menu_sound.mp3')
        minus3 = Button(round(WIDTH // 2 * 0.79), round(HEIGHT * 0.725), 60, 60, '', 'resources/images/minus.png',
                        'resources/images/minus_act.png', 'resources/sounds/button_menu_sound.mp3')

        apfsds_count_txt = Text(round(WIDTH // 2 * 0.187), round(HEIGHT * 0.75), (200, 200, 200), str(APFSDS_COUNT), 32)
        apfsds_count_txt_bl = Text(round(WIDTH // 2 * 0.187) + 4, round(HEIGHT * 0.75) + 4, (0, 0, 0),
                                   str(APFSDS_COUNT), 32)
        he_count_txt = Text(round(WIDTH // 2 * 0.457), round(HEIGHT * 0.75), (200, 200, 200), str(HE_COUNT), 32)
        he_count_txt_bl = Text(round(WIDTH // 2 * 0.457) + 4, round(HEIGHT * 0.75) + 4, (0, 0, 0), str(HE_COUNT), 32)
        heat_count_txt = Text(round(WIDTH // 2 * 0.727), round(HEIGHT * 0.75), (200, 200, 200), str(HEAT_COUNT), 32)
        heat_count_txt_bl = Text(round(WIDTH // 2 * 0.727) + 4, round(HEIGHT * 0.75) + 4, (0, 0, 0), str(HEAT_COUNT),
                                 32)
        max_ammo_text_bl = Text(round(WIDTH // 2 * 0.457) + 4, round(HEIGHT * 0.8) + 4, (0, 0, 0), f'0/{str(MAX_AMMO)}',
                                32)
        max_ammo_text = Text(round(WIDTH // 2 * 0.457), round(HEIGHT * 0.8), (200, 200, 200), f'0/{str(MAX_AMMO)}', 32)

        back_button = Button(round(WIDTH // 2 * 0.5) - 323, 900, 645, 100, 'Назад', 'resources/images/button_inact.png',
                             'resources/images/button_active.png',
                             'resources/sounds/button_menu_sound.mp3')
        play_button = Button(round(WIDTH // 4 * 3) - 323, 900, 645, 100, 'Играть', 'resources/images/button_inact.png',
                             'resources/images/button_active.png',
                             'resources/sounds/button_menu_sound.mp3')
        tank1_button = SelectButton(round(WIDTH // 2 * 0.060), round(HEIGHT * 0.23), w=180, h=92, w_r=200, h_r=150,
                                    text='Т-90М', im='resources/images/T-90M_profile.png',
                                    sound='resources/sounds/button_menu_sound.mp3')
        guide_button = SelectButton(round(WIDTH // 2 * 0.060), round(HEIGHT * 0.43), w=64, h=100, w_r=200, h_r=150,
                                    text='Обучение', im='resources/images/guide.png',
                                    sound='resources/sounds/button_menu_sound.mp3')

        ammo_descr_list = []
        k = 0.63
        for i in ammo:
            temp = Text(round(WIDTH // 2 * 0.9), round(HEIGHT * k), (200, 200, 200), i, 15, (50, 60, 50),
                        is_topleft=True)
            k += 0.018
            ammo_descr_list.append(temp)

        tank_descr_list = []
        k2 = 0.17
        for i in T_90M_descr:
            temp = Text(round(WIDTH // 2 * 0.9), round(HEIGHT * k2), (200, 200, 200), i, 15, (50, 60, 50),
                        is_topleft=True)
            k2 += 0.0166
            tank_descr_list.append(temp)

        k3 = 0.17
        T_90M_TTH_list = []
        for i in T_90M_TTH:
            temp = Text(round(WIDTH // 2 * 1.5), round(HEIGHT * k3), (200, 200, 200), i, 15, (50, 60, 50),
                        is_topleft=True)
            k3 += 0.0167
            T_90M_TTH_list.append(temp)

        k4 = 0.43
        guide_list = []
        for i in guide_descr:
            temp = Text(round(WIDTH // 2 * 0.9), round(HEIGHT * k4), (200, 200, 200), i, 15, (50, 60, 50),
                        is_topleft=True)
            k4 += 0.0167
            guide_list.append(temp)

        tank_list = [tank1_button]
        lvl_list = [guide_button]

        rect = pygame.Rect(round(WIDTH // 2 * 0.89), round(HEIGHT * 0.14), 1100, 730)
        button_list = [back_button, tank1_button, guide_button, play_button, plus1, plus2, plus3, minus1, minus2,
                       minus3]

        fps_count_text = Text(WIDTH * 0.96, HEIGHT * 0.97, (0, 0, 0), str(int(clock.get_fps())) + ' FPS', 20,
                              is_topleft=True)

        text_list = [header_bl, header, t_bl, t, lvl_bl, lvl, am_bl, am, apfsds_txt, heat_txt, he_txt,
                     apfsds_count_txt_bl, fps_count_text,
                     apfsds_count_txt, he_count_txt_bl, he_count_txt, heat_count_txt_bl, heat_count_txt,
                     max_ammo_text_bl, max_ammo_text]

        while gm:

            apfsds_txt.is_cl = True
            he_txt.is_cl = True
            heat_txt.is_cl = True

            fps_count_text.set_another_text(str(int(clock.get_fps())) + ' FPS')

            display.blit(menu_im, (0, 0))
            for i in range(len(tank_list)):
                tank_list[i].is_cl = tank_dict[i]
            for i in range(len(lvl_list)):
                lvl_list[i].is_cl = lvl_dict[i]

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
                        print([i for i, j in tank_dict.items() if j][0])
                        print([i for i, j in lvl_dict.items() if j][0])

                for i in button_list:
                    i.handle_event(event)

            for i in button_list:
                i.draw(display)

            for i in text_list:
                i.draw(display)

            pygame.draw.rect(display, (50, 60, 50), rect)
            for i in ammo_descr_list:
                i.draw(display)
            for i in tank_descr_list:
                i.draw(display)
            for i in T_90M_TTH_list:
                i.draw(display)
            for i in guide_list:
                i.draw(display)
            am_d.draw(display)
            tank_descr.draw(display)
            tank_tth.draw(display)
            lvl_descr.draw(display)

            pygame.display.flip()
            clock.tick(FPS)
