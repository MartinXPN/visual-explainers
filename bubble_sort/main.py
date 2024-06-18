import random
from textwrap import dedent

from manim import *

from bubble_sort.array import Array, TransformMatchingCells
from bubble_sort.clock import Clock

a = [12, 3, 5, 9, 4, 1, 7]
ORANGE = ManimColor('#fa541c')
BLUE_BACKGROUND = ManimColor('#ADD8E6')


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


def swap(array: Array, array_mobj: VGroup, i: int, j: int, aligned_edge=ORIGIN):
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
        cell_type=array.cell_type,
    )

    new_array_mobj = new_array.get_mobject().move_to(array_mobj, aligned_edge=aligned_edge)
    for i in range(len(array.labels)):
        if array.cell_type == 'rectangle':
            new_array.cells[i].set_stroke(
                color=array.cells[i].get_stroke_color(),
                width=array.cells[i].get_stroke_width(),
            )
        else:
            for j in range(len(new_array.cells[i])):
                new_array.cells[i][j].set_fill(color=array.cells[i][j].get_fill_color())

    return new_array, new_array_mobj


def highlight(array: Array, start: int, end: int, color: ManimColor, width=5.):
    if array.cell_type == 'rectangle':
        return [
            *[rect.animate.set_stroke(color=color, width=width) for rect in array.cells[start: end]],
        ]
    else:    # SVG => change the background color (id="background")
        darker = interpolate_color(color, BLACK, 0.1)
        return [
            *[rect[1].animate.set_fill(color=color) for rect in array.cells[start: end]],
            *[rect[3].animate.set_fill(color=darker) for rect in array.cells[start: end]],
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
        self.play(TransformMatchingCells(new_swapped_mobj, array_mobj, path_arc=PI/3), run_time=0.5)
        self.wait(0.1)

        # Run bubble-sort animation for 1 sweep
        def sweep(run_times: list):
            nonlocal array, array_mobj
            for i, time in enumerate(run_times):
                self.play(*highlight(array, i, i + 2, ORANGE, 5), run_time=time)
                self.wait(time)
                if array.values[i] > array.values[i + 1]:
                    new_array, new_array_mobj = swap(array, array_mobj, i, i + 1)
                    self.play(TransformMatchingCells(array_mobj, new_array_mobj, path_arc=PI/3), run_time=time * 7)
                    self.wait(time)
                    array, array_mobj = new_array, new_array_mobj
                else:
                    self.play(Indicate(array.labels[i]), run_time=3 * time)
                    self.play(Indicate(array.labels[i + 1]), run_time=3 * time)

                self.play(*highlight(array, i, i + 1, WHITE, 2), run_time=time / 10)
            self.play(*highlight(array, 0, len(array), WHITE, 2), run_time=0.1)

        sweep([0.1, 0.1, 0.07, 0.07, 0.07, 0.07])
        self.wait(0.1)
        sweep([0.1, 0.1, 0.07, 0.07, 0.07])
        self.wait(0.1)

        # Circumscribe the last 2 elements
        self.play(Circumscribe(array.labels[-1], Circle), run_time=0.5)
        self.play(Circumscribe(array.labels[-2], Circle), run_time=0.5)
        self.wait(0.1)

        self.play(ReplacementTransform(title, Title('Bubble Sort', include_underline=False)), run_time=0.5)
        initial_array = Array(a)
        initial_array_mobj = initial_array.get_mobject().center().shift(1.5 * UP)
        self.play(TransformMatchingCells(array_mobj, initial_array_mobj, path_arc=PI/3), run_time=0.5)
        self.wait(1)


class IntuitionBehindNaming(Scene):
    def construct(self):
        title = Title('Bubble Sort', include_underline=False)
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
        self.add(a_text, array_mobj, indices_mobj)
        self.wait(0.1)

        # Turn all the cell rectangles into bubbles
        array_mobj.z_index = 1
        for i, cell in enumerate(array.cells):
            bubble = SVGMobject(
                'bubble_sort/bubble.svg',
            ).scale(0.25 + (0.03 * array.values[i])).move_to(cell.get_center())
            self.play(
                ReplacementTransform(cell, bubble),
                array.labels[i].animate.set_color(BLACK),
                run_time=0.06,
            )
            array.cells[i] = bubble
            self.wait(0.1)

        array.cell_type = 'bubble'
        array.color = BLACK

        # Run bubble-sort animation for 1 sweep
        def sweep(run_times: list):
            nonlocal array, array_mobj
            for i, time in enumerate(run_times):
                self.play(*highlight(array, i, i + 2, ORANGE, 5), run_time=time)
                self.wait(time)
                if array.values[i] > array.values[i + 1]:
                    new_array, new_array_mobj = swap(array, array_mobj, i, i + 1, aligned_edge=RIGHT if i == 0 else LEFT)
                    self.play(TransformMatchingCells(array_mobj, new_array_mobj, path_arc=PI/3), run_time=time * 7)
                    self.wait(time)
                    array, array_mobj = new_array, new_array_mobj
                else:
                    self.wait(2 * time)

                self.play(*highlight(array, i, i + 1, BLUE_BACKGROUND, 0), run_time=time / 10)
            self.play(*highlight(array, 0, len(array), BLUE_BACKGROUND, 0), run_time=0.1)

        # Sweep + Highlight 12 at the end
        sweep([0.07, 0.06, 0.05, 0.05, 0.06, 0.06])
        self.play(Indicate(array.labels[-1], scale_factor=2, color=ORANGE), run_time=0.5)
        self.wait(0.1)

        # Sweep + Highlight 9 at the end
        sweep([0.07, 0.06, 0.05, 0.06, 0.06])
        self.play(Indicate(array.labels[-2], scale_factor=2, color=ORANGE), run_time=0.5)
        self.wait(0.1)

        sweep([0.05, 0.05, 0.05, 0.05])
        sweep([0.05, 0.05, 0.05])
        sweep([0.05, 0.05])
        sweep([0.05])

        for i in range(len(array)):
            self.play(*highlight(array, i, i + 1, ORANGE, 5), run_time=0.1)
            self.play(*highlight(array, i, i + 1, BLUE_BACKGROUND, 0), run_time=0.01)
        self.wait(0.1)

        # Change the bubbles back to rectangles
        rectangles = [
            Rectangle(
                height=array.height,
                width=array.width,
                fill_color=array.fill_color,
                fill_opacity=array.fill_opacity,
                stroke_width=array.stroke_width[i],
                stroke_color=array.stroke_color[i],
            ).move_to(cell.get_center())
            for i, cell in enumerate(array.cells)
        ]
        self.play(*[
            ReplacementTransform(cell, rectangle)
            for cell, rectangle in zip(array.cells, rectangles)
        ], *[
            array.labels[i].animate.set_color(WHITE)
            for i in range(len(array.labels))
        ], run_time=2)
        array.cells = rectangles
        self.wait(0.1)

        # Bring back the bubbles
        bubbles = [
            SVGMobject(
                'bubble_sort/bubble.svg',
            ).scale(0.25 + (0.03 * array.values[i])).move_to(cell.get_center())
            for i, cell in enumerate(array.cells)
        ]
        self.play(*[
            ReplacementTransform(cell, bubble)
            for cell, bubble in zip(array.cells, bubbles)
        ], *[
            array.labels[i].animate.set_color(BLACK)
            for i in range(len(array.labels))
        ], run_time=2)
        array.cells = bubbles
        self.wait(0.1)

        # Bring the array to the initial state
        initial_array = Array(a, color=BLACK, cell_type='bubble')
        initial_array_mobj = initial_array.get_mobject().center().shift(1.5 * UP)
        self.play(TransformMatchingCells(array_mobj, initial_array_mobj, path_arc=PI/3), run_time=0.5)
        self.wait(1)


class IntuitionDetails(Scene):
    def construct(self):
        title = Title('Bubble Sort', include_underline=False)
        self.add(title)

        array = Array(a, color=BLACK, cell_type='bubble')
        array_mobj = array.get_mobject().center().shift(1.5 * UP)
        a_text = Tex('a:').scale(0.9).next_to(array_mobj, LEFT)

        indices = Array(
            [i for i in range(len(array))],
            width=array.width, height=array.height,
            spacing=array.spacing, scale_text=array.scale_text, stroke_color=BLACK,
        )
        indices_mobj = indices.get_mobject().center().next_to(array_mobj, 0.1 * UP)
        self.add(a_text, array_mobj, indices_mobj)
        self.wait(0.1)

        # Run bubble-sort animation for 1 sweep
        def sweep(run_times: list):
            nonlocal array, array_mobj
            for i, time in enumerate(run_times):
                self.play(*highlight(array, i, i + 2, ORANGE, 5), run_time=time)
                self.wait(time)
                if array.values[i] > array.values[i + 1]:
                    new_array, new_array_mobj = swap(array, array_mobj, i, i + 1, aligned_edge=RIGHT if i == 0 else LEFT)
                    self.play(TransformMatchingCells(array_mobj, new_array_mobj, path_arc=PI/3), run_time=time * 7)
                    self.wait(time)
                    array, array_mobj = new_array, new_array_mobj
                else:
                    self.wait(2 * time)

                self.play(*highlight(array, i, i + 1, BLUE_BACKGROUND, 0), run_time=time / 10)
            self.play(*highlight(array, 0, len(run_times) + 1, BLUE_BACKGROUND, 0), run_time=0.1)

        sweep([0.08, 0.07, 0.05, 0.05, 0.05, 0.05])
        self.play(Indicate(array.labels[-1], scale_factor=2, color=ORANGE), run_time=0.5)
        self.play(*highlight(array, 6, 7, GREEN, 5), run_time=0.1)
        self.wait(0.1)

        sweep([0.09, 0.07, 0.05, 0.05, 0.05])
        self.play(Indicate(array.labels[-2], scale_factor=2, color=ORANGE), run_time=0.5)
        self.play(*highlight(array, 5, 6, GREEN, 5), run_time=0.1)
        self.wait(0.1)

        self.play(Indicate(array.labels[-2], scale_factor=2, color=ORANGE), run_time=0.5)
        self.play(Indicate(array.labels[-1], scale_factor=2, color=ORANGE), run_time=0.5)
        self.wait(0.1)

        sweep([0.05, 0.05, 0.05, 0.05])
        self.play(Indicate(array.labels[-3], scale_factor=2, color=ORANGE), run_time=0.5)
        self.play(*highlight(array, 4, 5, GREEN, 5), run_time=0.1)
        self.wait(0.1)

        self.play(Indicate(array.labels[-4], scale_factor=2, color=ORANGE), run_time=0.5)
        self.wait(0.1)

        sweep([0.05, 0.05, 0.05])
        self.play(*highlight(array, 3, 4, GREEN, 5), run_time=0.1)
        self.wait(0.1)

        # Indicate one by one 4, 5, 7, 9, 12
        for label in array.labels[2:]:
            self.play(Indicate(label, scale_factor=2, color=ORANGE), run_time=0.3)
            self.wait(0.1)

        sweep([0.05, 0.05])
        self.play(*highlight(array, 2, 3, GREEN, 5), run_time=0.1)
        self.wait(0.1)

        # Indicate one by one all the elements from left to right
        for label in array.labels:
            self.play(Indicate(label, scale_factor=2, color=ORANGE), run_time=0.3)
            self.wait(0.1)

        sweep([0.05])
        self.play(*highlight(array, 1, 2, GREEN, 5), run_time=0.1)
        self.wait(0.1)
        self.play(*highlight(array, 0, 1, GREEN, 5), run_time=0.1)
        self.wait(0.1)

        # Highlight with BLUE_BACKGROUND one by one from right to left
        for i in range(len(array) - 1, -1, -1):
            self.play(*highlight(array, i, i + 1, ORANGE, 0), run_time=0.2)
            self.play(*highlight(array, i, i + 1, BLUE_BACKGROUND, 0), run_time=0.1)
            self.wait(0.1)

        # Brace for all the elements with n at the bottom
        brace = Brace(indices_mobj, DOWN, color=ORANGE).move_to(array_mobj, DOWN).shift(0.4 * DOWN)
        n = brace.get_text('n', buff=0.1).set_color(ORANGE)
        self.play(Create(brace), Create(n), run_time=0.2)
        self.wait(0.1)

        # Bring the array to the initial state
        initial_array = Array(a, color=BLACK, cell_type='bubble')
        initial_array_mobj = initial_array.get_mobject().center().shift(1.5 * UP)
        self.play(TransformMatchingCells(array_mobj, initial_array_mobj, path_arc=PI/3), run_time=0.5)
        self.wait(0.1)


class IntuitionBehindN1Loops(Scene):
    def construct(self):
        title = Title('Bubble Sort', include_underline=False)
        self.add(title)

        array = Array(a, color=BLACK, cell_type='bubble')
        array_mobj = array.get_mobject().center().shift(1.5 * UP)
        a_text = Tex('a:').scale(0.9).next_to(array_mobj, LEFT)

        indices = Array(
            [i for i in range(len(array))],
            width=array.width, height=array.height,
            spacing=array.spacing, scale_text=array.scale_text, stroke_color=BLACK,
        )
        indices_mobj = indices.get_mobject().center().next_to(array_mobj, 0.1 * UP)
        self.add(a_text, array_mobj, indices_mobj)

        brace = Brace(indices_mobj, DOWN, color=ORANGE).move_to(array_mobj, DOWN).shift(0.4 * DOWN)
        n = brace.get_text('n', buff=0.1).set_color(ORANGE)
        self.add(brace, n)
        self.wait(0.1)

        # Add counter = 0
        counter = Variable(0, Text('Loops'), var_type=Integer, color=ORANGE).next_to(n, DOWN).shift(0.5 * DOWN)
        self.play(Write(counter), run_time=0.5)
        self.wait(0.1)

        # Run bubble-sort animation for 1 sweep
        def sweep(run_times: list):
            nonlocal array, array_mobj
            for i, time in enumerate(run_times):
                self.play(*highlight(array, i, i + 2, ORANGE, 5), run_time=time)
                self.wait(time)
                if array.values[i] > array.values[i + 1]:
                    new_array, new_array_mobj = swap(array, array_mobj, i, i + 1, aligned_edge=RIGHT if i == 0 else LEFT)
                    self.play(TransformMatchingCells(array_mobj, new_array_mobj, path_arc=PI/3), run_time=time * 7)
                    self.wait(time)
                    array, array_mobj = new_array, new_array_mobj
                else:
                    self.wait(2 * time)

                self.play(*highlight(array, i, i + 1, BLUE_BACKGROUND, 0), run_time=time / 10)
            self.play(*highlight(array, 0, len(run_times) + 1, BLUE_BACKGROUND, 0), run_time=0.1)

        sweep([0.04, 0.04, 0.04, 0.04, 0.04, 0.04])
        self.play(*highlight(array, 6, 7, GREEN, 5), run_time=0.1)
        self.play(counter.tracker.animate.set_value(1), run_time=0.5)
        self.wait(0.1)

        sweep([0.04, 0.04, 0.04, 0.04, 0.04])
        self.play(*highlight(array, 5, 6, GREEN, 5), run_time=0.1)
        self.play(counter.tracker.animate.set_value(2), run_time=0.5)
        self.wait(0.1)

        sweep([0.04, 0.04, 0.04, 0.04])
        self.play(*highlight(array, 4, 5, GREEN, 5), run_time=0.1)
        self.play(counter.tracker.animate.set_value(3), run_time=0.5)
        self.wait(0.1)

        sweep([0.04, 0.04, 0.04])
        self.play(*highlight(array, 3, 4, GREEN, 5), run_time=0.1)
        self.play(counter.tracker.animate.set_value(4), run_time=0.5)
        self.wait(0.1)

        sweep([0.04, 0.04])
        self.play(*highlight(array, 2, 3, GREEN, 5), run_time=0.1)
        self.play(counter.tracker.animate.set_value(5), run_time=0.5)
        self.wait(0.1)

        sweep([0.04])
        self.play(*highlight(array, 1, 2, GREEN, 5), run_time=0.1)
        self.play(counter.tracker.animate.set_value(6), run_time=0.5)
        self.wait(0.1)

        self.play(Indicate(counter.value, scale_factor=2, color=ORANGE), run_time=0.5)
        final_count = Text('Loops')
        final_count.add(MathTex(' = n - 1').next_to(final_count, RIGHT).shift(0.03 * UP))
        final_count.move_to(counter, DOWN).move_to(counter, LEFT)
        self.play(
            FadeOut(counter),
            FadeIn(final_count), run_time=0.5)
        self.wait(0.1)

        self.play(ReplacementTransform(title, Title('Bubble Sort Implementation', include_underline=False)), run_time=0.5)
        # Bring back the initial array
        initial_array = Array(a, color=BLACK, cell_type='bubble')
        initial_array_mobj = initial_array.get_mobject().center().shift(1.5 * UP)
        self.play(TransformMatchingCells(array_mobj, initial_array_mobj, path_arc=PI/3), run_time=0.5)
        self.wait(1)

        self.play(Indicate(final_count, scale_factor=2, color=ORANGE), run_time=0.5)
        self.wait(1)
        self.play(FadeOut(final_count, brace, n), run_time=0.1)


class Implementation(Scene):
    def construct(self):
        title = Title('Bubble Sort Implementation', include_underline=False)
        self.add(title)

        array = Array(a, color=BLACK, cell_type='bubble')
        array_mobj = array.get_mobject().center().shift(1.5 * UP)
        a_text = Tex('a:').scale(0.9).next_to(array_mobj, LEFT)

        indices = Array(
            [i for i in range(len(array))],
            width=array.width, height=array.height,
            spacing=array.spacing, scale_text=array.scale_text, stroke_color=BLACK,
        )
        indices_mobj = indices.get_mobject().center().next_to(array_mobj, 0.1 * UP)
        self.add(a_text, array_mobj, indices_mobj)

        code = Code(
            code=dedent('''
                for _ in range(len(a) - 1):
                    for i in range(len(a) - 1):
                        if a[i] > a[i + 1]:
                            a[i], a[i + 1] = a[i + 1], a[i]
            ''').strip(),
            tab_width=4,
            language='Python',
            line_spacing=0.6,
            font='Monospace',
            style='monokai',
        ).next_to(array_mobj, DOWN).shift(0.5 * RIGHT).code

        # Type the first line of the code
        self.play(AddTextLetterByLetter(code.chars[0], run_time=0.05 * len(code.chars[0])))
        self.wait(0.1)

        self.play(AddTextLetterByLetter(code.chars[1], run_time=0.05 * len(code.chars[1])))
        self.wait(0.1)

        # Indicate len(a) - 1
        self.play(Indicate(code.chars[1][-12: -2], scale_factor=1.2), run_time=1)
        self.wait(0.1)

        self.play(AddTextLetterByLetter(code.chars[2], run_time=0.05 * len(code.chars[2])))
        self.play(AddTextLetterByLetter(code.chars[3], run_time=0.05 * len(code.chars[3])))
        self.wait(0.1)

        # Circumscribe the code
        self.play(Circumscribe(code), run_time=0.5)
        self.wait(0.1)


class Optimization1(Scene):
    def construct(self):
        title = Title('Bubble Sort Implementation', include_underline=False)
        self.add(title)

        array = Array(a, color=BLACK, cell_type='bubble')
        array_mobj = array.get_mobject().center().shift(1.5 * UP)
        a_text = Tex('a:').scale(0.9).next_to(array_mobj, LEFT)

        indices = Array(
            [i for i in range(len(array))],
            width=array.width, height=array.height,
            spacing=array.spacing, scale_text=array.scale_text, stroke_color=BLACK,
        )
        indices_mobj = indices.get_mobject().center().next_to(array_mobj, 0.1 * UP)
        self.add(a_text, array_mobj, indices_mobj)

        code = Code(
            code=dedent('''
                for _ in range(len(a) - 1):
                    for i in range(len(a) - 1):
                        if a[i] > a[i + 1]:
                            a[i], a[i + 1] = a[i + 1], a[i]
            ''').strip(),
            tab_width=4,
            language='Python',
            line_spacing=0.6,
            font='Monospace',
            style='monokai',
        ).next_to(array_mobj, DOWN).shift(0.5 * RIGHT).code
        self.add(code)

        self.play(Indicate(code.chars[1], run_time=0.5))
        self.play(Indicate(code.chars[-1], run_time=0.5))
        self.wait(0.1)

        # Run bubble-sort animation for 1 sweep
        def sweep(run_times: list):
            nonlocal array, array_mobj
            for i, time in enumerate(run_times):
                self.play(*highlight(array, i, i + 2, ORANGE, 5), run_time=time)
                self.wait(time)
                if array.values[i] > array.values[i + 1]:
                    new_array, new_array_mobj = swap(array, array_mobj, i, i + 1, aligned_edge=RIGHT if i == 0 else LEFT)
                    self.play(TransformMatchingCells(array_mobj, new_array_mobj, path_arc=PI/3), run_time=time * 7)
                    self.wait(time)
                    array, array_mobj = new_array, new_array_mobj
                else:
                    self.wait(2 * time)

                self.play(*highlight(array, i, i + 1, BLUE_BACKGROUND, 0), run_time=time / 10)
            self.play(*highlight(array, 0, len(run_times) + 1, BLUE_BACKGROUND, 0), run_time=0.1)

        sweep([0.04, 0.04, 0.04, 0.04, 0.04, 0.04])
        self.play(*highlight(array, 6, 7, GREEN, 5), run_time=0.1)
        self.wait(0.1)

        sweep([0.04, 0.04, 0.04, 0.04, 0.04])
        self.play(*highlight(array, 5, 6, GREEN, 5), run_time=0.1)
        self.wait(0.1)

        self.play(Circumscribe(VGroup(*array.cells[:-2]), run_time=0.5))
        self.play(Indicate(code.chars[0], run_time=0.5))

        optimized_code = Code(
            code=dedent('''
                for u in range(len(a) - 1, 0, -1):
                    for i in range(u):
                        if a[i] > a[i + 1]:
                            a[i], a[i + 1] = a[i + 1], a[i]
            ''').strip(),
            tab_width=4,
            language='Python',
            line_spacing=0.6,
            font='Monospace',
            style='monokai',
        ).next_to(array_mobj, DOWN).shift(0.3 * RIGHT).code

        self.play(Indicate(array.cells[-1], run_time=0.5))
        self.play(Indicate(array.cells[-2], run_time=0.5))
        self.play(Indicate(array.cells[-3], run_time=0.5))
        self.wait(0.1)

        self.play(RemoveTextLetterByLetter(code.chars[0], run_time=0.05 * len(code.chars[0])))
        self.play(AddTextLetterByLetter(optimized_code.chars[0], run_time=0.05 * len(optimized_code.chars[0])))

        self.play(RemoveTextLetterByLetter(code.chars[-1], run_time=0.05 * len(code.chars[1])))
        self.play(AddTextLetterByLetter(optimized_code.chars[-1], run_time=0.05 * len(optimized_code.chars[-1])))

        code.become(optimized_code)
        self.play(ApplyWave(code, run_time=0.5))


class Optimization2(Scene):
    def construct(self):
        title = Title('Bubble Sort Implementation', include_underline=False)
        self.add(title)

        array = Array([3, 5, 4, 1, 7, 9, 12], color=BLACK, cell_type='bubble')
        array_mobj = array.get_mobject().center().shift(1.5 * UP)
        a_text = Tex('a:').scale(0.9).next_to(array_mobj, LEFT)

        # Highlight (without any animation) the last 2 cells and make them green
        darker = interpolate_color(GREEN, BLACK, 0.1)
        for rect in array.cells[-2:]:
            rect[1].set_fill(color=GREEN)
            rect[3].set_fill(color=darker)

        indices = Array(
            [i for i in range(len(array))],
            width=array.width, height=array.height,
            spacing=array.spacing, scale_text=array.scale_text, stroke_color=BLACK,
        )
        indices_mobj = indices.get_mobject().center().next_to(array_mobj, 0.1 * UP)
        self.add(a_text, array_mobj, indices_mobj)

        code = Code(
            code=dedent('''
                for u in range(len(a) - 1, 0, -1):
                    for i in range(u):
                        if a[i] > a[i + 1]:
                            a[i], a[i + 1] = a[i + 1], a[i]
            ''').strip(),
            tab_width=4,
            language='Python',
            line_spacing=0.6,
            font='Monospace',
            style='monokai',
        ).next_to(array_mobj, DOWN).shift(0.3 * RIGHT).code
        self.add(code)

        # Run bubble-sort animation for 1 sweep
        def sweep(run_times: list):
            nonlocal array, array_mobj
            for i, time in enumerate(run_times):
                self.play(*highlight(array, i, i + 2, ORANGE, 5), run_time=time)
                self.wait(time)
                if array.values[i] > array.values[i + 1]:
                    new_array, new_array_mobj = swap(array, array_mobj, i, i + 1, aligned_edge=RIGHT if i == 0 else LEFT)
                    self.play(TransformMatchingCells(array_mobj, new_array_mobj, path_arc=PI/3), run_time=time * 7)
                    self.wait(time)
                    array, array_mobj = new_array, new_array_mobj
                else:
                    self.wait(2 * time)

                self.play(*highlight(array, i, i + 1, BLUE_BACKGROUND, 0), run_time=time / 10)
            self.play(*highlight(array, 0, len(run_times) + 1, BLUE_BACKGROUND, 0), run_time=0.1)

        sweep([0.04, 0.04, 0.04, 0.04])
        self.play(*highlight(array, 4, 5, GREEN, 5), run_time=0.1)

        self.play(
            Indicate(array.cells[-1]),
            Indicate(array.cells[-2]),
            Indicate(array.cells[-3]),
            Indicate(array.cells[-4]),
            run_time=0.5
        )
        self.play(Indicate(code.chars[0], run_time=0.5))

        sweep([0.04, 0.04, 0.04])
        self.play(*highlight(array, 3, 4, GREEN, 5), run_time=0.1)
        sweep([0.04])
        self.play(*highlight(array, 2, 3, GREEN, 5), run_time=0.1)

        optimized_code = Code(
            code=dedent('''
                for u in range(len(a) - 1, 0, -1):
                    changed = False
                    for i in range(u):
                        if a[i] > a[i + 1]:
                            a[i], a[i + 1] = a[i + 1], a[i]
                            changed = True
                    if not changed:
                        break
            ''').strip(),
            tab_width=4,
            language='Python',
            line_spacing=0.6,
            font='Monospace',
            style='monokai',
        ).next_to(array_mobj, DOWN).shift(0.15 * DOWN).shift(0.25 * RIGHT).code

        self.play(VGroup(*code.chars[1:]).animate.shift(0.6 * DOWN), run_time=0.1)
        self.wait(0.1)
        self.play(AddTextLetterByLetter(optimized_code.chars[1], run_time=0.05 * len(optimized_code.chars[1])))
        self.wait(0.1)

        self.play(AddTextLetterByLetter(optimized_code.chars[5], run_time=0.05 * len(optimized_code.chars[2])))
        self.wait(0.1)

        # Indicate the inner loop along with its contents
        self.play(Indicate(VGroup(code.chars[1], code.chars[2], code.chars[3], optimized_code.chars[5]), run_time=0.5))

        self.play(AddTextLetterByLetter(optimized_code.chars[6], run_time=0.05 * len(optimized_code.chars[6])))
        self.play(AddTextLetterByLetter(optimized_code.chars[7], run_time=0.05 * len(optimized_code.chars[7])))
        self.wait(0.1)

        for i, time in enumerate([0.04] * len(array)):
            self.play(*highlight(array, i, i + 2, ORANGE, 5), run_time=time)
            self.wait(time)
            self.play(*highlight(array, i, i + 1, BLUE_BACKGROUND, 0), run_time=time / 10)

        self.play(ReplacementTransform(title, Title('Bubble Sort', include_underline=False)), run_time=0.5)
        self.wait(0.1)

        # Bring the array to the initial state
        initial_array = Array(a, color=BLACK, cell_type='bubble')
        initial_array_mobj = initial_array.get_mobject().center().shift(1.5 * UP)
        self.play(TransformMatchingCells(array_mobj, initial_array_mobj, path_arc=PI/3), run_time=0.5)
        self.wait(1)


class Simulation(Scene):
    def construct(self):
        title = Title('Bubble Sort', include_underline=False)
        self.add(title)

        array = Array(a, color=BLACK, cell_type='bubble')
        array_mobj = array.get_mobject().center().shift(1.5 * UP)
        a_text = Tex('a:').scale(0.9).next_to(array_mobj, LEFT)

        indices = Array(
            [i for i in range(len(array))],
            width=array.width, height=array.height,
            spacing=array.spacing, scale_text=array.scale_text, stroke_color=BLACK,
        )
        indices_mobj = indices.get_mobject().center().next_to(array_mobj, 0.1 * UP)
        self.add(a_text, array_mobj, indices_mobj)

        code = Code(
            code=dedent('''
                for u in range(len(a) - 1, 0, -1):
                    changed = False
                    for i in range(u):
                        if a[i] > a[i + 1]:
                            a[i], a[i + 1] = a[i + 1], a[i]
                            changed = True
                    if not changed:
                        break
            ''').strip(),
            tab_width=4,
            language='Python',
            line_spacing=0.6,
            font='Monospace',
            style='monokai',
        ).next_to(array_mobj, DOWN).shift(0.15 * DOWN).shift(0.25 * RIGHT).code
        self.add(code)

        self.play(VGroup(*code.chars).animate.shift(1.5 * LEFT))
        self.wait(0.1)

        # Arrow to show which part of the code is being executed
        arrow = Arrow(
            start=LEFT, end=RIGHT, color=RED, buff=0.1,
            stroke_width=10, max_stroke_width_to_length_ratio=15,
            max_tip_length_to_length_ratio=0.5, tip_length=0.2,
        ).scale(0.3).next_to(code, LEFT).align_to(code, UP).shift(0.08 * DOWN)
        self.play(Create(arrow), run_time=0.5)

        # show real-time values to better understand the code
        def get_debug(u, changed, i):
            res = Code(
                code=dedent(f'''
                # {u}
                # {changed}
                # {i}
                ''').strip(),
                tab_width=4,
                language='Python',
                line_spacing=0.6,
                font='Monospace',
                style='monokai',
            ).next_to(code, RIGHT).align_to(code, UP).shift(0.25 * UP).code
            return res

        def before_sweep(u: int):
            debug = get_debug(u, False, 0)
            self.play(AddTextLetterByLetter(debug.chars[0], run_time=0.05 * len(debug.chars[0])))
            self.wait(0.5)

            self.play(arrow.animate.shift(0.4 * DOWN), run_time=0.2)
            self.wait(0.1)
            self.play(AddTextLetterByLetter(debug.chars[1], run_time=0.05 * len(debug.chars[1])))
            self.wait(0.1)

            # Move the arrow to the inner loop
            self.play(arrow.animate.shift(0.4 * DOWN), run_time=0.2)
            return debug

        # Run bubble-sort animation for 1 sweep
        def sweep(run_times: list, u: int):
            nonlocal array, array_mobj, debug
            debugs = [debug]
            changed = entered_if = False
            for i, time in enumerate(run_times):
                # Add the debug value for the current iteration
                debug = get_debug(u, changed, i)
                debugs.append(debug)
                self.play(ReplacementTransform(debugs[-2].chars[2], debugs[-1].chars[2]), run_time=time)
                self.wait(time)

                self.play(arrow.animate.shift(0.4 * DOWN), run_time=time)
                self.play(*highlight(array, i, i + 2, ORANGE, 5), run_time=time)
                self.wait(2 * time)
                entered_if = False
                if array.values[i] > array.values[i + 1]:
                    entered_if = True
                    self.play(arrow.animate.shift(0.4 * DOWN), run_time=time)
                    new_array, new_array_mobj = swap(array, array_mobj, i, i + 1, aligned_edge=RIGHT if i == 0 else LEFT)
                    self.play(TransformMatchingCells(array_mobj, new_array_mobj, path_arc=PI/3), run_time=time * 7)
                    self.play(arrow.animate.shift(0.4 * DOWN), run_time=time)
                    if not changed:
                        self.play(*[RemoveTextLetterByLetter(d.chars[1], run_time=0.01 * len(d.chars[1])) for d in debugs])
                        changed = True
                        debug = get_debug(u, changed, i)
                        debugs.append(debug)
                        self.play(AddTextLetterByLetter(debug.chars[1], run_time=0.05 * len(debug.chars[1])))
                    self.wait(time)
                    array, array_mobj = new_array, new_array_mobj
                else:
                    self.wait(2 * time)

                # Move to the start of the inner loop
                if i != len(run_times) - 1:
                    self.remove(*[d.chars[2] for d in debugs[:-1]])
                    self.play(
                        arrow.animate.shift(1.2 * UP if entered_if else 0.4 * UP),
                        run_time=time,
                    )

                self.play(*highlight(array, i, i + 1, BLUE_BACKGROUND, 0), run_time=time / 10)

            # Move to the `if not changed` part
            self.play(
                arrow.animate.shift(0.4 * DOWN if entered_if else 1.2 * DOWN),
                *highlight(array, len(run_times), len(run_times) + 1, GREEN, 5),
                run_time=0.2,
            )
            self.wait(0.1)
            if not changed:
                self.play(arrow.animate.shift(0.4 * DOWN), run_time=0.2)
            else:
                self.play(arrow.animate.shift(2.4 * UP), run_time=0.2)
            self.wait(0.1)

            # Make sure we properly delete the unnecessary debug values
            self.add(debugs[-1])
            self.remove(*[d.chars[2] for d in debugs[:-1]])
            self.remove(*[d.chars[1] for d in debugs[:-1]])
            self.remove(*[d.chars[0] for d in debugs[:-1]])
            self.play(RemoveTextLetterByLetter(debugs[-1].chars[2], run_time=0.01 * len(debugs[-1].chars[2])))
            self.play(RemoveTextLetterByLetter(debugs[-1].chars[1], run_time=0.01 * len(debugs[-1].chars[1])))
            self.play(RemoveTextLetterByLetter(debugs[-1].chars[0], run_time=0.01 * len(debugs[-1].chars[0])))

        debug = before_sweep(6)
        sweep([0.08, 0.08, 0.08, 0.08, 0.08, 0.08], 6)
        self.wait(0.1)

        debug = before_sweep(5)
        sweep([0.08, 0.08, 0.08, 0.08, 0.08], 5)
        self.wait(0.1)

        debug = before_sweep(4)
        sweep([0.08, 0.08, 0.08, 0.08], 4)
        self.wait(0.1)

        debug = before_sweep(3)
        sweep([0.08, 0.08, 0.08], 3)
        self.wait(0.1)

        debug = before_sweep(2)
        sweep([0.08, 0.08], 2)
        self.wait(0.1)

        debug = before_sweep(1)
        sweep([0.08], 1)
        self.wait(0.1)

        self.play(FadeOut(arrow), run_time=0.1)
        self.wait(0.1)

        self.play(*highlight(array, 0, len(array), BLUE_BACKGROUND, 0), run_time=0.5)
        for cell in array.cells:
            self.play(Indicate(cell, scale_factor=1.5), run_time=0.2)
        self.wait(0.1)

        # Transition to the next scene
        new_a = [12, 7, 5, 7, 7, 1, 7]
        new_array = Array(new_a, color=BLACK, cell_type='bubble')
        new_array_mobj = new_array.get_mobject().center().shift(1.5 * UP)
        self.play(TransformMatchingCells(array_mobj, new_array_mobj, path_arc=PI/3), run_time=0.5)

        self.play(VGroup(*code.chars).animate.shift(1.5 * RIGHT))
        self.wait(0.1)


class StableSorting(Scene):
    def construct(self):
        title = Title('Bubble Sort', include_underline=False)
        self.add(title)

        array = Array([12, 7, 5, 7, 7, 1, 7], color=BLACK, cell_type='bubble')
        array_mobj = array.get_mobject().center().shift(1.5 * UP)
        a_text = Tex('a:').scale(0.9).next_to(array_mobj, LEFT)

        indices = Array(
            [i for i in range(len(array))],
            width=array.width, height=array.height,
            spacing=array.spacing, scale_text=array.scale_text, stroke_color=BLACK,
        )
        indices_mobj = indices.get_mobject().center().next_to(array_mobj, 0.1 * UP)
        self.add(a_text, array_mobj, indices_mobj)

        code = Code(
            code=dedent('''
                for u in range(len(a) - 1, 0, -1):
                    changed = False
                    for i in range(u):
                        if a[i] > a[i + 1]:
                            a[i], a[i + 1] = a[i + 1], a[i]
                            changed = True
                    if not changed:
                        break
            ''').strip(),
            tab_width=4,
            language='Python',
            line_spacing=0.6,
            font='Monospace',
            style='monokai',
        ).next_to(array_mobj, DOWN).shift(0.15 * DOWN).shift(0.25 * RIGHT).code
        self.add(code)
        self.wait(0.1)

        # Highlight different 7s with different colors
        ...

        self.wait(0.1)

