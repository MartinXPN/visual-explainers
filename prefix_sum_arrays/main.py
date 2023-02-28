import random
from textwrap import dedent

from manim import *
from prefix_sum_arrays.array import Array


class UploadToYoutube(Scene):
    def construct(self):
        # Add the Youtube logo
        logo = SVGMobject('prefix_sum_arrays/youtube-icon.svg')
        logo.scale(0.5)
        # Add text "Uploading..."
        text = Text('Uploading...')
        text.next_to(logo, DOWN)
        # Add the progress bar
        bar = RoundedRectangle(width=6., height=0.25, corner_radius=0.125)
        bar.next_to(text, DOWN)

        # Group the logo, text and progress bar + Center the group
        group = VGroup(logo, text, bar)
        group.center()

        # Animate the progress bar
        progress = ValueTracker(0)

        # Add filler to the progress bar
        def get_filler():
            fill = Rectangle(
                width=max(0, progress.get_value() - 0.25), height=0.25, fill_color=GREEN, fill_opacity=1, stroke_width=0
            ).align_to(bar, DOWN).align_to(bar, LEFT).shift(0.125 * RIGHT)
            left = Circle(
                radius=0.125, fill_color=GREEN, fill_opacity=1, stroke_width=0
            ).align_to(bar, DOWN).align_to(bar, LEFT)
            right = Circle(
                radius=0.125, fill_color=GREEN, fill_opacity=1, stroke_width=0
            ).align_to(bar, DOWN).align_to(fill, RIGHT).shift(0.125 * RIGHT)
            fill.add(left, right)
            return fill
        filler = always_redraw(get_filler)
        self.add(logo, text, bar, filler)
        self.play(progress.animate.set_value(6), run_time=2)

        # Move the logo to the top and turn the progress bar to a green tick
        tick = SVGMobject('prefix_sum_arrays/tick.svg', color=GREEN, fill_color=GREEN, fill_opacity=1).scale(0.5)
        tick.align_to(bar, DOWN)
        self.remove(bar, progress, text)
        self.play(
            logo.animate.move_to(2.5 * UP),
            ReplacementTransform(filler, tick, run_time=0.5),
        )
        self.wait()

        # Remove the tick and add an array that represents the video performance by days
        self.remove(tick)
        array = Array([None] * 9, width=0.8, height=0.8, spacing=0.05, scale_text=0.8)\
            .get_mobject()\
            .center()
        text = Text('Video Score by Day').center().next_to(array, UP)
        self.play(
            FadeIn(text),
            FadeIn(array),
        )
        self.wait()


class FillInitialArray(Scene):
    def construct(self):
        logo = SVGMobject('prefix_sum_arrays/youtube-icon.svg').scale(0.5).move_to(2.5 * UP)

        # Add the array
        array = Array([None] * 9, width=0.8, height=0.8, spacing=0.05, scale_text=0.8)
        array_mobj = array.get_mobject().center()

        # Add indices below the array
        indices = Array(
            [i for i in range(len(array))],
            width=array.width, height=array.height,
            spacing=array.spacing, scale_text=array.scale_text, stroke_color=BLACK,
        ).get_mobject().center().next_to(array_mobj, 0.0001 * DOWN)

        text = Text('Video Score By Day').center().next_to(array_mobj, UP)
        self.add(logo, text, indices, array_mobj)

        def get_reactions(nb_likes: int, nb_dislikes: int):
            like_svg = SVGMobject(
                'prefix_sum_arrays/dislike.svg', color=WHITE, fill_color=WHITE, fill_opacity=1
            ).scale(0.5).rotate(PI).shift(LEFT).shift(2 * DOWN)
            like_text = Text(
                f'{nb_likes}', color=BLACK, weight=BOLD, font='Consolas',
            ).scale(0.7).align_to(like_svg, RIGHT).shift(0.35 * LEFT).align_to(like_svg, UP).shift(0.5 * DOWN)
            like = VGroup(like_svg, like_text)

            dislike_svg = SVGMobject(
                'prefix_sum_arrays/dislike.svg', color=WHITE, fill_color=WHITE, fill_opacity=1
            ).scale(0.5).shift(RIGHT).shift(2.35 * DOWN)
            dislike_text = Text(
                f'{nb_dislikes}', color=BLACK, weight=BOLD, font='Consolas',
            ).scale(0.7).align_to(dislike_svg, LEFT).shift(0.35 * RIGHT).align_to(dislike_svg, UP).shift(0.2 * DOWN)
            dislike = VGroup(dislike_svg, dislike_text)

            return [like, dislike]

        # Animate the array: When adding each value animate the number of likes and dislikes
        values = [8,    3, -2, 4, 10, -1, 0, 5, 3]
        upvotes = [8,   3,  2, 4, 10,  0, 2, 7, 3]
        downvotes = [0, 0,  4, 0,  0,  1, 2, 2, 0]

        # On the day of uploading the video it got 8 likes, so we add 8 to day 0
        for i, val in enumerate(values):
            # Add the reactions
            reactions = get_reactions(upvotes[i], downvotes[i])
            [l, d] = reactions
            if i < 4:
                if upvotes[i] > 0:
                    self.play(
                        FadeIn(l),
                        Flash(l, flash_radius=0.8, line_length=0.3, color=ORANGE)
                    )
                if downvotes[i] > 0:
                    self.play(FadeIn(d), run_time=0.2)

            # Increase the value up to the number of upvotes and then decrease it by the number of downvotes
            for diff in range(1, upvotes[i] + 1):
                array.values[i] = diff
                self.play(array_mobj.animate.become(array.get_mobject().center()), run_time=0.001)
                self.wait(0.1)
            if downvotes[i] > 0:
                self.wait(0.5)
            for diff in range(1, downvotes[i] + 1):
                array.values[i] = upvotes[i] - diff
                self.play(array_mobj.animate.become(array.get_mobject().center()), run_time=0.001)
                self.wait(0.1)

            # Fade out the reactions
            if i < 4:
                to_remove = []
                if upvotes[i] > 0:
                    to_remove.append(l)
                if downvotes[i] > 0:
                    to_remove.append(d)
                self.play(FadeOut(*to_remove))
                self.wait(0.5)

        self.wait()

        # Highlight the 2 -> 7
        array.stroke_color = [WHITE, WHITE, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, WHITE]
        array.stroke_width = [2, 2, 5, 5, 5, 5, 5, 5, 2]
        self.play(
            logo.animate.shift(5 * UP),
            text.animate.become(Text("What's the Sum of the Range?").center().next_to(array_mobj, UP).shift(1.5 * UP)),
        )
        self.play(array_mobj.animate.become(array.get_mobject().center()), run_time=0.001)
        self.wait(2)

        # Highlight the 3 -> 6
        array.stroke_color = [WHITE, WHITE, WHITE, ORANGE, ORANGE, ORANGE, ORANGE, WHITE, WHITE]
        array.stroke_width = [2, 2, 2, 5, 5, 5, 5, 2, 2]
        self.play(array_mobj.animate.become(array.get_mobject().center()), run_time=0.001)
        self.wait(2)


