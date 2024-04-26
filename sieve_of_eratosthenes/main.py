from textwrap import dedent

from manim import *

from sieve_of_eratosthenes.numbers import NumberGrid

primes = {
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97,
    101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199,
}


class Opening(Scene):
    def construct(self):
        title = Title('Prime Numbers', include_underline=False)
        self.add(title)
        self.wait(0.1)

        seven = Text('7:', color=GREEN, weight=BOLD).scale(0.8).next_to(title, DOWN).shift(DOWN).shift(3 * LEFT)
        seven_divisors = MathTex(
            r'\frac{7}{1} = 7 \hspace{1cm} \frac{7}{7} = 1'
        ).scale(0.8).next_to(seven, RIGHT, buff=0.5).shift(0.03 * DOWN)
        self.play(Write(seven), run_time=0.1)
        self.play(Write(seven_divisors), run_time=0.1)
        self.wait(0.1)

        five = Text('5:', color=GREEN, weight=BOLD).scale(0.8).next_to(seven, 0.5 * DOWN).shift(DOWN)
        five_divisors = MathTex(
            r'\frac{5}{1} = 5 \hspace{1cm} \frac{5}{5} = 1'
        ).scale(0.8).next_to(five, RIGHT, buff=0.5).shift(0.03 * DOWN)
        self.play(Write(five), run_time=0.1)
        self.play(Write(five_divisors), run_time=0.1)

        nine = Text('9:', color=RED, weight=BOLD).scale(0.8).next_to(five, 0.5 * DOWN).shift(DOWN)
        nine_divisors = MathTex(
            r'\frac{9}{1} = 9 \hspace{1cm} \frac{9}{3} = 3 \hspace{1cm} \frac{9}{9} = 1'
        ).scale(0.8).next_to(nine, RIGHT, buff=0.5).shift(0.03 * DOWN)
        self.play(Write(nine), run_time=0.1)
        self.play(Write(nine_divisors, run_time=0.1))

        # Draw 2, 3, 5, 7, 11, 13: Prime
        # Draw 4, 6, 8, 9, 10, 12: Not prime
        primes = MathTex(
            r'2, \hspace{0.5cm} 3, \hspace{0.5cm} 5, \hspace{0.5cm} 7, \hspace{0.5cm} 11, \hspace{0.5cm} 13: \hspace{0.5cm} \mathrm{Prime}',
            color=GREEN,
        ).scale(0.8).next_to(nine, 3 * DOWN).align_to(nine, LEFT).shift(0.03 * DOWN)
        self.play(Write(primes, run_time=0.1))

        non_primes = MathTex(
            r'4, \hspace{0.5cm} 6, \hspace{0.5cm} 8, \hspace{0.5cm} 9, \hspace{0.5cm} 10, \hspace{0.5cm} 12: \hspace{0.5cm} \mathrm{Not \, Prime}',
            color=RED,
        ).scale(0.8).next_to(nine, 5 * DOWN).align_to(nine, LEFT).shift(0.03 * DOWN)
        self.play(Write(non_primes, run_time=0.1))

        # Transition to the next scene
        new_title = Title(r'Find All Prime Numbers \textless \, n', include_underline=False)
        self.play(ReplacementTransform(title, new_title), run_time=0.2)

        # Fade out the rest
        self.play(FadeOut(primes), FadeOut(non_primes), run_time=0.1)
        self.play(FadeOut(seven_divisors), FadeOut(five_divisors), FadeOut(nine_divisors), run_time=0.1)
        self.play(FadeOut(seven), FadeOut(five), FadeOut(nine), run_time=0.1)
        self.wait(1)


