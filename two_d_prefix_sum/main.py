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
        title = Title('2D Prefix Sum', include_underline=False)
        self.play(Write(title))
        self.wait(2)

        m = Matrix(a)
        m_mobj = m.get_mobject()
        self.play(FadeIn(m_mobj))
        self.wait(2)