class NaiveApproach(Scene):
    def construct(self):
        # Add the array
        values = [8, 3, -2, 4, 10, -1, 0, 5, 3]
        array = Array(values, width=0.8, height=0.8, spacing=0.05, scale_text=0.8)
        array.stroke_color = [WHITE, WHITE, WHITE, ORANGE, ORANGE, ORANGE, ORANGE, WHITE, WHITE]
        array.stroke_width = [2, 2, 2, 5, 5, 5, 5, 2, 2]
        array_mobj = array.get_mobject().center()

        # Add indices below the array
        indices = Array(
            [i for i in range(len(array))],
            width=array.width, height=array.height,
            spacing=array.spacing, scale_text=array.scale_text, stroke_color=BLACK,
        ).get_mobject().center().next_to(array_mobj, 0.0001 * DOWN)

        text = Text("What's the Sum of the Range?").center().next_to(array_mobj, UP).shift(1.5 * UP)
        arrow = Arrow(
            start=UP, end=DOWN, color=ORANGE, buff=0.1,
            stroke_width=10, max_stroke_width_to_length_ratio=15,
            max_tip_length_to_length_ratio=0.5, tip_length=0.2,
        ).scale(0.3).next_to(array_mobj, UP).shift(array.width * 1 * LEFT)
        self.add(text, indices, array_mobj, arrow)
        self.wait()

        self.play(arrow.animate.shift(array.width * RIGHT), run_time=0.5)
        self.play(arrow.animate.shift(array.width * RIGHT), run_time=0.5)
        self.play(arrow.animate.shift(array.width * RIGHT), run_time=0.5)
        self.wait()

        # Highlight the 2 -> 7
        array.stroke_color = [WHITE, WHITE, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, WHITE]
        array.stroke_width = [2, 2, 5, 5, 5, 5, 5, 5, 2]
        self.play(
            array_mobj.animate.become(array.get_mobject().center()),
            FadeOut(arrow),
            run_time=0.001
        )

        # Range sum from 2 to 7
        start, end = 2, 7
        total_text = Text('Sum: ')
        total_num = Integer(0).next_to(total_text, RIGHT).scale(1.3)
        total = always_redraw(
            lambda: VGroup(total_text, total_num)
        ).center().next_to(array_mobj, DOWN).scale(0.8).shift(1.5 * DOWN)
        arrow.shift(0.8 * 4 * LEFT).set_color(YELLOW)
        self.play(Write(total))
        self.wait()

        self.play(
            DrawBorderThenFill(arrow),
            total_num.animate.set_value(values[start]),
        )
        for i in range(start + 1, end + 1):
            self.play(
                total_num.animate.set_value(sum(values[start:i + 1])),
                arrow.animate.shift(array.width * RIGHT),
                run_time=1,
            )
        self.wait()
        self.play(FadeOut(arrow))

        # Range sum from 3 to 6
        start, end = 3, 6
        arrow.shift(array.width * 4 * LEFT).set_color(ORANGE)
        array.stroke_color = [WHITE, WHITE, WHITE, ORANGE, ORANGE, ORANGE, ORANGE, WHITE, WHITE]
        array.stroke_width = [2, 2, 2, 5, 5, 5, 5, 2, 2]
        self.play(
            array_mobj.animate.become(array.get_mobject().center()),
            total_num.animate.set_value(0),
            run_time=0.001
        )
        self.wait(2)
        self.play(
            DrawBorderThenFill(arrow),
            total_num.animate.set_value(values[start]),
            run_time=0.5,
        )

        for i in range(start + 1, end + 1):
            self.play(
                arrow.animate.shift(array.width * RIGHT),
                total_num.animate.set_value(sum(values[start:i + 1])),
                run_time=0.5,
            )
        self.wait(2)


