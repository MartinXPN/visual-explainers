import random

from manim import *

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
