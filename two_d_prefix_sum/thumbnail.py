from manim import *

from two_d_prefix_sum.matrix import Matrix

a = [
    [1, 2, -1, -3, 4, 2, 0],
    [3, -2, 4, 5, -3, -1, 1],
    [0, 1, -3, 1, 3, 2, 4],
    [-1, 3, 4, 7, -2, 0, 1],
    [3, 4, 2, 4, -7, -1, 3],
]


class CreateThumbnail(Scene):
    def construct(self):
        with register_font('font/JetBrainsMono-Bold.ttf'):
            fast = Text('Fast', color=RED, font='JetBrains Mono Bold', font_size=64).shift(4.5 * LEFT).shift(2.5 * UP)
            submatrix_sum = Text('Submatrix Sum', font='JetBrains Mono Bold', font_size=64).next_to(fast, DOWN).align_to(fast, LEFT)
        self.add(fast, submatrix_sum)

        m = Matrix(a)
        m.highlight(1, 2, 2, 4)
        m_mobj = m.get_mobject().center().shift(3 * LEFT).shift(1.2 * DOWN)
        self.add(m_mobj)
