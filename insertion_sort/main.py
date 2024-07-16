import random
from textwrap import dedent

from manim import *

from insertion_sort.array import Array


small = [10, 2, 7, 5, 3]
medium = [2, 7, 10, 5, 3, -1]
large = [12, 3, 5, 9, 4, 1, 7]
ORANGE = ManimColor('#fa541c')
BLUE_BACKGROUND = ManimColor('#ADD8E6')
random.seed(42)


class Introduction(Scene):
    def construct(self):
        # Create vertical bars representing the array and sort them with insertion sort
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

        array_shadow = Array(medium, color=BLACK, cell_type='card')
        array_shadow_mobj = array_shadow.get_mobject().center().shift(1 * UP)
        array = Array(medium[:3], color=BLACK, cell_type='card')
        array_mobj = array.get_mobject().align_to(array_shadow_mobj, LEFT).align_to(array_shadow_mobj, DOWN)
        a_text = Tex('a:').scale(0.9).next_to(array_mobj, LEFT)

        indices = Array(
            [i for i in range(len(array))],
            width=array.width, height=array.height,
            spacing=array.spacing, scale_text=array.scale_text, stroke_color=BLACK,
        )
        indices_mobj = indices.get_mobject().center().next_to(array_mobj, UP, buff=0.4)
        self.play(Create(array_mobj), Create(a_text), Create(indices_mobj), run_time=1)
        self.wait(0.5)

        self.play(LaggedStart(*[
            Indicate(VGroup(cell, label))
            for cell, label in zip(array.cells, array.labels)
        ], lag_ratio=0.4, run_time=1))
        self.wait(0.5)

        def insert(new_value: int, highlight: bool = False, run_time: float = 0.2):
            new_element = Array([new_value], color=BLACK, cell_type='card')
            new_element_mobj = new_element.get_mobject() \
                .align_to(array_mobj, LEFT).align_to(array_mobj, UP) \
                .shift(len(array) * (array.width + array.spacing) * RIGHT) \
                .shift(0.3 * UP).shift(10 * RIGHT)
            self.add(new_element_mobj)
            self.play(new_element_mobj.animate.shift(10 * LEFT), run_time=2 * run_time)

            new_indices = Array(
                [i for i in range(len(array) + 1)],
                width=array.width, height=array.height,
                spacing=array.spacing, scale_text=array.scale_text, stroke_color=BLACK,
            )
            new_indices_mobj = new_indices.get_mobject().align_to(indices_mobj, LEFT).align_to(indices_mobj, UP)
            indices_mobj.become(new_indices_mobj)
            self.wait(run_time)

            # Insert in the right place
            insert_idx = len(array)
            for i in range(len(array) - 1, -1, -1):
                if highlight:
                    self.play(array.cells[i][0].animate.set_color(YELLOW), run_time=run_time)

                if array.values[i] < new_value:
                    if highlight:
                        self.play(array.cells[i][0].animate.set_color(WHITE), run_time=2 * run_time)
                    break

                insert_idx = i
                to_path = ArcBetweenPoints(array.cells[i].get_center(), new_element_mobj.copy().shift(0.3 * DOWN).get_center(), angle=PI / 4)
                from_path = ArcBetweenPoints(new_element_mobj.get_center(), array.cells[i].copy().shift(0.3 * UP).get_center(), angle=PI / 4)
                self.play(
                    MoveAlongPath(VGroup(array.cells[i], array.labels[i]), path=to_path),
                    MoveAlongPath(new_element_mobj, path=from_path),
                    run_time=run_time,
                )

                if highlight:
                    self.play(array.cells[i][0].animate.set_color(WHITE), run_time=run_time)
            self.wait(run_time)

            self.play(new_element_mobj.animate.shift(0.3 * DOWN), run_time=run_time)
            array.values.insert(insert_idx, new_element.values[0])
            array.cells.insert(insert_idx, new_element.cells[0])
            array.labels.insert(insert_idx, new_element.labels[0])
            array.color.insert(insert_idx, new_element.color[0])
            print(f'Array became: {array.values}')
            array_mobj.add(new_element_mobj)
            self.wait(run_time)

        insert(medium[3], run_time=0.6)
        insert(medium[4], highlight=True, run_time=0.5)
        insert(medium[5], highlight=True, run_time=0.4)
        self.wait(0.1)

        # Transition to the next scene
        new_array = Array(small, color=BLACK, cell_type='card')
        new_array_mobj = new_array.get_mobject().center().shift(1 * UP)
        indices_mobj.submobjects.pop()
        indices_mobj.submobjects.pop()

        self.play(
            ReplacementTransform(array_mobj, new_array_mobj),
            indices_mobj.animate.next_to(new_array_mobj, UP, buff=0.4),
            a_text.animate.scale(0.9).next_to(new_array_mobj, LEFT),
            run_time=0.5,
        )
        self.wait(0.5)
