from manim import *

from insertion_sort.array import Array

small = [2, 5, 7, 10]
ORANGE = ManimColor('#fa541c')


class Cards(Scene):
    def construct(self):
        array = Array(small.copy(), color=BLACK, cell_type='card')
        array_mobj = array.get_mobject().center().shift(UP)
        array.cells[2].shift(1.2 * UP)
        array.labels[2].shift(1.2 * UP)

        self.add(array_mobj)
