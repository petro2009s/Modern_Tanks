import sys

from settings import *
from buttons import *
import pygame
import random

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Симулятор современного танка')
        pygame.display.set_icon(icon)

    # pygame.mixer.music.load('sounds/button_menu_sound.mp3')

    def start_game(self):
        show = True

        menu_im = menu_list[random.randint(0, 4)]

        play_button = Button(WIDTH // 2 - 323, 450, 645, 100, 'Играть', 'images/button_inact.png',
                             'images/button_active.png',
                             'sounds/button_menu_sound.mp3')

        settings_button = Button(WIDTH // 2 - 323, 600, 645, 100, 'Настройки', 'images/button_inact.png',
                                 'images/button_active.png',
                                 'sounds/button_menu_sound.mp3')

        quit_button = Button(WIDTH // 2 - 323, 750, 645, 100, 'Выйти', 'images/button_inact.png',
                             'images/button_active.png',
                             'sounds/button_menu_sound.mp3')
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

                play_button.handle_event(event)
                settings_button.handle_event(event)
                quit_button.handle_event(event)
               # test_sbutton.handle_event(event)

            display.blit(menu_im, (0, 0))

            play_button.draw(display)
            quit_button.draw(display)
            settings_button.draw(display)

           # test_sbutton.draw(display)

            pygame.display.update()
            clock.tick(60)

    def settings_menu(self):
        show = True

        menu_im = menu_list[random.randint(0, 4)]

        font = pygame.font.Font('fonts/pixel_font.otf', 48)
        text_surface = font.render('Настройки графики', True, (200, 200, 200), (50, 60, 50))
        text_rect = text_surface.get_rect(center=(WIDTH // 2, round(HEIGHT * 0.1)))

        font2 = pygame.font.Font('fonts/pixel_font.otf', 36)
        text_surface2 = font2.render('Разрешение рендера', True, (200, 200, 200), (50, 60, 50))
        text_rect2 = text_surface.get_rect(center=(WIDTH // 2, round(HEIGHT * 0.2)))

        font3 = pygame.font.Font('fonts/pixel_font.otf', 36)
        text_surface3 = font3.render('Дальность прорисовки', True, (200, 200, 200), (50, 60, 50))
        text_rect3 = text_surface.get_rect(center=(WIDTH // 2, round(HEIGHT * 0.4)))

        back_button = Button(WIDTH // 2 - 323, 750, 645, 100, 'Назад', 'images/button_inact.png',
                             'images/button_active.png',
                             'sounds/button_menu_sound.mp3')
        gr_low = SelectButton(510, HEIGHT * 0.23, 300, 150, 'Низкое', sound='sounds/button_menu_sound.mp3')
        gr_mid = SelectButton(810, HEIGHT * 0.23, 300, 150, 'Среднее', sound='sounds/button_menu_sound.mp3')
        gr_high = SelectButton(1110, HEIGHT * 0.23, 300, 150, 'Высокое', sound='sounds/button_menu_sound.mp3')

        d_low = SelectButton(510, HEIGHT * 0.43, 300, 150, 'Низкая', sound='sounds/button_menu_sound.mp3')
        d_mid = SelectButton(810, HEIGHT * 0.43, 300, 150, 'Средняя', sound='sounds/button_menu_sound.mp3')
        d_high = SelectButton(1110, HEIGHT * 0.43, 300, 150, 'Высокая', sound='sounds/button_menu_sound.mp3')
        while show:

            back_button.check(pygame.mouse.get_pos())

            gr_list = [gr_low, gr_mid, gr_high]
            for i in range(3):
                gr_list[i].is_cl = graph_dict[i]

            gr_low.check(pygame.mouse.get_pos())
            gr_mid.check(pygame.mouse.get_pos())
            gr_high.check(pygame.mouse.get_pos())

            d_list = [d_low, d_mid, d_high]
            for i in range(3):
                d_list[i].is_cl = d_dict[i]

            d_low.check(pygame.mouse.get_pos())
            d_mid.check(pygame.mouse.get_pos())
            d_high.check(pygame.mouse.get_pos())

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.USEREVENT:
                    if event.button == back_button:
                        show = False

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

                back_button.handle_event(event)
                gr_high.handle_event(event)
                gr_mid.handle_event(event)
                gr_low.handle_event(event)

                d_high.handle_event(event)
                d_mid.handle_event(event)
                d_low.handle_event(event)

            display.blit(menu_im, (0, 0))

            back_button.draw(display)
            gr_high.draw(display)
            gr_low.draw(display)
            gr_mid.draw(display)
            d_high.draw(display)
            d_low.draw(display)
            d_mid.draw(display)

            display.blit(text_surface, text_rect)
            display.blit(text_surface2, text_rect2)
            display.blit(text_surface3, text_rect3)

            pygame.display.update()

            clock.tick(60)