class NaiveApproach(Scene):
    def construct(self):
        title = Title(r'Find All Prime Numbers \textless \, n', include_underline=False)
        self.add(title)

        # Draw the number grid
        grid = NumberGrid(100, values_per_row=20)
        grid.highlight(0, color=DARKER_GREY)
        grid.highlight(1, color=DARKER_GREY)
        grid_mob = grid.get_mobject().center().next_to(title, DOWN).shift(0.5 * DOWN)
        self.play(Create(grid_mob), run_time=1)

        for i in range(2, 101):
            if i != 100:
                grid.highlight(i, color=RED)
            if i != 2:
                grid.highlight(i - 1, WHITE)
            self.wait(0.3 if i < 10 else 0.15 if i < 25 else 0.08)

        self.wait(1)

        def draw_divisors(n: int, mobject: VMobject):
            divisors = []
            for div in range(1, n + 1):
                divisor = Text(str(div), color=GREEN if n % div == 0 else RED).scale(0.5)
                divisor.next_to(divisors[-1] if divisors else mobject, RIGHT, buff=0.2)
                divisors.append(divisor)
            return divisors

        two = Text('2:', color=GREEN).scale(0.5).next_to(grid_mob, DOWN, buff=0.5).align_to(grid_mob, LEFT)
        two_divisors = draw_divisors(2, two)
        self.play(Write(two), run_time=0.1)
        self.play(*[Write(div) for div in two_divisors], run_time=0.5)
        grid.highlight(2, GREEN)

        three = Text('3:', color=GREEN).scale(0.5).next_to(two, DOWN).align_to(two, LEFT)
        three_divisors = draw_divisors(3, three)
        self.play(Write(three), run_time=0.1)
        self.play(*[Write(div) for div in three_divisors], run_time=0.5)
        grid.highlight(3, GREEN)

        four = Text('4:', color=RED).scale(0.5).next_to(three, DOWN).align_to(three, LEFT)
        four_divisors = draw_divisors(4, four)
        self.play(Write(four), run_time=0.1)
        self.play(*[Write(div) for div in four_divisors], run_time=0.5)
        grid.highlight(4, DARKER_GREY)

        five = Text('5:', color=GREEN).scale(0.5).next_to(four, DOWN).align_to(four, LEFT)
        five_divisors = draw_divisors(5, five)
        self.play(Write(five), run_time=0.1)
        self.play(*[Write(div) for div in five_divisors], run_time=0.5)
        grid.highlight(5, GREEN)

        etc = Text('...', color=WHITE).scale(0.5).next_to(five, DOWN).align_to(five, LEFT)
        self.play(Write(etc), run_time=0.1)

        for i in range(6, 100):
            if i in primes:
                grid.highlight(i, GREEN)
            else:
                grid.highlight(i, DARKER_GREY)
            self.wait(0.3 if i < 10 else 0.15 if i < 25 else 0.08)

        twenty_five = Text('25:', color=RED).scale(0.5).next_to(etc, DOWN).align_to(etc, LEFT)
        twenty_five_divisors = draw_divisors(25, twenty_five)
        self.play(Write(twenty_five), run_time=0.1)
        self.play(*[Write(div) for div in twenty_five_divisors], run_time=0.5)

        self.play(Circumscribe(VGroup(*twenty_five_divisors)), run_time=0.5)

        # Fade 6...25
        for i in range(5, 25):
            twenty_five_divisors[i].set_color(DARKER_GREY)

        self.play(Circumscribe(VGroup(*twenty_five_divisors[:5])), run_time=0.5)

        # Write O(n * sqrt(n)) on the right side (below the grid)
        complexity = MathTex(r'\mathcal{O}(n \cdot \sqrt{n})').scale(0.8).center().next_to(grid_mob, DOWN, buff=1)
        self.play(Write(complexity), run_time=0.1)

        # Transition to the next scene
        new_title = Title('Sieve of Eratosthenes', include_underline=False)
        self.play(ReplacementTransform(title, new_title), run_time=0.2)

        # Fade out the rest
        self.play(
            FadeOut(two), FadeOut(three), FadeOut(four), FadeOut(five), FadeOut(etc), FadeOut(twenty_five),
            *map(FadeOut, two_divisors + three_divisors + four_divisors + five_divisors + twenty_five_divisors),
            FadeOut(complexity),
            run_time=2,
        )

        # Replace the grid with 200 numbers
        grid = NumberGrid(200, values_per_row=20)
        grid.highlight(0, color=DARKER_GREY)
        grid.highlight(1, color=DARKER_GREY)
        self.play(
            Create(grid.get_mobject().center().next_to(new_title, DOWN).shift(0.5 * DOWN)),
            run_time=1,
        )

        self.wait(1)


