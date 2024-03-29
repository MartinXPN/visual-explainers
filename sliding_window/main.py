from textwrap import dedent

from manim import *

from sliding_window.array import Array

a = [8, 3, -2, 4, 5, -1, 0, 5, 3, 9, -6]
k = 5


class OpeningScene(Scene):
    def construct(self):
        title = Title('Maximum Sum Subarray of Size K', include_underline=False)
        k_name = Text('K = 5').scale(0.8).center().move_to(title, DOWN).shift(0.7 * DOWN)

        array = Array(a, width=0.8, height=0.8, spacing=0.05, scale_text=0.8)
        array_mobj = array.get_mobject().center()
        array_name = Text('a:').scale(0.8).move_to(array_mobj, LEFT).shift(0.7 * LEFT)
        self.play(Create(array_mobj), Write(array_name), run_time=2)
        self.wait()
        self.play(Write(title), Write(k_name))
        self.wait()

        # Take the range [0, 4] as an example
        brace = Brace(array_mobj, DOWN, stroke_width=2, color=RED).scale(k / len(a)).align_to(array_mobj, LEFT)
        sum_text = Tex(sum(a[0: k]), color=RED).scale(0.8).next_to(brace, DOWN, buff=0.2)
        array.highlight(0, k - 1, color=RED)
        self.play(
            array_mobj.animate.become(array.get_mobject(), match_center=True),
            GrowFromCenter(brace),
            Write(sum_text),
            run_time=0.5,
        )
        self.wait(0.5)

        def highlight(start, additional_mobj=None, shift=0):
            array.unhighlight()
            array.highlight(start, start + k - 1, color=RED)
            end = start + k - 1
            if additional_mobj is None:
                # Create a dummy variable
                additional_mobj = VGroup()

            self.play(
                array_mobj.animate.become(array.get_mobject(), match_center=True),
                brace.animate.become(
                    Brace(array_mobj, DOWN, stroke_width=len(array) / max(end - start + 1, 2), color=RED)
                    .scale((end - start + 1) / len(array))
                    .align_to(array_mobj, LEFT)
                    .shift((array.width + array.spacing) * RIGHT * start)
                ),
                sum_text.animate.become(
                    Tex(sum(a[start: end + 1]), color=RED).scale(0.8).next_to(brace, DOWN, buff=0.2)
                    .align_to(array_mobj, LEFT)
                    .shift((array.width + array.spacing) * RIGHT * (start + (end - start + 0.75) / 2))
                ),
                additional_mobj.animate.shift(shift),
                run_time=0.3,
            )
            self.wait(0.5)

        highlight(start=2)      # Take the range [2, 6] as an example
        highlight(start=5)      # Take the range [5, 9] as an example
        highlight(start=4)      # Take the range [4, 8] as an example
        self.wait(6)

        # Add an arrow at location 4 and iterate up to the end
        highlight(start=0)
        arrow = Arrow(
            start=UP, end=DOWN, color=RED, buff=0.1,
            stroke_width=10, max_stroke_width_to_length_ratio=15,
            max_tip_length_to_length_ratio=0.5, tip_length=0.2,
        ).scale(0.3).next_to(array_mobj, UP).shift((array.width + array.spacing) * 1 * LEFT)
        self.play(Create(arrow))
        for end in range(5, len(array)):
            highlight(start=end - k + 1, additional_mobj=arrow, shift=(array.width + array.spacing) * RIGHT)
            self.wait(0.2)
        self.wait(3)

        # Move to start
        highlight(start=0, additional_mobj=arrow, shift=(array.width + array.spacing) * 6 * LEFT)
        self.wait(0.1)

        # Iterate from 4 to the end and display the sum of each subarray
        sums = [Text(' - ').next_to(array_mobj, DOWN).align_to(array_mobj, LEFT).shift(0.8 * DOWN)]
        for end in range(k, len(array)):
            # Write the formula
            formula = MathTex(
                f'{{{{ \\mathrm{{sum}}[{end - k}: {end - 1}] }}}} = '
                f'{{{{ a[{end - k}] }}}} + {{{{ a[{end - k + 1}] }}}} + {{{{ a[{end - k + 2}] }}}} + '
                f'{{{{ a[{end - k + 3}] }}}} + {{{{ a[{end - k + 4}] }}}} = {{{{ {sum(a[end - k: end])} }}}}',
                color=YELLOW,
            ).scale(0.7).next_to(sums[-1], DOWN, buff=0.2).align_to(sums[-1], LEFT)
            [formula[i].set_color(BLACK) for i in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]]
            if len(sums) <= 4:
                self.play(Write(formula), run_time=0.1)
                sums.append(formula)
            else:
                formula = None

            for i in range(end - k, end):
                array.highlight(i, i, color=YELLOW, width=8.)
                if i - 1 >= end - k:
                    array.highlight(i - 1, i - 1, color=RED)
                array_mobj.become(array.get_mobject(), match_center=True)
                if formula is not None:
                    self.play(formula[2 + 2 * (i - end + k)].animate.set_color(YELLOW), run_time=0.1)
                    self.play(formula[3 + 2 * (i - end + k)].animate.set_color(YELLOW), run_time=0.1)
                self.wait(0.2)
            array.highlight(end - 1, end - 1, color=RED)
            array_mobj.become(array.get_mobject(), match_center=True)
            if formula is not None:
                self.play(formula[11].animate.set_color(YELLOW), run_time=0.1)
                self.play(formula[12].animate.set_color(YELLOW), run_time=0.1)
            highlight(start=end - k + 1, additional_mobj=arrow, shift=(array.width + array.spacing) * RIGHT)

        self.play(Circumscribe(VGroup(*sums[1:]), run_time=1.5))
        self.play(FadeOut(VGroup(*sums)), run_time=0.2)
        complexity = Tex('Time Complexity: $\\mathcal{O}(n \\cdot k)$', color=RED).next_to(array_mobj, DOWN, buff=2)
        self.play(Write(complexity))
        self.wait(5)

        # Move to next scene
        array.unhighlight()
        self.play(
            FadeOut(complexity, arrow, brace, sum_text),
            array_mobj.animate.become(array.get_mobject(), match_center=True),
        )
        self.wait(3)