def get_sum_tex(a):
    res = f'{{{{ {len(a) - 1} }}}}: ' + ' + '.join([f'{{{{ a_{i} }}}}' for i in range(len(a))]) + ' = '
    res += f'{{{{ {a[0]} }}}}'
    for i in range(1, len(a)):
        res += f' + {{{{ {a[i]} }}}}' if a[i] >= 0 else f' - {{{{ {-a[i]} }}}}'
    res += f' = {{{{ {sum(a)} }}}}'
    print(res)
    return res


class NaivePrefixSum(Scene):
    def construct(self):
        values = [8, 3, -2, 4, 10, -1, 0, 5, 3]
        array = Array(values, width=0.8, height=0.8, spacing=0.05, scale_text=0.8)
        array.stroke_color = [ORANGE, ORANGE, ORANGE, ORANGE, ORANGE, ORANGE, ORANGE, WHITE, WHITE]
        array.stroke_width = [5, 5, 5, 5, 5, 5, 5, 2, 2]
        array_mobj = array.get_mobject().center().move_to(1.2 * UP)

        # Add indices below the array
        indices = Array(
            [i for i in range(len(array))],
            width=array.width, height=array.height,
            spacing=array.spacing, scale_text=array.scale_text, stroke_color=BLACK,
        ).get_mobject().center().next_to(array_mobj, 0.0001 * DOWN)

        text = Text("What's the Sum Up To Day X?").center().next_to(array_mobj, UP).shift(0.5 * UP)
        self.add(text, indices, array_mobj)
        self.wait()

        # 0 -> 3
        array.stroke_color = [YELLOW, YELLOW, YELLOW, YELLOW, WHITE, WHITE, WHITE, WHITE, WHITE]
        array.stroke_width = [5, 5, 5, 5, 2, 2, 2, 2, 2]
        self.play(array_mobj.animate.become(array.get_mobject().center().move_to(1.2 * UP)), run_time=0.001)
        self.wait()

        # 0 -> 5
        array.stroke_color = [RED, RED, RED, RED, RED, RED, WHITE, WHITE, WHITE]
        array.stroke_width = [5, 5, 5, 5, 5, 5, 2, 2, 2]
        self.play(array_mobj.animate.become(array.get_mobject().center().move_to(1.2 * UP)), run_time=0.001)
        self.wait()

        # 0 -> 2
        array.stroke_color = [GREEN, GREEN, GREEN, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE]
        array.stroke_width = [5, 5, 5, 2, 2, 2, 2, 2, 2]
        self.play(array_mobj.animate.become(array.get_mobject().center().move_to(1.2 * UP)), run_time=0.001)
        self.wait()

        # 0 -> 7
        array.stroke_color = [ORANGE, ORANGE, ORANGE, ORANGE, ORANGE, ORANGE, ORANGE, ORANGE, WHITE]
        array.stroke_width = [5, 5, 5, 5, 5, 5, 5, 5, 2]
        self.play(array_mobj.animate.become(array.get_mobject().center().move_to(1.2 * UP)), run_time=0.001)
        self.wait()

        # Arrow shows which element is currently being added to the sum
        arrow = Arrow(
            start=UP, end=DOWN, color=YELLOW, buff=0,
            stroke_width=10, max_stroke_width_to_length_ratio=15,
            max_tip_length_to_length_ratio=0.5, tip_length=0.2,
        ).scale(0.25).next_to(array_mobj, UP).shift((array.width + array.spacing) * 4 * LEFT).shift(0.1 * DOWN)
        self.add(arrow)

        def animate_sum(color, x, align_mobj, shift=0):
            array.stroke_color = [color] * (x + 1) + [WHITE] * (len(values) - x - 1)
            array.stroke_width = [5] * (x + 1) + [2] * (len(values) - x - 1)
            arrow.set_color(color)
            self.play(array_mobj.animate.become(array.get_mobject().center().move_to(1.2 * UP)), run_time=0.001)
            self.wait()

            # Animate the arrow
            for _ in range(x):
                self.play(arrow.animate.shift((array.width + array.spacing) * RIGHT), run_time=0.5)

            res = MathTex(get_sum_tex(values[: x + 1])).scale(0.6)\
                .next_to(align_mobj, DOWN).align_to(align_mobj, LEFT).shift(shift)
            self.play(Write(res), run_time=0.5)
            self.wait()
            arrow.shift((array.width + array.spacing) * LEFT * x)
            return res

        sum3 = animate_sum(YELLOW, 3, indices, 0.5 * DOWN)
        sum5 = animate_sum(RED, 5, sum3)
        sum2 = animate_sum(GREEN, 2, sum5)
        sum7 = animate_sum(ORANGE, 7, sum2)
        self.play(FadeOut(arrow))
        self.wait()

        # Common for 3 and 5 -> Isolate the common parts of the sums
        common = ['a_0', 'a_1', 'a_2', 'a_3']
        for tex in common:
            sum3.set_color_by_tex(tex, ORANGE)
            sum5.set_color_by_tex(tex, ORANGE)
        self.wait(3)

        # Reset the colors
        sum3.set_color(WHITE)
        sum5.set_color(WHITE)

        # common for 5 and 7
        common = ['a_0', 'a_1', 'a_2', 'a_3', 'a_4', 'a_5']
        for tex in common:
            sum5.set_color_by_tex(tex, ORANGE)
            sum7.set_color_by_tex(tex, ORANGE)
        self.wait(3)

        array.stroke_color = [WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE]
        array.stroke_width = [2, 2, 2, 2, 2, 2, 2, 2, 2]
        self.play(array_mobj.animate.become(array.get_mobject().center().move_to(1.2 * UP)), run_time=0.001)

        # Transition to the next scene
        p = Array(
            [None] * len(values),
            width=array.width, height=array.height,
            spacing=array.spacing, scale_text=array.scale_text
        )
        p_mobj = p.get_mobject().center().next_to(array_mobj, DOWN)

        array_name = Text('a:').scale(0.8).move_to(array_mobj, LEFT).shift(0.7 * LEFT)
        p_name = Text('p:').scale(0.8).move_to(p_mobj, LEFT).shift(0.7 * LEFT)

        self.play(
            FadeOut(sum3), FadeOut(sum5), FadeOut(sum2), FadeOut(sum7),
            FadeIn(p_mobj), FadeIn(p_name), FadeIn(array_name),
            indices.animate.next_to(p_mobj, 0.0001 * DOWN)
        )
        self.wait()


