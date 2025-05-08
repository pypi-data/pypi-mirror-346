import pygame
from abc import ABC, abstractmethod

from .ui_element import UIElement
from .anchor import Anchor


class Layout(UIElement, ABC):
    """Base layout class."""

    anchor = Anchor.TOP_LEFT
    margin = 0
    relative_width = None
    relative_height = None
    min_width = 0
    min_height = 0
    max_width = None
    max_height = None
    debug = False

    def __init__(self):
        super().__init__()

        # Set initial dimensions based on class attributes
        if not hasattr(self, "width") or self.width == 0:
            self.width = self.min_width
        if not hasattr(self, "height") or self.height == 0:
            self.height = self.min_height

    @abstractmethod
    def arrange_widgets(self) -> None:
        """Arrange child elements according to layout rules."""
        pass

    def on_parent_resize(self, parent_width: int, parent_height: int) -> None:
        """Handle parent container resize."""
        old_width, old_height = self.width, self.height

        # Calculate new size based on relative dimensions
        if self.relative_width is not None:
            self.width = int(parent_width * self.relative_width)
        if self.relative_height is not None:
            self.height = int(parent_height * self.relative_height)

        # Apply min/max constraints
        if self.min_width:
            self.width = max(self.width, self.min_width)
        if self.min_height:
            self.height = max(self.height, self.min_height)

        if self.max_width:
            self.width = min(self.width, self.max_width)
        if self.max_height:
            self.height = min(self.height, self.max_height)

        # Calculate position based on anchor
        anchor_x, anchor_y = self.anchor.value
        self.x = int((parent_width - self.width) * anchor_x)
        self.y = int((parent_height - self.height) * anchor_y)

        # If size changed, rearrange widgets
        if old_width != self.width or old_height != self.height:
            self.arrange_widgets()

        # Propagate resize to children
        for child in self._children:
            if hasattr(child, "on_parent_resize"):
                child.on_parent_resize(self.width, self.height)

    def render(self, surface: pygame.Surface) -> None:
        # Render all children
        for child in self._children:
            child.render(surface)
