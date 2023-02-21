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
        array = Array([8, 3, -2, 4, 10, -1, 0, 5, 3]).get_mobject().center()
        text = Text('Video Score by Day').center().next_to(array, UP)
        self.play(
            FadeIn(array),
            FadeIn(text),
        )
        self.wait()
