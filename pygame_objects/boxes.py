import pygame
import abc

from pygame.font import Font
from tkinter import Tk


class Box(abc.ABC):
    @abc.abstractmethod
    def handle_event(self, event):
        pass

    @abc.abstractmethod
    def draw(self, screen):
        pass


class ButtonBox(Box):
    def __init__(
            self,
            x: int,
            y: int,
            width: int,
            height: int,
            text: str,
            font: Font,
            box_colour: tuple[int, int, int] = (255, 100, 0),
            text_colour: tuple[int, int, int] = (0, 255, 0),
            event: callable = None,
            args: tuple = tuple(),
            kwargs: dict = None
    ):
        if kwargs is None:
            kwargs = {}

        self.x = x
        self.y = y
        self.args = args
        self.kwargs = kwargs
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.box_colour = box_colour
        self.click_event = event
        self.text = self.font.render(text, False, text_colour)
        self.text_rect = self.text.get_rect(center=self.rect.center)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.click_event is None:
                    raise ValueError(f"Event was not specified in {self.__class__}")

                self.click_event(*(arg() if callable(arg) else arg for arg in self.args), **self.kwargs)

    def draw(self, screen):
        pygame.draw.rect(screen, self.box_colour, self.rect)
        screen.blit(self.text, self.text_rect)


class InputBox(Box):
    def __init__(
            self,
            x: int,
            y: int,
            width: int,
            height: int,
            font: Font,
            title: str,
            text: str = '',
            active_colour: tuple[int, int, int] = (255, 0, 0),
            inactive_colour: tuple[int, int, int] = (255, 100, 0)
    ):
        self.x = x
        self.y = y
        self.init_width = width
        self.rect = pygame.Rect(x, y, width, height)
        self.title_text = title
        self.colour = inactive_colour
        self.inactive_colour = inactive_colour
        self.active_colour = active_colour
        self.text = text
        self.font = font
        self.title_surface = self.font.render(self.title_text, False, self.colour)
        self.txt_surface = self.font.render(text, True, self.colour)
        self.active = False

    def value(self):
        return self.text

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.mod == pygame.KMOD_NONE:
                    if event.key == pygame.K_RETURN:
                        self.active = False
                    elif event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        self.text += event.unicode
                else:
                    if event.mod & pygame.KMOD_CTRL:
                        if event.key == pygame.K_v:
                            self.text += Tk().clipboard_get()

        self.colour = self.active_colour if self.active else self.inactive_colour
        self.txt_surface = self.font.render(self.text, True, self.colour)
        self.update()

    def update(self):
        # Resize the box if the text is too long.
        width = max(self.init_width, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        screen.blit(self.title_surface, (self.rect.x, self.rect.y - 35))
        # Blit the rect.
        pygame.draw.rect(screen, self.colour, self.rect, 2)
