from manim import *

from merge_sort.array import Array

arr = [3, 9, 4, 1, 7]
ORANGE = ManimColor('#fa541c')


class Thumbnail(Scene):
    def construct(self):
        left = Array([3, 9], stroke_width=6)
        right = Array([1, 4, 7], stroke_width=6)
        s = sorted(arr)
        s[2] = '?'
        res = Array(s, color=BLACK, stroke_width=6)

        res_mobj = res.get_mobject().center().shift(UP)
        left_mobj = left.get_mobject().next_to(res_mobj, DOWN, buff=0.8).align_to(res_mobj, LEFT).shift(0.4 * LEFT)
        right_mobj = right.get_mobject().next_to(res_mobj, DOWN, buff=0.8).align_to(res_mobj, RIGHT).shift(0.8 * RIGHT)

        for label in res.labels:
            label.set_opacity(0)
        res.labels[2].set_opacity(1).scale(2).set_color(WHITE)

        # Create arrows that point from the center of left to the center of res and from the center of right to the center of res
        left_arrow = Arrow(
            start=left_mobj.get_top(), end=res_mobj.get_bottom(),
            color=ORANGE, buff=0.2, stroke_width=20, max_stroke_width_to_length_ratio=10,
            max_tip_length_to_length_ratio=0.5, tip_length=0.25,
        )
        right_arrow = Arrow(
            start=right_mobj.get_top(), end=res_mobj.get_bottom(),
            color=ORANGE, buff=0.2, stroke_width=20, max_stroke_width_to_length_ratio=10,
            max_tip_length_to_length_ratio=0.5, tip_length=0.25,
        )

        self.add(VGroup(left_mobj, right_mobj, res_mobj, left_arrow, right_arrow).scale(2))