class PrefixSumCalculation(Scene):
    def construct(self):
        values = [8, 3, -2, 4, 10, -1, 0, 5, 3]
        array = Array(values, width=0.8, height=0.8, spacing=0.05, scale_text=0.8)
        array_mobj = array.get_mobject().center().move_to(1.2 * UP)
        text = Text("What's the Sum Up To Day X?").center().next_to(array_mobj, UP).shift(0.5 * UP)

        p = Array(
            [None] * len(values),
            width=array.width, height=array.height,
            spacing=array.spacing, scale_text=array.scale_text
        )
        p_mobj = p.get_mobject().center().next_to(array_mobj, DOWN)

        array_name = Text('a:').scale(0.8).move_to(array_mobj, LEFT).shift(0.7 * LEFT)
        p_name = Text('p:').scale(0.8).move_to(p_mobj, LEFT).shift(0.7 * LEFT)

        # Add indices below the array
        indices = Array(
            [i for i in range(len(array))],
            width=array.width, height=array.height,
            spacing=array.spacing, scale_text=array.scale_text, stroke_color=BLACK,
        ).get_mobject().center().next_to(p_mobj, 0.0001 * DOWN)
        self.add(text, indices, array_mobj, array_name, p_mobj, p_name)
        self.wait()

        # Highlight the 7th cell of the prefix sum
        p.stroke_color = [WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, ORANGE, WHITE]
        p.stroke_width = [2, 2, 2, 2, 2, 2, 2, 5, 2]
        self.play(p_mobj.animate.become(p.get_mobject().center().next_to(array_mobj, DOWN)), run_time=0.001)
        self.wait()

        def highlight_sum(x, align_mobj):
            array.stroke_color = [YELLOW] * (x + 1) + [WHITE] * (len(values) - x - 1)
            array.stroke_width = [5] * (x + 1) + [2] * (len(values) - x - 1)
            p.stroke_color = [WHITE] * len(values)
            p.stroke_color[x] = ORANGE
            p.stroke_width = [2] * len(values)
            p.stroke_width[x] = 5
            self.play(
                array_mobj.animate.become(array.get_mobject().center().move_to(1.2 * UP)),
                p_mobj.animate.become(p.get_mobject().center().next_to(array_mobj, DOWN)),
                run_time=0.001
            )

            if x < 4:
                res = MathTex(get_sum_tex(values[: x + 1]))
            elif x == 4:
                res = MathTex(f'{{{{ {x} }}}}: ...')
            else:
                res = None

            if res:
                res = res.scale(0.6).next_to(align_mobj, DOWN).align_to(align_mobj, LEFT)
                self.play(Write(res), run_time=0.5)
            self.wait()
            return res

        highlights = [highlight_sum(0, indices)]
        for i in range(1, len(values)):
            highlights.append(highlight_sum(i, highlights[-1]))
        self.wait()

        # Remove the highlights
        array.stroke_color = [WHITE] * len(values)
        array.stroke_width = [2] * len(values)
        p.stroke_color = [WHITE] * len(values)
        p.stroke_width = [2] * len(values)
        self.play(
            array_mobj.animate.become(array.get_mobject().center().move_to(1.2 * UP)),
            p_mobj.animate.become(p.get_mobject().center().next_to(array_mobj, DOWN)),
            FadeOut(*[item for item in highlights if item is not None]),
            run_time=0.001,
        )
        self.wait()

        # Compute the prefix sum
        def get_one_tex(x):
            res = f'{{{{ {x} }}}}: ' + (f'{{{{ p_{x - 1} }}}} + ' if x > 0 else '') + f'{{{{ a_{x} }}}} = '
            if x == 0:
                res += f'{{{{ {values[x]} }}}}'
                return res
            res += f'{{{{ {p.values[x - 1]} }}}}'
            res += f' + {{{{ {values[x]} }}}}' if values[x] >= 0 else f' - {{{{ {-values[x]} }}}}'
            res += f' = {{{{ {p.values[x - 1] + values[x]} }}}}'
            print(res)
            return res

        def highlight_one(x, align_mobj):
            array.stroke_color = [WHITE] * (len(values))
            array.stroke_color[x] = YELLOW
            array.stroke_width = [2] * (len(values))
            array.stroke_width[x] = 5
            p.stroke_color = [WHITE] * len(values)
            p.stroke_color[x] = ORANGE
            p.stroke_width = [2] * len(values)
            p.stroke_width[x] = 5

            if x == 0:
                p.values[x] = values[x]
            else:
                p.values[x] = p.values[x - 1] + values[x]
                p.stroke_color[x - 1] = YELLOW
                p.stroke_width[x - 1] = 5
            self.play(
                array_mobj.animate.become(array.get_mobject().center().move_to(1.2 * UP)),
                p_mobj.animate.become(p.get_mobject().center().next_to(array_mobj, DOWN)),
                run_time=0.001
            )

            if x < 4:
                res = MathTex(get_one_tex(x))
            elif x == 4:
                res = MathTex(f'{{{{ {x} }}}}: ...')
            else:
                res = None

            if res:
                res = res.scale(0.6).next_to(align_mobj, DOWN).align_to(align_mobj, LEFT)
                self.play(Write(res), run_time=0.5)
            self.wait()
            return res

        highlights = [highlight_one(0, indices)]
        for i in range(1, len(values)):
            highlights.append(highlight_one(i, highlights[-1]))
        self.wait()

        # Transition to the next scene
        array.stroke_color = [WHITE] * (len(values))
        array.stroke_width = [2] * (len(values))
        p.stroke_color = [WHITE] * len(values)
        p.stroke_width = [2] * len(values)
        self.play(
            array_mobj.animate.become(array.get_mobject().center().move_to(1.2 * UP)),
            p_mobj.animate.become(p.get_mobject().center().next_to(array_mobj, DOWN)),
            run_time=0.001
        )
        self.play(
            text.animate.become(Text('Prefix Sum Array').center().next_to(array_mobj, UP).shift(0.5 * UP)),
            FadeOut(*[item for item in highlights if item is not None]),
        )
        self.wait()


