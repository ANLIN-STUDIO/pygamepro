from ctypes import windll
from typing import Union
from win32con import WM_INPUTLANGCHANGEREQUEST
import win32gui
import win32api
import pygame
import os
from pygamepro.parameter import *


class Window:
    def __init__(self,
                 title: str,
                 size: Union[list, tuple],
                 flags: int = 0,
                 depth: int = 0,
                 display: int = 0,
                 vsync: int = 0,
                 bg: Union[list, tuple] = None,
                 ico_path: str = None,
                 Whether_the_window_is_appropriate_or_not: bool = False,
                 window_position: Union[list, tuple] = None):
        if bg is None:
            bg = Black
        pygame.init()
        self.text_show_pos = {}
        self.full_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
        self.bg = bg
        if size is None:
            self.WS = [800, 600]
        else:
            self.WS = size
        if Whether_the_window_is_appropriate_or_not:
            os.environ['SDL_VIDEO_CENTERED'] = '1'
        elif window_position is not None:
            x, y = window_position
            os.environ['SDL_VIDEO_WINDOW_POS'] = '%s,%s' % (x, y)
        self.win_init(title, ico_path)
        self.screen = pygame.display.set_mode(self.WS, flags, depth, display, vsync)
        self.display()

    @staticmethod
    def win_init(title: str,
                 ico_path: str = None):
        pygame.display.set_caption(title)
        if ico_path is not None:
            if os.path.exists(ico_path):
                ico = pygame.image.load(ico_path)
                pygame.display.set_icon(ico)
            else:
                raise Exception('"%s" is not a true path' % ico_path)

    def display(self, *args, if_fill: bool = True):
        if if_fill:
            self.screen.fill(self.bg)
        def show_the_arg(arg_):
            if type(arg_) == list or type(arg_) == tuple:
                for arg in arg_:
                    show_the_arg(arg)
            else:
                try:
                    arg_.show(self.screen)
                except Exception as e:
                    print(e)
                    arg_()

        show_the_arg(args)

        pygame.display.flip()


class Surface:
    def __init__(self,
                 size: Union[list, tuple],
                 mask: Union[list, tuple] = Black):
        self.surface = self.s = pygame.surface.Surface(size, masks=mask)
        self.w = size[0]
        self.h = size[1]
    def display(self, *args, if_fill: Union[list, tuple] = White):
        self.surface.fill(if_fill)

        def show_the_arg(arg_):
            if type(arg_) == list or type(arg_) == tuple:
                for arg in arg_:
                    show_the_arg(arg)
            else:
                try:
                    arg_.show(self.surface)
                except Exception as e:
                    print(e)
                    arg_()

        show_the_arg(args)


class item(object):
    pass


class Font:
    def __init__(self,
                 text: str,
                 color: Union[list, tuple],
                 pos: Union[list, tuple],
                 size: Union[int, float],
                 *args: str,
                 background: Union[list, tuple] = None,
                 id: str = None
                 ):
        self.id = id
        self.word_wrap = False # 自动换行（默认打开）
        self.text = text
        self.pos = pos
        self.color = color
        self.size = size
        if len(args) == 0:
            self.mode = [Center]
        else:
            self.mode = list(args)
        self.background = background

    def show(self,
             screen_toShow: pygame.Surface,
             SysFont: str = 'simhei',
             antialiasing: bool = True):
        font = pygame.font.SysFont(SysFont, self.size)
        if self.background is not None:
            text_surface = font.render(self.text, antialiasing, self.color, self.background)
        else:
            text_surface = font.render(self.text, antialiasing, self.color)
        text_rect = text_surface.get_rect()
        if Left in self.mode:
            text_rect.left = self.pos[0]
        elif Right in self.mode:
            text_rect.right = self.pos[0]
        if Top in self.mode:
            text_rect.top = self.pos[1]
        elif Bottom in self.mode:
            text_rect.bottom = self.pos[1]
        if Center in self.mode:
            text_rect.center = self.pos
        if self.word_wrap:
            if text_rect.x + text_rect.w > screen_toShow.get_width():
                self.pos[0] -= 1
                self.show(screen_toShow, SysFont, antialiasing)
                return True
        screen_toShow.blit(text_surface, text_rect)