class SieveOfEratosthenes(Scene):
    def construct(self):
        title = Title('Sieve of Eratosthenes', include_underline=False)
        self.add(title)

        # Draw the number grid
        grid = NumberGrid(200, values_per_row=20)
        grid.highlight(0, color=DARKER_GREY)
        grid.highlight(1, color=DARKER_GREY)
        grid_mob = grid.get_mobject().center().next_to(title, DOWN).shift(0.5 * DOWN)
        self.add(grid_mob)
        self.wait(1)

        # Highlight all the numbers
        for i in range(2, 200):
            grid.highlight(i, color=YELLOW)
        self.wait(1)

        # Un-highlight all the numbers
        for i in range(2, 200):
            grid.highlight(i, color=WHITE)
        self.wait(1)

        def mark_prime(n: int, wait_ms: float = 0.01):
            grid.highlight(n, color=GREEN)
            self.wait(wait_ms * 10)
            for mul in range(2 * n, 200, n):
                grid.highlight(mul, color=YELLOW)
                self.wait(wait_ms)
                grid.highlight(mul, color=DARKER_GREY)
                self.wait(wait_ms)

        for i in range(2, 200):
            if i in primes:
                mark_prime(i, wait_ms=0.05 if i <= 6 else 0.01)
            else:
                grid.highlight(i, color=RED)
                self.wait(0.05)
                grid.highlight(i, DARKER_GREY)
            self.wait(0.02)

        # Highlight 7 and its multiples
        grid.highlight(7, color=RED)
        self.wait(0.5)
        for i in range(14, 200, 7):
            grid.highlight(i, color=RED)
        self.wait(0.5)

        # Highlight 2 and 14 with yellow
        grid.highlight(2, color=YELLOW)
        grid.highlight(14, color=YELLOW)
        self.wait(0.5)

        # Highlight 3 and 21 with orange
        grid.highlight(3, color=BLUE)
        grid.highlight(21, color=BLUE)
        self.wait(0.5)

        # Highlight 2 and 28 with yellow
        grid.highlight(2, color=YELLOW)
        grid.highlight(28, color=YELLOW)
        self.wait(0.5)

        # Highlight 5 and 35 with white
        grid.highlight(5, color=PURPLE)
        grid.highlight(35, color=PURPLE)
        self.wait(0.5)

        # Highlight 7 and 49 with red
        grid.highlight(7, color=RED)
        grid.highlight(49, color=RED)
        self.wait(0.5)

        for i in range(49, 200, 7):
            grid.highlight(i, color=RED)
        self.wait(1)

        for i in range(2, 200):
            if i in primes:
                grid.highlight(i, color=YELLOW)
                self.wait(0.01)
                grid.highlight(i, color=GREEN)
            else:
                grid.highlight(i, DARKER_GREY)
            self.wait(0.01)

        self.wait(1)

        # Transition to the next scene (replace the grid with 100 numbers instead of 200)
        grid = NumberGrid(100, values_per_row=20)
        grid.highlight(0, color=DARKER_GREY)
        grid.highlight(1, color=DARKER_GREY)
        self.add(grid.get_mobject().center().next_to(title, DOWN).shift(0.5 * DOWN))
        self.remove(grid_mob)
        self.wait(1)


