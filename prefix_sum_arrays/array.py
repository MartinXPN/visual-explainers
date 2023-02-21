from dataclasses import dataclass

from manim import *


@dataclass
class Array:
    values: list[int]
    color: str = WHITE
    fill_color: str = BLACK
    fill_opacity: float = 0.5
    stroke_width: float = 2
    stroke_color: str = WHITE
    height: float = 0.5
    width: float = 0.5
    spacing: float = 0.5

    def __post_init__(self):
        self.values = [int(value) for value in self.values]
        self.length = len(self.values)
        self.total = sum(self.values)

    def get_rectangles(self):
        rectangles = []
        for i, value in enumerate(self.values):
            rectangle = Rectangle(
                height=self.height,
                width=self.width,
                color=self.color,
                fill_color=self.fill_color,
                fill_opacity=self.fill_opacity,
                stroke_width=self.stroke_width,
                stroke_color=self.stroke_color,
            )
            rectangle.shift(i * (self.width + self.spacing) * RIGHT)
            rectangles.append(rectangle)
        return rectangles

    def get_labels(self):
        labels = []
        for i, value in enumerate(self.values):
            label = Tex(str(value))
            label.scale(0.5)
            label.move_to(self.get_rectangles()[i])
            labels.append(label)
        return labels

    def get_mobjects(self):
        return self.get_rectangles() + self.get_labels()

    def get_mobject(self):
        return VGroup(*self.get_mobjects())

    def get_prefix_sum_array(self):
        prefix_sum_array = []
        for i in range(self.length):
            prefix_sum_array.append(sum(self.values[:i + 1]))
        return Array(prefix_sum_array, color=self.color, fill_color=self.fill_color, fill_opacity=self.fill_opacity,
                     stroke_width=self.stroke_width, stroke_color=self.stroke_color, height=self.height,
                     width=self.width, spacing=self.spacing)

    def get_prefix_sum_rectangles(self):
        prefix_sum_rectangles = []
        for i, rectangle in enumerate(self.get_rectangles()):
            prefix_sum_rectangles.append(
                Rectangle(
                    height=self.height * sum(self.values[:i + 1]) / self.total,
                    width=self.width,
                    color=self.color,
                    fill_color=self.fill_color,
                    fill_opacity=self.fill_opacity,
                    stroke_width=self.stroke_width,
                    stroke_color=self.stroke_color,
                )
            )
        return prefix_sum_rectangles
