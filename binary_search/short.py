from textwrap import dedent

from manim import *

from binary_search.array import Array


a = [20, 22, 23, 23, 34, 49, 52, 55, 58]
ORANGE = ManimColor('#fa541c')


class OverflowIssue(Scene):
    def __init__(self, *args, **kwargs):
        config.pixel_height, config.pixel_width = config.pixel_width, config.pixel_height
        config.frame_height = config.frame_height / 0.8
        config.frame_width = config.frame_height * 9 / 16
        super().__init__(*args, **kwargs)

    def construct(self):
        array = Array(a, scale_text=0.35, height=0.35, width=0.35, spacing=0.05)
        array_mobj = array.get_mobject().center().shift(3 * UP)
        a_text = Tex('a:').scale(0.6).next_to(array_mobj, LEFT)
        indices = Array(
            [i for i in range(len(array) + 1)],
            width=array.width, height=array.height,
            spacing=array.spacing, scale_text=array.scale_text, stroke_color=BLACK,
        )
        indices_mobj = indices.get_mobject().center().next_to(array_mobj, 0.1 * DOWN).align_to(array_mobj, LEFT)
        indices.labels[-1].set_color(BLACK)
        self.add(array_mobj, a_text, indices_mobj)

        left = Tex('l', color=ORANGE).scale(0.6)
        right = Tex('r', color=ORANGE).scale(0.6)
        l_inclusive = Tex('[', color=ORANGE).scale(0.6).next_to(left, LEFT, buff=0.05)
        r_exclusive = Tex(')', color=ORANGE).scale(0.6).next_to(right, RIGHT, buff=0.05)
        left = VGroup(l_inclusive, left).next_to(array.rectangles[0], UP).shift(0.1 * DOWN)
        right = VGroup(right, r_exclusive).next_to(array.rectangles[-1], UP).shift(0.1 * DOWN).shift((array.width + array.spacing) * RIGHT)
        self.add(left, right)

        code = Code(
            code=dedent('''
                l, r = 0, len(a)
                while r - l > 1:
                    mid = (l + r) // 2
                    if a[mid] > q:
                        r = mid
                    else:
                        l = mid

                print(l if a[l] == q else -1)
            ''').strip(),
            tab_width=4,
            language='Python',
            line_spacing=0.6,
            font='Monospace',
            style='monokai',
        ).scale(0.7).next_to(indices_mobj, 4 * DOWN).shift(0.5 * LEFT).code
        for line in code.chars:
            if line:
                self.play(AddTextLetterByLetter(line), run_time=0.02 * len(line))

        self.wait(1)
        self.play(
            FadeOut(left),
            FadeOut(right),
            FadeOut(array_mobj),
            FadeOut(a_text),
            FadeOut(indices_mobj),
            run_time=0.5,
        )
        self.wait(0.5)

        # Add a segment with two sides: -2,147,483,648 on the left side and 2,147,483,647 on the right side
        segment = Line(start=1.5 * LEFT, end=1.5 * RIGHT, color=WHITE).center().shift(3 * UP)
        minimum = Integer(0).set_color(ORANGE).scale(0.5)     # -2_147_483_648
        maximum = Integer(0).set_color(ORANGE).scale(0.5)     # 2_147_483_647
        minimum.add_updater(lambda m: m.next_to(segment, UP).align_to(segment, LEFT).shift(LEFT))
        maximum.add_updater(lambda m: m.next_to(segment, UP).align_to(segment, RIGHT).shift(RIGHT))

        # Draw segment endpoints
        left_endpoint = Line(start=0.1 * DOWN, end=0.1 * UP, color=WHITE)
        right_endpoint = Line(start=0.1 * DOWN, end=0.1 * UP, color=WHITE)
        left_endpoint.add_updater(lambda m: m.next_to(segment, UP, buff=-0.1).align_to(segment, LEFT).shift(0.01 * LEFT))
        right_endpoint.add_updater(lambda m: m.next_to(segment, UP, buff=-0.1).align_to(segment, RIGHT).shift(0.01 * RIGHT))
        self.add(left_endpoint, right_endpoint)

        self.play(
            GrowFromCenter(segment),
            ChangeDecimalToValue(minimum, -2_147_483_648),
            ChangeDecimalToValue(maximum, 2_147_483_647),
            run_time=4,
            rate_func=linear,
        )
        self.wait(6)

        # Indicate the `mid = (l + r) // 2` line
        self.play(Indicate(code.chars[2]), run_time=2)
        self.wait(4)

        # Add l (arrow) at the 1.5 billion point and r (arrow) at 1.7 billion point of the segment
        l_arrow = Arrow(start=DOWN, end=UP, tip_length=0.1, color=YELLOW).scale(0.2).next_to(segment, DOWN).align_to(segment, RIGHT).shift(0.9 * LEFT)
        r_arrow = Arrow(start=DOWN, end=UP, tip_length=0.1, color=YELLOW).scale(0.2).next_to(segment, DOWN).align_to(segment, RIGHT).shift(0.2 * LEFT)
        l_label = Text('l', color=YELLOW).scale(0.4).next_to(l_arrow, DOWN)
        r_label = Text('r', color=YELLOW).scale(0.4).next_to(r_arrow, DOWN)
        self.play(Write(l_arrow), Write(l_label), run_time=0.5)
        self.wait(0.5)
        self.play(Write(r_arrow), Write(r_label), run_time=0.5)
        self.wait(6)

        sum_arrow = Arrow(start=DOWN, end=UP, tip_length=0.1, color=RED).scale(0.2).next_to(segment, DOWN).align_to(segment, RIGHT).shift(0.5 * RIGHT)
        sum_label = Text('l + r', color=RED).scale(0.4).next_to(sum_arrow, DOWN)
        self.play(Write(sum_label), run_time=0.5)
        self.wait(1)
        self.play(Write(sum_arrow), run_time=0.5)
        self.wait(6)

        # Move l + r to the start of the segment
        self.play(VGroup(sum_arrow, sum_label).animate.next_to(segment, DOWN).align_to(segment, LEFT).shift(0.2 * RIGHT), run_time=2)
        self.wait(3)
