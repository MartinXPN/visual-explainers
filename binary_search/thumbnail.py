from manim import *

from binary_search.array import Array

a = [20, 22, 23, 23, 34, 49, 52, 55, 58]
ORANGE = ManimColor('#fa541c')


class Left(Scene):
    def construct(self):
        array = Array(a[:5], color=WHITE)
        array_mobj = array.get_mobject().center().shift(1.5 * UP)
        self.add(array_mobj)


class Right(Scene):
    def construct(self):
        array = Array(a[5:], color=WHITE)
        array_mobj = array.get_mobject().center().shift(1.5 * UP)
        self.add(array_mobj)
