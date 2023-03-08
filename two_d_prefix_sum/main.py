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
