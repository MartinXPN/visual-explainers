from dataclasses import dataclass

from manim import *


@dataclass
class Matrix:
    values: list[list[int | None]]
    color: str = WHITE
    fill_color: str = BLACK
    fill_opacity: float = 0.5
    stroke_width: float | list[list[float]] = 2.
    stroke_color: str | list[list[str]] = WHITE
    height: float = 0.5
    width: float = 0.5
    spacing: float = 0.1
    scale_text: float = 0.5

    def __post_init__(self):
        self.stroke_color: list[list[str]] = [[self.stroke_color] * len(self.values[0])
                                              for _ in range(len(self.values))] \
            if isinstance(self.stroke_color, str) \
            else self.stroke_color
        self.stroke_width: list[list[float]] = [[self.stroke_width] * len(self.values[0])
                                                for _ in range(len(self.values))] \
            if isinstance(self.stroke_width, (float, int)) \
            else self.stroke_width

    def get_rectangles(self) -> list[VMobject]:
        rectangles = []
        for i, row in enumerate(self.values):
            for j, value in enumerate(row):
                rectangle = Rectangle(
                    height=self.height,
                    width=self.width,
                    fill_color=self.fill_color,
                    fill_opacity=self.fill_opacity,
                    stroke_width=self.stroke_width[i][j],
                    stroke_color=self.stroke_color[i][j],
                )
                rectangle.shift(i * (self.height + self.spacing) * DOWN)
                rectangle.shift(j * (self.width + self.spacing) * RIGHT)
                rectangles.append(rectangle)
        return rectangles

    def get_labels(self) -> list[VMobject]:
        rectangles = self.get_rectangles()
        labels = []
        for i, row in enumerate(self.values):
            # Add index for the row
            label = Tex(str(i), color=self.color)
            label.scale(self.scale_text)
            label.move_to(rectangles[i * len(row)])
            label.shift(0.9 * self.width * LEFT)
            labels.append(label)

            # Add all the values in the row
            for j, value in enumerate(row):
                label = Tex(str(value) if value is not None else '', color=self.color)
                label.scale(self.scale_text)
                label.move_to(rectangles[i * len(row) + j])
                labels.append(label)

        # Add index for the column
        for j in range(len(self.values[0])):
            label = Tex(str(j), color=self.color)
            label.scale(self.scale_text)
            label.move_to(rectangles[j])
            label.shift(0.9 * self.height * UP)
            labels.append(label)
        return labels

    def get_mobjects(self) -> list[VMobject]:
        return self.get_rectangles() + self.get_labels()

    def get_mobject(self) -> VMobject:
        return VGroup(*self.get_mobjects())

    def highlight(self, ur: int, uc: int, br: int, bc: int, color=RED, width=5.):
        """
        Highlight a rectangle of the matrix.
        :param ur: Upper row index
        :param uc: Upper column index
        :param br: Bottom row index
        :param bc: Bottom column index
        :param color: Highlight color
        :param width: Highlight stroke width
        """
        for i in range(ur, br + 1):
            for j in range(uc, bc + 1):
                self.stroke_color[i][j] = color
                self.stroke_width[i][j] = width

    def unhighlight(self):
        """
        Remove all highlights.
        """
        self.stroke_color = [[WHITE] * len(self.values[0]) for _ in range(len(self.values))]
        self.stroke_width = [[2.] * len(self.values[0]) for _ in range(len(self.values))]

    def __len__(self):
        return len(self.values)
