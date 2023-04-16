from manim import *

from prefix_sum_arrays.array import Array


class CreateThumbnail(Scene):
    def construct(self):
        with register_font('font/JetBrainsMono-Bold.ttf') as f:
            print(f)
            text = Text(
                'Prefix Sum\nExplained', font='JetBrains Mono Bold', font_size=77
            ).center().shift(3 * LEFT).shift(2 * UP)
        self.add(text)

        array = Array([3, -2, 4, 10, -1, 0, 5], width=0.8, height=0.8, spacing=0.05, scale_text=0.8)
        array.highlight(2, 5, color=ORANGE)
        array_mobj = array.get_mobject().center().next_to(text, DOWN, buff=1.5).align_to(text, LEFT)
        self.add(array_mobj)

        brace = Brace(array_mobj, DOWN).scale(0.57).shift(0.45 * RIGHT)
        self.add(brace)
        question_mark = Tex('?').scale(0.8).next_to(brace, DOWN, buff=0.1)
        self.add(question_mark)
