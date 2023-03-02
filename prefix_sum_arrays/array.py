from dataclasses import dataclass

from manim import *


@dataclass
class Array:
    values: list[int | None]
    color: str = WHITE
    fill_color: str = BLACK
    fill_opacity: float = 0.5
    stroke_width: float | list[float] = 2.
    stroke_color: str | list[str] = WHITE
    height: float = 0.5
    width: float = 0.5
    spacing: float = 0.1
    scale_text: float = 0.5

    def __post_init__(self):
        self.stroke_color: list[str] = [self.stroke_color] * len(self.values) \
            if isinstance(self.stroke_color, str) \
            else self.stroke_color
        self.stroke_width: list[float] = [self.stroke_width] * len(self.values) \
            if isinstance(self.stroke_width, (float, int)) \
            else self.stroke_width

    def get_rectangles(self):
        rectangles = []
        for i, value in enumerate(self.values):
            rectangle = Rectangle(
                height=self.height,
                width=self.width,
                fill_color=self.fill_color,
                fill_opacity=self.fill_opacity,
                stroke_width=self.stroke_width[i],
                stroke_color=self.stroke_color[i],
            )
            rectangle.shift(i * (self.width + self.spacing) * RIGHT)
            rectangles.append(rectangle)
        return rectangles

    def get_labels(self):
        labels = []
        for i, value in enumerate(self.values):
            label = Tex(str(value) if value is not None else '', color=self.color)
            label.scale(self.scale_text)
            label.move_to(self.get_rectangles()[i])
            labels.append(label)
        return labels

    def get_mobjects(self):
        return self.get_rectangles() + self.get_labels()

    def get_mobject(self):
        return VGroup(*self.get_mobjects())

    def highlight(self, start: int, end: int, color=RED, width=5.):
        self.stroke_color = [color if start <= i <= end else self.stroke_color[i] for i in range(len(self.values))]
        self.stroke_width = [width if start <= i <= end else self.stroke_width[i] for i in range(len(self.values))]

    def unhighlight(self):
        self.stroke_color = [WHITE] * len(self.values)
        self.stroke_width = [2.] * len(self.values)

    def __len__(self):
        return len(self.values)
