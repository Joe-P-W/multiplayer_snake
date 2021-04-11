import pygame
import abc

COLOUR_INACTIVE = (255, 100, 0)
COLOUR_ACTIVE = (255, 0, 0)


class Box(abc.ABC):
    @abc.abstractmethod
    def handle_event(self, event):
        pass

    @abc.abstractmethod
    def draw(self, screen):
        pass


class ButtonBox(Box):
    def __init__(
            self, x, y, width, height, text, font, box_colour, text_colour, click_event, args=tuple(), kwargs=None
    ):
        if kwargs is None:
            kwargs = {}

        self.args = args
        self.kwargs = kwargs
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.box_colour = box_colour
        self.click_event = click_event
        self.text = self.font.render(text, False, text_colour)
        self.text_rect = self.text.get_rect(center=self.rect.center)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.click_event(*(arg() if callable(arg) else arg for arg in self.args), **self.kwargs)

    def draw(self, screen):
        pygame.draw.rect(screen, self.box_colour, self.rect)
        screen.blit(self.text, self.text_rect)


class InputBox:
    def __init__(self, x, y, width, height, font, title, text=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.title_text = title
        self.colour = COLOUR_INACTIVE
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
            self.colour = COLOUR_ACTIVE if self.active else COLOUR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, self.colour)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        screen.blit(self.title_surface, (self.rect.x, self.rect.y - 35))
        # Blit the rect.
        pygame.draw.rect(screen, self.colour, self.rect, 2)
