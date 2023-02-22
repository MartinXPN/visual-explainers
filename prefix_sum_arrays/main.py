import random

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
        bar = Rectangle(width=6, height=0.5)
        bar.next_to(text, DOWN)

        # Group the logo, text and progress bar + Center the group
        group = VGroup(logo, text, bar)
        group.center()

        # Animate the progress bar
        progress = ValueTracker(0)

        # Add filler to the progress bar
        def get_filler():
            fill = Rectangle(width=progress.get_value(), height=0.5, fill_color=GREEN, fill_opacity=1)
            fill.set_stroke(width=0)
            fill.align_to(bar, DOWN)
            fill.align_to(bar, LEFT)
            return fill
        filler = always_redraw(get_filler)
        bar.add(filler)

        self.add(logo, text, bar)
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
            [i for i in range(9)],
            width=array.width, height=array.height,
            spacing=array.spacing, scale_text=array.scale_text, stroke_color=BLACK,
        ).get_mobject().center().next_to(array_mobj, 0.0001 * DOWN)

        text = Text('Video Score By Day').center().next_to(array_mobj, UP)
        self.add(logo, text, indices, array_mobj)

        def get_reactions(nb_likes: int, nb_dislikes: int):
            likes = [
                SVGMobject('prefix_sum_arrays/like.svg', color=WHITE, fill_color=WHITE, fill_opacity=1).scale(0.2)
                for _ in range(nb_likes)
            ]
            dislikes = [
                SVGMobject('prefix_sum_arrays/dislike.svg', color=RED, fill_color=RED, fill_opacity=1).scale(0.2)
                for _ in range(nb_dislikes)
            ]
            res = likes + dislikes
            # Move likes to a random position
            for reaction in res:
                left = random.uniform(-4, 4)
                down = random.uniform(1.5, 3.5)
                reaction.move_to(left * LEFT + down * DOWN)
            return res

        # Animate the array: When adding each value animate the number of likes and dislikes
        values = [8,    3, -2, 4, 10, -1, 0, 5, 3]
        upvotes = [8,   3,  2, 4, 10,  0, 2, 7, 3]
        downvotes = [0, 0,  4, 0,  0,  1, 2, 2, 0]

        # On the day of uploading the video it got 8 likes, so we add 8 to day 0
        for i, val in enumerate(values):
            # Add the reactions
            reactions = get_reactions(upvotes[i], downvotes[i])
            if len(reactions) > 0 and i < 4:
                self.play(*[DrawBorderThenFill(reaction, run_time=random.uniform(0.01, 4)) for reaction in reactions])

            # Increase the value up to the number of upvotes and then decrease it by the number of downvotes
            for diff in range(1, upvotes[i] + 1):
                array.values[i] = diff
                self.play(array_mobj.animate.become(array.get_mobject().center()), run_time=0.001)
                self.wait(0.1)
            for diff in range(1, downvotes[i] + 1):
                array.values[i] = upvotes[i] - diff
                self.play(array_mobj.animate.become(array.get_mobject().center()), run_time=0.001)
                self.wait(0.1)

            # Fade out the reactions
            if len(reactions) > 0 and i < 4:
                self.play(*[FadeOut(reaction, run_time=random.uniform(0.001, 1)) for reaction in reactions])
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
            [i for i in range(9)],
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
        total = Text('Sum: 0').center().next_to(array_mobj, DOWN).scale(0.8).shift(1.5 * DOWN)
        arrow.shift(0.8 * 4 * LEFT).set_color(YELLOW)
        self.play(Write(total))
        self.play(
            DrawBorderThenFill(arrow),
            total.animate.become(
                Text(f'Sum: {values[start]}').center().next_to(array_mobj, DOWN).scale(0.8).shift(1.5 * DOWN)
            ),
        )
        for i in range(start + 1, end + 1):
            self.play(
                arrow.animate.shift(array.width * RIGHT),
                total.animate.become(Text(f'Sum: {sum(values[start:i + 1])}')
                                     .center().next_to(array_mobj, DOWN)
                                     .scale(0.8).shift(1.5 * DOWN)),
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
            total.animate.become(Text('Sum: 0')).center().next_to(array_mobj, DOWN).scale(0.8).shift(1.5 * DOWN),
            run_time=0.001
        )
        self.wait(2)
        self.play(
            DrawBorderThenFill(arrow),
            total.animate.become(
                Text(f'Sum: {values[start]}').center().next_to(array_mobj, DOWN).scale(0.8).shift(1.5 * DOWN)
            )
        )

        for i in range(start + 1, end + 1):
            self.play(
                arrow.animate.shift(array.width * RIGHT),
                total.animate.become(Text(f'Sum: {sum(values[start:i + 1])}')
                                     .center().next_to(array_mobj, DOWN)
                                     .scale(0.8).shift(1.5 * DOWN)),
                run_time=0.5,
            )
        self.wait(2)