REMOVED_COLOR = '#ffeeee'


class SlidingWindowDiscovery(Scene):
    def construct(self):
        title = Title('Maximum Sum Subarray of Size K', include_underline=False)
        self.add(title)

        array = Array(a, width=0.8, height=0.8, spacing=0.05, scale_text=0.8)
        array_mobj = array.get_mobject().center()
        array_name = Text('a:').scale(0.8).move_to(array_mobj, LEFT).shift(0.7 * LEFT)
        k_name = Text('K = 5').scale(0.8).center().move_to(title, DOWN).shift(0.7 * DOWN)
        self.add(array_mobj, array_name, k_name)
        self.wait(0.1)

        arrow = Arrow(
            start=UP, end=DOWN, color=RED, buff=0.1,
            stroke_width=10, max_stroke_width_to_length_ratio=15,
            max_tip_length_to_length_ratio=0.5, tip_length=0.2,
        ).scale(0.3).next_to(array_mobj, UP).shift((array.width + array.spacing) * 1 * LEFT)
        self.play(Create(arrow))
        self.wait()

        brace = Brace(array_mobj, DOWN, stroke_width=2, color=RED).scale(k / len(a)).align_to(array_mobj, LEFT)
        sum_text = Tex(sum(a[: k]), color=RED).scale(0.8).next_to(brace, DOWN, buff=0.2)
        self.play(GrowFromCenter(brace), Write(sum_text))
        self.wait(3)

        def highlight(start, additional_mobj=None, shift=0, run_time=0.3, wait=0.5):
            array.unhighlight()
            array.highlight(start, start + k - 1, color=RED)
            end = start + k - 1
            if additional_mobj is None:
                # Create a dummy variable
                additional_mobj = VGroup()

            self.play(
                array_mobj.animate.become(array.get_mobject(), match_center=True),
                brace.animate.become(
                    Brace(array_mobj, DOWN, stroke_width=len(array) / max(end - start + 1, 2), color=RED)
                    .scale((end - start + 1) / len(array))
                    .align_to(array_mobj, LEFT)
                    .shift((array.width + array.spacing) * RIGHT * start)
                ),
                sum_text.animate.become(
                    Tex(sum(a[start: end + 1]), color=RED).scale(0.8).next_to(brace, DOWN, buff=0.2)
                    .align_to(array_mobj, LEFT)
                    .shift((array.width + array.spacing) * RIGHT * (start + (end - start + 0.75) / 2))
                ),
                additional_mobj.animate.shift(shift),
                run_time=run_time,
            )
            self.wait(wait)

        for end in range(k, k + 3):
            for i in range(end - k, end):
                array.highlight(i, i, color=YELLOW, width=8.)
                if i - 1 >= end - k:
                    array.highlight(i - 1, i - 1, color=RED)
                self.play(array_mobj.animate.become(array.get_mobject(), match_center=True), run_time=0.3)
            array.highlight(end - 1, end - 1, color=RED)
            self.play(array_mobj.animate.become(array.get_mobject(), match_center=True), run_time=0.3)
            self.wait(1.5)
            highlight(start=end - k + 1, additional_mobj=arrow, shift=(array.width + array.spacing) * RIGHT)

        self.wait(0.5)
        # Flicker the next element and the one leaving the window
        for i in range(5):
            array.highlight(k + 2, k + 2, color=RED, width=8.)
            array.highlight(2, 2, color=REMOVED_COLOR, width=2.)
            self.play(array_mobj.animate.become(array.get_mobject(), match_center=True), run_time=0.4)
            array.highlight(k + 2, k + 2, color=WHITE, width=2.)
            array.highlight(2, 2, color=RED, width=8.)
            self.play(array_mobj.animate.become(array.get_mobject(), match_center=True), run_time=0.4)

        highlight(start=3)
        self.wait(4)
        array.highlight(2, 2, color=YELLOW, width=8.)
        self.play(array_mobj.animate.become(array.get_mobject(), match_center=True), run_time=0.3)
        self.wait(2)
        array.highlight(k + 2, k + 2, color=GREEN, width=8.)
        self.play(array_mobj.animate.become(array.get_mobject(), match_center=True), run_time=0.3)
        self.wait(4)

        # Move back to start
        highlight(start=0, additional_mobj=arrow, shift=(array.width + array.spacing) * LEFT * 3)
        self.wait(2)

        # Write initial window formula
        formula = MathTex('\\mathrm{sum}_0 = a_0 + a_1 + ... + a_{k-1}', color=YELLOW).scale(0.8)
        formula.next_to(array_mobj, DOWN, buff=1.5)
        self.play(Write(formula))
        self.wait()

        # Move the window once
        highlight(start=1, additional_mobj=arrow, shift=(array.width + array.spacing) * RIGHT)
        self.wait(1)

        # Formula for any window
        window = MathTex('\\mathrm{sum}_i = \\mathrm{sum}_{i-1} + a_{r} - a_{r - k}', color=YELLOW).scale(0.8)
        window.next_to(formula, DOWN, buff=0.5).align_to(formula, LEFT)
        self.play(Write(window))
        self.wait(6)
        self.play(Circumscribe(window), run_time=2)
        self.wait(6)

        self.play(FadeOut(formula, window))
        self.wait(6)

        # Code for the sliding window
        code = Code(
            code=dedent('''
                cur = best = sum(a[:k])
                for r in range(k, len(a)):
                    cur = cur + a[r] - a[r - k]
                    best = max(best, cur)
            ''').strip(),
            tab_width=4,
            language='Python',
            line_spacing=0.6,
            font='Monospace',
            style='monokai',
        ).next_to(array_mobj, DOWN, buff=1).code
        for line in code.chars:
            self.play(AddTextLetterByLetter(line))
            self.wait(3)

        # Move to start
        self.wait(2)
        highlight(start=0, additional_mobj=arrow, shift=(array.width + array.spacing) * LEFT)
        self.wait(4)

        # Simulate the algorithm and keep the sum at each location (match the sum center)
        cur = sum_text.copy()
        self.add(cur)
        sums = [cur]
        for end in range(k, len(array)):
            highlight(start=end - k + 1, additional_mobj=arrow, shift=(array.width + array.spacing) * RIGHT,
                      run_time=0.1 if end > k + 1 else 0.3, wait=0.1 if end > k + 1 else 0.5)
            cur = sum_text.copy()
            self.add(cur)
            sums.append(cur)
            if end <= k + 1:
                self.wait(1)

        self.play(FadeOut(arrow, brace, sum_text))
        self.play(Circumscribe(VGroup(*sums)), run_time=3)

        # Indicate the first element in the sum (the final answer)
        self.play(Indicate(sums[0]), run_time=4)
        self.wait(2)


