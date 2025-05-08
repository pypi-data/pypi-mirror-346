import pygame
from abc import ABC, abstractmethod

from .ui_element import UIElement


class Widget(UIElement, ABC):
    """Abstract base class for all widgets."""

    def __init__(self):
        super().__init__()
        self._create_pygame_element()

    @abstractmethod
    def _create_pygame_element(self):
        """Create the pygame widget element. Must be implemented by subclasses."""
        pass


class Button(Widget):
    """Simple button widget."""

    text = "Button"
    width = 150
    height = 50
    color = (100, 100, 200)
    hover_color = (120, 120, 230)
    active_color = (140, 140, 255)
    font_size = 28

    def __init__(self):
        super().__init__()
        self.hover = False
        self.active = False
        self._create_pygame_element()

    def _create_pygame_element(self):
        """Create the pygame button element."""

        # Create a button class
        class ButtonElement:
            def __init__(self, parent):
                self.parent = parent
                self.rect = pygame.Rect(0, 0, parent.width, parent.height)
                self.font = pygame.font.Font(None, parent.font_size)

            def render(self, surface):
                # Determine color based on state
                if self.parent.active:
                    color = self.parent.active_color
                elif self.parent.hover:
                    color = self.parent.hover_color
                else:
                    color = self.parent.color

                # Get absolute position
                abs_x, abs_y = self.parent.absolute_position
                self.rect.topleft = (abs_x, abs_y)

                # Draw button with rounded corners
                pygame.draw.rect(surface, color, self.rect, border_radius=5)
                pygame.draw.rect(
                    surface, (255, 255, 255), self.rect, 2, border_radius=5
                )
                # Draw text
                text_surf = self.font.render(self.parent.text, True, (255, 255, 255))
                text_rect = text_surf.get_rect(center=self.rect.center)
                surface.blit(text_surf, text_rect)

            def handle_event(self, event):
                if event.type == pygame.MOUSEMOTION:
                    self.parent.hover = self.rect.collidepoint(event.pos)
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.rect.collidepoint(event.pos):
                        self.parent.active = True
                        print(f"Button clicked: {self.parent.text}")
                        return True
                return False

        # Create and attach the element
        self.set_pygame_element(ButtonElement(self))


class Label(Widget):
    """Simple text label widget."""

    text = "Label"
    font_size = 24
    color = (255, 255, 255)

    def __init__(self):
        super().__init__()
        self._create_pygame_element()

    def _create_pygame_element(self):
        """Create the pygame label element."""

        class LabelElement:
            def __init__(self, parent):
                self.parent = parent
                self.font = pygame.font.Font(None, parent.font_size)
                self.surface = self.font.render(parent.text, True, parent.color)
                self.rect = self.surface.get_rect()

                # Update parent dimensions based on text size
                parent.width = self.surface.get_width()
                parent.height = self.surface.get_height()

            def render(self, surface):
                abs_x, abs_y = self.parent.absolute_position
                self.rect.topleft = (abs_x, abs_y)
                surface.blit(self.surface, self.rect)

            def handle_event(self, event):
                return False

        # Create and attach the element
        self.set_pygame_element(LabelElement(self))
