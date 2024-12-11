import sys

from bin.buttons import *
import pygame
import random
from bin.text import Text


class Game:
    def __init__(self):

        pygame.init()
        pygame.display.set_caption('Симулятор современного танка')
        pygame.display.set_icon(icon)
        print(FPS)

    # pygame.mixer.music.load('sounds/button_menu_sound.mp3')

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
        # test_sbutton = SelectButton(0, 0, w=180, h=92, w_r=200, h_r=180, text='Т-90М', im='images/T-90M_profile.png', sound='sounds/button_menu_sound.mp3')
        while show:

            quit_button.check(pygame.mouse.get_pos())
            settings_button.check(pygame.mouse.get_pos())
            play_button.check(pygame.mouse.get_pos())
            # test_sbutton.check(pygame.mouse.get_pos())

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
            # test_sbutton.handle_event(event)

            display.blit(menu_im, (0, 0))

            play_button.draw(display)
            quit_button.draw(display)
            settings_button.draw(display)

            header_bl.draw(display)
            header.draw(display)
            # test_sbutton.draw(display)

            pygame.display.update()
            clock.tick(FPS)

    def settings_menu(self):
        global FPS
        sett = True
        print(FPS)
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
        while sett:

            back_button.check(pygame.mouse.get_pos())

            for i in range(3):
                gr_list[i].is_cl = graph_dict[i]

            gr_low.check(pygame.mouse.get_pos())
            gr_mid.check(pygame.mouse.get_pos())
            gr_high.check(pygame.mouse.get_pos())

            for i in range(3):
                d_list[i].is_cl = d_dict[i]

            d_low.check(pygame.mouse.get_pos())
            d_mid.check(pygame.mouse.get_pos())
            d_high.check(pygame.mouse.get_pos())

            for i in range(3):
                fps_list[i].is_cl = fps_dict[i]

            fps_low.check(pygame.mouse.get_pos())
            fps_mid.check(pygame.mouse.get_pos())
            fps_high.check(pygame.mouse.get_pos())

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
                gr_high.handle_event(event)
                gr_mid.handle_event(event)
                gr_low.handle_event(event)

                d_high.handle_event(event)
                d_mid.handle_event(event)
                d_low.handle_event(event)

                fps_high.handle_event(event)
                fps_mid.handle_event(event)
                fps_low.handle_event(event)

            display.blit(menu_im, (0, 0))

            back_button.draw(display)
            gr_high.draw(display)
            gr_low.draw(display)
            gr_mid.draw(display)
            d_high.draw(display)
            d_low.draw(display)
            d_mid.draw(display)
            fps_high.draw(display)
            fps_low.draw(display)
            fps_mid.draw(display)

            gr_text_bl.draw(display)
            gr_text.draw(display)
            d_text_bl.draw(display)
            d_text.draw(display)
            fps_text_bl.draw(display)
            fps_text.draw(display)
            header_bl.draw(display)
            header.draw(display)

            pygame.display.update()

            clock.tick(FPS)

    def game_menu(self):
        global FPS
        gm = True
        print(FPS)
        menu_im = menu_list[random.randint(0, 4)]

        header_bl = Text(WIDTH // 2 + 4, round(HEIGHT * 0.05) + 4, (0, 0, 0), 'Игра', 60)
        header = Text(WIDTH // 2, round(HEIGHT * 0.05), (200, 200, 200), 'Игра', 60)

        t_bl = Text(round(WIDTH // 2 * 0.06) + 4, round(HEIGHT * 0.14) + 4, (0, 0, 0), 'Выбор техники', 48, is_topleft=True)
        t = Text(round(WIDTH // 2 * 0.06), round(HEIGHT * 0.14), (200, 200, 200), 'Выбор техники', 48, is_topleft=True)

        lvl_bl = Text(round(WIDTH // 2 * 0.06) + 4, round(HEIGHT * 0.37) + 4, (0, 0, 0), 'Выбор уровня', 48, is_topleft=True)
        lvl = Text(round(WIDTH // 2 * 0.06), round(HEIGHT * 0.37), (200, 200, 200), 'Выбор уровня', 48, is_topleft=True)

        am_bl = Text(round(WIDTH // 2 * 0.06) + 4, round(HEIGHT * 0.57) + 4, (0, 0, 0), 'Выбор боеприпасов', 48,
                      is_topleft=True)
        am = Text(round(WIDTH // 2 * 0.06), round(HEIGHT * 0.57), (200, 200, 200), 'Выбор боеприпасов', 48, is_topleft=True)
        am_d = Text(round(WIDTH // 2 * 0.89) + 500, round(HEIGHT * 0.633), (200, 200, 200), 'Описание боеприпасов', 17)
        tank_descr = Text(round(WIDTH // 2 * 0.89) + 300, round(HEIGHT * 0.15), (200, 200, 200), 'Описание техники', 17)
        tank_tth = Text(round(WIDTH // 2 * 1.75), round(HEIGHT * 0.15), (200, 200, 200), 'ТТХ техники', 17)
        lvl_descr = Text(round(WIDTH // 2 * 0.89) + 300, round(HEIGHT * 0.4), (200, 200, 200), 'Описание уровня', 17)


        back_button = Button(round(WIDTH // 2 * 0.5) - 323, 900, 645, 100, 'Назад', 'resources/images/button_inact.png',
                             'resources/images/button_active.png',
                             'resources/sounds/button_menu_sound.mp3')
        play_button = Button(round(WIDTH // 4 * 3) - 323, 900, 645, 100, 'Играть', 'resources/images/button_inact.png',
                             'resources/images/button_active.png',
                             'resources/sounds/button_menu_sound.mp3')
        tank1_button = SelectButton(round(WIDTH // 2 * 0.060), round(HEIGHT * 0.23), w=180, h=92, w_r=200, h_r=150,
                                    text='Т-90М', im='resources/images/T-90M_profile.png', sound='resources/sounds/button_menu_sound.mp3')
        guide_button = SelectButton(round(WIDTH // 2 * 0.060), round(HEIGHT * 0.43), w=64, h=100, w_r=200, h_r=150,
                                    text='Обучение', im='resources/images/guide.png', sound='resources/sounds/button_menu_sound.mp3')
        ammo_descr_list = []
        k = 0.63
        rect = pygame.Rect(round(WIDTH // 2 * 0.89), round(HEIGHT * 0.14), 1100, 730)
        for i in ammo:
            temp = Text(round(WIDTH // 2 * 0.9), round(HEIGHT * k), (200, 200, 200), i, 15, (50, 60, 50), is_topleft=True)
            k += 0.018
            ammo_descr_list.append(temp)
        tank_descr_list = []
        k2 = 0.17
        k3 = 0.17
        T_90M_TTH_list = []
        for i in T_90M_descr:
            temp = Text(round(WIDTH // 2 * 0.9), round(HEIGHT * k2), (200, 200, 200), i, 15, (50, 60, 50), is_topleft=True)
            k2 += 0.0166
            tank_descr_list.append(temp)
        for i in T_90M_TTH:
            temp = Text(round(WIDTH // 2 * 1.5), round(HEIGHT * k3), (200, 200, 200), i, 15, (50, 60, 50), is_topleft=True)
            k3 += 0.0167
            T_90M_TTH_list.append(temp)
        tank_list = [tank1_button]
        lvl_list = [guide_button]
        while gm:
            for i in range(len(tank_list)):
                tank_list[i].is_cl = tank_dict[i]
            for i in range(len(lvl_list)):
                lvl_list[i].is_cl = lvl_dict[i]

            back_button.check(pygame.mouse.get_pos())
            tank1_button.check(pygame.mouse.get_pos())
            guide_button.check(pygame.mouse.get_pos())
            play_button.check(pygame.mouse.get_pos())

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.USEREVENT:
                    if event.button == back_button:
                        gm = False

                back_button.handle_event(event)
                tank1_button.handle_event(event)
                guide_button.handle_event(event)
                play_button.handle_event(event)

            display.blit(menu_im, (0, 0))

            back_button.draw(display)
            tank1_button.draw(display)
            guide_button.draw(display)
            play_button.draw(display)

            header_bl.draw(display)
            header.draw(display)
            t_bl.draw(display)
            t.draw(display)
            lvl_bl.draw(display)
            lvl.draw(display)
            am_bl.draw(display)
            am.draw(display)
            pygame.draw.rect(display, (50, 60, 50), rect)
            for i in ammo_descr_list:
                i.draw(display)
            for i in tank_descr_list:
                i.draw(display)
            for i in T_90M_TTH_list:
                i.draw(display)
            am_d.draw(display)
            tank_descr.draw(display)
            tank_tth.draw(display)
            lvl_descr.draw(display)
            pygame.display.update()
            clock.tick(FPS)
