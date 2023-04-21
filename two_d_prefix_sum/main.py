from textwrap import dedent

from manim import *

from two_d_prefix_sum.matrix import Matrix

a = [
    [1, 2, -1, -3, 4, 2, 0, 1],
    [3, -2, 4, 5, -3, -1, 1, 0],
    [0, 1, -3, 1, 3, 2, 4, -2],
    [-1, 3, 4, 7, -2, 0, 1, 3],
    [3, 4, 2, 4, -7, -1, 3, 0],
    [-5, 4, 1, -2, 3, -4, 3, 3],
]

p = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 3, 2, -1, 3, 5, 5, 6],
    [0, 4, 4, 7, 9, 10, 11, 12, 13],
    [0, 4, 5, 5, 8, 12, 15, 20, 19],
    [0, 3, 7, 11, 21, 23, 26, 32, 34],
    [0, 6, 14, 20, 34, 29, 31, 40, 42],
    [0, 1, 13, 20, 32, 30, 28, 40, 45],
]


class OpeningScene(Scene):
    def construct(self):
        title = Title("What's the Sum of a Submatrix?", include_underline=False).shift(0.5 * DOWN)
        self.add(title)

        m = Matrix(a)
        m_mobj = m.get_mobject().center()
        self.play(FadeIn(m_mobj))
        self.wait(4)

        # Highlight (1, 1) -> (5, 3)
        m.highlight(1, 1, 5, 3, color=RED, width=5)
        m_mobj.become(m.get_mobject().center())
        self.wait(0.8)

        # Highlight (3, 4) -> (5, 5)
        m.unhighlight()
        m.highlight(3, 4, 5, 5, color=YELLOW, width=5)
        m_mobj.become(m.get_mobject().center())
        self.wait(0.8)

        # Highlight (2, 2) -> (4, 6)
        m.unhighlight()
        m.highlight(2, 2, 4, 6, color=GREEN, width=5)
        m_mobj.become(m.get_mobject().center())
        self.wait(3)

        # Iterate over rows and columns and highlight each element
        for r in range(2, 5):
            for c in range(2, 7):
                m.highlight(r, c, r, c, color=GREEN, width=10)
                m_mobj.become(m.get_mobject().center())
                self.wait(0.3)
                m.highlight(r, c, r, c, color=GREEN, width=5)
                m_mobj.become(m.get_mobject().center())
        self.wait(6)

        # Move m to the left and add an empty p matrix on the right
        pref = Matrix([[None] * len(a[0]) for _ in range(len(a))])
        p_mobj = pref.get_mobject().center().shift(3 * RIGHT)
        self.play(
            m_mobj.animate.shift(3 * LEFT),
            FadeIn(p_mobj),
        )
        self.wait()

        # Fill the prefix sum matrix
        for i in range(len(a)):
            for j in range(len(a[0])):
                pref.values[i][j] = p[i + 1][j + 1]
                p_mobj.become(pref.get_mobject().center().shift(3 * RIGHT))
                self.wait(0.1)
        self.wait()

        # Highlight (0, 0) -> (3, 4) in a => (3, 4) in p
        m.highlight(0, 0, 3, 4, color=RED, width=5)
        m_mobj.become(m.get_mobject().center().shift(3 * LEFT))
        pref.highlight(3, 4, 3, 4, color=RED, width=5)
        p_mobj.become(pref.get_mobject().center().shift(3 * RIGHT))
        self.wait(7)

        # Transition to the next scene
        # Highlight only (2, 2) -> (4, 6) and nothing in p
        m.unhighlight()
        m.highlight(2, 2, 4, 6, color=GREEN, width=5)
        m_mobj.become(m.get_mobject().center().shift(3 * LEFT))
        pref.unhighlight()
        p_mobj.become(pref.get_mobject().center().shift(3 * RIGHT))
        self.wait(5)


