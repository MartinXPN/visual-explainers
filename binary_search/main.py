from textwrap import dedent

from manim import *


a = [20, 22, 23, 23, 34, 49, 52, 55, 58]


class ProblemStatement(Scene):
    def construct(self):
        title = Title('Find the Position of a Given Number', include_underline=False)
        self.play(Write(title))
        self.wait(1)
