# 🚧 WORK IN PROGESS 🚧

# PyGameDUI - Declarative UI Framework for Pygame

PyGameDUI is a declarative UI framework for Pygame applications. It allows you to create complex user interfaces using a clean, nested class syntax.

## Features

- **Declarative Syntax**: Define your UI layout using nested classes
- **Responsive Layouts**: Stack and grid layouts that adapt to window resizing
- **Anchoring System**: Position elements with anchor system
- **Component-Based**: Create reusable UI components
- **Event Handling**: Automatic event propagation to the  UI elements

## Installation

```bash
pip install pygamedui
```

## Quick Example

Here's a simple example of creating a game menu:

```python
import pygame
from pygamedui import Container, StackLayout, Label, Button, StackDirection, Anchor

class GameMenu(Container):
    """Example game menu using declarative syntax."""
    
    width = 600
    height = 400
    background_color = (30, 30, 40)
    
    class HeaderLayout(StackLayout):
        direction = StackDirection.VERTICAL
        spacing = 10
        anchor = Anchor.TOP_CENTER
        relative_width = 0.8
        height = 120
        margin = 20
        
        class Title(Label):
            text = "GAME TITLE"
            font_size = 48
            color = (220, 220, 100)
        
        class Subtitle(Label):
            text = "Subtitle of the game"
            font_size = 24
            color = (180, 180, 180)
    
    class MenuLayout(StackLayout):
        direction = StackDirection.VERTICAL
        spacing = 15
        anchor = Anchor.CENTER
        relative_width = 0.5
        relative_height = 0.4

        class NewGameButton(Button):
            text = "New Game"
            hover_color = (20, 60, 160)
            
        class ContinueButton(Button):
            text = "Continue"
            hover_color = (20, 60, 160)
        
        class SettingsButton(Button):
            text = "Settings"
            hover_color = (20, 60, 160)
        
        class QuitButton(Button):
            text = "Quit"
            hover_color = (20, 60, 160)

# Initialize pygame and create window
pygame.init()
screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
pygame.display.set_caption("PyGameDUI Example")

# Create the UI with just one line!
ui = GameMenu()
ui.resize(screen.get_width(), screen.get_height())

# Main game loop
clock = pygame.time.Clock()
running = True

while running:
    dt = clock.tick(60) / 1000.0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            width, height = event.size
            screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
            ui.resize(width, height)
        else:
            ui.handle_event(event)
    
    ui.update(dt)
    ui.render(screen)
    pygame.display.flip()

pygame.quit()
```

## Documentation

See detaile [DOCUMENTATION.md](DOCUMENTATION.md) file and examples directrory for more detailed guidance.

## License

PyGameDUI is released under the MIT License. See the LICENSE file for details.