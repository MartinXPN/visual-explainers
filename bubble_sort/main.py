from manim import *

a = [12, 3, 5, 9, 4, 1, 7]
ORANGE = ManimColor('#fa541c')


class Introduction(Scene):
    def construct(self):
        title = Title('...', include_underline=False)
        self.play(Write(title))
        self.wait(2)
