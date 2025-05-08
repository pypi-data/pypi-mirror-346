import pygame
from abc import ABC, ABCMeta, abstractmethod
from typing import Tuple


class UIElementMeta(type):
    """
    Metaclass for UI elements that makes them declarative
    """

    def __new__(mcs, name, bases, attrs):
        # Initialize containers for child elements and pygame elements
        attrs["_children"] = []
        attrs["_pygame_element"] = None

        # Take nested classes and make them child elements
        nested_classes = {}
        for key, value in list(attrs.items()):
            if isinstance(value, type) and issubclass(value, UIElement):
                nested_classes[key] = attrs.pop(key)

        # Create the class
        cls = super().__new__(mcs, name, bases, attrs)

        # Store the nested for instations
        cls._nested_classes = nested_classes

        return cls

    def __call__(cls, *args, **kwargs):
        # Create instance
        instance = super().__call__(*args, **kwargs)

        # Instantiate child elements from nested class definitions
        for name, child_cls in cls._nested_classes.items():
            # Create instance of child element
            child_instance = child_cls()
            child_instance.parent = instance

            # Add to children
            instance._children.append(child_instance)

            # Add as atribute to instance
            setattr(instance, name, child_instance)

        # Arrange widgets according to layout rules
        if hasattr(instance, "arrange_widgets"):
            instance.arrange_widgets()

        return instance


# Create a combined metaclass to allow classes inhereting from UIElement and ABC to be created
class UIElementABCMeta(ABCMeta, UIElementMeta):
    pass


class UIElement(ABC, metaclass=UIElementABCMeta):
    """
    Base class for all UI elements
    """

    x = 0
    y = 0
    width = 0
    height = 0

    def __init__(self):
        self.parent = None
        self._children = []  # Populated by metaclass
        self._pygame_element = None

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.width, self.height)

    @property
    def absolute_position(self) -> Tuple[int, int]:
        if self.parent:
            parent_x, parent_y = self.parent.absolute_position
            return parent_x + self.x, parent_y + self.y
        return self.x, self.y

    def render(self, surface: pygame.Surface) -> None:
        # Render this element if it has a pygame element
        if self._pygame_element and hasattr(self._pygame_element, "render"):
            self._pygame_element.render(surface)

        # Render all children
        for child in self._children:
            child.render(surface)

    def handle_event(self, event: pygame.event.Event) -> bool:
        # Check if mouse event is within UI element
        if event.type in (
            pygame.MOUSEBUTTONDOWN,
            pygame.MOUSEBUTTONUP,
            pygame.MOUSEMOTION,
        ):
            mouse_pos = pygame.mouse.get_pos()
            abs_x, abs_y = self.absolute_position
            rect = pygame.Rect(abs_x, abs_y, self.width, self.height)

            if not rect.collidepoint(mouse_pos):
                return False

        # Handle with pygame element if available
        if self._pygame_element and hasattr(self._pygame_element, "handle_event"):
            if self._pygame_element.handle_event(event):
                return True

        # Pass event to children
        for child in self._children:
            if child.handle_event(event):
                return True

        return False

    def update(self, dt: float) -> None:
        if self._pygame_element and hasattr(self._pygame_element, "update"):
            self._pygame_element.update(dt)

        for child in self._children:
            child.update(dt)

    def set_pygame_element(self, element):
        self._pygame_element = element
        if hasattr(element, "width"):
            self.width = element.width
        if hasattr(element, "height"):
            self.height = element.height
