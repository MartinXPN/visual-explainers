import random

from manim import *

from bubble_sort.array import Array, TransformMatchingCells
from bubble_sort.clock import Clock

a = [12, 3, 5, 9, 4, 1, 7]
ORANGE = ManimColor('#fa541c')


class Introduction(Scene):
    def construct(self):
        # Create vertical bars representing the array and sort them with bubble sort
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

        for i in range(len(array)):
            for j in range(len(array) - i - 1):
                # Un-highlight the previous bars
                bars[j - 1].set_color(WHITE)

                # Highlight the current bars being compared
                self.play(
                    bars[j].animate.set_color(ORANGE),
                    bars[j + 1].animate.set_color(ORANGE),
                    run_time=0.001,
                )
                if array[j] > array[j + 1]:
                    array[j], array[j + 1] = array[j + 1], array[j]
                    self.play(
                        bars[j].animate.move_to(bars[j + 1], aligned_edge=DOWN),
                        bars[j + 1].animate.move_to(bars[j], aligned_edge=DOWN),
                        run_time=0.001,
                    )
                    bars[j], bars[j + 1] = bars[j + 1], bars[j]

            bars[len(array) - i - 1].set_color(WHITE)
            bars[len(array) - i - 2].set_color(WHITE)
        self.wait(1)

        for i in range(len(array)):
            self.play(LaggedStart(
                *[bars[j].animate.set_color(ORANGE) for j in range(len(array) - i)],
                lag_ratio=0.95,
                run_time=5,
            ))
        self.wait(1)

        for bar in bars:
            bar.set_color(WHITE)
        self.wait(2)


class IntroductionClock(Scene):
    def construct(self):
        clock = Clock(hh=3, mh=30).center()
        self.add(clock)

        clock.add_updaters()
        self.play(clock.ht.animate.set_value(5), run_time=2, rate_func=linear)
        self.play(clock.ht.animate.set_value(10), run_time=1, rate_func=linear)
        self.play(clock.ht.animate.set_value(20), FadeOut(clock), run_time=2, rate_func=linear)


def swap(array: Array, array_mobj: VGroup, i: int, j: int):
    new_values = array.values.copy()
    new_values[i], new_values[j] = new_values[j], new_values[i]
    new_array = Array(
        values=new_values,
        color=array.color,
        fill_color=array.fill_color,
        fill_opacity=array.fill_opacity,
        stroke_width=array.stroke_width,
        stroke_color=array.stroke_color,
        height=array.height,
        width=array.width,
        spacing=array.spacing,
        scale_text=array.scale_text,
    )

    new_array_mobj = new_array.get_mobject().move_to(array_mobj)
    for i in range(len(array.labels)):
        new_array.cells[i].set_stroke(
            color=array.cells[i].get_stroke_color(),
            width=array.cells[i].get_stroke_width(),
        )

    return new_array, new_array_mobj


def highlight(array: Array, start: int, end: int, color, width=5.):
    return [
        *[rect.animate.set_stroke(color=color, width=width) for rect in array.cells[start: end]],
    ]


class Intuition(Scene):
    def construct(self):
        title = Title('Sort the Array', include_underline=False)
        self.add(title)

        array = Array(a)
        array_mobj = array.get_mobject().center().shift(1.5 * UP)
        a_text = Tex('a:').scale(0.9).next_to(array_mobj, LEFT)

        indices = Array(
            [i for i in range(len(array))],
            width=array.width, height=array.height,
            spacing=array.spacing, scale_text=array.scale_text, stroke_color=BLACK,
        )
        indices_mobj = indices.get_mobject().center().next_to(array_mobj, 0.1 * UP)

        self.add(a_text)
        self.play(Create(array_mobj), Create(indices_mobj), run_time=0.1)
        self.wait(0.1)

        # Sort the array
        sorted_array = Array(sorted(a))
        sorted_mobj = sorted_array.get_mobject().move_to(array_mobj)
        self.play(TransformMatchingCells(array_mobj, sorted_mobj, path_arc=PI/3), run_time=0.5)
        self.wait(0.1)

        # Show the permutation
        permuted_array = Array([3, 5, 9, 4, 1, 12, 7])
        permuted_mobj = permuted_array.get_mobject().move_to(array_mobj)
        self.play(TransformMatchingCells(sorted_mobj, permuted_mobj, path_arc=PI/3), run_time=1)

        # Loop to the pair 9, 4
        for i in range(1, 4):
            if i != 1:
                self.play(*highlight(permuted_array, i - 2, i - 1, WHITE, 2), run_time=0.01)
            self.play(*highlight(permuted_array, i - 1, i + 1, ORANGE, 5), run_time=0.1)
            self.wait(0.1)

        # Swap 9 and 4
        swapped_array, swapped_mobj = swap(permuted_array, permuted_mobj, 2, 3)
        self.play(TransformMatchingCells(permuted_mobj, swapped_mobj, path_arc=PI/2), run_time=0.5)
        self.wait(0.1)
        self.play(*highlight(swapped_array, 2, 3, WHITE, 2), run_time=0.1)
        self.wait(0.1)

        # Highlight 9 and after that 1
        self.play(*highlight(swapped_array, 3, 5, ORANGE, 5), run_time=0.1)
        self.wait(0.1)
        self.play(Indicate(swapped_array.labels[3]), run_time=0.5)
        self.play(Indicate(swapped_array.labels[4]), run_time=0.5)

        # Swap 9 and 1
        new_swapped_array, new_swapped_mobj = swap(swapped_array, swapped_mobj, 3, 4)
        self.play(TransformMatchingCells(swapped_mobj, new_swapped_mobj, path_arc=PI/2), run_time=0.5)
        self.wait(0.1)

        # Draw an arrow <- at the bottom of 1
        left_arrow = Arrow(
            start=RIGHT, end=LEFT, color=YELLOW, buff=0.1,
            stroke_width=10, max_stroke_width_to_length_ratio=15,
            max_tip_length_to_length_ratio=0.2, tip_length=0.15,
        ).scale(0.3).next_to(new_swapped_array.cells[3], DOWN)

        # Draw an arrow -> at the bottom of 9
        right_arrow = Arrow(
            start=LEFT, end=RIGHT, color=YELLOW, buff=0.1,
            stroke_width=10, max_stroke_width_to_length_ratio=15,
            max_tip_length_to_length_ratio=0.2, tip_length=0.15,
        ).scale(0.3).next_to(new_swapped_array.cells[4], DOWN)

        self.play(Create(left_arrow), Indicate(new_swapped_array.labels[3]), run_time=0.5)
        self.play(Create(right_arrow), Indicate(new_swapped_array.labels[4]), run_time=0.5)
        self.wait(0.1)

        self.play(*highlight(new_swapped_array, 3, 5, WHITE, 2), run_time=0.1)
        self.wait(0.1)

        # Bring the array to the initial state
        self.play(FadeOut(left_arrow, right_arrow), run_time=0.5)
        self.play(TransformMatchingCells(new_swapped_mobj, array_mobj, path_arc=PI/2), run_time=0.5)
        self.wait(0.5)
