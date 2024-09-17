import random
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
    def construct(self):
        array = Array(arr)
        array_mobj = array.get_mobject().center().shift(2.5 * UP)
        self.play(Create(array_mobj))
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
            run_time=4,
        ))

        self.wait(1)
