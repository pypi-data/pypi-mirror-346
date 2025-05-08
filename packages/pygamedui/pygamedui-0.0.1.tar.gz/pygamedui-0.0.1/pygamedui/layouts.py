from .layout import Layout
from enum import Enum


class StackDirection(Enum):
    HORIZONTAL = 0
    VERTICAL = 1


class StackLayout(Layout):
    """Layout that stacks elements horizontally or vertically."""

    direction = StackDirection.VERTICAL
    spacing = 5

    def arrange_widgets(self) -> None:
        """Stack elements in the specified direction."""
        if not self._children:
            return

        if self.direction == StackDirection.VERTICAL:
            self._arrange_vertical()
        else:
            self._arrange_horizontal()

    def _arrange_vertical(self) -> None:
        """Stack elements vertically."""
        y_offset = self.margin

        for child in self._children:
            # Center horizontally in layout with respect to margin
            available_width = self.width - (2 * self.margin)
            x_pos = self.margin + (available_width - child.width) // 2
            child.x = max(self.margin, x_pos)
            child.y = y_offset

            # Move to next position
            y_offset += child.height + self.spacing

    def _arrange_horizontal(self) -> None:
        """Stack elements horizontally."""
        x_offset = self.margin

        for child in self._children:
            # Center vertically in layout
            available_height = self.height - (2 * self.margin)
            y_pos = self.margin + (available_height - child.height) // 2
            child.y = max(self.margin, y_pos)
            child.x = x_offset

            # Move to next position
            x_offset += child.width + self.spacing


class GridLayout(Layout):
    """Layout that arranges elements in a grid."""

    rows = 2
    cols = 2
    h_spacing = 5
    v_spacing = 5

    def __init__(self):
        super().__init__()

        # Initialize grid with None values
        self.grid = [[None for _ in range(self.cols)] for _ in range(self.rows)]

        # Track positions for auto placement
        self.next_row = 0
        self.next_col = 0

    def arrange_widgets(self) -> None:
        """Arrange widgets in the grid."""
        # First, place widgets in the grid
        for i, child in enumerate(self._children):
            # Find position based on grid_row and grid_col attributes if they exist
            if hasattr(child, "grid_row") and hasattr(child, "grid_col"):
                row, col = child.grid_row, child.grid_col
            else:
                # Otherwise use automatic placement
                row, col = self.next_row, self.next_col

                # Update next position
                self.next_col += 1
                if self.next_col >= self.cols:
                    self.next_col = 0
                    self.next_row += 1
                if self.next_row >= self.rows:
                    self.next_row = 0  # Wrap around if needed

            # Store in grid if within bounds
            if 0 <= row < self.rows and 0 <= col < self.cols:
                self.grid[row][col] = child

        # Calculate cell dimensions
        cell_width = (
            self.width - self.margin * 2 - self.h_spacing * (self.cols - 1)
        ) // self.cols
        cell_height = (
            self.height - self.margin * 2 - self.v_spacing * (self.rows - 1)
        ) // self.rows

        # Position each widget in its cell
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] is not None:
                    child = self.grid[r][c]

                    # Calculate cell position
                    cell_x = self.margin + c * (cell_width + self.h_spacing)
                    cell_y = self.margin + r * (cell_height + self.v_spacing)

                    # Center widget in cell
                    child.x = cell_x + (cell_width - child.width) // 2
                    child.y = cell_y + (cell_height - child.height) // 2
