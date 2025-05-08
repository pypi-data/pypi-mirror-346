import pygame
from .ui_element import UIElement


class Container(UIElement):
    """
    Root container for UI elements
    """

    width = 800
    height = 600
    background_color = (0, 0, 0)

    def render(self, surface: pygame.Surface) -> None:
        # Fill background
        if hasattr(self, "background_color") and self.background_color is not None:
            # Fill with RGBA
            if len(self.background_color) == 4:
                temp_surface = pygame.Surface(
                    (self.width, self.height), pygame.SRCALPHA
                )
                temp_surface.fill(self.background_color)
                surface.blit(temp_surface, (0, 0))
            # Fill with RGB
            else:
                surface.fill(self.background_color)

        # Render all children
        for child in self._children:
            child.render(surface)

    def resize(self, width: int, height: int) -> None:
        """Handle window resize."""
        old_width, old_height = self.width, self.height
        self.width = width
        self.height = height

        # Notify all direct children of the resize
        for child in self._children:
            if hasattr(child, "on_parent_resize"):
                child.on_parent_resize(width, height)