class DynamicSizeSlidingWindow(Scene):
    a = [4, 5, 2, 0, 1, 8, 12, 3, 6, 9]

    def construct(self):
        title = Title('Longest Subarray With Sum $ < S$', include_underline=False)
        s_name = MathTex('S = 15').scale(0.8).center().next_to(title, RIGHT).shift(0.5 * RIGHT)
        self.add(title, s_name)
        self.wait(1)

        array = Array(self.a, width=0.8, height=0.8, spacing=0.05, scale_text=0.8)
        array_mobj = array.get_mobject().center()
        array_name = Text('a:').scale(0.8).move_to(array_mobj, LEFT).shift(0.7 * LEFT)
        self.play(Create(array_mobj))
        self.play(Write(array_name))
        self.wait(4)

        # Initial brace with [1: 6]
        brace = Brace(array_mobj, DOWN, stroke_width=2, color=ORANGE)\
            .scale(6 / len(array))\
            .align_to(array_mobj, LEFT)\
            .shift((array.width + array.spacing) * RIGHT)
        sum_text = Tex(sum(self.a[1: 7]), color=ORANGE).scale(0.8).next_to(brace, DOWN, buff=0.2)
        self.play(GrowFromCenter(brace), Write(sum_text))
        self.wait(0.5)

        def highlight(start, end):
            self.play(
                brace.animate.become(
                    Brace(array_mobj, DOWN, stroke_width=len(array) / max(end - start + 1, 2), color=ORANGE)
                    .scale((end - start + 1) / len(array))
                    .align_to(array_mobj, LEFT)
                    .shift((array.width + array.spacing) * RIGHT * start)
                ),
                sum_text.animate.become(
                    Tex(sum(self.a[start: end + 1]), color=ORANGE).scale(0.8).next_to(brace, DOWN, buff=0.2)
                    .align_to(array_mobj, LEFT)
                    .shift((array.width + array.spacing) * RIGHT * (start + (end - start + 0.75) / 2))
                ),
                run_time=0.3,
            )
            self.wait(0.5)

        highlight(start=3, end=5)
        highlight(start=0, end=4)
        highlight(start=7, end=8)
        self.wait(1)

        # Unhighlight
        self.play(
            brace.animate.set_color(BLACK),
            sum_text.animate.set_color(BLACK),
        )
        brace.shift((array.width + array.spacing) * LEFT * 7)
        sum_text.shift((array.width + array.spacing) * LEFT * 7)
        self.wait(1)

        highlight(start=0, end=0)
        s = Arrow(
            start=UP, end=DOWN, color=RED, buff=0.1,
            stroke_width=10, max_stroke_width_to_length_ratio=15,
            max_tip_length_to_length_ratio=0.5, tip_length=0.2,
        ).scale(0.3).next_to(array_mobj, UP).shift((array.width + array.spacing) * 5.5 * LEFT)
        e = Arrow(
            start=UP, end=DOWN, color=YELLOW, buff=0.1,
            stroke_width=10, max_stroke_width_to_length_ratio=15,
            max_tip_length_to_length_ratio=0.5, tip_length=0.2,
        ).scale(0.3).next_to(array_mobj, UP).shift((array.width + array.spacing) * 4.5 * LEFT)
        self.play(Create(s), Create(e))
        self.wait(2)

        start_index, end_index = -1, 0
        s_index = always_redraw(lambda: MathTex(str(start_index), color=RED).scale(0.6).next_to(s, UP, buff=0.1))
        e_index = always_redraw(lambda: MathTex(str(end_index), color=YELLOW).scale(0.6).next_to(e, UP, buff=0.1))
        self.play(Write(s_index))
        self.play(Write(e_index))
        self.wait(6)

        # Animate the algorithm
        cur = 0
        for end_index in range(0, len(self.a)):
            cur += self.a[end_index]
            if end_index > 0:
                self.play(e.animate.shift((array.width + array.spacing) * RIGHT), run_time=0.05)
            highlight(start=start_index + 1, end=end_index)
            while cur >= 15:
                start_index += 1
                cur -= self.a[start_index]
                self.play(s.animate.shift((array.width + array.spacing) * RIGHT), run_time=0.05)
                highlight(start=start_index + 1, end=end_index)
            self.wait(0.1)

        # Bring to 0
        self.play(
            VGroup(array_mobj, array_name, s, e, brace, sum_text, s_index, e_index).animate.shift(1.5 * UP),
            run_time=0.2,
        )
        self.play(
            s.animate.shift((array.width + array.spacing) * 9 * LEFT),
            e.animate.shift((array.width + array.spacing) * 9 * LEFT),
            run_time=0.3,
        )
        start_index, end_index = -1, 0
        highlight(start=0, end=0)
        self.wait(1)

        # Code for the sliding window
        code = Code(
            code=dedent('''
                l, cur, best = -1, 0, 0
                for r in range(len(a)):
                    cur += a[r]
                    while cur >= s:
                        l += 1
                        cur -= a[l]
                    best = max(best, r - l)
            ''').strip(),
            tab_width=4,
            language='Python',
            line_spacing=0.6,
            font='Monospace',
            style='monokai',
        ).next_to(array_mobj, DOWN, buff=1).code
        self.play(AddTextLetterByLetter(code.chars[0]))
        self.wait(5)
        self.play(AddTextLetterByLetter(code.chars[1]))
        self.wait(2.5)
        self.play(AddTextLetterByLetter(code.chars[2]))
        self.wait(0.5)
        self.play(AddTextLetterByLetter(code.chars[3]))
        self.play(AddTextLetterByLetter(code.chars[4]))
        self.play(AddTextLetterByLetter(code.chars[5]))
        self.wait(2)
        self.play(AddTextLetterByLetter(code.chars[6]))
        self.wait(1)
        self.play(
            VGroup(code.chars).animate.shift(2 * LEFT),
            VGroup(array_mobj, array_name, s, e, brace, sum_text, s_index, e_index).animate.shift(1.5 * LEFT),
        )

        # Table for the algorithm
        table = [
            ['ID', 'Sum', 'Len'],
            *[[f'{i}', '  ', ' '] for i in range(len(self.a))],
        ]
        table_mobj = Table(table).next_to(code, RIGHT).scale(0.45).shift(UP)
        self.play(Create(table_mobj))

        # Animate the algorithm
        cur = 0
        for end_index in range(0, len(self.a)):
            cur += self.a[end_index]
            if end_index > 0:
                self.play(e.animate.shift((array.width + array.spacing) * RIGHT), run_time=0.05)
            highlight(start=start_index + 1, end=end_index)
            while cur >= 15:
                self.wait(1)
                start_index += 1
                cur -= self.a[start_index]
                self.play(s.animate.shift((array.width + array.spacing) * RIGHT), run_time=0.05)
                highlight(start=start_index + 1, end=end_index)
                self.wait(1.5)

            table[end_index + 1] = [f'{end_index}', f'{cur}', f'{end_index - start_index}']
            table_mobj.become(Table(table), match_center=True, match_height=True, match_width=True)
            self.wait(0.5)

        self.wait(5)
        self.play(FadeOut(e, s, e_index, s_index, brace, sum_text))
        table_mobj.add(table_mobj.get_cell((6, 0), color=GREEN)),
        table_mobj.add(table_mobj.get_cell((6, 1), color=GREEN)),
        table_mobj.add(table_mobj.get_cell((6, 2), color=GREEN)),
        self.wait(10)