class PrefixSumFormula(Scene):
    def construct(self):
        title = Title("What's the Sum of a Submatrix?", include_underline=False).shift(0.5 * DOWN)
        self.add(title)

        m = Matrix(a)
        m.highlight(2, 2, 4, 6, color=GREEN, width=5)
        m_mobj = m.get_mobject().center().shift(3 * LEFT)
        self.add(m_mobj)

        # Move m to the left and add an empty p matrix on the right
        pref_values = [[p[i + 1][j + 1] for j in range(len(a[0]))] for i in range(len(a))]
        pref = Matrix(pref_values)
        p_mobj = pref.get_mobject().center().shift(3 * RIGHT)
        self.add(p_mobj)
        self.wait(6)

        # Add text for the formula
        example_equation = MathTex(
            '{{ \\mathrm{sum}(2,2,4,6) }} = {{ p[4][6] }} - {{ p[1][6] }} - {{ p[4][1] }} + {{ p[1][1] }}'
        ).scale(0.7).center().move_to(2.5 * DOWN).shift(2 * LEFT)
        [example_equation[i].set_color(BLACK) for i in [2, 3, 4, 5, 6, 7, 8]]

        matrix_name = Text('m').scale(0.6).move_to(m_mobj, LEFT).shift(0.5 * LEFT)
        p_name = Text('p').scale(0.6).move_to(p_mobj, LEFT).shift(0.5 * LEFT)

        self.play(FadeIn(matrix_name), FadeIn(p_name), Write(example_equation))
        self.wait(17)

        # Highlight (0, 0) -> (4, 6) in a => (4, 6) in p
        m.highlight(0, 0, 4, 6, color=ORANGE, width=5)
        m_mobj.become(m.get_mobject().center().shift(3 * LEFT))
        pref.highlight(4, 6, 4, 6, color=ORANGE, width=5)
        p_mobj.become(pref.get_mobject().center().shift(3 * RIGHT))
        self.play(example_equation[2].animate.set_color(ORANGE))
        self.wait(10)

        # Highlight (0, 0) -> (4, 1) in a => (4, 1) in p
        m.highlight(0, 0, 4, 1, color=YELLOW, width=5)
        m_mobj.become(m.get_mobject().center().shift(3 * LEFT))
        pref.highlight(4, 1, 4, 1, color=YELLOW, width=5)
        p_mobj.become(pref.get_mobject().center().shift(3 * RIGHT))
        self.play(example_equation[3].animate.set_color(YELLOW), run_time=0.2)
        self.play(example_equation[4].animate.set_color(YELLOW))

        # Highlight (0, 0) -> (1, 6) in a => (1, 6) in p
        m.highlight(0, 0, 1, 6, color=YELLOW, width=5)
        m_mobj.become(m.get_mobject().center().shift(3 * LEFT))
        pref.highlight(1, 6, 1, 6, color=YELLOW, width=5)
        p_mobj.become(pref.get_mobject().center().shift(3 * RIGHT))
        self.play(example_equation[5].animate.set_color(YELLOW), run_time=0.2)
        self.play(example_equation[6].animate.set_color(YELLOW))
        self.wait(6)

        # Flicker (0, 0) -> (1, 1) in a => (1, 1) in p
        for i in range(5):
            m.highlight(0, 0, 1, 1, color=YELLOW, width=5)
            m_mobj.become(m.get_mobject().center().shift(3 * LEFT))
            pref.highlight(1, 1, 1, 1, color=YELLOW, width=5)
            p_mobj.become(pref.get_mobject().center().shift(3 * RIGHT))
            self.wait(0.5)

            m.highlight(0, 0, 1, 1, color=RED, width=5)
            m_mobj.become(m.get_mobject().center().shift(3 * LEFT))
            pref.highlight(1, 1, 1, 1, color=RED, width=5)
            p_mobj.become(pref.get_mobject().center().shift(3 * RIGHT))
            self.wait(0.5)

        self.wait(1)
        self.play(example_equation[7].animate.set_color(RED), run_time=0.2)
        self.play(example_equation[8].animate.set_color(RED))
        self.wait(4)

        formula = MathTex(
            '{{ \\mathrm{sum}(ur, lc, br, rc) }} = '
            '{{p[br][rc]}} - {{p[ur - 1][rc]}} - {{p[br][lc - 1]}} + {{p[ur - 1][lc - 1]}}'
        ).scale(0.7).align_to(example_equation, LEFT).shift(3 * DOWN)
        [formula[i].set_color(BLACK) for i in [2, 3, 4, 5, 6, 7, 8]]
        self.play(Write(formula))
        self.wait(2)
        self.play(formula[2].animate.set_color(ORANGE))
        self.wait(2)
        self.play(formula[3].animate.set_color(YELLOW), run_time=0.2)
        self.play(formula[4].animate.set_color(YELLOW))
        self.play(formula[5].animate.set_color(YELLOW), run_time=0.2)
        self.play(formula[6].animate.set_color(YELLOW))
        self.wait()
        self.play(formula[7].animate.set_color(RED), run_time=0.2)
        self.play(formula[8].animate.set_color(RED))
        self.wait(4)

        # Highlight possibly negative values (lc-1) and (ur-1)
        self.play(Indicate(formula[6][6:10]), Indicate(formula[8][8:12]), color=WHITE)
        self.play(Indicate(formula[4][2:6]), Indicate(formula[8][2:6]), color=WHITE)
        self.wait(2)

        # Add padding to p
        new_pref = Matrix(p)
        new_pref.highlight(5, 7, 5, 7, color=ORANGE, width=5)
        new_pref.highlight(5, 2, 5, 2, color=YELLOW, width=5)
        new_pref.highlight(2, 7, 2, 7, color=YELLOW, width=5)
        new_pref.highlight(2, 2, 2, 2, color=RED, width=5)
        new_p_mobj = new_pref.get_mobject().align_to(p_mobj, LEFT).align_to(p_mobj, UP)
        self.play(
            p_mobj.animate.align_to(new_p_mobj, DOWN).align_to(new_p_mobj, RIGHT),
            example_equation.animate.shift(0.5 * DOWN),
            formula.animate.shift(0.5 * DOWN),
        )
        p_mobj.become(new_p_mobj),
        self.wait()

        def update_formula(new_example_text: str, new_formula_text: str):
            new_example = MathTex(new_example_text).scale(0.7).center().move_to(3 * DOWN).shift(2 * LEFT)
            new_formula = MathTex(new_formula_text).scale(0.7).align_to(example_equation, LEFT).shift(3.5 * DOWN)
            new_example[2].set_color(ORANGE)
            new_example[3].set_color(YELLOW)
            new_example[4].set_color(YELLOW)
            new_example[5].set_color(YELLOW)
            new_example[6].set_color(YELLOW)
            new_example[7].set_color(RED)
            new_example[8].set_color(RED)
            new_formula[2].set_color(ORANGE)
            new_formula[3].set_color(YELLOW)
            new_formula[4].set_color(YELLOW)
            new_formula[5].set_color(YELLOW)
            new_formula[6].set_color(YELLOW)
            new_formula[7].set_color(RED)
            new_formula[8].set_color(RED)
            self.play(
                example_equation.animate.become(new_example),
                formula.animate.become(new_formula),
                run_time=0.6,
            )


        update_formula(
            '{{ \\mathrm{sum}(2,2,4,6) }} = {{ p[5][7] }} - {{ p[1][6] }} - {{ p[4][1] }} + {{ p[1][1] }}',
            '{{ \\mathrm{sum}(ur, lc, br, rc) }} = {{p[br + 1][rc + 1]}} - {{p[ur - 1][rc]}} - {{p[br][lc - 1]}} + {{p[ur - 1][lc - 1]}}'
        )

        update_formula(
            '{{ \\mathrm{sum}(2,2,4,6) }} = {{ p[5][7] }} - {{ p[2][7] }} - {{ p[4][1] }} + {{ p[1][1] }}',
            '{{ \\mathrm{sum}(ur, lc, br, rc) }} = {{p[br + 1][rc + 1]}} - {{p[ur][rc + 1]}} - {{p[br][lc - 1]}} + {{p[ur - 1][lc - 1]}}'
        )

        update_formula(
            '{{ \\mathrm{sum}(2,2,4,6) }} = {{ p[5][7] }} - {{ p[2][7] }} - {{ p[5][2] }} + {{ p[1][1] }}',
            '{{ \\mathrm{sum}(ur, lc, br, rc) }} = {{p[br + 1][rc + 1]}} - {{p[ur][rc + 1]}} - {{p[br + 1][lc]}} + {{p[ur - 1][lc - 1]}}'
        )

        update_formula(
            '{{ \\mathrm{sum}(2,2,4,6) }} = {{ p[5][7] }} - {{ p[2][7] }} - {{ p[5][2] }} + {{ p[2][2] }}',
            '{{ \\mathrm{sum}(ur, lc, br, rc) }} = {{p[br + 1][rc + 1]}} - {{p[ur][rc + 1]}} - {{p[br + 1][lc]}} + {{p[ur][lc]}}'
        )
        self.wait(4)