class PrefixSumCode(Scene):
    def construct(self):
        values = [8, 3, -2, 4, 10, -1, 0, 5, 3]
        array = Array(values, width=0.8, height=0.8, spacing=0.05, scale_text=0.8)
        array_mobj = array.get_mobject().center().move_to(1.2 * UP)
        p = Array(
            [sum(values[:i + 1]) for i in range(len(values))],
            width=array.width, height=array.height,
            spacing=array.spacing, scale_text=array.scale_text
        )
        p_mobj = p.get_mobject().center().next_to(array_mobj, DOWN)
        array_name = Text('a:').scale(0.8).move_to(array_mobj, LEFT).shift(0.7 * LEFT)
        p_name = Text('p:').scale(0.8).move_to(p_mobj, LEFT).shift(0.7 * LEFT)

        text = Text('Prefix Sum Array').center().next_to(array_mobj, UP).shift(0.5 * UP)
        # Add indices below the array
        indices = Array(
            [i for i in range(len(array))],
            width=array.width, height=array.height,
            spacing=array.spacing, scale_text=array.scale_text, stroke_color=BLACK,
        ).get_mobject().center().next_to(p_mobj, 0.0001 * DOWN)
        self.add(text, indices, array_mobj, array_name, p_mobj, p_name)
        self.wait()

        code = Code(
            code=dedent('''
                p = [0] * n
                p[0] = a[0]
                for i in range(1, n):
                    p[i] = p[i - 1] + a[i]
            ''').strip(),
            tab_width=4,
            language='Python',
            line_spacing=0.6,
            font='Monospace',
            style='monokai',
        ).next_to(indices, DOWN).code
        for line in code.chars:
            self.play(AddTextLetterByLetter(line))
        self.wait()

        # Highlight p[6]
        p.stroke_color = [WHITE] * len(values)
        p.stroke_color[6] = ORANGE
        p.stroke_width = [2] * len(values)
        p.stroke_width[6] = 5
        self.play(p_mobj.animate.become(p.get_mobject().center().next_to(array_mobj, DOWN)), run_time=0.001)
        self.wait()

        # Highlight p[8]
        p.stroke_color = [WHITE] * len(values)
        p.stroke_color[8] = ORANGE
        p.stroke_width = [2] * len(values)
        p.stroke_width[8] = 5
        self.play(p_mobj.animate.become(p.get_mobject().center().next_to(array_mobj, DOWN)), run_time=0.001)
        self.wait()

        # Circumscribe p
        self.play(Circumscribe(p_mobj), run_time=3)
        self.wait()

        # Transition to the next scene
        p.stroke_color = [WHITE] * len(values)
        p.stroke_width = [2] * len(values)

        self.play(p_mobj.animate.become(p.get_mobject().center().next_to(array_mobj, DOWN)), run_time=0.001)
        self.play(
            FadeOut(code),
            text.animate.become(MathTex(
                '\\mathrm{Range \\ Sum } [l, r]'
            ).center().next_to(array_mobj, UP).shift(0.5 * UP)),
        )
        self.wait()


