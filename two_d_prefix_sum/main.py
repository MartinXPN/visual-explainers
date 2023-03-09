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
        self.wait(2)

        # Highlight (1, 1) -> (5, 3)
        m.highlight(1, 1, 5, 3, color=RED, width=5)
        m_mobj.become(m.get_mobject().center())
        self.wait()

        # Highlight (3, 4) -> (5, 5)
        m.unhighlight()
        m.highlight(3, 4, 5, 5, color=YELLOW, width=5)
        m_mobj.become(m.get_mobject().center())
        self.wait()

        # Highlight (2, 2) -> (4, 6)
        m.unhighlight()
        m.highlight(2, 2, 4, 6, color=GREEN, width=5)
        m_mobj.become(m.get_mobject().center())
        self.wait()

        # Move m to the left and add an empty p matrix on the right
        pref = Matrix([[None] * len(a[0]) for _ in range(len(a))])
        p_mobj = pref.get_mobject().center().shift(3 * RIGHT)
        self.play(
            m_mobj.animate.shift(3 * LEFT),
            FadeIn(p_mobj),
        )

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
        self.wait(2)

        # Transition to the next scene
        # Highlight only (2, 2) -> (4, 6) and nothing in p
        m.unhighlight()
        m.highlight(2, 2, 4, 6, color=GREEN, width=5)
        m_mobj.become(m.get_mobject().center().shift(3 * LEFT))
        pref.unhighlight()
        p_mobj.become(pref.get_mobject().center().shift(3 * RIGHT))
        self.wait()


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

        # Add text for the formula
        example_equation = MathTex(
            '{{ \\mathrm{sum}(2,2,4,6) }} = {{ p[4][6] }} - {{ p[1][6] }} - {{ p[4][1] }} + {{ p[1][1] }}'
        ).scale(0.7).center().move_to(2.5 * DOWN).shift(2 * LEFT)
        [example_equation[i].set_color(BLACK) for i in [2, 3, 4, 5, 6, 7, 8]]

        matrix_name = Text('m').scale(0.6).move_to(m_mobj, LEFT).shift(0.5 * LEFT)
        p_name = Text('p').scale(0.6).move_to(p_mobj, LEFT).shift(0.5 * LEFT)

        self.play(FadeIn(matrix_name), FadeIn(p_name), Write(example_equation))
        self.wait(2)

        # Highlight (0, 0) -> (4, 6) in a => (4, 6) in p
        m.highlight(0, 0, 4, 6, color=ORANGE, width=5)
        m_mobj.become(m.get_mobject().center().shift(3 * LEFT))
        pref.highlight(4, 6, 4, 6, color=ORANGE, width=5)
        p_mobj.become(pref.get_mobject().center().shift(3 * RIGHT))
        self.play(example_equation[2].animate.set_color(ORANGE))
        self.wait()

        # Highlight (0, 0) -> (4, 1) in a => (4, 1) in p
        m.highlight(0, 0, 4, 1, color=YELLOW, width=5)
        m_mobj.become(m.get_mobject().center().shift(3 * LEFT))
        pref.highlight(4, 1, 4, 1, color=YELLOW, width=5)
        p_mobj.become(pref.get_mobject().center().shift(3 * RIGHT))
        self.play(example_equation[3].animate.set_color(YELLOW), run_time=0.2)
        self.play(example_equation[4].animate.set_color(YELLOW))
        self.wait(2)

        # Highlight (0, 0) -> (1, 6) in a => (1, 6) in p
        m.highlight(0, 0, 1, 6, color=YELLOW, width=5)
        m_mobj.become(m.get_mobject().center().shift(3 * LEFT))
        pref.highlight(1, 6, 1, 6, color=YELLOW, width=5)
        p_mobj.become(pref.get_mobject().center().shift(3 * RIGHT))
        self.play(example_equation[5].animate.set_color(YELLOW), run_time=0.2)
        self.play(example_equation[6].animate.set_color(YELLOW))
        self.wait(2)

        # Flicker (0, 0) -> (1, 1) in a => (1, 1) in p
        for i in range(4):
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

        self.play(example_equation[7].animate.set_color(RED), run_time=0.2)
        self.play(example_equation[8].animate.set_color(RED))
        self.wait(2)

        formula = MathTex(
            '{{ \\mathrm{sum}(ur, lc, br, rc) }} = '
            '{{p[br][rc]}} - {{p[ur - 1][rc]}} - {{p[br][lc - 1]}} + {{p[ur - 1][lc - 1]}}'
        ).scale(0.7).align_to(example_equation, LEFT).shift(3 * DOWN)
        [formula[i].set_color(BLACK) for i in [2, 3, 4, 5, 6, 7, 8]]
        self.play(Write(formula))
        self.play(formula[2].animate.set_color(ORANGE))
        self.play(formula[3].animate.set_color(YELLOW), run_time=0.2)
        self.play(formula[4].animate.set_color(YELLOW))
        self.play(formula[5].animate.set_color(YELLOW), run_time=0.2)
        self.play(formula[6].animate.set_color(YELLOW))
        self.play(formula[7].animate.set_color(RED), run_time=0.2)
        self.play(formula[8].animate.set_color(RED))
        self.wait(1)

        # Add padding to p
        new_pref = Matrix(p)
        new_pref.highlight(5, 7, 5, 7, color=ORANGE, width=5)
        new_pref.highlight(5, 2, 5, 2, color=YELLOW, width=5)
        new_pref.highlight(2, 7, 2, 7, color=YELLOW, width=5)
        new_pref.highlight(2, 2, 2, 2, color=RED, width=5)
        new_p_mobj = new_pref.get_mobject().align_to(p_mobj, LEFT).align_to(p_mobj, UP)
        self.play(
            p_mobj.animate.become(new_p_mobj),
            example_equation.animate.shift(0.5 * DOWN),
            formula.animate.shift(0.5 * DOWN),
        )
        self.wait(2)

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
        self.wait(2)
