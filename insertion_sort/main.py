import random
from textwrap import dedent

from manim import *

from insertion_sort.array import Array, TransformMatchingCells

small = [10, 2, 7, 5, 3]
medium = [2, 7, 10, 5, 3, -1]
large = [12, 3, 5, 9, 4, 1, 7]
ORANGE = ManimColor('#fa541c')
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
        self.play(Write(title), run_time=2)
        self.wait(1)

        array_shadow = Array(medium, color=BLACK, cell_type='card')
        array_shadow_mobj = array_shadow.get_mobject().center().shift(UP)
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
        self.wait(1.5)

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

        self.wait(1)
        insert(medium[3], run_time=0.7)
        insert(medium[4], highlight=True, run_time=1.1)
        self.wait(3)
        self.play(LaggedStart(*[
            Indicate(VGroup(cell, label))
            for cell, label in zip(array.cells, array.labels)
        ], lag_ratio=0.4, run_time=1))
        self.wait(1)
        insert(medium[5], highlight=True, run_time=0.35)
        self.wait(0.5)

        # Transition to the next scene
        new_array = Array(small, color=BLACK, cell_type='card')
        new_array_mobj = new_array.get_mobject().center().shift(UP)
        indices_mobj.submobjects.pop()
        indices_mobj.submobjects.pop()

        self.play(
            ReplacementTransform(array_mobj, new_array_mobj),
            indices_mobj.animate.next_to(new_array_mobj, UP, buff=0.4),
            a_text.animate.scale(0.9).next_to(new_array_mobj, LEFT),
            run_time=0.5,
        )
        self.wait(0.5)


class IntuitionFull(Scene):
    def construct(self):
        title = Title('Insertion Sort', include_underline=False)
        self.add(title)
        
        array = Array(small.copy(), color=BLACK, cell_type='card')
        array_mobj = array.get_mobject().center().shift(UP)
        a_text = Tex('a:').scale(0.9).next_to(array_mobj, LEFT)
        indices = Array(
            [i for i in range(len(array))],
            width=array.width, height=array.height,
            spacing=array.spacing, scale_text=array.scale_text, stroke_color=BLACK,
        )
        indices_mobj = indices.get_mobject().center().next_to(array_mobj, UP, buff=0.4)
        self.add(array_mobj, a_text, indices_mobj)
        self.wait(3)

        # Shift all to the right and leave 10 on the left
        self.play(
            *[cell.animate.shift(2.5 * RIGHT) for cell in array.cells[1:]],
            *[label.animate.shift(2.5 * RIGHT) for label in array.labels[1:]],
            *[cell.animate.shift(2.5 * RIGHT) for cell in indices.cells[1:]],
            *[label.animate.shift(2.5 * RIGHT) for label in indices.labels[1:]],
            run_time=1,
        )
        self.play(*[index.animate.set_color(BLACK) for index in indices.labels[1:]], run_time=0.5)
        self.wait(2)

        def sort(index: int, highlight: bool = False, run_time: float = 0.2):
            value = array.values[index]
            self.play(
                array.cells[index].animate.shift(0.3 * UP),
                array.labels[index].animate.shift(0.3 * UP),
                run_time=run_time,
            )
            # Shift the index to the left
            self.play(
                indices.cells[index].animate.shift(2.5 * LEFT),
                indices.labels[index].animate.shift(2.5 * LEFT),
                array.cells[index].animate.shift(2.5 * LEFT),
                array.labels[index].animate.shift(2.5 * LEFT),
                run_time=run_time,
            )
            indices.labels[index].set_color(WHITE),

            # Insert in the right place
            for i in range(index, 0, -1):
                if highlight:
                    self.play(array.cells[i - 1][0].animate.set_color(YELLOW), run_time=run_time)

                if array.values[i - 1] < array.values[i]:
                    if highlight:
                        self.play(array.cells[i - 1][0].animate.set_color(WHITE), run_time=2 * run_time)
                    break

                to_path = ArcBetweenPoints(array.cells[i - 1].get_center(), array.cells[i].copy().shift(0.3 * DOWN).get_center(), angle=PI / 4)
                from_path = ArcBetweenPoints(array.cells[i].get_center(), array.cells[i - 1].copy().shift(0.3 * UP).get_center(), angle=PI / 4)
                self.play(
                    MoveAlongPath(VGroup(array.cells[i - 1], array.labels[i - 1]), path=to_path),
                    MoveAlongPath(VGroup(array.cells[i], array.labels[i]), path=from_path),
                    run_time=run_time,
                )
                array.values[i - 1], array.values[i] = array.values[i], array.values[i - 1]
                array.cells[i - 1], array.cells[i] = array.cells[i], array.cells[i - 1]
                array.labels[i - 1], array.labels[i] = array.labels[i], array.labels[i - 1]
                array.color[i - 1], array.color[i] = array.color[i], array.color[i - 1]

                if highlight:
                    self.play(array.cells[i][0].animate.set_color(WHITE), run_time=run_time)

            final_index = array.values.index(value)
            self.play(VGroup(array.cells[final_index], array.labels[final_index]).animate.shift(0.3 * DOWN), run_time=run_time)
            print(f'Array became: {array.values}')

        sort(1, highlight=True, run_time=1)
        self.play(Circumscribe(VGroup(array.cells[0], array.cells[1]), color=ORANGE, buff=0.3, stroke_width=8, run_time=1.5))
        self.wait(2)

        sort(2, highlight=True, run_time=0.9)
        sort(3, highlight=True, run_time=0.4)
        sort(4, highlight=True, run_time=0.45)

        self.play(Circumscribe(array_mobj, color=ORANGE, buff=0.3, stroke_width=8, run_time=2))
        self.wait(2)

        # Transition to the next scene
        new_array = Array(small, color=BLACK, cell_type='card')
        new_array_mobj = new_array.get_mobject().center().shift(UP)
        self.play(
            TransformMatchingCells(array_mobj, new_array_mobj, path_arc=PI/3),
            ReplacementTransform(title, Title('Insertion Sort Implementation', include_underline=False)),
            run_time=1,
        )
        self.wait(1)