class AnsweringRangeQueries(Scene):
    def construct(self):
        values = [8, 3, -2, 4, 10, -1, 0, 5, 3]
        array = Array(values, width=0.8, height=0.8, spacing=0.05, scale_text=0.8)
        array_mobj = array.get_mobject().center().move_to(1.2 * UP)
        p = Array(
            [sum(values[:i + 1]) for i in range(len(values))],
            width=array.width, height=array.height,
            spacing=array.spacing, scale_text=array.scale_text
        )
        p_mobj = p.get_mobject().center().next_to(array_mobj, DOWN)
        array_name = Text('a:').scale(0.8).move_to(array_mobj, LEFT).shift(0.7 * LEFT)
        p_name = Text('p:').scale(0.8).move_to(p_mobj, LEFT).shift(0.7 * LEFT)

        text = MathTex('\\mathrm{Range \\ Sum } [l, r]').center().next_to(array_mobj, UP).shift(0.5 * UP)
        # Add indices below the array
        indices = Array(
            [i for i in range(len(array))],
            width=array.width, height=array.height,
            spacing=array.spacing, scale_text=array.scale_text, stroke_color=BLACK,
        ).get_mobject().center().next_to(p_mobj, 0.0001 * DOWN)
        self.add(text, indices, array_mobj, array_name, p_mobj, p_name)
        self.wait()

        # Highlight the range 3 -> 6
        array.stroke_color = [WHITE, WHITE, WHITE, ORANGE, ORANGE, ORANGE, ORANGE, WHITE, WHITE]
        array.stroke_width = [2, 2, 2, 5, 5, 5, 5, 2, 2]
        self.play(array_mobj.animate.become(array.get_mobject().center().move_to(1.2 * UP)), run_time=0.001)
        self.wait(2)

        # Highlight the range 5 -> 8
        array.stroke_color = [WHITE, WHITE, WHITE, WHITE, WHITE, GREEN, GREEN, GREEN, GREEN]
        array.stroke_width = [2, 2, 2, 2, 2, 5, 5, 5, 5]
        self.play(array_mobj.animate.become(array.get_mobject().center().move_to(1.2 * UP)), run_time=0.001)
        self.wait(1)

        # Highlight the range 2 -> 7
        array.stroke_color = [WHITE, WHITE, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, WHITE]
        array.stroke_width = [2, 2, 5, 5, 5, 5, 5, 5, 2]
        self.play(array_mobj.animate.become(array.get_mobject().center().move_to(1.2 * UP)), run_time=0.001)
        self.wait(3)

        # Add a text Range [2; 7]
        range_2_7 = MathTex(
            '\\mathrm{Sum} \\ [2, 7]'
        ).scale(0.8).center().next_to(indices, DOWN).align_to(p_name, LEFT)
        self.add(range_2_7)

        # Highlight the range 0 -> 7
        array.stroke_color = [YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, WHITE]
        array.stroke_width = [5, 5, 5, 5, 5, 5, 5, 5, 2]
        p.stroke_color = [WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, YELLOW, WHITE]
        p.stroke_width = [2, 2, 2, 2, 2, 2, 2, 5, 2]
        self.play(
            array_mobj.animate.become(array.get_mobject().center().move_to(1.2 * UP)),
            p_mobj.animate.become(p.get_mobject().center().next_to(array_mobj, DOWN)),
            run_time=0.001
        )
        range_7 = MathTex(' = p_7').scale(0.8).center().next_to(range_2_7, RIGHT)
        self.play(Write(range_7))
        self.wait()

        # Subtract the range 0 -> 1
        array.stroke_color = [YELLOW_A, YELLOW_A, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, WHITE]
        array.stroke_width = [5, 5, 5, 5, 5, 5, 5, 5, 2]
        p.stroke_color = [WHITE, YELLOW_A, WHITE, WHITE, WHITE, WHITE, WHITE, YELLOW, WHITE]
        p.stroke_width = [2, 5, 2, 2, 2, 2, 2, 5, 2]
        self.play(
            array_mobj.animate.become(array.get_mobject().center().move_to(1.2 * UP)),
            p_mobj.animate.become(p.get_mobject().center().next_to(array_mobj, DOWN)),
            run_time=0.001
        )
        range_1 = MathTex(f' - p_1 = {p.values[7]} - {p.values[1]} = {p.values[7] - p.values[1]}')\
            .scale(0.8).center().next_to(range_7, RIGHT).shift(0.15 * LEFT)
        self.play(Write(range_1))
        self.wait()

        # The range query formula
        formula = MathTex(
            '\\mathrm{Sum} \\ [l, r] = p_r - p_{l - 1}'
        ).scale(0.8).center().next_to(range_2_7, DOWN).align_to(p_name, LEFT)
        self.play(Write(formula))
        self.wait()

        # Circumscribe the formula
        self.play(Circumscribe(formula), run_time=2)
        self.wait()

        self.play(
            FadeOut(range_2_7, range_1, range_7),
            formula.animate.scale(1.25).center().next_to(indices, DOWN),
        )
        self.wait()
        zero = MathTex('l = 0?').center().next_to(formula, DOWN)
        self.play(Write(zero))
        self.wait()

        # Add 0 at the beginning of p
        p.values.insert(0, 0)
        p.stroke_color = [WHITE, WHITE, YELLOW_A, WHITE, WHITE, WHITE, WHITE, WHITE, YELLOW, WHITE]
        p.stroke_width = [2, 2, 5, 2, 2, 2, 2, 2, 5, 2]
        new_p_mobj = p.get_mobject().next_to(p_name, RIGHT)
        new_indices = Array(
            [i for i in range(len(p))],
            width=p.width, height=p.height,
            spacing=p.spacing, scale_text=p.scale_text, stroke_color=BLACK,
        ).get_mobject().next_to(new_p_mobj, 0.0001 * DOWN)

        self.play(
            p_mobj.animate.become(new_p_mobj),
            indices.animate.become(new_indices),
            run_time=2
        )
        self.wait()

        # Update the formula
        new_formula = MathTex(
            '\\mathrm{Sum} \\ [l, r] = p_{r + 1} - p_{l}'
        ).center().next_to(indices, DOWN)
        self.play(
            formula.animate.become(new_formula),
            FadeOut(zero),
        )
        self.wait()

        # Transition to the next scene
        res_text = MathTex(
            '\\mathrm{Range \\ Sum } [l, r] = p_{r + 1} - p_{l}'
        ).center().next_to(array_mobj, UP).shift(0.5 * UP)
        self.play(
            text.animate.become(res_text),
            FadeOut(formula),
        )


