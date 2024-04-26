from dataclasses import dataclass, field

from manim import *


@dataclass
class NumberGrid:
    n: int                                                                          # Render all the numbers from 0 to n (exclusive)
    values_per_row: int = 10                                                        # Number of values per row (we render a grid)
    color: ManimColor | list[ManimColor] = field(default_factory=lambda: WHITE)     # Color for each number
    fill_color: ManimColor = field(default_factory=lambda: BLACK)
    fill_opacity: float = 0.5
    height: float = 0.4
    width: float = 0.4
    spacing: float = 0.15
    scale_text: float = 0.5
    labels: list[VMobject] = field(default_factory=lambda: [])
    rectangles: list[VMobject] = field(default_factory=lambda: [])

    def __post_init__(self):
        self.values = [[i * self.values_per_row + j for j in range(self.values_per_row)]
                       for i in range(self.n // self.values_per_row)]
        if self.n % self.values_per_row:
            self.values.append(list(range(self.values_per_row * len(self.values), self.n)))

    def get_rectangles(self) -> list[VMobject]:
        self.rectangles = []
        for i, row in enumerate(self.values):
            for j, value in enumerate(row):
                rectangle = Rectangle(
                    height=self.height,
                    width=self.width,
                    fill_color=self.fill_color,
                    fill_opacity=self.fill_opacity,
                    stroke_width=0,
                )
                rectangle.shift(i * (self.height + self.spacing) * DOWN)
                rectangle.shift(j * (self.width + self.spacing) * RIGHT)
                self.rectangles.append(rectangle)
        return self.rectangles

    def get_labels(self) -> list[VMobject]:
        rectangles = self.get_rectangles() if not self.rectangles else self.rectangles
        self.labels = []
        for i, row in enumerate(self.values):
            for j, value in enumerate(row):
                label = Tex(
                    str(value) if value is not None else '',
                    color=self.color[i * len(row) + j] if isinstance(self.color, list) else self.color,
                )
                label.scale(self.scale_text)
                label.move_to(rectangles[i * len(row) + j])
                self.labels.append(label)
        return self.labels

    def get_mobjects(self) -> list[VMobject]:
        if not self.rectangles:
            self.get_rectangles()
        if not self.labels:
            self.get_labels()
        return self.rectangles + self.labels

    def get_mobject(self) -> VMobject:
        return VGroup(*self.get_mobjects())

    def highlight(self, index: int, color: ManimColor):
        if not self.rectangles:
            self.get_rectangles()
        if not self.labels:
            self.get_labels()

        # Make sure we work with a list of colors
        if not isinstance(self.color, list):
            self.color = [self.color] * self.n

        # Modify the label mobject by changing the color
        self.labels[index].set_color(color)
        self.color[index] = color

    def __len__(self):
        return len(self.values)