class Implementation(Scene):
    def construct(self):
        title = Title('Insertion Sort Implementation', include_underline=False)
        self.add(title)

        array = Array(small.copy(), color=BLACK, cell_type='card')
        array_mobj = array.get_mobject().center().shift(UP)
        a_text = Tex('a:').scale(0.9).next_to(array_mobj, LEFT)
        indices = Array(
            [i for i in range(len(array))],
            width=array.width, height=array.height,
            spacing=array.spacing, scale_text=array.scale_text, stroke_color=BLACK,
        )
        indices_mobj = indices.get_mobject().center().next_to(array_mobj, UP, buff=0.4)
        self.add(array_mobj, a_text, indices_mobj)
        self.wait(4)

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
        ).next_to(array_mobj, DOWN, buff=0.8).shift(0.5 * RIGHT).code

        self.play(*[index.animate.set_color(BLACK) for index in indices.labels], run_time=1)
        self.play(array_mobj.animate.shift(2.5 * RIGHT), run_time=1)
        self.wait(1)

        self.play(AddTextLetterByLetter(code.chars[0], run_time=0.11 * len(code.chars[0])))
        self.wait(4)

        # Indicate 1 in the code + Bring 10 to the left
        self.play(
            array.cells[0].animate.shift(2.5 * LEFT),
            array.labels[0].animate.shift(2.5 * LEFT),
            indices.labels[0].animate.set_color(WHITE),
            run_time=0.5,
        )
        self.wait(2)

        self.play(Indicate(code.chars[0][15], scale_factor=2), run_time=2)
        self.wait(4)

        # Indicate the last 3 cards
        self.play(LaggedStart(
            *[Indicate(VGroup(cell, label)) for cell, label in zip(array.cells[-3:], array.labels[-3:])],
            lag_ratio=0.4,
            run_time=1,
        ))
        self.wait(2)

        # Move 2 at index 1 up (to insert it)
        self.play(array.cells[1].animate.shift(0.3 * UP), array.labels[1].animate.shift(0.3 * UP), run_time=1)
        self.wait(1)
        self.play(AddTextLetterByLetter(code.chars[1], run_time=0.1 * len(code.chars[1])))
        self.wait(2)

        # Move 2 to the left
        self.play(
            array.cells[1].animate.shift(2.5 * LEFT),
            array.labels[1].animate.shift(2.5 * LEFT),
            indices.labels[1].animate.set_color(WHITE),
            run_time=1,
        )
        self.wait(1)

        self.play(AddTextLetterByLetter(code.chars[2], run_time=0.05 * len(code.chars[2])))
        self.play(AddTextLetterByLetter(code.chars[3], run_time=0.05 * len(code.chars[3])))
        self.play(AddTextLetterByLetter(code.chars[4], run_time=0.1 * len(code.chars[4])))
        self.wait(1)

        def sort(index: int, highlight: bool = False, shift=True, run_time: float = 0.2):
            value = array.values[index]
            if shift:
                self.play(
                    array.cells[index].animate.shift(0.3 * UP),
                    array.labels[index].animate.shift(0.3 * UP),
                    run_time=run_time,
                )
                # Shift the index to the left
                self.play(
                    array.cells[index].animate.shift(2.5 * LEFT),
                    array.labels[index].animate.shift(2.5 * LEFT),
                    run_time=run_time,
                )
            indices.labels[index].set_color(WHITE),

            # Insert in the right place
            for i in range(index, 0, -1):
                if highlight:
                    self.play(array.cells[i - 1][0].animate.set_color(YELLOW), run_time=run_time)

                if array.values[i - 1] < array.values[i]:
                    if highlight:
                        self.play(array.cells[i - 1][0].animate.set_color(WHITE), run_time=2 * run_time)
                    break

                to_path = ArcBetweenPoints(array.cells[i - 1].get_center(), array.cells[i].copy().shift(0.3 * DOWN).get_center(), angle=PI / 4)
                from_path = ArcBetweenPoints(array.cells[i].get_center(), array.cells[i - 1].copy().shift(0.3 * UP).get_center(), angle=PI / 4)
                self.play(
                    MoveAlongPath(VGroup(array.cells[i - 1], array.labels[i - 1]), path=to_path),
                    MoveAlongPath(VGroup(array.cells[i], array.labels[i]), path=from_path),
                    run_time=run_time,
                )
                array.values[i - 1], array.values[i] = array.values[i], array.values[i - 1]
                array.cells[i - 1], array.cells[i] = array.cells[i], array.cells[i - 1]
                array.labels[i - 1], array.labels[i] = array.labels[i], array.labels[i - 1]
                array.color[i - 1], array.color[i] = array.color[i], array.color[i - 1]

                if highlight:
                    self.play(array.cells[i][0].animate.set_color(WHITE), run_time=run_time)

            final_index = array.values.index(value)
            self.play(VGroup(array.cells[final_index], array.labels[final_index]).animate.shift(0.3 * DOWN), run_time=run_time)
            print(f'Array became: {array.values}')
            self.wait(run_time)

        sort(1, highlight=True, shift=False, run_time=0.4)
        sort(2, highlight=True, run_time=0.5)
        self.wait(0.5)
        self.play(ApplyWave(code, run_time=2))
        self.wait(3)

        # Transition to the next scene
        new_array = Array(large, color=BLACK, cell_type='card')
        new_array_mobj = new_array.get_mobject().center().shift(UP)
        new_indices = Array(
            [i for i in range(len(new_array))],
            width=new_array.width, height=new_array.height,
            spacing=new_array.spacing, scale_text=new_array.scale_text, stroke_color=BLACK,
        )
        new_indices_mobj = new_indices.get_mobject().center().next_to(new_array_mobj, UP, buff=0.4)
        self.play(
            TransformMatchingCells(array_mobj, new_array_mobj, path_arc=PI/3),
            ReplacementTransform(title, Title('Insertion Sort', include_underline=False)),
            ReplacementTransform(indices_mobj, new_indices_mobj),
            a_text.animate.next_to(new_array_mobj, LEFT),
            run_time=1,
        )
        self.wait(0.5)


