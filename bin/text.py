import pygame


class Text:
    def __init__(self, x, y, color, text, size, bg_color=None, is_topleft=False):
        font = pygame.font.Font('resources/fonts/pixel_font.otf', size)
        self.text_surface = font.render(text, True, color, bg_color)
        if is_topleft:
            self.text_rect = self.text_surface.get_rect(topleft=(x, y))
        else:
            self.text_rect = self.text_surface.get_rect(center=(x, y))

    def draw(self, screen):
        screen.blit(self.text_surface, self.text_rect)