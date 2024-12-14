import pygame


class Text:
    def __init__(self, x, y, color, text, size, bg_color=None, is_topleft=False):
        self.font = pygame.font.Font('resources/fonts/pixel_font.otf', size)
        self.color = color
        self.size = size
        self.coord = (x, y)
        self.is_topleft = is_topleft
        self.bg = bg_color

        self.fps_s = {i: self.font.render(str(i) + ' FPS', True, self.color, self.bg) for i in range(91)}
        self.fps_rect = {i: self.fps_s[i].get_rect(topleft=self.coord) for i in range(91)}

        self.create_text(text)

    def create_text(self, text):
        self.text_surface = self.font.render(text, True, self.color, self.bg)
        if self.is_topleft:
            self.text_rect = self.text_surface.get_rect(topleft=self.coord)
        else:
            self.text_rect = self.text_surface.get_rect(center=self.coord)

    def draw(self, screen):
        screen.blit(self.text_surface, self.text_rect)

    def draw_fps(self, screen, fps):
        screen.blit(self.fps_s[fps], self.fps_rect[fps])

    def set_another_text(self, new_text):
        self.text_surface = self.font.render(new_text, True, self.color, self.bg)
        if self.is_topleft:
            self.text_rect = self.text_surface.get_rect(topleft=self.coord)
        else:
            self.text_rect = self.text_surface.get_rect(center=self.coord)