class Simulation(Scene):
    def construct(self):
        title = Title('Insertion Sort', include_underline=False)
        self.add(title)

        array = Array(large.copy(), color=BLACK, cell_type='card')
        array_mobj = array.get_mobject().center().shift(UP)
        a_text = Tex('a:').scale(0.9).next_to(array_mobj, LEFT)
        indices = Array(
            [i for i in range(len(array))],
            width=array.width, height=array.height,
            spacing=array.spacing, scale_text=array.scale_text, stroke_color=BLACK,
        )
        indices_mobj = indices.get_mobject().center().next_to(array_mobj, UP, buff=0.4)
        self.add(array_mobj, a_text, indices_mobj)

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
        ).next_to(array_mobj, DOWN, buff=0.8).shift(0.5 * RIGHT).code
        self.add(code)
        self.wait(3)

        self.play(
            *[cell.animate.shift(1.5 * RIGHT) for cell in array.cells[1:]],
            *[label.animate.shift(1.5 * RIGHT) for label in array.labels[1:]],
            *[label.animate.set_color(BLACK) for label in indices.labels[1:]],
            run_time=1,
        )
        self.play(code.animate.shift(2 * LEFT), run_time=1)
        self.wait(1)

        # Arrow to show which part of the code is being executed
        arrow = Arrow(
            start=LEFT, end=RIGHT, color=RED, buff=0.1,
            stroke_width=10, max_stroke_width_to_length_ratio=15,
            max_tip_length_to_length_ratio=0.5, tip_length=0.2,
        ).scale(0.3).next_to(code, LEFT).align_to(code, UP).shift(0.08 * DOWN)
        self.play(Create(arrow), run_time=0.5)
        self.wait(5)

        # show real-time values to better understand the code
        def get_debug(i, j, cur, prev):
            res = Code(
                code=dedent(f'''
                # i: {i}
                # j: {j}
                # {cur} < {prev} ?
                ''').strip(),
                tab_width=4,
                language='Python',
                line_spacing=0.6,
                font='Monospace',
                style='monokai',
            ).next_to(code, RIGHT).align_to(code, UP).shift(0.25 * UP).code
            return res

        def sort(index: int, highlight: bool = False, run_time: float = 0.2):
            value = array.values[index]

            debug = get_debug(i=index, j=index, cur=array.values[index], prev=array.values[index - 1])
            start_debug = debug
            self.play(AddTextLetterByLetter(debug.chars[0], run_time=0.05 * len(debug.chars[0])))
            self.wait(0.1)

            self.play(
                array.cells[index].animate.shift(0.3 * UP),
                array.labels[index].animate.shift(0.3 * UP),
                run_time=run_time,
            )
            # Shift the index to the left
            self.play(
                array.cells[index].animate.shift(1.5 * LEFT),
                array.labels[index].animate.shift(1.5 * LEFT),
                run_time=run_time,
            )
            indices.labels[index].set_color(WHITE)

            # Insert in the right place
            for i in range(index, 0, -1):
                debug = get_debug(i=index, j=i, cur=array.values[i], prev=array.values[i - 1])
                if i == index:
                    self.play(arrow.animate.shift(0.4 * DOWN), run_time=0.2)
                    self.play(AddTextLetterByLetter(debug.chars[1], run_time=0.05 * len(debug.chars[1])))
                else:
                    debug.chars[1] = next_debug.chars[1]
                self.wait(0.1)

                if i == index:
                    self.play(arrow.animate.shift(0.4 * DOWN), run_time=0.2)
                self.play(AddTextLetterByLetter(debug.chars[2], run_time=0.05 * len(debug.chars[2])))
                self.wait(0.1)

                if highlight:
                    self.play(array.cells[i - 1][0].animate.set_color(YELLOW), run_time=run_time)

                if array.values[i - 1] < array.values[i]:
                    if highlight:
                        self.play(array.cells[i - 1][0].animate.set_color(WHITE), run_time=run_time)
                    self.play(RemoveTextLetterByLetter(debug.chars[2], run_time=0.05 * len(debug.chars[2])))
                    break

                to_path = ArcBetweenPoints(array.cells[i - 1].get_center(), array.cells[i].copy().shift(0.3 * DOWN).get_center(), angle=PI / 4)
                from_path = ArcBetweenPoints(array.cells[i].get_center(), array.cells[i - 1].copy().shift(0.3 * UP).get_center(), angle=PI / 4)
                self.play(arrow.animate.shift(0.4 * DOWN), run_time=run_time)
                self.play(
                    MoveAlongPath(VGroup(array.cells[i - 1], array.labels[i - 1]), path=to_path),
                    MoveAlongPath(VGroup(array.cells[i], array.labels[i]), path=from_path),
                    run_time=run_time,
                )
                array.values[i - 1], array.values[i] = array.values[i], array.values[i - 1]
                array.cells[i - 1], array.cells[i] = array.cells[i], array.cells[i - 1]
                array.labels[i - 1], array.labels[i] = array.labels[i], array.labels[i - 1]
                array.color[i - 1], array.color[i] = array.color[i], array.color[i - 1]

                next_debug = get_debug(i=index, j=i - 1, cur=array.values[i - 1], prev=array.values[i - 2])
                self.play(arrow.animate.shift(0.4 * DOWN), run_time=run_time)
                self.remove(debug.chars[1])
                self.add(next_debug.chars[1])
                if highlight:
                    self.play(array.cells[i][0].animate.set_color(WHITE), run_time=run_time)

                self.play(
                    arrow.animate.shift(0.8 * UP),
                    RemoveTextLetterByLetter(debug.chars[2]),
                    run_time=run_time,
                )
                self.remove(debug.chars[2])

            final_index = array.values.index(value)
            self.play(VGroup(array.cells[final_index], array.labels[final_index]).animate.shift(0.3 * DOWN), run_time=run_time)
            print(f'Array became: {array.values}')
            self.play(arrow.animate.shift(0.8 * UP), run_time=run_time)
            self.remove(next_debug.chars[1])
            self.remove(start_debug.chars[0])

        sort(1, highlight=True, run_time=1)
        # Indicate the first 2 elements
        self.play(LaggedStart(
            *[Indicate(VGroup(cell, label)) for cell, label in zip(array.cells[:2], array.labels[:2])],
            lag_ratio=0.4,
            run_time=2,
        ))

        sort(2, highlight=True, run_time=0.8)
        sort(3, highlight=True, run_time=0.5)
        sort(4, highlight=True, run_time=0.6)
        self.wait(2)
        self.play(LaggedStart(
            *[Indicate(VGroup(cell, label)) for cell, label in zip(array.cells[:5], array.labels[:5])],
            lag_ratio=0.4,
            run_time=2,
        ))
        self.play(Circumscribe(VGroup(array.cells[-1], array.cells[-2]), color=ORANGE, buff=0.3, stroke_width=8, run_time=1))

        sort(5, highlight=True, run_time=0.4)
        sort(6, highlight=True, run_time=0.4)
        self.wait(2)

        self.play(LaggedStart(
            *[Indicate(VGroup(cell, label)) for cell, label in zip(array.cells, array.labels)],
            lag_ratio=0.4,
            run_time=2,
        ))
        self.wait(2)

        # Transition to the next scene
        self.play(
            ReplacementTransform(title, Title('Time Complexity', include_underline=False)),
            FadeOut(arrow),
            run_time=1,
        )
        self.wait(0.5)