class PrefixSumCalculation(Scene):
    def construct(self):
        title = Title('2D Prefix Sum', include_underline=False)
        self.add(title)

        m = Matrix(a)
        m_mobj = m.get_mobject().center().shift(3 * LEFT).shift(UP)
        self.add(m_mobj)

        # Move m to the left and add an empty p matrix on the right
        pref_values = [[0 if i == 0 or j == 0 else None
                        for j in range(len(a[0]))]
                       for i in range(len(a))]
        pref = Matrix(pref_values)
        p_mobj = pref.get_mobject().center().align_to(m_mobj, UP).shift(3 * RIGHT)
        self.add(p_mobj)

        matrix_name = Text('m').scale(0.6).move_to(m_mobj, LEFT).shift(0.5 * LEFT)
        p_name = Text('p').scale(0.6).move_to(p_mobj, LEFT).shift(0.5 * LEFT)
        self.add(matrix_name, p_name)
        self.wait(4)

        for i in range(1, len(pref_values)):
            for j in range(1, len(pref_values[0])):
                pref.unhighlight()
                pref.highlight(i, j, i, j, color=YELLOW, width=5)
                p_mobj.become(pref.get_mobject(), match_center=True)
                self.wait(0.4 if i * len(pref_values[0]) + j < 10 else 0.2)

        pref.unhighlight()
        p_mobj.become(pref.get_mobject(), match_center=True)
        self.wait(1)

        # Highlight upper row and leftmost column
        pref.highlight(0, 0, 0, len(pref_values[0]) - 1, color=YELLOW, width=5)
        pref.highlight(0, 0, len(pref_values) - 1, 0, color=YELLOW, width=5)
        p_mobj.become(pref.get_mobject(), match_center=True)
        self.wait(5)

        pref.unhighlight()
        p_mobj.become(pref.get_mobject(), match_center=True)
        self.wait(1)

        # Code for the prefix sum
        code = Code(
            code=dedent('''
                p = [[0] * (cols + 1) for _ in range(rows + 1)]
                for r in range(1, rows + 1):
                    for c in range(1, cols + 1):
                        p[r][c] = p[r - 1][c] + p[r][c - 1] \\
                                   - p[r - 1][c - 1] + m[r - 1][c - 1]
            ''').strip(),
            tab_width=4,
            language='Python',
            line_spacing=0.6,
            font='Monospace',
            style='monokai',
        ).scale(0.8).next_to(p_mobj, DOWN).align_to(matrix_name, LEFT).code
        for line in code.chars[:-2]:
            self.play(AddTextLetterByLetter(line), run_time=0.08 * len(line))
        self.wait(4)

        # Highlight (3, 4) in prefix sum
        pref.highlight(3, 4, 3, 4, color=ORANGE, width=5)
        p_mobj.become(pref.get_mobject(), match_center=True)
        self.wait(8)

        # Highlight (0, 0) -> (1, 3) in matrix => (2, 4) in prefix sum with YELLOW
        m.highlight(0, 0, 1, 3, color=YELLOW, width=5)
        pref.highlight(2, 4, 2, 4, color=YELLOW, width=5)
        m_mobj.become(m.get_mobject(), match_center=True)
        p_mobj.become(pref.get_mobject(), match_center=True)
        self.wait(2)

        # Highlight (0, 0) -> (2, 2) in matrix => (3, 3) in prefix sum with YELLOW
        m.highlight(0, 0, 2, 2, color=YELLOW, width=5)
        pref.highlight(3, 3, 3, 3, color=YELLOW, width=5)
        m_mobj.become(m.get_mobject(), match_center=True)
        p_mobj.become(pref.get_mobject(), match_center=True)
        self.wait(3)

        # Highlight (0, 0) -> (1, 2) in matrix => (2, 3) in prefix sum with RED
        m.highlight(0, 0, 1, 2, color=RED, width=5)
        pref.highlight(2, 3, 2, 3, color=RED, width=5)
        m_mobj.become(m.get_mobject(), match_center=True)
        p_mobj.become(pref.get_mobject(), match_center=True)
        self.wait(2)

        # Highlight (2, 3) in matrix with ORANGE
        m.highlight(2, 3, 2, 3, color=ORANGE, width=5)
        m_mobj.become(m.get_mobject(), match_center=True)

        for line in code.chars[-2:]:
            self.play(AddTextLetterByLetter(line), run_time=0.08 * len(line))
        self.wait(6)


