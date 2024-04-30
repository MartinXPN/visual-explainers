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
        self.play(Write(title), run_time=5)
        self.wait(1)

        # Definition
        definition = Text('N:', color=GREEN, weight=BOLD).scale(0.7).next_to(title, DOWN).shift(0.5 * DOWN).shift(3 * LEFT)
        definition_divisors = Text(
            r'Only Divisible by 1 and N'
        ).scale(0.7).next_to(definition, RIGHT, buff=0.5).shift(0.03 * DOWN)
        self.play(Write(definition), run_time=1)
        self.wait(1)
        self.play(Write(definition_divisors), run_time=2)
        self.wait(2)

        seven = Text('7:', color=GREEN, weight=BOLD).scale(0.8).next_to(definition, 0.5 * DOWN).shift(0.4 * DOWN)
        seven_divisors = MathTex(
            r'\frac{7}{1} = 7 \hspace{1cm} \frac{7}{7} = 1'
        ).scale(0.8).next_to(seven, RIGHT, buff=0.5).shift(0.03 * DOWN)
        self.play(Write(seven), run_time=1)
        self.play(Write(seven_divisors), run_time=2)
        self.wait(1)

        five = Text('5:', color=GREEN, weight=BOLD).scale(0.8).next_to(seven, 0.5 * DOWN).shift(0.8 * DOWN)
        five_divisors = MathTex(
            r'\frac{5}{1} = 5 \hspace{1cm} \frac{5}{5} = 1'
        ).scale(0.8).next_to(five, RIGHT, buff=0.5).shift(0.03 * DOWN)
        self.play(Write(five), run_time=1)
        self.play(Write(five_divisors), run_time=2)
        self.wait(1)

        nine = Text('9:', color=RED, weight=BOLD).scale(0.8).next_to(five, 0.5 * DOWN).shift(0.8 * DOWN)
        nine_divisors = MathTex(
            r'\frac{9}{1} = 9 \hspace{1cm} \frac{9}{3} = 3 \hspace{1cm} \frac{9}{9} = 1'
        ).scale(0.8).next_to(nine, RIGHT, buff=0.5).shift(0.03 * DOWN)
        self.play(Write(nine), run_time=1)
        self.play(Write(nine_divisors, run_time=2))
        self.wait(2)

        # Draw 2, 3, 5, 7, 11, 13: Prime
        # Draw 4, 6, 8, 9, 10, 12: Not prime
        primes = MathTex(
            r'2, \hspace{0.5cm} 3, \hspace{0.5cm} 5, \hspace{0.5cm} 7, \hspace{0.5cm} 11, \hspace{0.5cm} 13: \hspace{0.5cm} \mathrm{Prime}',
            color=GREEN,
        ).scale(0.8).next_to(nine, 3 * DOWN).align_to(nine, LEFT).shift(0.03 * DOWN)
        self.play(Write(primes, run_time=4))
        self.wait(4)

        non_primes = MathTex(
            r'4, \hspace{0.5cm} 6, \hspace{0.5cm} 8, \hspace{0.5cm} 9, \hspace{0.5cm} 10, \hspace{0.5cm} 12: \hspace{0.5cm} \mathrm{Not \, Prime}',
            color=RED,
        ).scale(0.8).next_to(nine, 5 * DOWN).align_to(nine, LEFT).shift(0.03 * DOWN)
        self.play(Write(non_primes, run_time=4))
        self.wait(4)

        # Fade out the rest
        self.play(FadeOut(primes), FadeOut(non_primes), run_time=0.5)
        self.play(
            FadeOut(definition), FadeOut(definition_divisors),
            FadeOut(seven), FadeOut(seven_divisors),
            FadeOut(five), FadeOut(five_divisors),
            FadeOut(nine), FadeOut(nine_divisors),
            run_time=1,
        )

        # Transition to the next scene
        new_title = Title(r'Find All Prime Numbers \textless \, n', include_underline=False)
        self.play(ReplacementTransform(title, new_title), run_time=1)
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
        self.play(Create(grid_mob), run_time=5)
        self.wait(2)

        for i in range(2, 101):
            if i != 100:
                grid.highlight(i, color=YELLOW)
            if i != 2:
                grid.highlight(i - 1, WHITE)
            self.wait(0.3 if i < 4 else 0.15 if i < 10 else 0.07)

        def draw_divisors(n: int, mobject: VMobject):
            divisors = []
            for div in range(1, n + 1):
                divisor = Text(
                    str(div),
                    color=YELLOW if n % div == 0 and div not in {1, n} else GREEN if n % div == 0 else DARKER_GREY,
                ).scale(0.5)
                divisor.next_to(divisors[-1] if divisors else mobject, RIGHT, buff=0.2)
                divisors.append(divisor)
            return divisors

        two = Text('2:', color=GREEN).scale(0.5).next_to(grid_mob, DOWN, buff=0.5).align_to(grid_mob, LEFT)
        two_divisors = draw_divisors(2, two)
        self.play(Write(two), run_time=1)
        self.play(*[Write(div) for div in two_divisors], run_time=2)
        self.wait(2)
        grid.highlight(2, GREEN)
        self.wait(2)

        three = Text('3:', color=GREEN).scale(0.5).next_to(two, DOWN).align_to(two, LEFT)
        three_divisors = draw_divisors(3, three)
        self.play(Write(three), run_time=1)
        self.play(*[Write(div) for div in three_divisors], run_time=2)
        self.wait(2)
        grid.highlight(3, GREEN)
        self.wait(2)

        four = Text('4:', color=RED).scale(0.5).next_to(three, DOWN).align_to(three, LEFT)
        four_divisors = draw_divisors(4, four)
        self.play(Write(four), run_time=1)
        self.play(*[Write(div) for div in four_divisors], run_time=2)
        self.wait(2)
        grid.highlight(4, DARKER_GREY)
        self.wait(2)

        five = Text('5:', color=GREEN).scale(0.5).next_to(four, DOWN).align_to(four, LEFT)
        five_divisors = draw_divisors(5, five)
        self.play(Write(five), run_time=1)
        self.play(*[Write(div) for div in five_divisors], run_time=2)
        self.wait(1)
        grid.highlight(5, GREEN)

        etc = Text('...', color=WHITE).scale(0.5).next_to(five, DOWN).align_to(five, LEFT)
        self.play(Write(etc), run_time=1)

        for i in range(6, 100):
            if i in primes:
                grid.highlight(i, GREEN)
            else:
                grid.highlight(i, DARKER_GREY)
            self.wait(0.3 if i < 4 else 0.15 if i < 10 else 0.07)

        self.wait(1)
        twenty_five = Text('25:', color=RED).scale(0.5).next_to(etc, DOWN).align_to(etc, LEFT)
        twenty_five_divisors = draw_divisors(25, twenty_five)
        self.play(Write(twenty_five), run_time=1)
        self.play(*[Write(div) for div in twenty_five_divisors], run_time=2)
        self.wait(1)

        # Highlight each divisor of 25
        for i in range(1, 26):
            self.play(twenty_five_divisors[i - 1].animate.set_color(YELLOW), run_time=0.1)

        self.play(Circumscribe(VGroup(*twenty_five_divisors)), run_time=1)

        # Fade 6...25
        self.play(*[div.animate.set_color(DARKER_GREY) for div in twenty_five_divisors])
        self.wait()

        self.play(Circumscribe(VGroup(*twenty_five_divisors[:5])), run_time=1)

        # Highlight up to 5
        for i in range(1, 6):
            self.play(twenty_five_divisors[i - 1].animate.set_color(YELLOW), run_time=0.1)
            self.play(twenty_five_divisors[i - 1].animate.set_color(
                YELLOW if 25 % i == 0 and i not in {1, 25} else GREEN if 25 % i == 0 else DARKER_GREY
            ), run_time=0.2)

        self.play(Circumscribe(VGroup(*twenty_five_divisors[:5])), run_time=1)
        self.wait(5)

        # Write O(n * sqrt(n)) on the right side (below the grid)
        item_complexity = MathTex(r'\mathcal{O}(\sqrt{n}) \, \text{ For Each Number}').scale(0.8).center().next_to(grid_mob, DOWN, buff=1).shift(RIGHT)
        self.play(Write(item_complexity), run_time=2)
        self.wait(4)
        complexity = MathTex(r'\mathcal{O}(n \cdot \sqrt{n})  \, \text{ In Total}').scale(0.8).next_to(item_complexity, DOWN).align_to(item_complexity, LEFT)
        self.play(Write(complexity), run_time=2)
        self.wait(5)

        # Transition to the next scene
        new_title = Title('Sieve of Eratosthenes', include_underline=False)
        self.play(ReplacementTransform(title, new_title), run_time=1)

        # Fade out the rest
        self.play(
            FadeOut(two), FadeOut(three), FadeOut(four), FadeOut(five), FadeOut(etc), FadeOut(twenty_five),
            *map(FadeOut, two_divisors + three_divisors + four_divisors + five_divisors + twenty_five_divisors),
            FadeOut(complexity), FadeOut(item_complexity),
            run_time=1,
        )

        # Replace the grid with 200 numbers
        grid = NumberGrid(200, values_per_row=20)
        grid.highlight(0, color=DARKER_GREY)
        grid.highlight(1, color=DARKER_GREY)
        self.play(
            Create(grid.get_mobject().center().next_to(new_title, DOWN).shift(0.5 * DOWN)),
            run_time=3,
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
        self.wait(4)

        # Highlight all the numbers
        for i in range(2, 200):
            grid.highlight(i, color=YELLOW)
        self.wait(3)

        # Un-highlight all the numbers
        for i in range(2, 200):
            grid.highlight(i, color=WHITE)
        self.wait(2)

        def mark_prime(n: int, wait_ms: float):
            grid.highlight(n, color=GREEN)
            self.wait(wait_ms * 10 if n <= 6 else wait_ms)
            for mul in range(2 * n, 200, n):
                grid.highlight(mul, color=YELLOW)
                if mul < 100 or n >= 5:
                    self.wait(2 * wait_ms if mul < 15 else wait_ms)
                grid.highlight(mul, color=DARKER_GREY)
                if mul < 15:
                    self.wait(2 * wait_ms)

        for i in range(2, 10):
            if i in primes:
                mark_prime(i, wait_ms=0.07)
            else:
                grid.highlight(i, color=RED)
                self.wait(7 if i <= 6 else 0.1)
                grid.highlight(i, DARKER_GREY)
                self.wait(0.1)

        # Mark the rest without loops
        for i in range(10, 25):
            grid.highlight(i, color=YELLOW)
            self.wait(0.07)
            grid.highlight(i, color=GREEN if i in primes else DARKER_GREY)
            self.wait(0.07)

        for i in range(25, 200):
            grid.highlight(i, color=GREEN if i in primes else DARKER_GREY)
            if i < 50:
                self.wait(0.07)

        # Highlight 7 and its multiples
        grid.highlight(7, color=RED)
        self.wait(2)
        for i in range(14, 200, 7):
            grid.highlight(i, color=RED)
        self.wait(1)
        self.play(Circumscribe(grid.rectangles[7]), run_time=2)
        self.wait(6)

        # Circumscribe 14, 21, 28, 35, 42, 49
        for i in range(14, 43, 7):
            self.play(Circumscribe(grid.rectangles[i]), run_time=1)
        self.wait(1)
        self.play(Circumscribe(grid.rectangles[49], color=RED), run_time=1)
        self.wait(2)

        # Highlight 2 and 14 with yellow
        grid.highlight(14, color=YELLOW)
        self.play(Circumscribe(grid.rectangles[14], color=YELLOW), run_time=0.5)

        # Highlight 3 and 21 with orange
        grid.highlight(21, color=BLUE)
        self.play(Circumscribe(grid.rectangles[21], color=BLUE), run_time=0.5)

        # Highlight 4 and 28 with yellow
        grid.highlight(28, color=YELLOW)
        self.play(Circumscribe(grid.rectangles[28], color=YELLOW), run_time=0.5)

        # Highlight 5 and 35 with white
        grid.highlight(35, color=PURPLE)
        self.play(Circumscribe(grid.rectangles[35], color=PURPLE), run_time=0.5)

        grid.highlight(42, color=YELLOW)
        self.play(Circumscribe(grid.rectangles[42], color=YELLOW), run_time=0.5)
        self.wait(4)

        # Highlight 2, 3, 5
        grid.highlight(2, color=YELLOW)
        self.play(
            Circumscribe(grid.rectangles[2], color=YELLOW),
            Circumscribe(grid.rectangles[14], color=YELLOW),
            Circumscribe(grid.rectangles[28], color=YELLOW),
            Circumscribe(grid.rectangles[42], color=YELLOW),
            run_time=1,
        )
        grid.highlight(3, color=BLUE)
        self.play(
            Circumscribe(grid.rectangles[3], color=BLUE),
            Circumscribe(grid.rectangles[21], color=BLUE),
            run_time=0.75,
        )
        grid.highlight(5, color=PURPLE)
        self.play(
            Circumscribe(grid.rectangles[5], color=PURPLE),
            Circumscribe(grid.rectangles[35], color=PURPLE),
            run_time=0.5,
        )

        # Highlight 7 and 49 with red
        grid.highlight(7, color=RED)
        grid.highlight(49, color=RED)
        self.wait(2)
        self.play(Circumscribe(grid.rectangles[49]), run_time=2)

        grid.highlight(2, color=GREEN)
        grid.highlight(3, color=GREEN)
        grid.highlight(5, color=GREEN)
        grid.highlight(7, color=GREEN)
        grid.highlight(14, color=DARKER_GREY)
        grid.highlight(21, color=DARKER_GREY)
        grid.highlight(28, color=DARKER_GREY)
        grid.highlight(35, color=DARKER_GREY)
        grid.highlight(42, color=DARKER_GREY)
        self.wait(5)
        self.play(Circumscribe(grid.rectangles[14]), Circumscribe(grid.rectangles[49]), run_time=2)
        self.wait(4)

        # Highlight 14, 21, 28, 35, 42 to show all the redundant operations
        for i in range(14, 49, 7):
            grid.highlight(i, color=YELLOW)
        self.wait(3)
        for i in range(14, 49, 7):
            grid.highlight(i, color=DARKER_GREY)
        self.wait(0.5)

        for i in range(2, 200):
            if i in primes:
                grid.highlight(i, color=YELLOW)
                self.wait(0.07)
                grid.highlight(i, color=GREEN)
            else:
                grid.highlight(i, DARKER_GREY)
            if i < 20:
                self.wait(0.07)

        # Highlight all the prime numbers
        self.play(*[Circumscribe(grid.rectangles[i], color=GREEN, run_time=2) for i in range(2, 200) if i in primes])
        self.wait(1.5)

        # Transition to the next scene (replace the grid with 100 numbers instead of 200)
        grid = NumberGrid(100, values_per_row=20)
        self.add(grid.get_mobject().center().next_to(title, DOWN).shift(0.5 * DOWN))
        self.play(FadeOut(grid_mob), run_time=1)
        self.wait(1)


class Implementation(Scene):
    def construct(self):
        title = Title('Sieve of Eratosthenes', include_underline=False)
        self.add(title)

        # Draw the number grid
        grid = NumberGrid(100, values_per_row=20)
        grid_mob = grid.get_mobject().center().next_to(title, DOWN).shift(0.5 * DOWN)
        self.add(grid_mob)
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
        ).scale(0.8).next_to(grid_mob, DOWN, buff=0.3).code
        for line in code.chars:
            if line:
                self.play(AddTextLetterByLetter(line), run_time=0.1 * len(line))
            self.wait(1.5)
            if 'if' in line:
                self.wait(1.5)
        self.play(Circumscribe(code.chars[5]), run_time=1)
        self.wait(8)

        # Arrow to show which part of the code is being executed
        arrow = Arrow(
            start=LEFT, end=RIGHT, color=RED, buff=0.1,
            stroke_width=10, max_stroke_width_to_length_ratio=15,
            max_tip_length_to_length_ratio=0.5, tip_length=0.2,
        ).scale(0.3).next_to(code, LEFT).shift(0.95 * UP)
        self.play(Create(arrow), run_time=1)
        self.wait(5)

        # Highlight the 2nd line of the code + Make 0 and 1 transparent
        self.play(arrow.animate.shift(0.35 * DOWN))
        grid.highlight(0, color=DARKER_GREY)
        grid.highlight(1, color=DARKER_GREY)
        self.wait(5)

        # Move arrow to `for p...`
        self.play(arrow.animate.shift(0.6 * DOWN))
        self.wait(4)

        # Show the process
        for p in range(2, 18):
            grid.highlight(p, color=GREEN if p in primes else RED)
            debug_p = Text(
                f'p = {p}', color=GREEN if p in primes else RED,
            ).scale(0.5).next_to(code, RIGHT, buff=0.3)
            self.play(Write(debug_p), run_time=1)

            debug_if = Text(
                f'prime[{p}] = {True if p in primes else False}'
            ).scale(0.5).next_to(debug_p, DOWN, buff=0).align_to(debug_p, LEFT)
            self.play(Write(debug_if), arrow.animate.shift(0.35 * DOWN), run_time=1)
            self.wait(4 if p < 6 else 0.1)

            debug_for = None
            if p in primes:
                multiples = [m for m in range(p * p, 100, p)]
                debug_for = Text(
                    'm = ' + (', '.join(map(str, multiples[:3])) + ', ...' if len(multiples) > 3
                              else ', '.join(map(str, multiples)) if multiples
                              else '∅')
                ).scale(0.5).next_to(debug_if, DOWN, buff=0).align_to(debug_if, LEFT)
                self.play(Write(debug_for), arrow.animate.shift(0.35 * DOWN), run_time=1)

                # Highlight multiples with dark grey
                for m in range(p * p, 100, p):
                    if p >= 5:
                        grid.highlight(m, color=YELLOW)
                        self.wait(0.07)
                    grid.highlight(m, color=DARKER_GREY)
                    self.wait(0.07)

                if p == 17:
                    self.play(Circumscribe(code.chars[5]), run_time=2)
                    self.wait(3)

                # Move the arrow up
                self.play(arrow.animate.shift(0.35 * UP), run_time=0.2)

            # Move the arrow up
            self.play(
                arrow.animate.shift(0.35 * UP),
                FadeOut(debug_p, debug_if, *([debug_for] if debug_for else [])),
                run_time=0.2,
            )

        # Highlight the outer loop
        self.wait(1)
        sqrt_n = MathTex(r'\sqrt{n}').scale(0.5).next_to(arrow, LEFT, buff=0.2)
        self.play(Write(sqrt_n), run_time=1)
        self.wait(3)

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
        self.play(AddTextLetterByLetter(new_code.chars[3]), run_time=0.1 * len(new_code.chars[3]))
        self.wait(7)

        self.play(FadeOut(sqrt_n), FadeOut(arrow), run_time=0.5)
        self.wait(2)
        self.play(Circumscribe(code))
        self.wait(6)

        # Highlight the prime numbers
        for i in range(2, 100):
            if i in primes:
                grid.highlight(i, color=YELLOW)
            else:
                grid.highlight(i, color=DARKER_GREY)
        self.wait(3)

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
        self.wait(3)

        self.play(VGroup(code.chars).animate.shift(2.5 * LEFT), run_time=1)

        # Memory complexity
        self.play(Circumscribe(grid_mob, run_time=2))
        self.wait(2)
        memory_complexity = Tex(
            r'Memory Complexity: $\mathcal{O}(n)$'
        ).scale(0.6).next_to(VGroup(code.chars), RIGHT, buff=0.5).shift(0.2 * UP)
        self.play(Write(memory_complexity), run_time=1)
        self.wait(2)

        # Time complexity
        time_complexity = Tex(
            r'Time Complexity: $\mathcal{O}(n \cdot \log(\log(n)))$'
        ).scale(0.6).next_to(memory_complexity, DOWN, buff=0.2).align_to(memory_complexity, LEFT)
        self.play(Write(time_complexity), run_time=1)
        self.wait(15)

        # Practice (Remove the code and write it again)
        for line in code.chars[::-1]:
            if line:
                self.play(RemoveTextLetterByLetter(line), run_time=0.02 * len(line))
        for line in code.chars:
            if line:
                self.play(AddTextLetterByLetter(line), run_time=0.08 * len(line))

        self.wait(7.5)
