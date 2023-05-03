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
        self.wait(0.2)

        def highlight(new_start, shift):
            nonlocal start
            array.unhighlight()
            array.highlight(new_start, new_start + k - 1, color=RED)
            array_mobj.become(array.get_mobject(), match_center=True)
            self.play(brace.animate.shift((array.width + array.spacing) * RIGHT * shift / 2), run_time=0.1)
            start = new_start
            self.play(brace.animate.shift((array.width + array.spacing) * RIGHT * shift / 2), run_time=0.1)
            self.wait(0.2)

        highlight(new_start=2, shift=2)     # Take the range [2, 6] as an example
        highlight(new_start=5, shift=3)     # Take the range [5, 9] as an example
        highlight(new_start=4, shift=-1)    # Take the range [4, 8] as an example

        # Add an arrow at location 4 and iterate up to the end
        highlight(new_start=0, shift=-4)
        arrow = Arrow(
            start=UP, end=DOWN, color=RED, buff=0.1,
            stroke_width=10, max_stroke_width_to_length_ratio=15,
            max_tip_length_to_length_ratio=0.5, tip_length=0.2,
        ).scale(0.3).next_to(array_mobj, UP).shift((array.width + array.spacing) * 1 * LEFT)
        self.play(Create(arrow))
        for end in range(5, len(array)):
            self.play(arrow.animate.shift((array.width + array.spacing) * RIGHT), run_time=0.1)
            highlight(new_start=end - k + 1, shift=1)
        self.wait(0.2)

        # Move to start
        self.play(arrow.animate.shift((array.width + array.spacing) * 6 * LEFT), run_time=0.1)
        highlight(new_start=0, shift=-6)
        self.wait(0.1)

        # Iterate from 4 to the end and display the sum of each subarray
        sums = [Text(' - ').next_to(array_mobj, DOWN).align_to(array_mobj, LEFT).shift(0.8 * DOWN)]
        for end in range(k, len(array)):
            # Write the formula
            formula = MathTex(
                f'{{{{ \\mathrm{{sum}}[{end - k}: {end - 1}] }}}} = '
                f'{{{{ a[{end - k}] }}}} + {{{{ a[{end - k + 1}] }}}} + {{{{ a[{end - k + 2}] }}}} + '
                f'{{{{ a[{end - k + 3}] }}}} + {{{{ a[{end - k + 4}] }}}} = {{{{ {sum(a[end - k: end])} }}}}',
                color=YELLOW,
            ).scale(0.7).next_to(sums[-1], DOWN, buff=0.2).align_to(sums[-1], LEFT)
            [formula[i].set_color(BLACK) for i in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]]
            if len(sums) <= 4:
                self.play(Write(formula), run_time=0.1)
                sums.append(formula)
            else:
                formula = None

            for i in range(end - k, end):
                array.highlight(i, i, color=YELLOW, width=8.)
                if i - 1 >= end - k:
                    array.highlight(i - 1, i - 1, color=RED)
                array_mobj.become(array.get_mobject(), match_center=True)
                if formula is not None:
                    self.play(formula[2 + 2 * (i - end + k)].animate.set_color(YELLOW), run_time=0.1)
                    self.play(formula[3 + 2 * (i - end + k)].animate.set_color(YELLOW), run_time=0.1)
                self.wait(0.1)
            array.highlight(end - 1, end - 1, color=RED)
            array_mobj.become(array.get_mobject(), match_center=True)
            if formula is not None:
                self.play(formula[11].animate.set_color(YELLOW), run_time=0.1)
                self.play(formula[12].animate.set_color(YELLOW), run_time=0.1)

            self.play(arrow.animate.shift((array.width + array.spacing) * RIGHT), run_time=0.1)
            highlight(new_start=end - k + 1, shift=1)

        self.wait(0.1)
        self.play(Circumscribe(VGroup(*sums[1:]), run_time=0.3))
        self.wait(0.1)

        self.play(FadeOut(VGroup(*sums)), run_time=0.1)
        complexity = Tex('Time Complexity: $\\mathcal{O}(n \\cdot k)$', color=RED).next_to(array_mobj, DOWN, buff=1)
        self.play(Write(complexity), run_time=0.1)
        self.wait(0.1)

        # Move to next scene
        self.play(FadeOut(complexity, arrow, brace, sum_text), run_time=0.1)
        self.wait(0.1)


class SlidingWindowDiscovery(Scene):
    def construct(self):
        title = Title('Maximum Sum Subarray of Size K', include_underline=False)
        self.add(title)

        array = Array(a, width=0.8, height=0.8, spacing=0.05, scale_text=0.8)
        array_mobj = array.get_mobject().center()
        array_name = Text('a:').scale(0.8).move_to(array_mobj, LEFT).shift(0.7 * LEFT)
        k_name = Text('K = 5').scale(0.8).center().move_to(title, DOWN).shift(0.7 * DOWN)
        self.add(array_mobj, array_name, k_name)
        self.wait(0.1)

        arrow = Arrow(
            start=UP, end=DOWN, color=RED, buff=0.1,
            stroke_width=10, max_stroke_width_to_length_ratio=15,
            max_tip_length_to_length_ratio=0.5, tip_length=0.2,
        ).scale(0.3).next_to(array_mobj, UP).shift((array.width + array.spacing) * 1 * LEFT)
        self.play(Create(arrow))

        start = 0
        brace = Brace(array_mobj, DOWN, stroke_width=2, color=RED).scale(k / len(a)).align_to(array_mobj, LEFT)
        sum_text = always_redraw(
            lambda: Tex(sum(a[start: start + k]), color=RED).scale(0.8).next_to(brace, DOWN, buff=0.2)
        )
        self.add(brace, sum_text)

        def highlight(new_start, shift):
            nonlocal start
            array.unhighlight()
            array.highlight(new_start, new_start + k - 1, color=RED)
            array_mobj.become(array.get_mobject(), match_center=True)
            self.play(brace.animate.shift((array.width + array.spacing) * RIGHT * shift / 2), run_time=0.1)
            start = new_start
            self.play(brace.animate.shift((array.width + array.spacing) * RIGHT * shift / 2), run_time=0.1)
            self.wait(0.2)

        for end in range(k, k + 3):
            for i in range(end - k, end):
                array.highlight(i, i, color=YELLOW, width=8.)
                if i - 1 >= end - k:
                    array.highlight(i - 1, i - 1, color=RED)
                array_mobj.become(array.get_mobject(), match_center=True)
                self.wait(0.1)
            array.highlight(end - 1, end - 1, color=RED)
            array_mobj.become(array.get_mobject(), match_center=True)

            self.play(arrow.animate.shift((array.width + array.spacing) * RIGHT), run_time=0.1)
            highlight(new_start=end - k + 1, shift=1)
