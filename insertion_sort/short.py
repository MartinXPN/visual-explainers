from textwrap import dedent

from manim import *

from insertion_sort.array import Array, TransformMatchingCells

ORANGE = ManimColor('#fa541c')


class UseCase(Scene):
    def __init__(self, *args, **kwargs):
        config.pixel_height, config.pixel_width = config.pixel_width, config.pixel_height
        config.frame_height = config.frame_height / 0.8
        config.frame_width = config.frame_height * 9 / 16
        super().__init__(*args, **kwargs)

    def construct(self):
        array = Array([1, 4, 5, 3, 12, 9], color=BLACK, cell_type='card')
        array_mobj = array.get_mobject().scale(0.5).center().shift(2.5 * UP)
        a_text = Tex('a:').scale(0.5).next_to(array_mobj, LEFT)
        indices = Array(
            [i for i in range(len(array))],
            width=array.width, height=array.height,
            spacing=array.spacing, scale_text=array.scale_text, stroke_color=BLACK,
        )
        indices_mobj = indices.get_mobject().scale(0.5).center().next_to(array_mobj, UP, buff=0.2)
        self.add(a_text, array_mobj, indices_mobj)
        self.wait(1)
        self.play(LaggedStart(*[
            Indicate(VGroup(cell, label))
            for cell, label in zip(array.cells, array.labels)
        ], lag_ratio=0.4, run_time=1))
        self.wait(1)

        new_array_mobj = array_mobj.copy()
        self.play(new_array_mobj.animate.shift(DOWN), run_time=1)
        self.wait(2)
        new_array = Array([1, 3, 4, 5, 9, 12], color=BLACK, cell_type='card')

        # Write Elements are at most 3 locations away from the final position
        text = Text(
            'At most 3 locations ⇄', font='Monospace', color=WHITE
        ).scale(0.4).next_to(new_array_mobj, DOWN, buff=0.8).align_to(new_array_mobj, LEFT)
        self.play(AddTextLetterByLetter(text, run_time=1))
        self.wait(1)

        self.play(
            TransformMatchingCells(new_array_mobj, new_array.get_mobject().scale(0.5).center().shift(1.5 * UP), path_arc=PI / 3),
            run_time=2,
        )

        # Draw arrows between 3s and 9s
        arrow3 = Arrow(
            start=array.cells[3].get_bottom(), end=new_array.cells[1].get_top(),
            color=ORANGE, buff=0.2, stroke_width=5, max_stroke_width_to_length_ratio=10,
            max_tip_length_to_length_ratio=0.5, tip_length=0.15,
        )
        arrow9 = Arrow(
            start=array.cells[5].get_bottom(), end=new_array.cells[4].get_top(),
            color=ORANGE, buff=0.2, stroke_width=5, max_stroke_width_to_length_ratio=10,
            max_tip_length_to_length_ratio=0.5, tip_length=0.15,
        )
        self.play(Create(arrow3), Create(arrow9), run_time=0.5)

        code = Code(
            code=dedent('''
                for i in range(1, len(a)):
                    j = i
                    while j > 0 and a[j] < a[j - 1]:
                        a[j - 1], a[j] = a[j], a[j - 1]
                        j -= 1
            ''').strip(),
            tab_width=4,
            language='Python',
            line_spacing=0.6,
            font='Monospace',
            style='monokai',
        ).scale(0.6).center().shift(1.5 * DOWN).shift(0.2 * LEFT).code

        for line in code.chars:
            self.play(AddTextLetterByLetter(line, run_time=0.03 * len(line)))
        self.wait(2.5)

        # Write 3*n = O(n)
        _3n = MathTex(r'3 \cdot n = ', color=WHITE).scale(0.7).next_to(code, DOWN, buff=0.5).align_to(text, LEFT)
        on = MathTex(r'\mathcal{O}(n)', color=ORANGE).scale(0.7).next_to(_3n, RIGHT, buff=0.2)
        self.play(Write(_3n), run_time=1)
        self.wait(3)
        self.play(Write(on), run_time=1)
        self.wait(2)

        comparison = MathTex(r'< \mathcal{O}(n \log{n})').scale(0.7).next_to(on, RIGHT, buff=0.2)
        self.play(Write(comparison), run_time=1)
        self.wait(3)

        self.play(ApplyWave(code), run_time=2)

        # Indicate the text
        self.play(Indicate(text, run_time=0.5))
        self.wait(2)