class Rect:
    def __init__(self,
                 color: Union[list, tuple],
                 pos: Union[list, tuple],
                 size: Union[list, tuple],
                 outline: int = 0
                 ):
        self.color = color
        self.pos = pos
        self.size = size
        self.outline = outline

    def show(self,
             screen_toShow: pygame.Surface):
        pygame.draw.rect(screen_toShow, self.color, (self.pos[0], self.pos[1], self.size[0], self.size[1]),
                         self.outline)


class Button:
    def __init__(self,
                 text: str,
                 color: Union[list, tuple],
                 pos: Union[list, tuple],
                 size: Union[list, tuple],
                 img: str = None,
                 text_size: int = None,
                 text_color: Union[list, tuple] = None,
                 outline: bool = True,
                 outline_color: Union[list, tuple] = None,
                 follow_text_to_change_size: bool = True
                 ):
        self.clicked = False
        if outline_color is None:
            outline_color = gray81
        self.surface = None
        self.text = text
        self.color = color
        self.color_ = self.color
        self.color_bd = grey41
        self.pos = pos
        self.rect_size = size
        if text_size is None:
            self.text_size = size[1]
        if img is None:
            if self.text_size * len(text) > self.rect_size[0] and follow_text_to_change_size:
                self.rect_size[0] = self.text_size * len(text)
        else:
            self.text_size = self.text_size//2
            self.rect_size[1] = self.rect_size[0]
        if text_color is None:
            color_invert = []
            for each_color in color:
                color_invert.append(255 - each_color)
            self.text_color = color_invert
        else:
            self.text_color = text_color
        self.outline = outline
        self.outline_color = outline_color
        if img is not None:
            self.outline = False
            self.img = Image(img, self.pos, self.rect_size)
        else:
            self.img = None
        self.re_surface()

    def re_surface(self):
        self.surface = pygame.surface.Surface(self.rect_size)
        if self.color_ != Black:
            self.surface.set_colorkey(Black)
        if self.outline or self.color != self.color_:
            self.surface.fill(self.color)
        if self.img is None:
            Font(self.text, self.text_color, [self.rect_size[0] // 2, self.rect_size[1] // 2], self.text_size).show(self.surface)
        if self.outline:
            Rect(self.outline_color, [0, 0], self.rect_size, outline=1).show(self.surface)

    def show(self, screen_toShow: pygame.surface):
        self.screen_toShow = screen_toShow
        self.screen_toShow.blit(self.surface, self.pos)
        if self.img is not None:
            self.img.show(self.screen_toShow)


    def test_mouse_if_in_win(self,
                             mouse_pos: Union[list, tuple]
                             ):
        mp = mouse_pos
        p = self.pos
        s = self.rect_size
        if p[0] < mp[0] < p[0] + s[0] and p[1] < mp[1] < p[1] + s[1]:
            return True
        else:
            return False

    def button_detection(self, do_=None, items=0):
        if do_ is None:
            def do_():
                if self.img is not None:
                    for font in items:
                        if type(font) == Font:
                            if font.id == self:
                                items.remove(font)
                    items.append(Font(self.text, self.text_color, pygame.mouse.get_pos(), self.text_size,
                                      Left, Bottom, background=self.outline_color, id=self))
        if self.test_mouse_if_in_win(pygame.mouse.get_pos()):
            self.color = self.color_bd
            do_()
        else:
            if self.img is not None:
                for font in items:
                    if type(font) == Font:
                        if font.id == self:
                            items.remove(font)
            self.color = self.color_

        self.re_surface()

    def bd(self):
        if self.test_mouse_if_in_win(pygame.mouse.get_pos()):
            self.color = self.color_bd
            self.re_surface()
            return True
        else:
            self.color = self.color_
            self.re_surface()
            return False

    def if_clicked(self, event_=None, do_=None, if_up_return: bool = False):
        if do_ is None:
            def do_(): pass

        def test(event_2):
            if self.test_mouse_if_in_win(pygame.mouse.get_pos()):
                if self.clicked:
                    if event_2.type == pygame.MOUSEBUTTONUP:
                        self.clicked = False
                        do_()
                        return True
                else:
                    if event_2.type == pygame.MOUSEBUTTONDOWN:
                        if if_up_return:
                            self.clicked = True
                        else:
                            do_()
                            return True
            else:
                self.clicked = False

        if event_ is None:
            for event_ in pygame.event.get():
                if test(event_):
                    return True
        else:
            if test(event_):
                return True
        return False


class Image:
    def __init__(self,
                 img: Union[pygame.Surface, str],
                 pos: Union[list, tuple],
                 size: Union[list, tuple] = None,
                 outline_size: Union[list, tuple] = None,
                 outline_color: Union[list, tuple] = None
                 ):
        if type(img) == str:
            self.img = pygame.image.load(img)
        else:
            self.img = img
        self.pos = pos
        if size is not None:
            if size[0] == 0:
                h = size[1]
                w = self.img.get_width() * h / self.img.get_height()
                self.img = pygame.transform.smoothscale(self.img, [w, h])
            elif size[1] == 0:
                w = size[0]
                h = self.img.get_height() * w / self.img.get_width()
                self.img = pygame.transform.smoothscale(self.img, [w, h])
            else:
                self.img = pygame.transform.smoothscale(self.img, size)
        self.outline = [outline_size, outline_color]

    def show(self,
             screen_toShow: pygame.Surface):
        if self.outline[0] is not None and self.outline[1] is not None:
            Rect(self.outline[1], [self.pos[0]-self.outline[0][0], self.pos[1]-self.outline[0][1]], self.outline[0])
        screen_toShow.blit(self.img, self.pos)


class Input_rect(Button):
    def __init__(self,
                 color: Union[list, tuple],
                 pos: Union[list, tuple],
                 size: Union[list, tuple],
                 text: str = '',
                 if_select_color: Union[list, tuple] = None,
                 img: str = None,
                 text_size: int = None,
                 text_color: Union[list, tuple] = None,
                 outline: bool = True,
                 outline_color: Union[list, tuple] = None,
                 follow_text_to_change_size: bool = True
                 ):
        super().__init__(text, color, pos, size, img, text_size, text_color, outline, outline_color, follow_text_to_change_size)
        self.letters = '!@#$%^&*()_-+=*.qwertyuiopasdfghjklzxcvbnm1234567890'
        self.if_select = False
        if if_select_color is None:
            self.if_select_color = [255, 255, 255]
        else:
            self.if_select_color = if_select_color
        self.color_default = color

    def clean(self):
        self.text = ''

    def select(self, event_=None):
        def test(event_2):
            if event_2.type == pygame.MOUSEBUTTONDOWN:
                if self.test_mouse_if_in_win(pygame.mouse.get_pos()):
                    self.if_select = True
                else:
                    self.if_select = False

        if event_ is None:
            for event_ in pygame.event.get():
                if test(event_):
                    return True
        else:
            if test(event_):
                return True
        return False

    def show(self,
             screen_toShow: pygame.Surface):
        if self.if_select:
            self.color = self.if_select_color
        else:
            self.color = self.color_default
        self.re_surface()
        screen_toShow.blit(self.surface, self.pos)

    def bd(self):
        if self.test_mouse_if_in_win(pygame.mouse.get_pos()):
            self.outline_color = grey41
            self.re_surface()
            return True
        else:
            self.outline_color = gray81
            self.re_surface()
            return False

    def typing(self, event_=None):
        def test(event_2):
            if event_2.type == pygame.KEYDOWN:
                key = str(event_2.unicode)
                if key == '\x08':
                    if len(self.text) > 0:
                        self.text = self.text[:-1]
                elif key == '\x1b':
                    self.if_select = False
                elif key == '\r':
                    return True
                elif key.lower() in self.letters:
                    self.text += key
                self.re_surface()
        if self.if_select:
            if event_ is None:
                for event_ in pygame.event.get():
                    if test(event_):
                        return True
            else:
                if test(event_):
                    return True
        else:
            return False


def display(screen: pygame.Surface, *args, if_fill: Union[list, tuple] = White):
    screen.fill(if_fill)

    def show_the_arg(arg_):
        if type(arg_) == list or type(arg_) == tuple:
            for arg in arg_:
                show_the_arg(arg)
        else:
            try:
                arg_.show(screen)
            except Exception as e:
                print(e)
                arg_()

    show_the_arg(args)


def alwaysOnTop(YorN: bool = True):
    hwnd = pygame.display.get_wm_info()["window"]
    windll.user32.SetWindowPos(hwnd, (-2, -1)[YorN], 0, 0, 0, 0, 2 | 1)


def os_quit():
    # noinspection PyProtectedMember
    os._exit(0)


def set_input_method(EC=en):
    hwnd = win32gui.GetForegroundWindow()
    win32gui.GetWindowText(hwnd)
    im_list = win32api.GetKeyboardLayoutList()
    list(map(hex, im_list))
    win32api.SendMessage(hwnd, WM_INPUTLANGCHANGEREQUEST, 0, EC)
