import random
import string
from itertools import chain
from textwrap import dedent

from manim import *

from merge_sort.array import Array, TransformMatchingCells

arr = [12, 3, 5, 9, 4, 1, 7]
ORANGE = ManimColor('#fa541c')
random.seed(42)


class IntroductionBars(Scene):
    def construct(self):
        # Create vertical bars representing the array and sort them with insertion sort
        array = list(range(1, 65))
        random.shuffle(array)

        base = Rectangle(height=1, width=1, color=WHITE, fill_opacity=1).center().to_edge(DOWN).shift(UP)
        rectangles = [
            Rectangle(height=0.12 * value, width=0.05, color=WHITE, fill_opacity=1).align_to(base, DOWN).shift(0.12 * i * RIGHT)
            for i, value in enumerate(array)
        ]
        bars = VGroup(*rectangles).center()
        self.play(Create(bars, run_time=0.5))

        class Item:
            def __init__(self, value: int, bar: Mobject):
                self.value = value
                self.bar = bar

        def merge(a: list[Item], b: list[Item]) -> list[Item]:
            i, j, res = 0, 0, []
            self.play(
                a[i].bar.animate.set_color(ORANGE),
                b[j].bar.animate.set_color(ORANGE),
                run_time=0.01,
            )
            while i < len(a) or j < len(b):
                ai = a[i].value if i < len(a) else float('inf')
                bj = b[j].value if j < len(b) else float('inf')

                if ai < bj:
                    self.play(
                        a[i].bar.animate.set_color(WHITE),
                        *([a[i + 1].bar.animate.set_color(ORANGE)] if i + 1 < len(a) else []),
                        run_time=0.01,
                    )
                    res.append(a[i])
                    i += 1
                else:
                    self.play(
                        # Shift all a[i:] to the right and bring the j-th bar to the place of a[i]
                        b[j].bar.animate.set_color(WHITE).shift(0.12 * len(a[i:]) * LEFT),
                        *[ai.bar.animate.shift(0.12 * RIGHT) for ai in a[i:]],
                        *([b[j + 1].bar.animate.set_color(ORANGE)] if j + 1 < len(b) else []),
                        run_time=0.01,
                    )
                    res.append(b[j])
                    j += 1
            return res

        def merge_sort(a: list[Item]) -> list[Item]:
            if len(a) <= 1:
                return a

            # Set the right part to dark gray
            self.play(*[item.bar.animate.set_color(GRAY) for item in a[len(a) // 2:]], run_time=0.1)
            l = merge_sort(a[: len(a) // 2])
            # Set the left part to dark gray and right part to white
            self.play(
                *[item.bar.animate.set_color(GRAY) for item in a[: len(a) // 2]],
                *[item.bar.animate.set_color(WHITE) for item in a[len(a) // 2:]],
                run_time=0.1,
            )
            r = merge_sort(a[len(a) // 2:])
            # Set the left part to white
            self.play(*[item.bar.animate.set_color(WHITE) for item in a[: len(a) // 2]], run_time=0.1)
            return merge(l, r)

        items = [Item(value, bar) for value, bar in zip(array, bars)]
        sorted_array = merge_sort(items)
        self.wait(0.2)

        self.play(LaggedStart(
            *[item.bar.animate.set_color(ORANGE) for item in sorted_array],
            lag_ratio=0.6,
            run_time=2,
        ))
        self.wait(0.5)

        for item in sorted_array:
            item.bar.set_color(WHITE)
        self.wait(1)


class IntroductionSortingVisualized(Scene):
    def construct(self, animate_creation=True):
        array = Array(arr)
        array_mobj = array.get_mobject().center().shift(2.2 * UP)
        if animate_creation:
            self.play(Create(array_mobj))
        else:
            self.add(array_mobj)
        self.wait(1)

        def merge_sort(a: Array, a_mobj: Mobject) -> tuple[Array, Mobject]:
            if len(a) <= 1:
                return a, a_mobj

            # Copy the left part of the array and place it on the bottom-left side of the current array => sort it
            l = Array(a.values[: len(a) // 2], width=a.width, height=a.height, spacing=a.spacing, scale_text=a.scale_text, stroke_color=a.stroke_color)
            l_mobj = l.get_mobject().next_to(a_mobj, DOWN, buff=0.4).align_to(a_mobj, LEFT).shift(0.4 * LEFT)
            l_arrow = Arrow(
                start=a_mobj.get_bottom(), end=l_mobj.get_top(),
                color=ORANGE, buff=0.2, stroke_width=5, max_stroke_width_to_length_ratio=10,
                max_tip_length_to_length_ratio=0.5, tip_length=0.15,
            )
            self.play(
                *[item.animate.set_color(ORANGE).scale(1.25) for item in a.labels[:len(a) // 2]],
                *[item.animate.set_color(DARK_GRAY) for item in a.labels[len(a) // 2:]],
                run_time=0.2,
            )
            self.play(Create(l_mobj), Create(l_arrow), run_time=0.5)
            left, left_mobj = merge_sort(l, l_mobj)

            # Copy the right part of the array and place it on the bottom-right side of the current array => sort it
            r = Array(a.values[len(a) // 2:], width=a.width, height=a.height, spacing=a.spacing, scale_text=a.scale_text, stroke_color=a.stroke_color)
            r_mobj = r.get_mobject().next_to(a_mobj, DOWN, buff=0.4).align_to(a_mobj, RIGHT).shift(0.4 * RIGHT)
            r_arrow = Arrow(
                start=a_mobj.get_bottom(), end=r_mobj.get_top(),
                color=ORANGE, buff=0.2, stroke_width=5, max_stroke_width_to_length_ratio=10,
                max_tip_length_to_length_ratio=0.5, tip_length=0.15,
            )
            self.play(
                l_arrow.animate.set_color(DARK_GRAY),
                *[item.animate.set_color(DARK_GRAY).scale(1 / 1.25) for item in a.labels[: len(a) // 2]],
                *[item.animate.set_color(ORANGE).scale(1.25) for item in a.labels[len(a) // 2:]],
                run_time=0.2,
            )
            self.play(Create(r_mobj), Create(r_arrow), run_time=0.5)
            right, right_mobj = merge_sort(r, r_mobj)

            # Merge the sorted left and right parts and fade the parts out
            res = Array(sorted(a.values), width=a.width, height=a.height, spacing=a.spacing, scale_text=a.scale_text, stroke_color=a.stroke_color)
            res_mobj = res.get_mobject().align_to(a_mobj, DOWN).align_to(a_mobj, LEFT)

            # Merge the left and right into res by moving each number along the straight path from left/right to res cell
            # Hide all the labels of the current array + Reverse the arrows (make pointers direct in the opposite direction)
            self.play(
                *[item.animate.set_color(BLACK) for item in a.labels],
                l_arrow.animate.rotate(PI).set_color(ORANGE),
                r_arrow.animate.rotate(PI).set_color(ORANGE),
                run_time=0.5,
            )

            # Merge the left and right parts into res
            for i, val in enumerate(sorted(a.values)):
                if val in left.values:
                    index = left.values.index(val)
                    label = left.labels[index].copy()
                    self.play(label.animate.move_to(res.labels[i]), run_time=0.5)
                    self.remove(a.labels[i], a.rectangles[i], label)
                    self.add(res.labels[i].set_z_index(1000000), res.rectangles[i])
                else:
                    index = right.values.index(val)
                    label = right.labels[index].copy()
                    self.play(label.animate.move_to(res.labels[i]), run_time=0.5)
                    self.remove(a.labels[i], a.rectangles[i], label)
                    self.add(res.labels[i].set_z_index(1000000), res.rectangles[i])

            self.remove(l_mobj, r_mobj)
            self.play(FadeOut(left_mobj, right_mobj, l_arrow, r_arrow), run_time=1)
            return res, res_mobj


        merge_sort(array, array_mobj)
        self.wait(1)

class IntroductionImplementation(Scene):
    def construct(self):
        code = Code(
            code=dedent('''
                def merge(a, b):
                    i, j, res = 0, 0, []
                    while i < len(a) or j < len(b):
                        ai = a[i] if i < len(a) else float('inf')
                        bj = b[j] if j < len(b) else float('inf')
                
                        if ai < bj:
                            res.append(ai)
                            i += 1
                        else:
                            res.append(bj)
                            j += 1
                    return res
                
                
                def merge_sort(a):
                    if len(a) <= 1:
                        return a
                
                    l = merge_sort(a[: len(a) // 2])
                    r = merge_sort(a[len(a) // 2:])
                    return merge(l, r)
            ''').strip(),
            tab_width=4,
            language='Python',
            line_spacing=0.6,
            font='Monospace',
            style='monokai',
        ).center().scale(0.7).code

        for line in code:
            if line:
                self.play(AddTextLetterByLetter(line, run_time=len(line) * 0.05))
        self.wait(0.5)

class IntroductionPlots(Scene):
    def construct(self):
        """ Plot O(n^2), O(n log n), and O(n) """
        # Set up the axes
        axes = Axes(
            x_range=[0, 10, 1],     # x-axis from 0 to 10 with step size of 1
            y_range=[0, 100, 10],   # y-axis from 0 to 100 with step size of 10
            axis_config={'include_ticks': False},
            # axis_config={'color': BLUE}
        ).scale(0.7)

        # Plotting the functions
        graph_n2 = axes.plot(lambda x: x ** 2, color=RED, x_range=[0, 10], use_smoothing=True)
        graph_nlogn = axes.plot(lambda x: x * np.log(x), color=YELLOW, x_range=[1, 10], use_smoothing=True)
        graph_n = axes.plot(lambda x: x, color=GREEN, x_range=[0, 10], use_smoothing=True)

        # Add graph labels
        graph_n2_label = axes.get_graph_label(graph_n2, label=MathTex(r'\mathcal{O}(n^2)'), x_val=10)
        graph_nlogn_label = axes.get_graph_label(graph_nlogn, label=MathTex(r'\mathcal{O}(n \log{n})'), x_val=11.5)
        graph_n_label = axes.get_graph_label(graph_n, label=MathTex(r'\mathcal{O}(n)'), x_val=10)

        # Add all elements to the scene
        self.play(LaggedStart(
            Create(axes),
            Create(graph_n2), Write(graph_n2_label),
            Create(graph_nlogn), Write(graph_nlogn_label),
            Create(graph_n), Write(graph_n_label),
            lag_ratio=0.7,
            run_time=6,
        ))

        self.wait(1)


class IntroductionRecursionVisualized(Scene):
    def construct(self):
        array = Array(arr, fill_color=WHITE, fill_opacity=1)
        array_mobj = array.get_mobject().center().shift(2.5 * UP)
        self.play(Create(array_mobj))
        self.wait(1)

        def merge_sort(a: Array, a_mobj: Mobject) -> tuple[Array, Mobject]:
            if len(a) <= 1:
                return a, a_mobj

            # Copy the left part of the array and place it on the bottom-left side of the current array => sort it
            l = Array(a.values[: len(a) // 2], fill_color=a.fill_color, fill_opacity=a.fill_opacity)
            l_mobj = l.get_mobject().next_to(a_mobj, DOWN, buff=0.4).align_to(a_mobj, LEFT).shift(0.4 * LEFT)
            l_arrow = Arrow(
                start=a_mobj.get_bottom(), end=l_mobj.get_top(),
                color=ORANGE, buff=0.2, stroke_width=5, max_stroke_width_to_length_ratio=10,
                max_tip_length_to_length_ratio=0.5, tip_length=0.15,
            )
            self.play(
                *[item.animate.set_color(ORANGE) for item in a.labels[:len(a) // 2]],
                *[item.animate.set_fill(ORANGE).set_stroke(ORANGE) for item in a.rectangles[:len(a) // 2]],
                *[item.animate.set_color(DARK_GRAY) for item in a.labels[len(a) // 2:]],
                *[item.animate.set_fill(DARK_GRAY).set_stroke(DARK_GRAY) for item in a.rectangles[len(a) // 2:]],
                run_time=0.2,
            )
            self.play(Create(l_mobj), Create(l_arrow), run_time=0.5)
            left, left_mobj = merge_sort(l, l_mobj)

            # Copy the right part of the array and place it on the bottom-right side of the current array => sort it
            r = Array(a.values[len(a) // 2:], fill_color=a.fill_color, fill_opacity=a.fill_opacity)
            r_mobj = r.get_mobject().next_to(a_mobj, DOWN, buff=0.4).align_to(a_mobj, RIGHT).shift(0.4 * RIGHT)
            r_arrow = Arrow(
                start=a_mobj.get_bottom(), end=r_mobj.get_top(),
                color=ORANGE, buff=0.2, stroke_width=5, max_stroke_width_to_length_ratio=10,
                max_tip_length_to_length_ratio=0.5, tip_length=0.15,
            )
            self.play(
                l_arrow.animate.set_color(DARK_GRAY),
                *[item.animate.set_color(DARK_GRAY) for item in a.labels[: len(a) // 2]],
                *[item.animate.set_fill(DARK_GRAY).set_stroke(DARK_GREY) for item in a.rectangles[: len(a) // 2]],
                *[item.animate.set_color(ORANGE) for item in a.labels[len(a) // 2:]],
                *[item.animate.set_fill(ORANGE).set_stroke(ORANGE) for item in a.rectangles[len(a) // 2:]],
                run_time=0.2,
            )
            self.play(Create(r_mobj), Create(r_arrow), run_time=0.5)
            right, right_mobj = merge_sort(r, r_mobj)

            # Merge the left and right into res by moving each number along the straight path from left/right to res cell
            # Hide all the labels of the current array + Reverse the arrows (make pointers direct in the opposite direction)
            self.play(
                *[item.animate.set_color(WHITE) for item in a.labels],
                *[item.animate.set_fill(WHITE).set_stroke(WHITE) for item in a.rectangles],
                l_arrow.animate.rotate(PI).set_color(ORANGE),
                r_arrow.animate.rotate(PI).set_color(ORANGE),
                run_time=0.5,
            )

            # Merge the left and right parts into res
            self.remove(l_mobj, r_mobj, left_mobj, right_mobj)
            self.play(FadeOut(l_arrow, r_arrow), run_time=0.2)
            return a, a_mobj


        merge_sort(array, array_mobj)
        self.wait(1)


class MergeStep(Scene):
    def construct(self):
        title = Title('Merge Two Sorted Arrays', include_underline=False)
        left = Array([3, 5, 12])
        right = Array([1, 4, 7, 9])
        res = Array(sorted(arr), color=BLACK)

        res_mobj = res.get_mobject().center().shift(UP)
        left_mobj = left.get_mobject().next_to(res_mobj, DOWN, buff=0.8).align_to(res_mobj, LEFT).shift(0.8 * LEFT)
        right_mobj = right.get_mobject().next_to(res_mobj, DOWN, buff=0.8).align_to(res_mobj, RIGHT).shift(1.2 * RIGHT)
        left_text = Tex('a:').scale(0.9).next_to(left_mobj, LEFT)
        right_text = Tex('b:').scale(0.9).next_to(right_mobj, LEFT)

        # Create arrows that point from the center of left to the center of res and from the center of right to the center of res
        left_arrow = Arrow(
            start=left_mobj.get_top(), end=res_mobj.get_bottom(),
            color=ORANGE, buff=0.2, stroke_width=5, max_stroke_width_to_length_ratio=10,
            max_tip_length_to_length_ratio=0.5, tip_length=0.15,
        )
        right_arrow = Arrow(
            start=right_mobj.get_top(), end=res_mobj.get_bottom(),
            color=ORANGE, buff=0.2, stroke_width=5, max_stroke_width_to_length_ratio=10,
            max_tip_length_to_length_ratio=0.5, tip_length=0.15,
        )

        self.play(Create(left_mobj), Write(left_text), run_time=0.5)
        self.play(Create(right_mobj), Write(right_text), run_time=0.5)
        self.wait(0.2)

        self.play(Write(title), run_time=0.5)
        self.wait(0.5)

        self.play(Create(res_mobj), Create(left_arrow), Create(right_arrow), run_time=1)
        self.play(LaggedStart(
            *[item.animate.set_color(WHITE) for item in res.labels],
            lag_ratio=0.6,
            run_time=1.5,
        ))
        self.wait(1)

        self.play(Indicate(left_mobj, color=ORANGE), Indicate(left_text, color=ORANGE), run_time=0.5)
        self.play(Indicate(right_mobj, color=ORANGE), Indicate(right_text, color=ORANGE), run_time=0.5)
        self.wait(2)

        self.play(Indicate(res_mobj), run_time=2)

        o_a_plus_b = MathTex(r'\mathcal{O}(A + B)').scale(0.9).center().shift(2 * DOWN)
        self.play(Write(o_a_plus_b), run_time=1)
        self.wait(0.5)

        self.play(Indicate(left_mobj, color=ORANGE), Indicate(left_text, color=ORANGE), Indicate(o_a_plus_b[0][2], color=ORANGE, scale_factor=1.6), run_time=2)
        self.play(Indicate(right_mobj, color=ORANGE), Indicate(right_text, color=ORANGE), Indicate(o_a_plus_b[0][4], color=ORANGE, scale_factor=1.6), run_time=2)
        self.wait(1)

        # Highlight the elements of the resulting array one by one and highlight the corresponding element in a or b.
        for i, value in enumerate(res.values):
            if value in left.values:
                index = left.values.index(value)
                self.play(Indicate(left.labels[index], color=ORANGE, scale_factor=1.8), Indicate(res.labels[i], color=ORANGE, scale_factor=1.8), run_time=1.1)
            else:
                index = right.values.index(value)
                self.play(Indicate(right.labels[index], color=ORANGE, scale_factor=1.8), Indicate(res.labels[i], color=ORANGE, scale_factor=1.8), run_time=1.1)
        self.wait(1)

        self.play(FadeOut(o_a_plus_b), run_time=1)

        self.play(LaggedStart(
            Indicate(VGroup(left_mobj, left_text), color=ORANGE),
            Indicate(VGroup(right_mobj, right_text), color=ORANGE),
            run_time=2,
            lag_ratio=0.6,
        ))
        self.wait(0.5)

        self.play(Circumscribe(res_mobj), run_time=1.5)
        self.play(LaggedStart(
            *[Indicate(item, color=ORANGE, scale_factor=1.8) for item in res.labels],
            lag_ratio=0.6,
            run_time=2,
        ))
        self.wait(0.2)

        # Make the numbers in the resulting array black
        self.play(LaggedStart(
            *[item.animate.set_color(BLACK) for item in res.labels],
            lag_ratio=0.6,
            run_time=0.5,
        ))

        # draw 2 arrows pointing to the first elements of the left and right arrays
        left_pointer = Arrow(
            start=left.rectangles[0].get_bottom() + 0.8 * DOWN, end=left.rectangles[0].get_bottom(),
            color=ORANGE, buff=0.2, stroke_width=5, max_stroke_width_to_length_ratio=10,
            max_tip_length_to_length_ratio=0.5, tip_length=0.15,
        )

        right_pointer = Arrow(
            start=right.rectangles[0].get_bottom() + 0.8 * DOWN, end=right.rectangles[0].get_bottom(),
            color=ORANGE, buff=0.2, stroke_width=5, max_stroke_width_to_length_ratio=10,
            max_tip_length_to_length_ratio=0.5, tip_length=0.15,
        )

        # Highlight the first 2 elements (orange + increase size)
        self.play(Create(left_pointer), Create(right_pointer), run_time=2)
        self.wait(2)
        self.play(
            left.labels[0].animate.set_color(ORANGE).scale(1.25),
            right.labels[0].animate.set_color(ORANGE).scale(1.25),
            run_time=1,
        )
        self.wait(3)

        def move_smallest(l_index, r_index, res_index, run_time=0.5):
            l_val = left.values[l_index] if l_index < len(left) else float('inf')
            r_val = right.values[r_index] if r_index < len(right) else float('inf')
            if l_val < r_val:
                label = left.labels[l_index].copy()
                self.play(label.animate.move_to(res.labels[res_index]).set_color(WHITE), run_time=run_time)
                self.play(
                    left.labels[l_index].animate.set_color(WHITE).scale(1 / 1.25),
                    left_pointer.animate.shift((left.width + left.spacing) * RIGHT),
                    *([left.labels[l_index + 1].animate.set_color(ORANGE).scale(1.25)] if l_index + 1 < len(left) else []),
                    run_time=run_time,
                )
                self.remove(res.labels[res_index])
                res.labels[res_index] = label
                return l_index + 1, r_index
            else:
                label = right.labels[r_index].copy()
                self.play(label.animate.move_to(res.labels[res_index]).set_color(WHITE), run_time=run_time)
                self.play(
                    right.labels[r_index].animate.set_color(WHITE).scale(1 / 1.25),
                    right_pointer.animate.shift((right.width + right.spacing) * RIGHT),
                    *([right.labels[r_index + 1].animate.set_color(ORANGE).scale(1.25)] if r_index + 1 < len(right) else []),
                    run_time=run_time,
                )
                self.remove(res.labels[res_index])
                res.labels[res_index] = label
                return l_index, r_index + 1

        l, r = 0, 0
        l, r = move_smallest(l, r, 0, run_time=2)
        self.wait(2.5)
        l, r = move_smallest(l, r, 1, run_time=1)

        # Highlight the second arrow
        self.play(Indicate(right_pointer, scale_factor=1.5), run_time=2)
        self.wait(2)

        # Highlight the elements in a and b from smallest to largest
        self.play(LaggedStart(
            *[Indicate(label, color=YELLOW, scale_factor=1.8) for label in left.labels],
            lag_ratio=0.6,
            run_time=1,
        ))
        self.play(LaggedStart(
            *[Indicate(label, color=YELLOW, scale_factor=1.8) for label in right.labels],
            lag_ratio=0.6,
            run_time=1,
        ))
        self.wait(2)

        l, r = move_smallest(l, r, 2, run_time=1)
        l, r = move_smallest(l, r, 3, run_time=1)
        l, r = move_smallest(l, r, 4, run_time=0.8)
        l, r = move_smallest(l, r, 5, run_time=0.8)
        self.wait(0.5)
        self.play(Indicate(right_pointer, color=YELLOW, scale_factor=1.5), run_time=2)
        self.wait(3)
        self.play(Indicate(left.labels[-1], color=YELLOW, scale_factor=1.8), run_time=1)
        self.wait(1)
        l, r = move_smallest(l, r, 6, run_time=0.8)
        self.wait(3)

        # Highlight all the elements in the resulting array from smallest to largest (LaggedStart)
        self.play(LaggedStart(
            *[Indicate(label, color=YELLOW, scale_factor=1.8) for label in res.labels],
            lag_ratio=0.6,
            run_time=2,
        ))
        self.wait(1)

        # Transition to the next scene
        self.play(FadeOut(left_pointer, right_pointer), run_time=0.2)
        self.play(VGroup(left_text, right_text, left_mobj, right_mobj, res_mobj, left_arrow, right_arrow, *res.labels).animate.shift(1.2 * UP), run_time=1)
        self.play(
            *[item.animate.set_color(BLACK) for item in res.labels],
            run_time=0.5,
        )
        # Move the left and right arrays up and adjust their corresponding arrows
        self.play(
            left_mobj.animate.shift(0.4 * UP),
            right_mobj.animate.shift(0.4 * UP),
            left_text.animate.shift(0.4 * UP),
            right_text.animate.shift(0.4 * UP),
            left_arrow.animate.become(Arrow(
                start=left_mobj.get_top() + 0.4 * UP, end=res_mobj.get_bottom(),
                color=ORANGE, buff=0.2, stroke_width=5, max_stroke_width_to_length_ratio=10,
                max_tip_length_to_length_ratio=0.5, tip_length=0.15,
            )),
            right_arrow.animate.become(Arrow(
                start=right_mobj.get_top() + 0.4 * UP, end=res_mobj.get_bottom(),
                color=ORANGE, buff=0.2, stroke_width=5, max_stroke_width_to_length_ratio=10,
                max_tip_length_to_length_ratio=0.5, tip_length=0.15,
            )),
            run_time=0.5,
        )

        self.wait(1)


class MergeStepImplementation(Scene):
    def construct(self):
        title = Title('Merge Two Sorted Arrays', include_underline=False)
        left = Array([3, 5, 12])
        right = Array([1, 4, 7, 9])
        res = Array(sorted(arr), color=BLACK)

        res_mobj = res.get_mobject().center().shift(2.2 * UP)
        left_mobj = left.get_mobject().next_to(res_mobj, DOWN, buff=0.4).align_to(res_mobj, LEFT).shift(0.8 * LEFT)
        right_mobj = right.get_mobject().next_to(res_mobj, DOWN, buff=0.4).align_to(res_mobj, RIGHT).shift(1.2 * RIGHT)
        left_text = Tex('a:').scale(0.9).next_to(left_mobj, LEFT)
        right_text = Tex('b:').scale(0.9).next_to(right_mobj, LEFT)

        # Create arrows that point from the center of left to the center of res and from the center of right to the center of res
        left_arrow = Arrow(
            start=left_mobj.get_top(), end=res_mobj.get_bottom(),
            color=ORANGE, buff=0.2, stroke_width=5, max_stroke_width_to_length_ratio=10,
            max_tip_length_to_length_ratio=0.5, tip_length=0.15,
        )
        right_arrow = Arrow(
            start=right_mobj.get_top(), end=res_mobj.get_bottom(),
            color=ORANGE, buff=0.2, stroke_width=5, max_stroke_width_to_length_ratio=10,
            max_tip_length_to_length_ratio=0.5, tip_length=0.15,
        )

        self.add(title, left_mobj, right_mobj, res_mobj, left_text, right_text, left_arrow, right_arrow)
        self.wait(1)

        # draw 2 arrows pointing to the first elements of the left and right arrays
        left_pointer = Arrow(
            start=left.rectangles[0].get_bottom() + 0.8 * DOWN, end=left.rectangles[0].get_bottom(),
            color=ORANGE, buff=0.2, stroke_width=5, max_stroke_width_to_length_ratio=10,
            max_tip_length_to_length_ratio=0.5, tip_length=0.15,
        )

        right_pointer = Arrow(
            start=right.rectangles[0].get_bottom() + 0.8 * DOWN, end=right.rectangles[0].get_bottom(),
            color=ORANGE, buff=0.2, stroke_width=5, max_stroke_width_to_length_ratio=10,
            max_tip_length_to_length_ratio=0.5, tip_length=0.15,
        )
        self.play(
            Create(left_pointer), Create(right_pointer),
            left.labels[0].animate.set_color(ORANGE).scale(1.25),
            right.labels[0].animate.set_color(ORANGE).scale(1.25),
            run_time=0.5,
        )

        code = Code(
            code=dedent('''
                i, j, res = 0, 0, []
                while i < len(a) or j < len(b):
                    ai = a[i] if i < len(a) else float('inf')
                    bj = b[j] if j < len(b) else float('inf')

                    if ai < bj:
                        res.append(ai)
                        i += 1
                    else:
                        res.append(bj)
                        j += 1
            ''').strip(),
            tab_width=4,
            language='Python',
            line_spacing=0.6,
            font='Monospace',
            style='monokai',
        ).scale(0.75).center().shift(1.75 * DOWN).code

        self.play(AddTextLetterByLetter(code.chars[0], run_time=0.1 * len(code.chars[0])))
        self.wait(0.2)
        self.play(AddTextLetterByLetter(code.chars[1], run_time=0.1 * len(code.chars[1])))
        self.wait(0.2)
        self.play(AddTextLetterByLetter(code.chars[2], run_time=0.1 * len(code.chars[2])))
        self.wait(0.2)
        self.play(AddTextLetterByLetter(code.chars[3], run_time=0.1 * len(code.chars[3])))

        self.play(AddTextLetterByLetter(code.chars[5], run_time=0.1 * len(code.chars[5])))
        self.play(AddTextLetterByLetter(code.chars[6], run_time=0.1 * len(code.chars[6])))
        self.play(AddTextLetterByLetter(code.chars[7], run_time=0.1 * len(code.chars[7])))
        self.wait(0.2)

        self.play(AddTextLetterByLetter(code.chars[8], run_time=0.1 * len(code.chars[8])))
        self.play(AddTextLetterByLetter(code.chars[9], run_time=0.1 * len(code.chars[9])))
        self.play(AddTextLetterByLetter(code.chars[10], run_time=0.1 * len(code.chars[10])))
        self.wait(1)

        def move_smallest(l_index, r_index, res_index, run_time=0.5, move_pointer=True):
            l_val = left.values[l_index] if l_index < len(left) else float('inf')
            r_val = right.values[r_index] if r_index < len(right) else float('inf')
            if l_val < r_val:
                label = left.labels[l_index].copy()
                self.play(label.animate.move_to(res.labels[res_index]).set_color(WHITE), run_time=run_time)
                self.play(
                    left.labels[l_index].animate.set_color(WHITE).scale(1 / 1.25),
                    *([left_pointer.animate.shift((left.width + left.spacing) * RIGHT)] if move_pointer else []),
                    *([left.labels[l_index + 1].animate.set_color(ORANGE).scale(1.25)] if l_index + 1 < len(left) else []),
                    run_time=run_time,
                )
                self.remove(res.labels[res_index])
                res.labels[res_index] = label
                return l_index + 1, r_index
            else:
                label = right.labels[r_index].copy()
                self.play(label.animate.move_to(res.labels[res_index]).set_color(WHITE), run_time=run_time)
                self.play(
                    right.labels[r_index].animate.set_color(WHITE).scale(1 / 1.25),
                    *([right_pointer.animate.shift((right.width + right.spacing) * RIGHT)] if move_pointer else []),
                    *([right.labels[r_index + 1].animate.set_color(ORANGE).scale(1.25)] if r_index + 1 < len(right) else []),
                    run_time=run_time,
                )
                self.remove(res.labels[res_index])
                res.labels[res_index] = label
                return l_index, r_index + 1
        l, r = 0, 0
        l, r = move_smallest(l, r, 0, run_time=0.5)
        l, r = move_smallest(l, r, 1, run_time=0.2)
        l, r = move_smallest(l, r, 2, run_time=0.2)
        l, r = move_smallest(l, r, 3, run_time=0.2)
        l, r = move_smallest(l, r, 4, run_time=0.2)
        l, r = move_smallest(l, r, 5, run_time=0.2)
        l, r = move_smallest(l, r, 6, run_time=0.2)
        self.wait(1)

        # Hide pointers and move the arrays down a bit
        self.play(FadeOut(left_pointer, right_pointer), run_time=0.2)
        self.play(VGroup(left_text, right_text, left_mobj, right_mobj, res_mobj, left_arrow, right_arrow, *res.labels).animate.shift(0.5 * DOWN), run_time=1)
        self.wait(1)

        # Highlight one cell in the result
        self.play(Indicate(res.rectangles[4], scale_factor=1.5, color=ORANGE), run_time=1)

        # Highlight the arrows from a and b to the result (ShowPassingFlash)
        self.play(
            ShowPassingFlash(left_arrow.copy().set_color(WHITE), time_width=0.5, run_time=1),
            ShowPassingFlash(right_arrow.copy().set_color(WHITE), time_width=0.5, run_time=1),
        )
        # Draw an arrow at the top of the result & A+B at the top
        res_arrow = DoubleArrow(
            start=res_mobj.get_left() + 0.5 * UP, end=res_mobj.get_right() + 0.5 * UP,
            color=ORANGE, buff=0, stroke_width=5, max_stroke_width_to_length_ratio=10,
            max_tip_length_to_length_ratio=0.5, tip_length=0.15,
        )
        a_plus_b = MathTex(r'\mathcal{O}(A + B)', color=ORANGE).scale(0.7).next_to(res_arrow, UP, buff=0.1)
        self.play(Create(res_arrow), Write(a_plus_b), run_time=0.5)
        self.wait(1)

        # Highlight A from O(A+B) and the first array
        self.play(Indicate(a_plus_b[0][2], scale_factor=1.6), Indicate(left_mobj), run_time=1)
        self.wait(0.2)
        self.play(Indicate(a_plus_b[0][4], scale_factor=1.6), Indicate(right_mobj), run_time=1)
        self.wait(0.2)

        self.play(ApplyWave(code.chars, run_time=2))
        self.wait(0.5)

        # Transition to the next scene
        self.play(FadeOut(code, a_plus_b, res_arrow), run_time=0.5)
        self.play(*[item.animate.set_color(BLACK) for item in res.labels], run_time=0.5)
        self.play(
            ReplacementTransform(title, Title('Split and Merge', include_underline=False)),
            VGroup(left_mobj, right_mobj, res_mobj, left_text, right_text, left_arrow, right_arrow, *res.labels).animate.shift(0.5 * UP),
            run_time=0.5,
        )
        self.wait(0.5)

        # Move the elements from a and b into the result
        self.play(
            left.labels[0].animate.set_color(ORANGE).scale(1.25),
            right.labels[0].animate.set_color(ORANGE).scale(1.25),
            run_time=0.5,
        )
        l, r = 0, 0
        l, r = move_smallest(l, r, 0, run_time=0.5, move_pointer=False)
        l, r = move_smallest(l, r, 1, run_time=0.2, move_pointer=False)
        l, r = move_smallest(l, r, 2, run_time=0.2, move_pointer=False)
        l, r = move_smallest(l, r, 3, run_time=0.2, move_pointer=False)
        l, r = move_smallest(l, r, 4, run_time=0.2, move_pointer=False)
        l, r = move_smallest(l, r, 5, run_time=0.2, move_pointer=False)
        l, r = move_smallest(l, r, 6, run_time=0.2, move_pointer=False)

        # Fade out a and b
        self.play(FadeOut(
            left_mobj, left_text, left_arrow,
            right_mobj, right_text, right_arrow,
        ), run_time=0.5)

        # Replace the result with the unsorted array [12, 3, 5, 9, 4, 1, 7]
        unsorted = Array(arr)
        unsorted_mobj = unsorted.get_mobject().center().shift(2.2 * UP)
        self.play(TransformMatchingCells(
            VGroup(*chain.from_iterable(zip(res.rectangles, res.labels))),
            unsorted_mobj,
            path_arc=PI/2,
        ), run_time=1)
        self.wait(1)


class SplitMerge(IntroductionSortingVisualized):
    def construct(self):
        title = Title('Split and Merge', include_underline=False)
        self.add(title)
        super().construct(animate_creation=False)


class SplitMergeImplementation(Scene):
    def construct(self):
        title = Title('Split and Merge', include_underline=False)
        self.add(title)
        array = Array(arr)
        array_mobj = array.get_mobject().center().shift(2.2 * UP)
        self.add(array_mobj)

        sorted_array = Array(sorted(arr))
        sorted_array_mobj = sorted_array.get_mobject().center().next_to(array_mobj, DOWN, buff=1)
        pointer_to_sorted = Arrow(
            start=array_mobj.get_bottom(), end=sorted_array_mobj.get_top(),
            color=ORANGE, buff=0.2, stroke_width=5, max_stroke_width_to_length_ratio=10,
            max_tip_length_to_length_ratio=0.5, tip_length=0.15,
        )
        self.play(Create(sorted_array_mobj), Create(pointer_to_sorted), run_time=1)
        self.wait(1)

        code = Code(
            code=dedent('''
                def merge_sort(a):
                    if len(a) <= 1:
                        return a
                
                    l = merge_sort(a[: len(a) // 2])
                    r = merge_sort(a[len(a) // 2:])
                    return merge(l, r)
            ''').strip(),
            tab_width=4,
            language='Python',
            line_spacing=0.6,
            font='Monospace',
            style='monokai',
        ).scale(0.75).center().shift(1.75 * DOWN).code

        self.play(AddTextLetterByLetter(code.chars[0], run_time=0.1 * len(code.chars[0])), FadeOut(pointer_to_sorted, sorted_array_mobj))
        self.wait(0.2)

        self.play(AddTextLetterByLetter(code.chars[1], run_time=0.1 * len(code.chars[1])))
        self.play(AddTextLetterByLetter(code.chars[2], run_time=0.1 * len(code.chars[2])))
        self.wait(0.2)

        # Add left part (code + array)
        l = Array(array.values[: len(array) // 2])
        l_mobj = l.get_mobject().next_to(array_mobj, DOWN, buff=0.4).align_to(array_mobj, LEFT).shift(0.4 * LEFT)
        l_arrow = Arrow(
            start=array_mobj.get_bottom(), end=l_mobj.get_top(),
            color=ORANGE, buff=0.2, stroke_width=5, max_stroke_width_to_length_ratio=10,
            max_tip_length_to_length_ratio=0.5, tip_length=0.15,
        )
        self.play(
            AddTextLetterByLetter(code.chars[4], run_time=0.1 * len(code.chars[4])),
            *[item.animate.set_color(ORANGE).scale(1.25) for item in array.labels[:len(array) // 2]],
            *[item.animate.set_color(DARK_GRAY) for item in array.labels[len(array) // 2:]],
            Create(l_mobj, run_time=1),
            Create(l_arrow, run_time=1),
        )

        # Add right aprt (code + array)
        r = Array(array.values[len(array) // 2:])
        r_mobj = r.get_mobject().next_to(array_mobj, DOWN, buff=0.4).align_to(array_mobj, RIGHT).shift(0.4 * RIGHT)
        r_arrow = Arrow(
            start=array_mobj.get_bottom(), end=r_mobj.get_top(),
            color=ORANGE, buff=0.2, stroke_width=5, max_stroke_width_to_length_ratio=10,
            max_tip_length_to_length_ratio=0.5, tip_length=0.15,
        )
        self.play(
            AddTextLetterByLetter(code.chars[5], run_time=0.1 * len(code.chars[5])),
            l_arrow.animate.set_color(DARK_GRAY),
            *[item.animate.set_color(DARK_GRAY).scale(1 / 1.25) for item in array.labels[: len(array) // 2]],
            *[item.animate.set_color(ORANGE).scale(1.25) for item in array.labels[len(array) // 2:]],
            Create(r_mobj, run_time=1),
            Create(r_arrow, run_time=1),
        )
        self.wait(0.2)

        # Highlight the merge_sort parts of the code
        self.play(
            Indicate(code.chars[4][5:15], scale_factor=1.5),
            Indicate(code.chars[5][5:15], scale_factor=1.5),
            run_time=1,
        )
        self.wait(0.2)

        # Replace the labels of the left and right parts by their sorted versions
        l_sorted = Array(sorted(l.values))
        r_sorted = Array(sorted(r.values))
        l_sorted_mobj = l_sorted.get_mobject().align_to(l_mobj, DOWN).align_to(l_mobj, LEFT)
        r_sorted_mobj = r_sorted.get_mobject().align_to(r_mobj, DOWN).align_to(r_mobj, RIGHT)
        self.play(
            TransformMatchingShapes(l_mobj, l_sorted_mobj),
            TransformMatchingShapes(r_mobj, r_sorted_mobj),
            run_time=1,
        )
        self.wait(0.2)

        self.play(
            *[item.animate.set_color(BLACK) for item in array.labels],
            l_arrow.animate.rotate(PI).set_color(ORANGE),
            r_arrow.animate.rotate(PI).set_color(ORANGE),
            run_time=0.5,
        )
        self.wait(0.2)

        self.play(AddTextLetterByLetter(code.chars[6], run_time=0.1 * len(code.chars[6])))
        self.wait(0.2)

        merge_code = Code(
            code=dedent('''
                def merge(a, b):
                    i, j, res = 0, 0, []
                    while i < len(a) or j < len(b):
                        ai = a[i] if i < len(a) else float('inf')
                        bj = b[j] if j < len(b) else float('inf')
                
                        if ai < bj:
                            res.append(ai)
                            i += 1
                        else:
                            res.append(bj)
                            j += 1
                    return res
            ''').strip(),
            tab_width=4,
            language='Python',
            line_spacing=0.6,
            font='Monospace',
            style='monokai',
        ).scale(0.7).center().shift(1.7 * DOWN).shift(3 * LEFT).code

        # Move the code to the right
        self.play(code.animate.scale(1 / 0.75 * 0.7).align_to(merge_code, UP).shift(3.5 * RIGHT), run_time=1)
        self.wait(0.2)

        for line in merge_code.chars:
            if line:
                self.play(AddTextLetterByLetter(line, run_time=0.01 * len(line)))
        self.wait(0.2)

        # Transition to the next scene
        self.play(
            ReplacementTransform(title, Title('Merge Sort', include_underline=False)),
            code.animate.align_to(merge_code, DOWN),
            FadeOut(l_arrow, r_arrow, l_sorted_mobj, r_sorted_mobj),
            *[item.animate.set_color(WHITE) for item in array.labels],
            run_time=0.5,
        )
        self.wait(1)


class Simulation(Scene):
    def construct(self):
        title = Title('Merge Sort', include_underline=False)
        array = Array(arr)
        array_mobj = array.get_mobject().center().shift(2.2 * UP)
        self.add(title, array_mobj)

        merge_code = Code(
            code=dedent('''
                def merge(a, b):
                    i, j, res = 0, 0, []
                    while i < len(a) or j < len(b):
                        ai = a[i] if i < len(a) else float('inf')
                        bj = b[j] if j < len(b) else float('inf')

                        if ai < bj:
                            res.append(ai)
                            i += 1
                        else:
                            res.append(bj)
                            j += 1
                    return res
            ''').strip(),
            tab_width=4,
            language='Python',
            line_spacing=0.6,
            font='Monospace',
            style='monokai',
        ).scale(0.7).center().shift(1.7 * DOWN).shift(3 * LEFT).code
        self.add(merge_code)

        sort_code = Code(
            code=dedent('''
                def merge_sort(a):
                    if len(a) <= 1:
                        return a

                    l = merge_sort(a[: len(a) // 2])
                    r = merge_sort(a[len(a) // 2:])
                    return merge(l, r)
            ''').strip(),
            tab_width=4,
            language='Python',
            line_spacing=0.6,
            font='Monospace',
            style='monokai',
        ).scale(0.7).center().align_to(merge_code, DOWN).shift(0.25 * DOWN).shift(3.5 * RIGHT).code
        self.add(sort_code)

        self.play(array_mobj.animate.shift(2.8 * RIGHT).shift(0.3 * UP), run_time=0.5)
        self.wait(0.2)

        merge_arrow = Arrow(
            start=LEFT, end=RIGHT, color=YELLOW, buff=0.1,
            stroke_width=10, max_stroke_width_to_length_ratio=15,
            max_tip_length_to_length_ratio=0.5, tip_length=0.2,
        ).scale(0.3).next_to(merge_code, LEFT).align_to(merge_code, UP)

        sort_arrow = Arrow(
            start=LEFT, end=RIGHT, color=RED, buff=0.1,
            stroke_width=10, max_stroke_width_to_length_ratio=15,
            max_tip_length_to_length_ratio=0.5, tip_length=0.2,
        ).scale(0.3).next_to(sort_code, LEFT).align_to(sort_code, UP)
        self.play(Create(sort_arrow), run_time=0.5)
        self.wait(1)

        def merge_sort(a: Array, a_mobj: Mobject, run_time) -> tuple[Array, Mobject]:
            sort_arrow.next_to(sort_code[0], LEFT)
            self.play(FadeIn(sort_arrow), run_time=run_time)
            self.play(sort_arrow.animate.next_to(sort_code[1], LEFT).shift(0.1 * DOWN), run_time=run_time)
            self.wait(run_time)
            if len(a) <= 1:
                self.play(sort_arrow.animate.next_to(sort_code[2], LEFT).shift(0.1 * DOWN), run_time=run_time)
                self.wait(run_time)
                self.play(FadeOut(sort_arrow), run_time=run_time)
                return a, a_mobj

            # Copy the left part of the array and place it on the bottom-left side of the current array => sort it
            l = Array(a.values[: len(a) // 2], width=a.width, height=a.height, spacing=a.spacing, scale_text=a.scale_text, stroke_color=a.stroke_color)
            l_mobj = l.get_mobject().next_to(a_mobj, DOWN, buff=0.4).align_to(a_mobj, LEFT).shift(0.4 * LEFT)
            l_arrow = Arrow(
                start=a_mobj.get_bottom(), end=l_mobj.get_top(),
                color=ORANGE, buff=0.2, stroke_width=5, max_stroke_width_to_length_ratio=10,
                max_tip_length_to_length_ratio=0.5, tip_length=0.15,
            )
            self.play(
                sort_arrow.animate.next_to(sort_code[4], LEFT).shift(0.2 * DOWN),
                *[item.animate.set_color(ORANGE).scale(1.25) for item in a.labels[:len(a) // 2]],
                *[item.animate.set_color(DARK_GRAY) for item in a.labels[len(a) // 2:]],
                run_time=run_time,
            )
            self.wait(run_time)
            self.play(Create(l_mobj), Create(l_arrow), run_time=run_time)
            self.wait(run_time)
            left, left_mobj = merge_sort(l, l_mobj, run_time=run_time)

            # Copy the right part of the array and place it on the bottom-right side of the current array => sort it
            r = Array(a.values[len(a) // 2:], width=a.width, height=a.height, spacing=a.spacing, scale_text=a.scale_text, stroke_color=a.stroke_color)
            r_mobj = r.get_mobject().next_to(a_mobj, DOWN, buff=0.4).align_to(a_mobj, RIGHT).shift(0.4 * RIGHT)
            r_arrow = Arrow(
                start=a_mobj.get_bottom(), end=r_mobj.get_top(),
                color=ORANGE, buff=0.2, stroke_width=5, max_stroke_width_to_length_ratio=10,
                max_tip_length_to_length_ratio=0.5, tip_length=0.15,
            )
            self.play(
                l_arrow.animate.set_color(DARK_GRAY),
                sort_arrow.animate.next_to(sort_code[5], LEFT).shift(0.1 * DOWN),
                *[item.animate.set_color(DARK_GRAY).scale(1 / 1.25) for item in a.labels[: len(a) // 2]],
                *[item.animate.set_color(ORANGE).scale(1.25) for item in a.labels[len(a) // 2:]],
                run_time=run_time,
            )
            self.wait(run_time)
            self.play(Create(r_mobj), Create(r_arrow), run_time=run_time)
            self.wait(run_time)
            right, right_mobj = merge_sort(r, r_mobj, run_time=run_time)

            # Merge the sorted left and right parts and fade the parts out
            res = Array(sorted(a.values), width=a.width, height=a.height, spacing=a.spacing, scale_text=a.scale_text, stroke_color=a.stroke_color)
            res_mobj = res.get_mobject().align_to(a_mobj, DOWN).align_to(a_mobj, LEFT)

            # Merge the left and right into res by moving each number along the straight path from left/right to res cell
            # Hide all the labels of the current array + Reverse the arrows (make pointers direct in the opposite direction)
            self.play(
                sort_arrow.animate.next_to(sort_code[6], LEFT).shift(0.1 * DOWN),
                *[item.animate.set_color(BLACK) for item in a.labels],
                l_arrow.animate.rotate(PI).set_color(ORANGE),
                r_arrow.animate.rotate(PI).set_color(ORANGE),
                run_time=run_time,
            )
            self.wait(run_time)

            # Merge the left and right parts into res
            merge_arrow.next_to(merge_code[0], LEFT)
            self.play(FadeIn(merge_arrow), run_time=run_time)
            self.play(merge_arrow.animate.next_to(merge_code[1], LEFT).shift(0.1 * DOWN), run_time=run_time)
            self.wait(run_time)

            # draw 2 arrows pointing to the first elements of the left and right arrays
            left_pointer = Arrow(
                start=left.rectangles[0].get_bottom() + 0.8 * DOWN, end=left.rectangles[0].get_bottom(),
                color=YELLOW, buff=0.2, stroke_width=5, max_stroke_width_to_length_ratio=10,
                max_tip_length_to_length_ratio=0.5, tip_length=0.15,
            )

            right_pointer = Arrow(
                start=right.rectangles[0].get_bottom() + 0.8 * DOWN, end=right.rectangles[0].get_bottom(),
                color=YELLOW, buff=0.2, stroke_width=5, max_stroke_width_to_length_ratio=10,
                max_tip_length_to_length_ratio=0.5, tip_length=0.15,
            )

            # Highlight the first 2 elements (orange + increase size)
            self.play(
                Create(left_pointer), Create(right_pointer),
                left.labels[0].animate.set_color(YELLOW).scale(1.25),
                right.labels[0].animate.set_color(YELLOW).scale(1.25),
                run_time=run_time,
            )
            self.wait(run_time)

            self.play(merge_arrow.animate.next_to(merge_code[2], LEFT).shift(0.1 * DOWN), run_time=run_time)
            self.wait(run_time)

            for i, val in enumerate(sorted(a.values)):
                self.play(merge_arrow.animate.next_to(merge_code[3], LEFT).shift(0.1 * DOWN), run_time=run_time)
                self.wait(run_time)
                self.play(merge_arrow.animate.next_to(merge_code[4], LEFT).shift(0.1 * DOWN), run_time=run_time)
                self.wait(run_time)
                self.play(merge_arrow.animate.next_to(merge_code[6], LEFT).shift(0.2 * DOWN), run_time=run_time)
                self.wait(run_time)
                if val in left.values:
                    index = left.values.index(val)
                    label = left.labels[index].copy()
                    self.play(merge_arrow.animate.next_to(merge_code[7], LEFT).shift(0.1 * DOWN), run_time=run_time)
                    self.play(label.animate.move_to(res.labels[i].set_color(WHITE)), run_time=run_time)
                    self.wait(run_time)
                    self.play(merge_arrow.animate.next_to(merge_code[8], LEFT).shift(0.1 * DOWN), run_time=run_time)
                    self.play(
                        left.labels[index].animate.set_color(WHITE).scale(1 / 1.25),
                        left_pointer.animate.shift((left.width + left.spacing) * RIGHT),
                        *([left.labels[index + 1].animate.set_color(YELLOW).scale(1.25)] if index + 1 < len(left) else []),
                        run_time=run_time,
                    )
                    self.remove(a.labels[i], a.rectangles[i], label)
                    self.add(res.labels[i].set_z_index(1000000), res.rectangles[i])
                    self.wait(run_time)
                else:
                    index = right.values.index(val)
                    label = right.labels[index].copy()
                    self.play(merge_arrow.animate.next_to(merge_code[10], LEFT).shift(0.1 * DOWN), run_time=run_time)
                    self.play(label.animate.move_to(res.labels[i]), run_time=run_time)
                    self.wait(run_time)
                    self.play(merge_arrow.animate.next_to(merge_code[11], LEFT).shift(0.1 * DOWN), run_time=run_time)
                    self.play(
                        right.labels[index].animate.set_color(WHITE).scale(1 / 1.25),
                        right_pointer.animate.shift((right.width + right.spacing) * RIGHT),
                        *([right.labels[index + 1].animate.set_color(YELLOW).scale(1.25)] if index + 1 < len(right) else []),
                        run_time=run_time,
                    )
                    self.remove(a.labels[i], a.rectangles[i], label)
                    self.add(res.labels[i].set_z_index(1000000), res.rectangles[i])
                    self.wait(run_time)

            self.play(merge_arrow.animate.next_to(merge_code[12], LEFT).shift(0.1 * DOWN), run_time=run_time)
            self.wait(run_time)
            self.remove(l_mobj, r_mobj)
            self.play(FadeOut(left_mobj, right_mobj, l_arrow, r_arrow, merge_arrow, left_pointer, right_pointer), run_time=run_time)
            return res, res_mobj

        merge_sort(array, array_mobj, run_time=0.25)
        self.play(FadeOut(sort_arrow), run_time=0.2)
        self.wait(1)


class ComplexityAnalysis(Scene):
    def construct(self):
        title = Title('Merge Sort', include_underline=False)
        self.add(title)
        array = Array(arr)
        array_mobj = array.get_mobject().center().shift(2.2 * UP).shift(2.8 * RIGHT).shift(0.3 * UP)
        self.add(title, array_mobj)

        merge_code = Code(
            code=dedent('''
                def merge(a, b):
                    i, j, res = 0, 0, []
                    while i < len(a) or j < len(b):
                        ai = a[i] if i < len(a) else float('inf')
                        bj = b[j] if j < len(b) else float('inf')

                        if ai < bj:
                            res.append(ai)
                            i += 1
                        else:
                            res.append(bj)
                            j += 1
                    return res
            ''').strip(),
            tab_width=4,
            language='Python',
            line_spacing=0.6,
            font='Monospace',
            style='monokai',
        ).scale(0.7).center().shift(1.7 * DOWN).shift(3 * LEFT).code
        self.add(merge_code)

        sort_code = Code(
            code=dedent('''
                def merge_sort(a):
                    if len(a) <= 1:
                        return a

                    l = merge_sort(a[: len(a) // 2])
                    r = merge_sort(a[len(a) // 2:])
                    return merge(l, r)
            ''').strip(),
            tab_width=4,
            language='Python',
            line_spacing=0.6,
            font='Monospace',
            style='monokai',
        ).scale(0.7).center().align_to(merge_code, DOWN).shift(0.25 * DOWN).shift(3.5 * RIGHT).code
        self.add(sort_code)

        self.wait(0.2)
        all_mobjects = []
        def merge_sort(a: Array, a_mobj: Mobject) -> tuple[Array, Mobject]:
            nonlocal all_mobjects
            if len(a) <= 1:
                if a.values != [3] and a.values != [5] and a.values != [12]:
                    all_mobjects.append(a_mobj)
                return a, a_mobj

            # Copy the left part of the array and place it on the bottom-left side of the current array => sort it
            l = Array(a.values[: len(a) // 2], width=a.width, height=a.height, spacing=a.spacing, scale_text=a.scale_text, stroke_color=a.stroke_color)
            l_mobj = l.get_mobject().next_to(a_mobj, DOWN, buff=0.4).align_to(a_mobj, LEFT).shift(0.4 * LEFT)
            l_arrow = Arrow(
                start=a_mobj.get_bottom(), end=l_mobj.get_top(),
                color=ORANGE, buff=0.2, stroke_width=5, max_stroke_width_to_length_ratio=10,
                max_tip_length_to_length_ratio=0.5, tip_length=0.15,
            )
            self.play(Create(l_mobj), Create(l_arrow), run_time=0.1)
            left, left_mobj = merge_sort(l, l_mobj)

            # Copy the right part of the array and place it on the bottom-right side of the current array => sort it
            r = Array(a.values[len(a) // 2:], width=a.width, height=a.height, spacing=a.spacing, scale_text=a.scale_text, stroke_color=a.stroke_color)
            r_mobj = r.get_mobject().next_to(a_mobj, DOWN, buff=0.4).align_to(a_mobj, RIGHT).shift(0.4 * RIGHT)
            r_arrow = Arrow(
                start=a_mobj.get_bottom(), end=r_mobj.get_top(),
                color=ORANGE, buff=0.2, stroke_width=5, max_stroke_width_to_length_ratio=10,
                max_tip_length_to_length_ratio=0.5, tip_length=0.15,
            )
            self.play(Create(r_mobj), Create(r_arrow), run_time=0.1)
            right, right_mobj = merge_sort(r, r_mobj)

            # Merge the sorted left and right parts and fade the parts out
            res = Array(sorted(a.values), width=a.width, height=a.height, spacing=a.spacing, scale_text=a.scale_text, stroke_color=a.stroke_color)
            res_mobj = res.get_mobject().align_to(a_mobj, DOWN).align_to(a_mobj, LEFT)
            self.play(TransformMatchingShapes(a_mobj, res_mobj), run_time=0.2)
            if res.values == [3, 5]:
                self.remove(l_mobj, r_mobj)
                self.play(FadeOut(left_mobj, right_mobj, l_arrow, r_arrow), run_time=0.1)
            elif res.values == [3, 5, 12]:
                self.remove(l_mobj, r_mobj)
                self.play(FadeOut(left_mobj, right_mobj), run_time=0.1)
                all_mobjects += [res_mobj, l_arrow, r_arrow]
            else:
                all_mobjects += [res_mobj, l_arrow, r_arrow]
            return res, res_mobj

        merge_sort(array, array_mobj)
        self.wait(0.5)
        self.play(*[mobj.animate.shift(0.4 * DOWN).shift(LEFT) for mobj in all_mobjects], run_time=0.5)
        self.wait(1)

        self.play(LaggedStart(
            ShowPassingFlash(all_mobjects[18].copy().set_color(WHITE), time_width=0.5),
            ShowPassingFlash(all_mobjects[14].copy().set_color(WHITE), time_width=0.5),
            ShowPassingFlash(all_mobjects[7].copy().set_color(WHITE), time_width=0.5),
            lag_ratio=0.6,
            run_time=1,
        ))

        # Bracket next to the depth of the tree (right side)
        depth_bracket = Brace(VGroup(*all_mobjects), direction=RIGHT, stroke_width=1, buff=0.1, color=ORANGE)
        depth_text = depth_bracket.get_tex(r'\mathcal{O}(\log{n})', buff=0).scale(0.6).shift(0.3 * LEFT).set_color(ORANGE)
        self.play(Create(depth_bracket), Write(depth_text), run_time=1)

        # Circumscribe the first, second, and third levels
        self.play(LaggedStart(
            Circumscribe(VGroup(all_mobjects[3], all_mobjects[4], all_mobjects[8], all_mobjects[9]), buff=0.2),
            Circumscribe(VGroup(all_mobjects[5], all_mobjects[10]), buff=0.2),
            Circumscribe(VGroup(all_mobjects[13], all_mobjects[0]), buff=0.2),
            Circumscribe(all_mobjects[16], buff=0.2),
            lag_ratio=0.6,
            run_time=3,
        ))
        self.wait(0.2)

        # Highlight the `merge` function
        self.play(Indicate(merge_code.chars[0][4: 9], scale_factor=1.8), run_time=1)
        self.wait(0.2)

        # Place O(n) next to the fist line
        o_n_1 = MathTex(r'\mathcal{O}(n)', color=YELLOW).scale(0.6).next_to(all_mobjects[16], LEFT, buff=0.8)
        o_n_2 = MathTex(r'\mathcal{O}(n)', color=YELLOW).scale(0.6).next_to(all_mobjects[13], LEFT).align_to(o_n_1, LEFT)
        etc = MathTex(r'\cdots', color=YELLOW).scale(0.6).next_to(o_n_2, DOWN, buff=0.5).align_to(o_n_2, LEFT)
        self.play(LaggedStart(
            Write(o_n_1),
            Write(o_n_2),
            Write(etc),
            run_time=1,
        ))
        self.wait(0.2)

        # Brace at the top with O(n) ⇒ remove the O(n)s for each row
        top_brace = Brace(VGroup(*all_mobjects), direction=UP, stroke_width=1, buff=0.1, color=YELLOW)
        top_text = top_brace.get_tex(r'\mathcal{O}(n)', buff=0).scale(0.6).set_color(YELLOW)
        self.play(
            Create(top_brace),
            ReplacementTransform(VGroup(o_n_1, o_n_2, etc), top_text),
            run_time=1,
        )
        self.wait(0.2)

        # Write Time Complexity:
        time_complexity = Tex('Time Complexity:').scale(0.6).next_to(title, DOWN, buff=1.5).to_edge(LEFT).shift(0.2 * RIGHT)
        self.play(Write(time_complexity), run_time=0.5)
        self.wait(0.2)

        time_o = MathTex(r'\mathcal{O}').scale(0.6).next_to(time_complexity, RIGHT, buff=0.2)
        time_open = MathTex(r'(').scale(0.6).next_to(time_o, RIGHT, buff=0.05)
        time_n = MathTex(r'n').scale(0.6).next_to(time_open, RIGHT, buff=0.05)
        time_times = MathTex(r'\cdot').scale(0.6).next_to(time_n, RIGHT, buff=0.1)
        time_log = MathTex(r'\log{n}').scale(0.6).next_to(time_times, RIGHT, buff=0.1)
        time_close = MathTex(r')').scale(0.6).next_to(time_log, RIGHT, buff=0.05)
        self.play(LaggedStart(
            Write(time_o),
            Write(time_open),
            ReplacementTransform(top_text.copy(), time_n),
            Write(time_times),
            ReplacementTransform(depth_text.copy(), time_log),
            Write(time_close),
            run_time=3,
        ))
        self.wait(0.2)

        # Highlight the res and res.append() calls in the merge function
        self.play(LaggedStart(
            Indicate(merge_code.chars[1][7:10], scale_factor=1.5),
            Indicate(merge_code.chars[7], scale_factor=1.5),
            Indicate(merge_code.chars[10], scale_factor=1.5),
            lag_ratio=0.6,
            run_time=1,
        ))

        self.play(LaggedStart(
            Circumscribe(VGroup(all_mobjects[3], all_mobjects[4], all_mobjects[8], all_mobjects[9]), buff=0.2),
            Circumscribe(VGroup(all_mobjects[5], all_mobjects[10]), buff=0.2),
            Circumscribe(VGroup(all_mobjects[13], all_mobjects[0]), buff=0.2),
            Circumscribe(all_mobjects[16], buff=0.2),
            lag_ratio=0.6,
            run_time=3,
        ))
        self.wait(0.2)

        memory_complexity = Tex(
            r'Memory Complexity: $\mathcal{O}(n)$',
        ).scale(0.6).next_to(time_complexity, DOWN).align_to(time_complexity, LEFT)
        self.play(Write(memory_complexity), run_time=0.5)
        self.wait(0.2)


        self.play(FadeOut(memory_complexity, time_complexity, top_brace, top_text, time_o, time_open, time_n, time_times, time_log, time_close), run_time=0.5)
        self.wait(0.5)

        self.play(Indicate(merge_code.chars[6]), run_time=0.5)
        self.wait(0.2)

        # Write “Radix Sort: Operates on Digits”
        radix_sort = Tex('Radix Sort: Operates on Digits').scale(0.6).next_to(title, DOWN, buff=1.5).to_edge(LEFT).shift(0.2 * RIGHT)
        self.play(Write(radix_sort), run_time=0.5)
        self.wait(0.2)

        merge_sort_text = Tex('Merge Sort: Comparison-Based').scale(0.6).next_to(radix_sort, DOWN, buff=0.2).align_to(radix_sort, LEFT)
        self.play(Write(merge_sort_text), run_time=0.5)
        self.wait(0.2)

        self.play(Indicate(merge_code.chars[6]), run_time=0.5)
        self.wait(1)

        # Replace the numbers with letters
        num2letters = []
        for mobj in all_mobjects:
            if isinstance(mobj, VGroup):
                for item in mobj:
                    if isinstance(item, Tex):
                        letter = string.ascii_lowercase[int(item.tex_string.lower())]
                        num2letters.append(item.animate.become(Tex(letter).scale(0.6), match_center=True))
        self.play(LaggedStart(*num2letters, lag_ratio=0.6, run_time=2))
        self.wait(1)

        # Bring back the numbers
        letters2num = []
        for mobj in all_mobjects:
            if isinstance(mobj, VGroup):
                for item in mobj:
                    if isinstance(item, Tex):
                        letters2num.append(item.animate.become(Tex(item.tex_string).scale(0.6), match_center=True))
        self.play(LaggedStart(*letters2num, lag_ratio=0.6, run_time=2))
        self.wait(1)

        # Final scene
        self.play(merge_sort_text.animate.shift(0.55 * DOWN), run_time=0.2)
        self.play(FadeIn(time_complexity, top_brace, top_text, time_o, time_open, time_n, time_times, time_log, time_close), run_time=0.2)
        self.play(FadeIn(memory_complexity), run_time=0.2)

        # Re-implement the algorithm
        self.play(FadeOut(merge_code, radix_sort), run_time=0.5)
        for line in merge_code.chars:
            if line:
                self.play(AddTextLetterByLetter(line, run_time=0.005 * len(line)))
        self.wait(0.2)

        self.play(FadeOut(sort_code), run_time=0.5)
        for line in sort_code.chars:
            if line:
                self.play(AddTextLetterByLetter(line, run_time=0.005 * len(line)))
        self.wait(0.2)
