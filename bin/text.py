import pygame


class Text:
    def __init__(self, x, y, color, text, size, bg_color=None, is_topleft=False,
                 font_name='resources/fonts/pixel_font.otf'):
        # параметры текста
        self.font = pygame.font.Font(font_name, size)
        self.is_topleft = is_topleft
        self.size = size
        self.coord = (x, y)
        # цвет
        self.color = color
        self.bg = bg_color
        # текст
        self.text_surface = self.font.render(text, True, color, bg_color)
        if is_topleft:
            self.text_rect = self.text_surface.get_rect(topleft=(x, y))
        else:
            self.text_rect = self.text_surface.get_rect(center=(x, y))

    # отображение текста
    def draw(self, screen):
        screen.blit(self.text_surface, self.text_rect)

    # установка нового текста
    def set_another_text(self, new_text):
        self.text_surface = self.font.render(new_text, True, self.color, self.bg)
        if self.is_topleft:
            self.text_rect = self.text_surface.get_rect(topleft=self.coord)
        else:
            self.text_rect = self.text_surface.get_rect(center=self.coord)
