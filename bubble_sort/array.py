from dataclasses import dataclass, field
from itertools import chain

from manim import *
from manim.animation.transform_matching_parts import TransformMatchingAbstractBase


@dataclass
class Array:
    values: list[int | None]
    color: str = field(default_factory=lambda: WHITE)
    fill_color: str = field(default_factory=lambda: BLACK)
    fill_opacity: float = 0.5
    stroke_width: float | list[float] = 2.
    stroke_color: str | list[str] = field(default_factory=lambda: WHITE)
    height: float = 0.6
    width: float = 0.6
    spacing: float = 0.1
    scale_text: float = 0.6

    rectangles: list[Rectangle] = field(default_factory=lambda: [])
    labels: list[VMobject] = field(default_factory=lambda: [])

    def __post_init__(self):
        self.stroke_color: list[str] = [self.stroke_color] * len(self.values) \
            if isinstance(self.stroke_color, ManimColor) \
            else self.stroke_color
        self.stroke_width: list[float] = [self.stroke_width] * len(self.values) \
            if isinstance(self.stroke_width, (float, int)) \
            else self.stroke_width

    def get_rectangles(self):
        self.rectangles = []
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
            self.rectangles.append(rectangle)
        return self.rectangles

    def get_labels(self):
        rectangles = self.get_rectangles() if not self.rectangles else self.rectangles
        self.labels = []
        for i, value in enumerate(self.values):
            label = Tex(str(value) if value is not None else '', color=self.color)
            label.scale(self.scale_text)
            label.move_to(rectangles[i])
            self.labels.append(label)
        return self.labels

    def get_mobjects(self):
        if not self.rectangles:
            self.get_rectangles()
        if not self.labels:
            self.get_labels()
        return chain.from_iterable(zip(self.rectangles, self.labels))

    def get_mobject(self):
        return VGroup(*self.get_mobjects())

    def __len__(self):
        return len(self.values)


class TransformMatchingCells(TransformMatchingAbstractBase):
    """ Similar to TransformMatchingShapes but transforms the matching cells (label + rectangle) of an Array. """
    def __init__(
        self,
        mobject: Mobject,
        target_mobject: Mobject,
        transform_mismatches: bool = False,
        fade_transform_mismatches: bool = False,
        key_map: dict | None = None,
        **kwargs,
    ):
        super().__init__(
            mobject,
            target_mobject,
            transform_mismatches=transform_mismatches,
            fade_transform_mismatches=fade_transform_mismatches,
            key_map=key_map,
            **kwargs,
        )

    @staticmethod
    def get_mobject_parts(mobject: Mobject) -> list[Mobject]:
        # Group the list of submobjects into pairs of (rectangle, label)
        res = [VGroup(*mobject.submobjects[i:i + 2]) for i in range(0, len(mobject.submobjects), 2)]
        return res

    @staticmethod
    def get_mobject_key(mobject: list[tuple[Rectangle, Tex]]) -> int:
        return hash(mobject[1].tex_string)
