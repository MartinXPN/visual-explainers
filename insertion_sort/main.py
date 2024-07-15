import random
from textwrap import dedent

from manim import *

from insertion_sort.array import Array


small = [2, 7, 10, 5, 3, -1]
large = [12, 3, 5, 9, 4, 1, 7]
ORANGE = ManimColor('#fa541c')
BLUE_BACKGROUND = ManimColor('#ADD8E6')


class Introduction(Scene):
    def construct(self):
        # Create vertical bars representing the array and sort them with insertion sort
        random.seed(42)
        array = list(range(1, 55))
        random.shuffle(array)

        base = Rectangle(height=1, width=1, color=WHITE, fill_opacity=1).center().to_edge(DOWN).shift(UP)
        rectangles = [
            Rectangle(height=0.12 * value, width=0.05, color=WHITE, fill_opacity=1).align_to(base, DOWN).shift(0.12 * i * RIGHT)
            for i, value in enumerate(array)
        ]
        bars = VGroup(*rectangles).center()
        self.play(Create(bars, run_time=0.2))

        for i in range(1, len(array)):
            while i > 0 and array[i] < array[i - 1]:
                # Highlight the current bars being compared
                self.play(
                    bars[i].animate.set_color(ORANGE),
                    bars[i - 1].animate.set_color(ORANGE),
                    run_time=0.001,
                )
                array[i], array[i - 1] = array[i - 1], array[i]
                self.play(
                    bars[i].animate.move_to(bars[i - 1], aligned_edge=DOWN),
                    bars[i - 1].animate.move_to(bars[i], aligned_edge=DOWN),
                    run_time=0.001,
                )
                bars[i], bars[i - 1] = bars[i - 1], bars[i]

                # Un-highlight bars[i]
                bars[i].set_color(WHITE)
                i -= 1

            bars[i].set_color(WHITE)
        self.wait(1)

        for i in range(len(array)):
            self.play(LaggedStart(
                *[bars[j].animate.set_color(ORANGE) for j in range(len(array) - i)],
                lag_ratio=0.8,
                run_time=5,
            ))
        self.wait(1)

        for bar in bars:
            bar.set_color(WHITE)
        self.wait(2)


class IntroductionImplementation(Scene):
    def construct(self):
        code = Code(
            code=dedent('''
                for i in range(1, len(a)):
                j = i
                while j > 0 and a[j] < a[j - 1]:
                    a[j - 1], a[j] = a[j], a[j - 1]
                    j -= 1
            ''').strip(),
            tab_width=4,
            language='Python',
            line_spacing=0.6,
            font='Monospace',
            style='monokai',
        ).center().code

        for line in code.chars:
            self.play(AddTextLetterByLetter(line, run_time=0.1 * len(line)))
        self.wait(2)


class Intuition(Scene):
    def construct(self):
        title = Title('Insertion Sort', include_underline=False)
        self.play(Write(title), run_time=0.2)

        array = Array(small, color=BLACK, cell_type='card')
        array_mobj = array.get_mobject().center().shift(1.5 * UP)
        a_text = Tex('a:').scale(0.9).next_to(array_mobj, LEFT)

        indices = Array(
            [i for i in range(len(array))],
            width=array.width, height=array.height,
            spacing=array.spacing, scale_text=array.scale_text, stroke_color=BLACK,
        )
        indices_mobj = indices.get_mobject().center().next_to(array_mobj, 0.1 * UP)
        self.play(Create(array_mobj), Create(a_text), Create(indices_mobj), run_time=2)

        self.wait(0.5)
