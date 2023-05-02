from manim import *

from sliding_window.array import Array

a = [8, 3, -2, 4, 5, -1, 0, 5, 3, 9, -6]
k = 5


class OpeningScene(Scene):
    def construct(self):
        title = Title('Maximum Sum Subarray of Size K', include_underline=False)
        self.add(title)

        array = Array(a, width=0.8, height=0.8, spacing=0.05, scale_text=0.8)
        array_mobj = array.get_mobject().center()
        array_name = Text('a:').scale(0.8).move_to(array_mobj, LEFT).shift(0.7 * LEFT)
        k_name = Text('K = 5').scale(0.8).center().move_to(title, DOWN).shift(0.7 * DOWN)
        self.play(
            Create(array_mobj),
            Write(array_name),
            Write(k_name),
        )
        self.wait(0.1)

        # Take the range [0, 4] as an example
        start = 0
        brace = Brace(array_mobj, DOWN, stroke_width=2, color=RED).scale(k / len(a)).align_to(array_mobj, LEFT)
        sum_text = always_redraw(
            lambda: Tex(sum(a[start: start + k]), color=RED).scale(0.8).next_to(brace, DOWN, buff=0.2)
        )
        array.highlight(start, start + k - 1, color=RED)
        array_mobj.become(array.get_mobject(), match_center=True)
        self.add(brace, sum_text)
        self.wait(0.5)

        def highlight(new_start, shift):
            nonlocal start
            array.unhighlight()
            array.highlight(new_start, new_start + k - 1, color=RED)
            array_mobj.become(array.get_mobject(), match_center=True)
            self.play(brace.animate.shift((array.width + array.spacing) * RIGHT * shift / 2), run_time=0.1)
            start = new_start
            self.play(brace.animate.shift((array.width + array.spacing) * RIGHT * shift / 2), run_time=0.1)
            self.wait(0.5)

        highlight(new_start=2, shift=2)     # Take the range [2, 6] as an example
        highlight(new_start=5, shift=3)     # Take the range [5, 9] as an example
        highlight(new_start=4, shift=-1)    # Take the range [4, 8] as an example

