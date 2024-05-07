from textwrap import dedent

from manim import *

from sieve_of_eratosthenes.numbers import NumberGrid


all_primes = {
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97,
}


class Opening(Scene):
    def __init__(self, *args, **kwargs):
        config.pixel_height, config.pixel_width = config.pixel_width, config.pixel_height
        config.frame_height = config.frame_height / 0.8
        config.frame_width = config.frame_height * 9 / 16
        super().__init__(*args, **kwargs)

    def construct(self):
        title = Tex(r'Find All Prime Numbers \textless \, n', font_size=32).center().shift(3.5 * UP)
        self.wait(1)
        self.play(Write(title), run_time=2)
        self.wait(3)

        # Definition
        definition = Text('N:', color=GREEN, weight=BOLD, font_size=22).next_to(title, DOWN, buff=1).shift(2 * LEFT)
        definition_divisors = Text(
            r'Only Divisible by 1 and N', font_size=22,
        ).next_to(definition, RIGHT, buff=0.5).shift(0.03 * DOWN)
        self.play(Write(definition), run_time=1)
        self.wait(1)
        self.play(Write(definition_divisors), run_time=1)
        self.wait(2)

        # Draw primes
        primes = MathTex(
            r'5, \, 7, \text{ or } 11: \, \text{Prime}',
            color=GREEN,
        ).scale(0.6).next_to(definition, DOWN, buff=0.5).align_to(definition, LEFT)
        self.play(Write(primes), run_time=2)
        self.wait(3)

        # Draw non-primes
        non_primes = MathTex(
            r'6, \, 8, \text{ or } 12: \, \text{Not Prime}',
            color=RED,
        ).scale(0.6).next_to(primes, DOWN, buff=0.5).align_to(primes, LEFT)
        self.play(Write(non_primes), run_time=2)
        self.wait(5)

        # Change the title and fade out the rest
        new_title = Tex(r'Sieve of Eratosthenes', font_size=32).center().shift(3.5 * UP)
        self.play(
            Transform(title, new_title),
            FadeOut(primes), FadeOut(non_primes), FadeOut(definition), FadeOut(definition_divisors),
            run_time=1,
        )

        # Draw the number grid
        grid = NumberGrid(100, values_per_row=10, spacing=0.05, scale_text=0.4)
        grid.highlight(0, color=DARKER_GREY)
        grid.highlight(1, color=DARKER_GREY)
        grid_mob = grid.get_mobject().center().next_to(title, DOWN).shift(0.2 * DOWN).shift(0.2 * LEFT)
        self.play(Create(grid_mob), run_time=3)
        self.wait(1)

        # Highlight all the prime numbers
        for prime in all_primes:
            grid.highlight(prime, color=GREEN)

        # Make the prime numbers larger
        self.play(*[grid.labels[prime].animate.scale(1.5) for prime in all_primes], run_time=1)
        self.play(*[Wiggle(grid.labels[prime]) for prime in all_primes], run_time=1)
        self.play(*[Wiggle(grid.labels[prime]) for prime in all_primes], run_time=1.5)
        self.play(*[grid.labels[prime].animate.scale(1 / 1.5) for prime in all_primes], run_time=1)


class SieveOfEratosthenesImplementation(Scene):
    def __init__(self, *args, **kwargs):
        config.pixel_height, config.pixel_width = config.pixel_width, config.pixel_height
        config.frame_height = config.frame_height / 0.8
        config.frame_width = config.frame_height * 9 / 16
        super().__init__(*args, **kwargs)

    def construct(self):
        title = Tex(r'Sieve of Eratosthenes', font_size=32).center().shift(3.5 * UP)
        self.add(title)

        # Draw the number grid
        grid = NumberGrid(80, values_per_row=10, spacing=0.05, scale_text=0.4)
        grid.highlight(0, color=DARKER_GREY)
        grid.highlight(1, color=DARKER_GREY)
        grid_mob = grid.get_mobject().center().next_to(title, DOWN).shift(0.2 * DOWN).shift(0.2 * LEFT)
        self.add(grid_mob)

        # Highlight all the prime numbers
        global all_primes
        all_primes = {prime for prime in all_primes if prime < 80}
        for prime in all_primes:
            grid.highlight(prime, color=GREEN)

        # Make the prime numbers larger
        self.play(*[grid.labels[prime].animate.scale(1.5) for prime in all_primes])
        self.play(*[Wiggle(grid.labels[prime]) for prime in all_primes])
        self.play(*[Wiggle(grid.labels[prime]) for prime in all_primes], run_time=1.5)
        self.play(*[grid.labels[prime].animate.scale(1 / 1.5) for prime in all_primes])
        self.wait(2)

        # Code for the Sieve of Eratosthenes
        code = Code(
            code=dedent('''
                prime = [True] * n
                prime[0] = prime[1] = False

                for p in range(2, n):
                    if prime[p]:
                        for m in range(p * p, n, p):
                            prime[m] = False
                ''').strip(),
            tab_width=4,
            language='Python',
            line_spacing=0.6,
            font='Monospace',
            style='monokai',
        ).scale(0.6).next_to(grid_mob, DOWN, buff=0.3).shift(0.25 * LEFT).code
        for line in code.chars:
            if line:
                self.play(AddTextLetterByLetter(line), run_time=0.1 * len(line))
            self.wait(1.5)
            if 'for p' in line:
                self.wait(1.5)
            if 'if' in line:
                self.wait(1.5)

        # Arrow to show which part of the code is being executed
        arrow = (Arrow(
            start=LEFT, end=RIGHT, color=RED, buff=0.1,
            stroke_width=10, max_stroke_width_to_length_ratio=15,
            max_tip_length_to_length_ratio=0.5, tip_length=0.2,
        ).scale(0.3).next_to(code, LEFT).shift(0.55 * DOWN).shift(0.7 * RIGHT))
        self.play(Create(arrow), run_time=1)
        self.wait(2)

        self.play(arrow.animate.shift(0.25 * DOWN))
        self.wait(3)
