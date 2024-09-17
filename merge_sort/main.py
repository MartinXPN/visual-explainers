import random
from textwrap import dedent

from manim import *

from merge_sort.array import Array, TransformMatchingCells

arr = [12, 3, 5, 9, 4, 1, 7]
ORANGE = ManimColor('#fa541c')
random.seed(42)


class Introduction(Scene):
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
        self.wait(1)

        self.play(LaggedStart(
            *[item.bar.animate.set_color(ORANGE) for item in sorted_array],
            lag_ratio=0.6,
            run_time=4,
        ))
        self.wait(1)

        for item in sorted_array:
            item.bar.set_color(WHITE)
        self.wait(1)
