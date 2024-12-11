from bin.settings import *

class Button:
    def __init__(self, x, y, w, h, text, im_inact, im_act, sound):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.text = text
        self.im_inact = pygame.image.load(im_inact)
        self.im_inact = pygame.transform.scale(self.im_inact, (w, h))
        self.im_act = pygame.image.load(im_act)
        self.im_act = pygame.transform.scale(self.im_act, (w, h))
        self.rect = self.im_inact.get_rect(topleft=(x, y))
        self.sound = pygame.mixer.Sound(sound)
        self.is_hov = False

    def draw(self, screen):
        current_im = self.im_act if self.is_hov else self.im_inact
        screen.blit(current_im, (self.x, self.y))

        font2 = pygame.font.Font('resources/fonts/pixel_font.otf', 36)
        text_surface2 = font2.render(self.text, True, (0, 0, 0))
        text_rect2 = text_surface2.get_rect(center=(self.rect.center[0] + 4, self.rect.center[1] + 4))
        screen.blit(text_surface2, text_rect2)

        font = pygame.font.Font('resources/fonts/pixel_font.otf', 36)
        text_surface = font.render(self.text, True, (200, 200, 200))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check(self, mouse_pos):
        self.is_hov = self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hov:
            self.sound.play()
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))


class SelectButton:
    def __init__(self, x, y, w_r, h_r, text, w=None, h=None, sound=None, im=None):
        self.x = x
        self.y = y
        self.width = w_r
        self.height = h_r
        self.width_r = w_r
        self.height_r = h_r
        self.text = text
        self.im = None
        self.sound = None
        self.border = self.width_r // 20
        self.rect = pygame.Rect(self.x, self.y, self.width_r, self.height_r)
        if im:
            self.im = pygame.image.load(im)
            self.im = pygame.transform.scale(self.im, (w, h))
            self.width = w
            self.height = h
        if sound:
            self.sound = pygame.mixer.Sound(sound)
        self.is_hov = False
        self.is_cl = False

    def draw(self, screen):
        if self.is_hov or self.is_cl:
            pygame.draw.rect(screen, button_color, self.rect)
        else:
            pygame.draw.rect(screen, button_color, self.rect, self.border)

        if self.im:
            screen.blit(self.im, (self.x + (self.width_r - self.width) // 2, self.y))

        font = pygame.font.Font('resources/fonts/pixel_font.otf', 36)
        text_surface = font.render(self.text, True, (200, 200, 200))
        font2 = pygame.font.Font('resources/fonts/pixel_font.otf', 36)
        text_surface2 = font2.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self.width_r // 2 + self.x, self.y + self.height_r // 2 + (self.height_r - self.height) * 0.6))
        text_rect2 = text_surface.get_rect(center=(self.width_r // 2 + self.x + 4, self.y + 4 + self.height_r // 2 + (self.height_r - self.height) * 0.6))
        screen.blit(text_surface2, text_rect2)
        screen.blit(text_surface, text_rect)

    def check(self, mouse_pos):
        self.is_hov = self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hov:
            if self.sound:
                self.sound.play()
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))
            if self.is_cl:
                self.is_cl = False
            else:
                self.is_cl = True

    def __str__(self):
        return self.__class__.__name__