import pygame


class Button:
    def __init__(self, x, y, w, h, text, size_text, im_inact=None, im_act=None, sound=None):
        # координаты
        self.x = x
        self.y = y
        # ширина и высота
        self.width = w
        self.height = h
        # картинки
        if im_inact:
            self.im_inact = pygame.image.load(im_inact).convert_alpha()
            self.im_inact = pygame.transform.scale(self.im_inact, (w, h)).convert_alpha()
        if im_act:
            self.im_act = pygame.image.load(im_act).convert_alpha()
            self.im_act = pygame.transform.scale(self.im_act, (w, h)).convert_alpha()
        self.rect = self.im_inact.get_rect(topleft=(x, y))
        # звук
        if sound:
            self.sound = pygame.mixer.Sound(sound)
        # наведение на кнопку
        self.is_hov = False
        # текст
        self.text = text
        self.size_text = size_text
        font = pygame.font.Font('resources/fonts/pixel_font.otf', self.size_text)
        self.text_surface = font.render(self.text, True, (200, 200, 200))
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
        font2 = pygame.font.Font('resources/fonts/pixel_font.otf', self.size_text)
        self.text_surface2 = font2.render(self.text, True, (0, 0, 0))
        self.text_rect2 = self.text_surface2.get_rect(
            center=(self.rect.center[0] + self.size_text * 0.11, self.rect.center[1] + self.size_text * 0.11))

    # отображение кнопки
    def draw(self, screen):
        # нынешняя картинка
        current_im = self.im_act if self.is_hov else self.im_inact
        # отображение картинки
        screen.blit(current_im, (self.x, self.y))
        # отображение текста
        screen.blit(self.text_surface2, self.text_rect2)
        screen.blit(self.text_surface, self.text_rect)

    # проверка на наведение
    def check(self, mouse_pos):
        self.is_hov = self.rect.collidepoint(mouse_pos)

    # проверка на нажатие
    def handle_event(self, event, volume):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hov:
            if self.sound:
                self.sound.set_volume(volume / 100)
                self.sound.play()
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))


class SelectButton:
    def __init__(self, x, y, w_r, h_r, text, w=None, h=None, sound=None, im=None, font_size=None):
        # координаты
        self.x = x
        self.y = y
        # ширина и высота
        self.width = w_r
        self.height = h_r
        self.width_r = w_r
        self.height_r = h_r
        # картинки и прямоугольник кнопки
        self.border = self.width_r // 20
        self.rect = pygame.Rect(self.x, self.y, self.width_r, self.height_r)
        self.im = None
        if im:
            self.im = pygame.image.load(im).convert_alpha()
            self.im = pygame.transform.scale(self.im, (w, h)).convert_alpha()
            self.width = w
            self.height = h
        # звук
        self.sound = None
        if sound:
            self.sound = pygame.mixer.Sound(sound)
        # наведение и нажатие на кнопку
        self.is_hov = False
        self.is_cl = False
        # текст
        self.text = text
        self.font_size = font_size
        font = pygame.font.Font('resources/fonts/pixel_font.otf', self.font_size)
        self.text_surface = font.render(self.text, True, (200, 200, 200))
        font2 = pygame.font.Font('resources/fonts/pixel_font.otf', self.font_size)
        self.text_surface2 = font2.render(self.text, True, (0, 0, 0))
        self.text_rect = self.text_surface.get_rect(
            center=(self.width_r // 2 + self.x, self.y + self.height_r // 2 + (self.height_r - self.height) * 0.6))
        self.text_rect2 = self.text_surface.get_rect(
            center=(self.width_r // 2 + self.x + self.font_size * 0.11,
                    self.y + self.font_size * 0.11 + self.height_r // 2 + (self.height_r - self.height) * 0.6))

    # отображение кнопки
    def draw(self, screen):
        # проверка на нажатие и наведение
        if self.is_hov or self.is_cl:
            pygame.draw.rect(screen, (50, 60, 50), self.rect)
        else:
            pygame.draw.rect(screen, (50, 60, 50), self.rect, int(self.border))
        # отображение картинки
        if self.im:
            screen.blit(self.im, (self.x + (self.width_r - self.width) // 2, self.y))
        # отображение текста
        screen.blit(self.text_surface2, self.text_rect2)
        screen.blit(self.text_surface, self.text_rect)

    # проверка на наведение
    def check(self, mouse_pos):
        self.is_hov = self.rect.collidepoint(mouse_pos)

    # проверка на нажатие
    def handle_event(self, event, volume=None):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hov:
            if self.sound:
                self.sound.set_volume(volume / 100)
                self.sound.play()
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))
            if self.is_cl:
                self.is_cl = False
            else:
                self.is_cl = True