class NewCode(Scene):
    def construct(self):
        values = [8, 3, -2, 4, 10, -1, 0, 5, 3]
        array = Array(values, width=0.8, height=0.8, spacing=0.05, scale_text=0.8)
        array.stroke_color = [YELLOW_A, YELLOW_A, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, YELLOW, WHITE]
        array.stroke_width = [5, 5, 5, 5, 5, 5, 5, 5, 2]
        array_mobj = array.get_mobject().center().move_to(1.2 * UP)
        p = Array(
            [sum(values[:i + 1]) for i in range(len(values))],
            width=array.width, height=array.height,
            spacing=array.spacing, scale_text=array.scale_text
        )
        p.values.insert(0, 0)
        p.stroke_color = [WHITE, WHITE, YELLOW_A, WHITE, WHITE, WHITE, WHITE, WHITE, YELLOW, WHITE]
        p.stroke_width = [2, 2, 5, 2, 2, 2, 2, 2, 5, 2]
        p_mobj = p.get_mobject().center().next_to(array_mobj, DOWN).align_to(array_mobj, LEFT)
        array_name = Text('a:').scale(0.8).move_to(array_mobj, LEFT).shift(0.7 * LEFT)
        p_name = Text('p:').scale(0.8).move_to(p_mobj, LEFT).shift(0.7 * LEFT)

        text = MathTex(
            '\\mathrm{Range \\ Sum } [l, r] = p_{r + 1} - p_{l}'
        ).center().next_to(array_mobj, UP).shift(0.5 * UP)
        # Add indices below the array
        indices = Array(
            [i for i in range(len(p))],
            width=array.width, height=array.height,
            spacing=array.spacing, scale_text=array.scale_text, stroke_color=BLACK,
        ).get_mobject().center().next_to(p_mobj, 0.0001 * DOWN).align_to(p_mobj, LEFT)
        self.add(text, indices, array_mobj, array_name, p_mobj, p_name)
        self.wait()

        code = Code(
            code=dedent('''
                p = [0] * (n + 1)
                for i in range(1, n + 1):
                    p[i] = p[i - 1] + a[i - 1]
            ''').strip(),
            tab_width=4,
            language='Python',
            line_spacing=0.6,
            font='Monospace',
            style='monokai',
        ).next_to(indices, DOWN).code
        for line in code.chars:
            self.play(AddTextLetterByLetter(line))
        self.wait()

        # The algorithm in action
        array.stroke_color = [WHITE] * len(array)
        array.stroke_width = [2] * len(array)
        p.values = [0] * len(p)
        p.stroke_color = [WHITE] * len(p)
        p.stroke_width = [2] * len(p)
        self.play(
            array_mobj.animate.become(array.get_mobject().center().move_to(1.2 * UP)),
            p_mobj.animate.become(p.get_mobject().center().next_to(array_mobj, DOWN).align_to(array_mobj, LEFT)),
            run_time=0.001
        )
        self.wait()

        def highlight_one(x):
            array.stroke_color = [WHITE] * (len(array))
            array.stroke_color[x - 1] = YELLOW
            array.stroke_width = [2] * (len(array))
            array.stroke_width[x - 1] = 5
            p.stroke_color = [WHITE] * len(p)
            p.stroke_color[x] = ORANGE
            p.stroke_width = [2] * len(p)
            p.stroke_width[x] = 5

            p.values[x] = p.values[x - 1] + values[x - 1]
            p.stroke_color[x - 1] = YELLOW
            p.stroke_width[x - 1] = 5
            self.play(
                array_mobj.animate.become(array.get_mobject().center().move_to(1.2 * UP)),
                p_mobj.animate.become(p.get_mobject().center().next_to(array_mobj, DOWN).align_to(array_mobj, LEFT)),
                run_time=0.001
            )

        for i in range(1, len(values) + 1):
            highlight_one(i)
            self.wait()

        # Queries
        def highlight_query(l, r, align=None):
            array.stroke_color = [WHITE] * (len(array))
            array.stroke_color[l:r + 1] = [YELLOW] * (r - l + 1)
            array.stroke_width = [2] * (len(array))
            p.stroke_color = [WHITE] * len(p)
            p.stroke_color[r + 1] = YELLOW
            p.stroke_color[l] = YELLOW_A
            p.stroke_width = [2] * len(p)
            p.stroke_width[r + 1] = 5
            p.stroke_width[l] = 5
            self.play(
                array_mobj.animate.become(array.get_mobject().center().move_to(1.2 * UP)),
                p_mobj.animate.become(p.get_mobject().center().next_to(array_mobj, DOWN).align_to(array_mobj, LEFT)),
                run_time=0.001
            )
            self.wait()

            query = MathTex(
                f'\\mathrm{{Sum}} [{l}, {r}] = p_{r + 1} - p_{r} = {p.values[r + 1] - p.values[l]}'
            ).scale(0.7)
            if align is None:
                query = query.next_to(code, RIGHT).align_to(code, UP).shift(0.5 * RIGHT)
            else:
                query = query.next_to(align, DOWN).align_to(align, LEFT)
            self.play(Write(query))
            self.wait()
            return query

        self.play(code.animate.shift(3 * LEFT))
        self.wait()

        # Highlight 2 -> 4
        range_2_4 = highlight_query(2, 4)
        range_5_8 = highlight_query(5, 8, range_2_4)
        range_0_2 = highlight_query(0, 2, range_5_8)
        range_0_0 = highlight_query(0, 0, range_0_2)
        self.play(Circumscribe(range_0_0))
        self.play(Circumscribe(range_0_2))
        self.play(Circumscribe(range_5_8))
        self.wait()

        # Time complexity is O(n + q), Memory complexity is O(n)
        time_complexity = MathTex(
            '\\mathrm{Time \\ Complexity}: \\mathcal{O}(n + q)'
        ).scale(0.7).align_to(code, LEFT + UP)
        memory_complexity = MathTex(
            '\\mathrm{Memory \\ Complexity}: \\mathcal{O}(n)'
        ).scale(0.7).next_to(time_complexity, DOWN).align_to(time_complexity, LEFT)

        # Remove the code
        self.play(FadeOut(code))
        self.wait()
        self.play(Circumscribe(p_mobj))                                                 # O(n) for the prefix sum array
        self.play(Circumscribe(VGroup(range_2_4, range_5_8, range_0_2, range_0_0)))     # O(q) for the queries
        self.play(Write(time_complexity))
        self.wait()

        # O(n) memory for the prefix sum array
        self.play(Circumscribe(p_mobj))
        self.play(Write(memory_complexity))
        self.wait()