class TimeComplexity(Scene):
    def construct(self):
        title = Title('Time Complexity', include_underline=False)
        self.add(title)

        array = Array(sorted(large), color=BLACK, cell_type='card')
        array_mobj = array.get_mobject().center().shift(UP)
        a_text = Tex('a:').scale(0.9).next_to(array_mobj, LEFT)
        indices = Array(
            [i for i in range(len(array))],
            width=array.width, height=array.height,
            spacing=array.spacing, scale_text=array.scale_text, stroke_color=BLACK,
        )
        indices_mobj = indices.get_mobject().center().next_to(array_mobj, UP, buff=0.4)
        self.add(array_mobj, a_text, indices_mobj)

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
        ).next_to(array_mobj, DOWN, buff=0.8).shift(0.5 * RIGHT).shift(2 * LEFT).code
        self.add(code)
        self.wait(1)

        # Indicate the outer loop
        self.play(Indicate(code.chars[0], run_time=2))
        self.wait(2)

        # Indicate the inner loop
        self.play(Indicate(code.chars[2], run_time=2))
        self.wait(2)

        # Indicate the outer loop and write n - 1 next to it
        n_1 = MathTex('n - 1', color=ORANGE).scale(0.9).next_to(code.chars[0], RIGHT, buff=3)
        self.play(Indicate(code.chars[0], run_time=1))
        self.play(Write(n_1), run_time=0.5)
        self.wait(1)

        # Indicate the inner loop
        self.play(Indicate(code.chars[2], run_time=2))
        self.wait(7)

        # Reverse order of the array (half sorted on the left - half reverse on the right)
        new_array = Array(sorted(large, reverse=True), color=BLACK, cell_type='card')
        new_array_mobj = new_array.get_mobject().center().shift(UP)
        self.play(TransformMatchingCells(array_mobj, new_array_mobj, path_arc=PI/3), run_time=1)
        self.wait(2)

        o_n = MathTex(r'\mathcal{O}(n)', color=ORANGE).scale(0.9).next_to(n_1, DOWN).align_to(n_1, LEFT).shift(0.2 * DOWN)
        self.play(Write(o_n), run_time=0.5)
        self.wait(3)

        # Draw curved-arrows for each element to the very start of the array
        arrows = [CurvedArrow(
            start_point=array.cells[i].get_top(), end_point=array.cells[0].get_top(),
            angle=PI/4, color=WHITE if array.color[i] == BLACK else array.color[i], stroke_width=6,
        ) for i in range(1, len(array))]
        for i in range(len(arrows) + 2):
            if 0 <= i < len(arrows):
                self.play(Create(arrows[i]), run_time=0.5)
            if i >= 2:
                self.play(FadeOut(arrows[i - 2]), run_time=0.2)
        self.wait(3)

        # Write O(n^2)
        n_2 = MathTex(r'\mathcal{O}(n^2)', color=ORANGE).next_to(code.chars[1], RIGHT).align_to(n_1, LEFT)
        self.play(ReplacementTransform(VGroup(n_1, o_n), n_2), run_time=1)
        self.wait(2)


