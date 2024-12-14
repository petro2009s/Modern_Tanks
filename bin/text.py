import pygame


class Text:
    def __init__(self, x, y, color, text, size, bg_color=None, is_topleft=False):
        self.font = pygame.font.Font('resources/fonts/pixel_font.otf', size)
        self.color = color
        self.size = size
        self.coord = (x, y)
        self.is_topleft = is_topleft
        self.bg = bg_color

        self.text_surface = self.font.render(text, True, color, bg_color)
        if is_topleft:
            self.text_rect = self.text_surface.get_rect(topleft=(x, y))
        else:
            self.text_rect = self.text_surface.get_rect(center=(x, y))

    def draw(self, screen):
        screen.blit(self.text_surface, self.text_rect)

    def set_another_text(self, new_text):
        self.text_surface = self.font.render(new_text, True, self.color, self.bg)
        if self.is_topleft:
            self.text_rect = self.text_surface.get_rect(topleft=self.coord)
        else:
            self.text_rect = self.text_surface.get_rect(center=self.coord)