class Examples(Scene):
    def construct(self):
        title = Title('2D Prefix Sum', include_underline=False)
        self.add(title)

        m = Matrix(a)
        m_mobj = m.get_mobject().center().shift(3 * LEFT).shift(UP)
        self.add(m_mobj)

        # Move m to the left and add an empty p matrix on the right
        pref = Matrix([[None] * len(p[0]) for _ in range(len(p))])
        p_mobj = pref.get_mobject().center().align_to(m_mobj, UP).shift(3 * RIGHT)
        self.add(p_mobj)

        matrix_name = Text('m').scale(0.6).move_to(m_mobj, LEFT).shift(0.5 * LEFT)
        p_name = Text('p').scale(0.6).move_to(p_mobj, LEFT).shift(0.3 * LEFT)
        self.add(matrix_name, p_name)

        code = Code(
            code=dedent('''
                p = [[0] * (cols + 1) for _ in range(rows + 1)]
                for r in range(1, rows + 1):
                    for c in range(1, cols + 1):
                        p[r][c] = p[r - 1][c] + p[r][c - 1] \\
                                   - p[r - 1][c - 1] + m[r - 1][c - 1]
            ''').strip(),
            tab_width=4,
            language='Python',
            line_spacing=0.6,
            font='Monospace',
            style='monokai',
        ).scale(0.8).next_to(p_mobj, DOWN).align_to(matrix_name, LEFT).code
        self.wait(4)

        pref = Matrix([[0] * len(p[0]) for _ in range(len(p))])
        self.play(
            p_mobj.animate.become(pref.get_mobject(), match_center=True),
            AddTextLetterByLetter(code.chars[0], run_time=0.05 * len(code.chars[0])),
        )
        self.wait(2)

        self.play(AddTextLetterByLetter(code.chars[1]), run_time=0.05 * len(code.chars[1]))
        self.play(AddTextLetterByLetter(code.chars[2]), run_time=0.05 * len(code.chars[2]))
        self.wait(3)

        # Highlight (1, 1) in prefix sum
        pref.highlight(1, 1, 1, 1, color=ORANGE, width=5)
        p_mobj.become(pref.get_mobject(), match_center=True)
        self.wait(2)

        # Highlight (0, 1), (1, 0), and (0, 0) in prefix sum
        pref.highlight(0, 1, 0, 1, color=YELLOW, width=5)
        pref.highlight(1, 0, 1, 0, color=YELLOW, width=5)
        p_mobj.become(pref.get_mobject(), match_center=True)
        self.wait(2)

        pref.highlight(0, 0, 0, 0, color=RED, width=5)
        p_mobj.become(pref.get_mobject(), match_center=True)
        self.wait(2)

        # Highlight (0, 0) in matrix with ORANGE
        m.highlight(0, 0, 0, 0, color=ORANGE, width=5)
        m_mobj.become(m.get_mobject(), match_center=True)
        self.wait()

        self.play(AddTextLetterByLetter(code.chars[3]), run_time=0.03 * len(code.chars[3]))
        self.play(AddTextLetterByLetter(code.chars[4]), run_time=0.03 * len(code.chars[4]))
        self.wait()

        # Fill the rows of the prefix sum array
        for r in range(1, len(p)):
            for c in range(1, len(p[0])):
                pref.values[r][c] = p[r][c]
                pref.unhighlight()
                pref.highlight(r, c, r, c, color=ORANGE, width=5)
                pref.highlight(r - 1, c, r - 1, c, color=YELLOW, width=5)
                pref.highlight(r, c - 1, r, c - 1, color=YELLOW, width=5)
                pref.highlight(r - 1, c - 1, r - 1, c - 1, color=RED, width=5)
                m.unhighlight()
                m.highlight(r - 1, c - 1, r - 1, c - 1, color=ORANGE, width=5)
                p_mobj.become(pref.get_mobject(), match_center=True)
                m_mobj.become(m.get_mobject(), match_center=True)
                if r == 1:
                    self.wait(0.6)
                elif r == 2:
                    self.wait(0.3)
                else:
                    self.wait(0.2)

        pref.unhighlight()
        m.unhighlight()
        p_mobj.become(pref.get_mobject(), match_center=True)
        m_mobj.become(m.get_mobject(), match_center=True)
        self.wait(2)
        self.play(
            FadeOut(code),
        )
        formula = MathTex(
            '{{ \\mathrm{sum}(ur, lc, br, rc) }} = '
            '{{p[br + 1][rc + 1]}} - {{p[ur][rc + 1]}} - {{p[br + 1][lc]}} + {{p[ur][lc]}}'
        ).scale(0.7).next_to(p_mobj, DOWN).align_to(m_mobj, LEFT)
        self.play(
            Write(formula),
        )
        self.wait(2)

        # Formula for (1, 1) -> (5, 3) => highlight the parts
        f1153 = MathTex(
            '{{ \\mathrm{sum}(1, 1, 5, 3) }} = {{p[6][4]}} - {{p[1][4]}} - {{p[6][1]}} + {{p[1][1]}}' +
            f' = {p[6][4] - p[1][4] - p[6][1] + p[1][1]}'
        ).scale(0.7).next_to(formula, DOWN).align_to(formula, LEFT)
        m.highlight(1, 1, 5, 3, color=ORANGE, width=5)
        pref.highlight(6, 4, 6, 4, color=ORANGE, width=5)
        pref.highlight(1, 4, 1, 4, color=YELLOW, width=5)
        pref.highlight(6, 1, 6, 1, color=YELLOW, width=5)
        pref.highlight(1, 1, 1, 1, color=RED, width=5)
        m_mobj.become(m.get_mobject(), match_center=True)
        p_mobj.become(pref.get_mobject(), match_center=True)
        self.wait(1)
        self.play(Write(f1153))
        self.wait(2)

        # Reset
        m.unhighlight()
        pref.unhighlight()
        m_mobj.become(m.get_mobject(), match_center=True)
        p_mobj.become(pref.get_mobject(), match_center=True)
        self.wait(1)

        # Formula for (0, 1) -> (5, 5) => highlight the parts
        f0155 = MathTex(
            f'{{ \\mathrm{{sum}}(0, 1, 5, 5) }} = {{p[6][6]}} - {{p[0][6]}} - {{p[6][1]}} + {{p[0][1]}}' +
            f' = {p[6][6] - p[0][6] - p[6][1] + p[0][1]}'
        ).scale(0.7).next_to(f1153, DOWN).align_to(f1153, LEFT)

        m.highlight(0, 1, 5, 5, color=ORANGE, width=5)
        pref.highlight(6, 6, 6, 6, color=ORANGE, width=5)
        pref.highlight(0, 6, 0, 6, color=YELLOW, width=5)
        pref.highlight(6, 1, 6, 1, color=YELLOW, width=5)
        pref.highlight(0, 1, 0, 1, color=RED, width=5)
        m_mobj.become(m.get_mobject(), match_center=True)
        p_mobj.become(pref.get_mobject(), match_center=True)
        self.wait(1)
        self.play(Write(f0155))
        self.wait(8)

        # Remove formulas
        self.play(
            FadeOut(f1153),
            FadeOut(f0155),
            FadeOut(formula),
        )
        self.wait(1)

        # Add Time and Memory Complexity text
        time_complexity = Tex(
            'Time Complexity: $\\mathcal{O}(R \\cdot C + Q)$'
        ).scale(0.7).next_to(p_mobj, DOWN).align_to(m_mobj, LEFT)
        self.play(Write(time_complexity))
        memory_complexity = Tex(
            'Memory Complexity: $\\mathcal{O}(R \\cdot C)$'
        ).scale(0.7).next_to(time_complexity, DOWN).align_to(time_complexity, LEFT)
        self.play(Write(memory_complexity))
        self.wait(10)

        self.play(Circumscribe(time_complexity))
        self.wait(3)
        self.play(Circumscribe(memory_complexity))
        self.wait(10)
