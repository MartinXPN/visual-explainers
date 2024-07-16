from dataclasses import dataclass, field
from itertools import chain

from manim import *
from manim.animation.transform_matching_parts import TransformMatchingAbstractBase


card_paths = [
    'insertion_sort/card-spade.svg',
    'insertion_sort/card-club.svg',
    'insertion_sort/card-diamond.svg',
    'insertion_sort/card-heart.svg',
]


@dataclass
class Array:
    values: list[int | None]
    color: str | list[str] = field(default_factory=lambda: WHITE)
    fill_color: str = field(default_factory=lambda: BLACK)
    fill_opacity: float = 0.5
    stroke_width: float | list[float] = 2.
    stroke_color: str | list[str] = field(default_factory=lambda: WHITE)
    height: float = 0.7
    width: float = 1.4
    spacing: float = 0.1
    scale_text: float = 0.9

    cell_type: str = 'rectangle'  # 'rectangle' or 'card'
    cells: list[Rectangle | SVGMobject] = field(default_factory=lambda: [])
    labels: list[VMobject] = field(default_factory=lambda: [])

    def __post_init__(self):
        self.stroke_color: list[str] = [self.stroke_color] * len(self.values) \
            if isinstance(self.stroke_color, ManimColor) \
            else self.stroke_color
        self.stroke_width: list[float] = [self.stroke_width] * len(self.values) \
            if isinstance(self.stroke_width, (float, int)) \
            else self.stroke_width
        self.color: list[str] = [self.color] * len(self.values) \
            if isinstance(self.color, ManimColor) \
            else self.color

    def get_cells(self):
        self.cells = []
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
            if self.cell_type == 'rectangle':
                self.cells.append(rectangle)
            elif self.cell_type == 'card':
                # Pick the card based on the value
                path = card_paths[value % 4]
                self.color[i] = BLACK if value % 4 in [0, 1] else RED
                card = SVGMobject(path).scale(self.width / 2)
                card.move_to(rectangle.get_center())
                self.cells.append(card)
            else:
                raise ValueError(f'Invalid cell type: {self.cell_type}')
        return self.cells

    def get_labels(self):
        cells = self.get_cells() if not self.cells else self.cells
        self.labels = []
        for i, value in enumerate(self.values):
            label = Tex(str(value) if value is not None else '', color=self.color[i])
            label.scale(self.scale_text)
            label.move_to(cells[i])
            self.labels.append(label)
        return self.labels

    def get_mobjects(self):
        if not self.cells:
            self.get_cells()
        if not self.labels:
            self.get_labels()
        return chain.from_iterable(zip(self.cells, self.labels))

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