class UseCase(Scene):
    def construct(self):
        title = Title('Insertion Sort Use Cases', include_underline=False)
        self.add(title)

        array = Array([1, 4, 5, 3, 7, 12, 9], color=BLACK, cell_type='card')
        array_mobj = array.get_mobject().center().shift(UP)
        a_text = Tex('a:').scale(0.9).next_to(array_mobj, LEFT)
        indices = Array(
            [i for i in range(len(array))],
            width=array.width, height=array.height,
            spacing=array.spacing, scale_text=array.scale_text, stroke_color=BLACK,
        )
        indices_mobj = indices.get_mobject().center().next_to(array_mobj, UP, buff=0.4)
        self.add(array_mobj, a_text, indices_mobj)
        self.wait(2)

        new_array_mobj = array_mobj.copy()
        self.play(new_array_mobj.animate.shift(2 * DOWN), run_time=1)
        self.wait(3)
        new_array = Array([1, 3, 4, 5, 7, 9, 12], color=BLACK, cell_type='card')

        # Write Elements are at most 3 locations away from the final position
        text = Text(
            'Elements are at most 3 locations\naway from the final position', font='Monospace', color=WHITE
        ).scale(0.5).next_to(new_array_mobj, DOWN, buff=0.5).align_to(new_array_mobj, LEFT)
        self.play(AddTextLetterByLetter(text, run_time=4))
        self.wait(1)

        self.play(TransformMatchingCells(new_array_mobj, new_array.get_mobject().center().shift(DOWN), path_arc=PI/3), run_time=2)

        # Draw arrows between 3s and 9s
        arrow3 = Arrow(
            start=array.cells[3].get_bottom(), end=new_array.cells[1].get_top(),
            color=ORANGE, buff=0.1, stroke_width=7, max_stroke_width_to_length_ratio=10,
            max_tip_length_to_length_ratio=0.5, tip_length=0.25,
        )
        arrow9 = Arrow(
            start=array.cells[6].get_bottom(), end=new_array.cells[5].get_top(),
            color=ORANGE, buff=0.1, stroke_width=7, max_stroke_width_to_length_ratio=10,
            max_tip_length_to_length_ratio=0.5, tip_length=0.25,
        )
        self.play(Create(arrow3), Create(arrow9), run_time=0.5)
        self.wait(3)

        # Write 3*n = O(n)
        _3n = MathTex(r'3 \cdot n = ', color=WHITE).scale(0.8).next_to(text, RIGHT, buff=0.5)
        on = MathTex(r'\mathcal{O}(n)', color=ORANGE).scale(0.8).next_to(_3n, RIGHT, buff=0.2)
        self.play(Write(_3n), run_time=1)
        self.wait(3)
        self.play(Write(on), run_time=1)
        self.wait(2)

        comparison = MathTex(r'< \mathcal{O}(n \log{n})').scale(0.8).next_to(on, RIGHT, buff=0.2)
        self.play(Write(comparison), run_time=1)
        self.wait(4)

        # Indicate the text
        self.play(Indicate(text), run_time=1)
        self.wait(2)


class Conclusion(Scene):
    def construct(self):
        title = Title('Insertion Sort', include_underline=False)
        self.add(title)

        array = Array(large.copy(), color=BLACK, cell_type='card')
        array_mobj = array.get_mobject().center().shift(UP)
        a_text = Tex('a:').scale(0.9).next_to(array_mobj, LEFT)
        indices = Array(
            [i for i in range(len(array))],
            width=array.width, height=array.height,
            spacing=array.spacing, scale_text=array.scale_text, stroke_color=BLACK,
        )
        indices_mobj = indices.get_mobject().center().next_to(array_mobj, UP, buff=0.4)
        self.add(array_mobj, a_text, indices_mobj)

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
        ).next_to(array_mobj, DOWN, buff=0.8).shift(0.5 * RIGHT).code

        for line in code.chars:
            self.play(AddTextLetterByLetter(line, run_time=0.05 * len(line)))
        self.wait(1)

        self.play(ApplyWave(code, run_time=2))
        self.wait(0.1)
