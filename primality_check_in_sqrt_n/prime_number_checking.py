from manim import *


class PrimeNumberChecking(MovingCameraScene):

    def plot_rectangle(self,
                       height, width,
                       old_rect=None):

        number = height * width
        rect = Rectangle(color=ORANGE, height=height, width=width, fill_opacity=1)

        # Position correctly
        rect.move_to([-6 + width / 2, 3 - height / 2, 0])

        if old_rect is None:
            # updates for n
            self.n = Integer(number)
            self.n_tracker = ValueTracker(number)
            self.n.add_updater(lambda d: d.set_value(self.n_tracker.get_value()))

            # updates for h
            self.h = Integer(height)
            self.h_tracker = ValueTracker(height)
            self.h.add_updater(lambda d: d.set_value(self.h_tracker.get_value()))
            self.h.add_updater(lambda d: d.move_to([-6 + self.w_tracker.get_value() + 0.5,
                                                    3 - self.h_tracker.get_value() / 2,
                                                    0]))

            # updates for w
            self.w = Integer(width)
            self.w_tracker = ValueTracker(width)
            self.w.add_updater(lambda d: d.set_value(self.w_tracker.get_value()))
            self.w.add_updater(lambda d: d.move_to([-6 + self.w_tracker.get_value() / 2,
                                                    3 - self.h_tracker.get_value() - 0.5,
                                                    0]))

            n = Tex(r'n = ')
            VGroup(n, self.n).arrange(RIGHT)
            n.shift(3.5 * UP)
            self.n.shift(3.5 * UP)
            self.play(
                Write(n),
                Create(self.n),
                FadeIn(rect),
                Create(self.h),
                Create(self.w),
            )

        else:
            self.play(
                self.n_tracker.animate.set_value(number),
                self.h_tracker.animate.set_value(height),
                self.w_tracker.animate.set_value(width),
                ReplacementTransform(old_rect, rect),
            )

        return rect

    def construct(self):
        # Title page
        title = Text('Checking if a number is prime')
        self.play(
            Write(title),
        )
        self.wait()

        # Grid
        grid = NumberPlane(y_range=[0, 64], x_range=[0, 80])
        self.add(grid)
        self.play(
            FadeOut(title),
            Create(grid, run_time=3, lag_ratio=0.1),
        )
        self.wait()

        # Any number can be represented as a product of two numbers
        rect = self.plot_rectangle(2, 3)
        self.wait(10)

        rect = self.plot_rectangle(5, 5, rect)
        self.wait(5)

        rect = self.plot_rectangle(1, 7, rect)
        self.wait(3)

        rect = self.plot_rectangle(1, 1, rect)
        self.wait(4)

        rect = self.plot_rectangle(5, 2, rect)
        self.wait(3)

        # Prime numbers
        text_background = Rectangle(color=BLACK, height=5, width=2.5, fill_opacity=1)
        text_background.to_corner(DR, buff=0)
        self.add(text_background)

        prime_5 = Text('5 is prime', color=YELLOW, font_size=23)
        prime_5.to_corner(DR)
        primes = prime_5
        self.add(prime_5)

        rect = self.plot_rectangle(1, 5, rect)
        self.wait(10)

        rect = self.plot_rectangle(5, 1, rect)
        self.wait(2)

        # There is no difference between 1*5 or 5*1 => we'll only consider 1 * 5
        rect = self.plot_rectangle(1, 5, rect)
        self.wait(2)

        rect = self.plot_rectangle(1, 6, rect)
        self.wait(2)

        prime_6 = Text('6 is not prime', color=WHITE, font_size=23)
        primes = VGroup(primes, prime_6)
        primes.arrange(UP)
        primes.to_corner(DR)
        self.add(prime_6)

        rect = self.plot_rectangle(2, 3, rect)
        self.wait(4)

        prime_24 = Text('24 is not prime', color=WHITE, font_size=23)
        primes = VGroup(primes, prime_24)
        primes.arrange(UP)
        primes.to_corner(DR)
        self.add(prime_24)

        rect = self.plot_rectangle(2, 12, rect)
        self.wait(4)
        rect = self.plot_rectangle(3, 8, rect)
        self.wait(2)
        rect = self.plot_rectangle(4, 6, rect)
        self.wait(2)

        prime_11 = Text('11 is prime', color=YELLOW, font_size=23)
        primes = VGroup(primes, prime_11)
        primes.arrange(UP)
        primes.to_corner(DR)
        self.add(prime_11)

        rect = self.plot_rectangle(1, 11, rect)
        self.wait(4)

        prime_7 = Text('7 is prime', color=YELLOW, font_size=23)
        primes = VGroup(primes, prime_7)
        primes.arrange(UP)
        primes.to_corner(DR)
        self.add(prime_7)

        rect = self.plot_rectangle(1, 7, rect)
        self.wait(2)

        prime_3 = Text('3 is prime', color=YELLOW, font_size=23)
        primes = VGroup(primes, prime_3)
        primes.arrange(UP)
        primes.to_corner(DR)
        self.add(prime_3)

        rect = self.plot_rectangle(1, 3, rect)
        self.wait(2)

        prime_2 = Text('2 is prime', color=YELLOW, font_size=23)
        primes = VGroup(primes, prime_2)
        primes.arrange(UP)
        primes.to_corner(DR)
        self.add(prime_2)

        rect = self.plot_rectangle(1, 2, rect)
        self.wait(4)

        prime_1 = Text('1 is not prime', color=RED, font_size=23)
        primes = VGroup(primes, prime_1)
        primes.arrange(UP)
        primes.to_corner(DR)
        self.add(prime_1)

        rect = self.plot_rectangle(1, 1, rect)
        self.wait(8)

        self.play(
            FadeOut(primes),
            FadeOut(text_background),
        )
        self.remove(primes, text_background)
        self.wait(4)

        # Checking if the number is prime
        rect = self.plot_rectangle(3, 4, rect)
        self.wait(15)
        rect = self.plot_rectangle(1, 25, rect)
        text_background = Rectangle(color=BLACK, height=5.5, width=2, fill_opacity=1)
        text_background.to_corner(DR, buff=0)
        self.add(text_background)

        checks = None
        for num in ['2', '3', '4', '5']:
            check_25 = Text(num, color=WHITE if num != '5' else YELLOW, font_size=23)
            checks = checks or check_25
            checks = VGroup(checks, check_25)
            checks.arrange(UP)
            checks.to_corner(DR)
            self.add(checks)
            self.wait(0.5)

        rect = self.plot_rectangle(5, 5, rect)
        self.wait(5)
        self.play(
            FadeOut(checks),
        )
        self.remove(checks)

        checks = None
        rect = self.plot_rectangle(1, 11, rect)
        for num in ['2', '3', '4', '5', '6', '7', '8', '9', '10']:
            check_11 = Text(num, color=WHITE, font_size=23)
            checks = checks or check_11
            checks = VGroup(checks, check_11)
            checks.arrange(UP)
            checks.to_corner(DR)
            self.add(checks)
            self.wait(0.5)

        self.wait(3)
        self.play(
            FadeOut(checks),
        )
        self.remove(checks)
        is_prime = Text('Prime!', color=GREEN, font_size=23)
        is_prime.to_corner(DR)
        self.add(is_prime)
        self.wait(3)
        self.play(
            FadeOut(is_prime),
        )
        self.remove(is_prime)

        checks = None
        rect = self.plot_rectangle(1, 13, rect)
        for num in ['2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']:
            check_13 = Text(num, color=WHITE, font_size=23)
            checks = checks or check_13
            checks = VGroup(checks, check_13)
            checks.arrange(UP)
            checks.to_corner(DR)
            self.add(checks)
            self.wait(0.5)

        self.wait(3)
        self.play(
            FadeOut(checks),
        )
        self.remove(checks)
        is_prime = Text('Prime!', color=GREEN, font_size=23)
        is_prime.to_corner(DR)
        self.add(is_prime)
        self.wait(5)
        self.play(
            FadeOut(is_prime),
        )
        self.remove(is_prime)

        self.play(
            FadeOut(text_background),
        )
        rect = self.plot_rectangle(2, 6, rect)

        text_background = Rectangle(color=BLACK, height=3.5, width=2, fill_opacity=1)
        text_background.to_corner(DR, buff=0)
        self.add(text_background)
        self.wait(15)

        rect = self.plot_rectangle(1, 25, rect)
        self.wait(5)

        checks = None
        for num in ['2', '3', '4', '5']:
            check_25 = Text(num, color=WHITE if num != '5' else YELLOW, font_size=23)
            checks = checks or check_25
            checks = VGroup(checks, check_25)
            checks.arrange(UP)
            checks.to_corner(DR)
            self.add(checks)
            self.wait(0.3)

        rect = self.plot_rectangle(5, 5, rect)
        self.wait(3)
        self.play(
            FadeOut(checks),
        )
        self.remove(checks)

        checks = None
        rect = self.plot_rectangle(1, 11, rect)
        self.wait(5)
        for num in ['2', '3', '4', '5']:
            check_11 = Text(num, color=WHITE, font_size=23)
            checks = checks or check_11
            checks = VGroup(checks, check_11)
            checks.arrange(UP)
            checks.to_corner(DR)
            self.add(checks)
            self.wait(0.3)

        self.wait(3)
        self.play(
            FadeOut(checks),
        )
        self.remove(checks)
        is_prime = Text('Prime!', color=GREEN, font_size=23)
        is_prime.to_corner(DR)
        self.add(is_prime)
        self.wait(3)
        self.play(
            FadeOut(is_prime),
        )
        self.remove(is_prime)

        checks = None
        rect = self.plot_rectangle(1, 13, rect)
        self.wait(5)
        for num in ['2', '3', '4', '5', '6']:
            check_13 = Text(num, color=WHITE, font_size=23)
            checks = checks or check_13
            checks = VGroup(checks, check_13)
            checks.arrange(UP)
            checks.to_corner(DR)
            self.add(checks)
            self.wait(0.3)

        self.wait(3)
        self.play(
            FadeOut(checks),
        )
        self.remove(checks)
        is_prime = Text('Prime!', color=GREEN, font_size=23)
        is_prime.to_corner(DR)
        self.add(is_prime)
        self.wait(2)
        self.play(
            FadeOut(is_prime),
        )
        self.remove(is_prime)

        self.play(
            FadeOut(text_background),
        )
        self.remove(text_background)

        self.wait(4)

        # Arriving to the idea that we only need sqrt(n) operations
        rect = self.plot_rectangle(2, 12, rect)
        self.wait(3)
        rect = self.plot_rectangle(3, 8, rect)
        self.wait(3)
        rect = self.plot_rectangle(4, 6, rect)
        self.wait(6)

        rect = self.plot_rectangle(2, 3, rect)
        self.wait(1)
        rect = self.plot_rectangle(3, 2, rect)
        self.wait(1)

        # We always keep the first number <= second
        # The slowest samples are those that approach the sqrt(n)
        rect = self.plot_rectangle(2, 15, rect)
        self.wait(2)
        rect = self.plot_rectangle(3, 10, rect)
        self.wait(2)
        rect = self.plot_rectangle(5, 6, rect)
        self.wait(4)

        rect = self.plot_rectangle(4, 4, rect)
        self.wait(4)
        rect = self.plot_rectangle(3, 3, rect)
        self.wait(4)
        rect = self.plot_rectangle(5, 5, rect)
        self.wait(4)

        sq1 = MathTex("n = \sqrt{n} \cdot \sqrt{n}").scale(1.2)
        sq1.move_to(3 * RIGHT)
        self.add(sq1)
        self.wait(8)

        self.clear()
        self.wait(1)
        ex = MathTex("49").scale(1.5)
        self.add(ex)
        self.wait(2)
        ex_ans = MathTex("49 = 7 \cdot 7").scale(1.5)
        self.play(ReplacementTransform(ex, ex_ans))
        self.wait(4)

        self.clear()
        self.wait(1)
        ex = MathTex("101").scale(1.5)
        self.add(ex)
        self.wait(5)
        ex_ans = MathTex("101 = ...").scale(1.5)
        self.play(ReplacementTransform(ex, ex_ans))
        self.wait(4)

        self.clear()
        self.wait(1)

        sq1 = MathTex("\sqrt{n}").scale(1.5)
        self.add(sq1)
        self.wait(8)
        self.clear()
        self.wait(1)