class Implementation(Scene):
    def construct(self):
        title = Title('Sieve of Eratosthenes', include_underline=False)
        self.add(title)

        # Draw the number grid
        grid = NumberGrid(100, values_per_row=20)
        grid_mob = grid.get_mobject().center().next_to(title, DOWN).shift(0.5 * DOWN)
        self.add(grid_mob)
        self.wait(0.1)

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
        ).scale(0.8).next_to(grid_mob, DOWN, buff=0.3).code
        for line in code.chars:
            if line:
                self.play(AddTextLetterByLetter(line), run_time=0.08 * len(line))
        self.wait(0.1)

        # Arrow to show which part of the code is being executed
        arrow = Arrow(
            start=LEFT, end=RIGHT, color=RED, buff=0.1,
            stroke_width=10, max_stroke_width_to_length_ratio=15,
            max_tip_length_to_length_ratio=0.5, tip_length=0.2,
        ).scale(0.3).next_to(code, LEFT).shift(0.95 * UP)
        self.play(Create(arrow), run_time=0.5)
        self.wait(1)

        # Highlight the 2nd line of the code + Make 0 and 1 transparent
        self.play(arrow.animate.shift(0.35 * DOWN))
        grid.highlight(0, color=DARKER_GREY)
        grid.highlight(1, color=DARKER_GREY)
        self.wait(0.1)

        # Move arrow to `for p...`
        self.play(arrow.animate.shift(0.6 * DOWN))

        # Show the process
        for p in range(2, 18):
            grid.highlight(p, color=GREEN if p in primes else RED)
            debug_p = Text(
                f'p = {p}', color=GREEN if p in primes else RED,
            ).scale(0.5).next_to(code, RIGHT, buff=0.3)
            self.play(Write(debug_p), run_time=0.1)

            debug_if = Text(
                f'prime[{p}] = {True if p in primes else False}'
            ).scale(0.5).next_to(debug_p, DOWN, buff=0).align_to(debug_p, LEFT)
            self.play(Write(debug_if), arrow.animate.shift(0.35 * DOWN), run_time=0.1)
            self.wait(0.1)

            if p in primes:
                multiples = [m for m in range(p * p, 100, p)]
                debug_for = Text(
                    'm = ' + (', '.join(map(str, multiples[:3])) + ', ...' if len(multiples) > 3
                              else ', '.join(map(str, multiples)) if multiples
                              else '∅')
                ).scale(0.5).next_to(debug_if, DOWN, buff=0).align_to(debug_if, LEFT)
                self.play(Write(debug_for), arrow.animate.shift(0.35 * DOWN), run_time=0.1)
                self.wait(0.1)

                # Highlight multiples with dark grey
                for m in range(p * p, 100, p):
                    grid.highlight(m, color=YELLOW)
                    self.wait(0.05)
                    grid.highlight(m, color=DARKER_GREY)
                    self.wait(0.05)

                if p == 17:
                    self.wait(1)

                # Move the arrow up
                self.play(arrow.animate.shift(0.35 * UP), run_time=0.1)

            # Move the arrow up
            self.play(arrow.animate.shift(0.35 * UP), run_time=0.1)
            self.play(FadeOut(debug_p, debug_if, debug_for), run_time=0.1)

        # Highlight the outer loop
        sqrt_n = MathTex(r'\sqrt{n}').scale(0.5).next_to(arrow, LEFT, buff=0.2)
        self.play(Write(sqrt_n), run_time=0.1)

        # New Code for the Sieve of Eratosthenes
        new_code = Code(
            code=dedent('''
                        prime = [True] * n
                        prime[0] = prime[1] = False

                        for p in range(2, isqrt(n) + 1):
                            if prime[p]:
                                for m in range(p * p, n, p):
                                    prime[m] = False
                        ''').strip(),
            tab_width=4,
            language='Python',
            line_spacing=0.6,
            font='Monospace',
            style='monokai',
        ).scale(0.8).next_to(grid_mob, DOWN, buff=0.3).code

        self.play(RemoveTextLetterByLetter(code.chars[3]), run_time=0.03 * len(code.chars[3]))
        self.play(AddTextLetterByLetter(new_code.chars[3]), run_time=0.08 * len(new_code.chars[3]))
        self.wait(1)

        self.play(FadeOut(sqrt_n), FadeOut(arrow), run_time=0.1)
        self.play(Circumscribe(code))

        # Highlight the prime numbers
        for i in range(2, 100):
            if i in primes:
                grid.highlight(i, color=YELLOW)
            else:
                grid.highlight(i, color=DARKER_GREY)
        self.wait(1)

        # Bring back the colors
        for i in range(2, 100):
            if i in primes:
                grid.highlight(i, color=GREEN)
        self.wait(1)


class TimeMemoryComplexity(Scene):
    def construct(self):
        title = Title('Sieve of Eratosthenes', include_underline=False)
        self.add(title)

        # Draw the number grid
        grid = NumberGrid(100, values_per_row=20)
        grid_mob = grid.get_mobject().center().next_to(title, DOWN).shift(0.5 * DOWN)
        for i in range(100):
            if i in primes:
                grid.highlight(i, color=GREEN)
            else:
                grid.highlight(i, DARKER_GREY)
        self.add(grid_mob)

        # Add the code
        code = Code(
            code=dedent('''
                        prime = [True] * n
                        prime[0] = prime[1] = False

                        for p in range(2, isqrt(n) + 1):
                            if prime[p]:
                                for m in range(p * p, n, p):
                                    prime[m] = False
                        ''').strip(),
            tab_width=4,
            language='Python',
            line_spacing=0.6,
            font='Monospace',
            style='monokai',
        ).scale(0.8).next_to(grid_mob, DOWN, buff=0.3).code
        self.add(code)
        self.wait(0.1)

        self.play(VGroup(code.chars).animate.shift(2.5 * LEFT), run_time=0.1)

        # Memory complexity
        self.play(Circumscribe(grid_mob))
        memory_complexity = Tex(
            r'Memory Complexity: $\mathcal{O}(n)$'
        ).scale(0.6).next_to(VGroup(code.chars), RIGHT, buff=0.5).shift(0.2 * UP)
        self.play(Write(memory_complexity), run_time=0.1)

        # Time complexity
        time_complexity = Tex(
            r'Time Complexity: $\mathcal{O}(n \cdot \log(\log(n)))$'
        ).scale(0.6).next_to(memory_complexity, DOWN, buff=0.2).align_to(memory_complexity, LEFT)
        self.play(Write(time_complexity), run_time=0.1)
        self.wait(2)

        # Practice (Remove the code and write it again)
        self.play(FadeOut(code), run_time=0.1)
        for line in code.chars:
            if line:
                self.play(AddTextLetterByLetter(line), run_time=0.08 * len(line))

        self.wait(1)
