from manim import *

from sliding_window.array import Array

a = [8, 3, -2, 4, 5, -1, 0, 5, 3, 9, -6]
k = 5


class CreateThumbnail(Scene):
    def construct(self):
        array = Array(a, width=0.8, height=0.8, spacing=0.05, scale_text=0.8)
        array.highlight(2, k + 1, color=RED)
        array_mobj = array.get_mobject().center()

        brace = Brace(array_mobj, DOWN, stroke_width=2, color=RED).scale(k / len(a))\
            .align_to(array_mobj, LEFT).shift((array.width + array.spacing) * 2 * RIGHT)
        sum_text = Tex(sum(a[0: k]), color=RED).scale(0.8).next_to(brace, DOWN, buff=0.2)
        self.add(array_mobj, brace, sum_text)
