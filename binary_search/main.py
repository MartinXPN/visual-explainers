from textwrap import dedent

from manim import *

from binary_search.array import Array
from binary_search.clock import Clock

a = [20, 22, 23, 23, 34, 49, 52, 55, 58]
ORANGE = ManimColor('#fa541c')


class ProblemStatement(Scene):
    def construct(self):
        title = Title('Find the Position of a Given Number', include_underline=False)
        self.play(Write(title, run_time=0.2))
        self.wait(0.1)

        array = Array(a, color=BLACK)
        array_mobj = array.get_mobject().center().shift(1.5 * UP)
        a_text = Tex('a:').scale(0.8).next_to(array_mobj, LEFT)

        indices = Array(
            [i for i in range(len(array))],
            width=array.width, height=array.height,
            spacing=array.spacing, scale_text=array.scale_text, stroke_color=BLACK,
        )
        indices_mobj = indices.get_mobject().center().next_to(array_mobj, 0.1 * UP)

        self.play(
            Create(array_mobj, run_time=0.5),
            Create(indices_mobj, run_time=0.5),
        )
        self.add(a_text)
        self.wait(0.1)

        q = Tex(r'q: 49', color=ORANGE).scale(0.8).next_to(array_mobj, 2 * DOWN).shift(DOWN)
        self.play(Write(q, run_time=0.5))

        search_svg = SVGMobject(
            'binary_search/search.svg', color=WHITE, fill_color=WHITE, fill_opacity=1,
        ).scale(0.7).move_to(q).shift(0.15 * DOWN).shift(0.45 * RIGHT)
        self.play(DrawBorderThenFill(search_svg, run_time=1))
        self.wait(0.1)

        # Loop from start to the index of 49 and move the search icon from element to element
        self.play(search_svg.animate.move_to(array.labels[0]).shift(0.16 * DOWN).shift(0.16 * RIGHT), run_time=0.5)
        self.play(array.labels[0].animate.set_color(WHITE), run_time=0.2)
        for i in range(5):
            self.play(
                search_svg.animate.shift((array.width + array.spacing) * RIGHT),
                array.labels[i + 1].animate.set_color(WHITE),
                array.labels[i].animate.set_color(BLACK),
                run_time=0.1,
            )

        # Hide search and circumscribe 49
        self.play(FadeOut(search_svg, run_time=0.5))
        self.play(Circumscribe(VGroup(array.rectangles[5], indices.rectangles[5]), run_time=0.5))

        # **** Linear Search ****
        # Move search to the start of the array
        search_svg.move_to(array.labels[0]).shift(0.16 * DOWN).shift(0.16 * RIGHT)

        # Loop from start to the index of 49 and move the search icon from element to element
        array.labels[5].set_color(BLACK)
        self.play(FadeIn(search_svg, run_time=0.2))
        self.play(array.labels[0].animate.set_color(WHITE), run_time=0.2)
        for i in range(5):
            self.play(
                search_svg.animate.shift((array.width + array.spacing) * RIGHT),
                array.labels[i + 1].animate.set_color(WHITE),
                array.labels[i].animate.set_color(BLACK),
                run_time=0.1,
            )

        self.play(FadeOut(search_svg, run_time=0.5))
        self.wait(0.1)

        # Add a green tick to the left of the array
        tick = SVGMobject(
            'binary_search/tick.svg', color=GREEN, fill_color=GREEN, fill_opacity=1,
        ).scale(0.2).next_to(a_text, LEFT)
        self.play(DrawBorderThenFill(tick, run_time=0.5))
        self.wait(0.1)

        # Add another long array
        long = Array([-7, -1, 3, 4, 6, 7, 10, 11, 15, 28, '...', 97], color=BLACK)
        long_mobj = long.get_mobject().next_to(array_mobj, DOWN).align_to(array_mobj, LEFT)
        long.rectangles[-2].set_color(BLACK)
        long.labels[-2].set_color(WHITE)
        self.play(Create(long_mobj, run_time=0.5))
        self.wait(0.1)

        # Animate the search icon moving from left to right on the long array
        search_svg.move_to(long.labels[0]).shift(0.16 * DOWN).shift(0.16 * RIGHT)
        self.play(FadeIn(search_svg, run_time=0.2))
        self.play(long.labels[0].animate.set_color(WHITE), run_time=0.2)
        for i in range(10):
            self.play(
                search_svg.animate.shift((long.width + long.spacing) * RIGHT),
                long.labels[i + 1].animate.set_color(WHITE),
                long.labels[i].animate.set_color(BLACK),
                run_time=0.1,
            )

        # Add a red cross near the long array
        cross = SVGMobject(
            'binary_search/cross.svg', color=RED, fill_color=RED, fill_opacity=1,
        ).scale(0.2).next_to(long_mobj, LEFT).align_to(tick, LEFT)
        self.play(DrawBorderThenFill(cross, run_time=0.5))
        self.play(FadeOut(search_svg, run_time=0.5))
        self.wait(0.1)

        self.play(
            FadeOut(tick),
            FadeOut(cross),
            FadeOut(long_mobj),
            run_time=0.5,
        )

        # Change the title to Binary search and make all the labels of the array WHITE
        self.play(
            Transform(title, Title('Binary Search', include_underline=False)),
            *[label.animate.set_color(WHITE) for label in array.labels],
            run_time=0.5,
        ),
        self.wait(0.1)


class BinarySearch(Scene):
    def construct(self):
        title = Title('Binary Search', include_underline=False)
        self.add(title)

        array = Array(a)
        array_mobj = array.get_mobject().center().shift(1.5 * UP)
        a_text = Tex('a:').scale(0.8).next_to(array_mobj, LEFT)

        indices = Array(
            [i for i in range(len(array))],
            width=array.width, height=array.height,
            spacing=array.spacing, scale_text=array.scale_text, stroke_color=BLACK,
        )
        indices_mobj = indices.get_mobject().center().next_to(array_mobj, 0.1 * UP)
        q = Tex(r'q: 49', color=ORANGE).scale(0.8).next_to(array_mobj, 2 * DOWN).shift(DOWN)

        self.add(array_mobj, indices_mobj, a_text, q)
        self.wait(0.1)

        # Circumscribe 2 halves of the array
        self.play(
            Circumscribe(VGroup(*array.rectangles[0:5]), color=RED, run_time=0.5),
            Circumscribe(VGroup(*array.rectangles[5:]), run_time=0.5),
        )

        def highlight(left, right, color, run_time=0.3):
            self.play(
                *[FadeToColor(label, color) for label in array.labels[left:right]],
                *[rect.animate.set_stroke(color) for rect in array.rectangles[left:right]],
                *[FadeToColor(label, color) for label in indices.labels[left:right]],
                run_time=run_time,
            )

        highlight(0, 5, DARKER_GREY)
        self.wait(0.1)
        highlight(0, 5, WHITE)
        self.wait(0.1)

        # Highlight the middle element (index = 4)
        highlight(4, 5, ORANGE)
        self.play(Circumscribe(VGroup(array.rectangles[4], indices.rectangles[4]), run_time=0.2))
        self.wait(0.1)

        highlight(0, 5, DARKER_GREY)
        self.wait(0.1)

        # Highlight the current middle element (52 at index 6)
        highlight(6, 7, ORANGE)
        self.play(Circumscribe(VGroup(array.rectangles[6], indices.rectangles[6]), run_time=0.2))
        self.wait(0.1)

        highlight(6, 9, DARKER_GREY)
        self.wait(0.1)

        # Highlight the middle element (index = 5)
        highlight(5, 6, ORANGE)
        self.play(Circumscribe(VGroup(array.rectangles[5], indices.rectangles[5]), run_time=0.2))
        self.wait(0.1)

        self.play(Flash(
            array.rectangles[5], num_lines=15, flash_radius=0.7, line_length=0.3, run_time=0.2, rate_func=rush_from,
        ))
        self.wait(0.1)

        # undim the whole array
        self.play(FadeOut(q), run_time=0.2)
        highlight(0, 9, WHITE)
        self.wait(0.1)

        self.play(Circumscribe(VGroup(*array.rectangles[0:5]), run_time=0.5))
        self.play(Circumscribe(VGroup(*array.rectangles[5:]), run_time=0.5))

        highlight(0, 5, DARKER_GREY)
        self.wait(0.1)
        self.play(Circumscribe(VGroup(*array.rectangles[5:7]), run_time=0.5))
        self.play(Circumscribe(VGroup(*array.rectangles[7:]), run_time=0.5))
        self.wait(0.1)

        highlight(7, 9, DARKER_GREY)

        # Transition to the next scene
        long = Array([-7, -1, 3, 4, 6, 7, 10, 11, 15, 28, 33, '...'])
        long_mobj = long.get_mobject().align_to(array_mobj, DOWN).align_to(array_mobj, LEFT)
        long.rectangles[-1].set_color(BLACK)
        self.play(
            ReplacementTransform(array_mobj, long_mobj),
            FadeOut(indices_mobj),
            run_time=0.5,
        )

        another_arr = Array(long.values, color=BLACK).get_mobject().center().align_to(long_mobj, DOWN).shift(0.5 * UP)

        # Center horizontally the new array (make sure the label a: stays on the left)
        self.play(
            long_mobj.animate.align_to(another_arr, LEFT).align_to(another_arr, UP),
            a_text.animate.next_to(another_arr, LEFT),
            run_time=0.5,
        )
        self.wait(0.1)


class TimeComplexity(Scene):
    def construct(self):
        title = Title('Binary Search', include_underline=False)
        self.add(title)

        array = Array([-7, -1, 3, 4, 6, 7, 10, 11, 15, 28, 33, '...'])
        array_mobj = array.get_mobject().center().shift(2 * UP)
        array.rectangles[-1].set_color(BLACK)
        a_text = Tex('a:').scale(0.8).next_to(array_mobj, LEFT)
        self.add(array_mobj, a_text)

        # Add a brace between the first and last element of the long array + Wright 10,000,000,000 at the bottom
        brace = Brace(VGroup(array.rectangles[0], array.rectangles[-1]), buff=0.1, direction=DOWN)
        brace_text = brace.get_text('10,000,000,000').scale(0.7).shift(0.15 * UP)
        self.play(
            GrowFromCenter(brace),
            Write(brace_text),
            run_time=0.5,
        )

        search_svg = SVGMobject(
            'binary_search/search.svg', color=WHITE, fill_color=WHITE, fill_opacity=1,
        ).scale(0.7).center()
        self.play(DrawBorderThenFill(search_svg, run_time=1))
        self.wait(0.1)

        # Animate the search icon moving from left to right on the long array
        self.play(search_svg.animate.move_to(array.labels[0]).shift(0.16 * DOWN).shift(0.16 * RIGHT), run_time=0.5)
        for i in range(11):
            self.play(search_svg.animate.shift((array.width + array.spacing) * RIGHT), run_time=0.1)
        self.wait(0.1)

        # Indicate the brace text
        self.play(Indicate(brace_text, run_time=0.5))
        self.wait(0.1)
        self.play(FadeOut(search_svg, run_time=0.5))

        # Split the screen in 2 parts
        linear_search_text = Text('Linear Search', color=WHITE).scale(0.8).next_to(brace, DOWN, buff=1).shift(4 * LEFT)
        binary_search_text = Text('Binary Search', color=WHITE).scale(0.8).next_to(brace, DOWN, buff=1).shift(4 * RIGHT)
        linear_search_nb_operations = Text('10,000,000,000', color=ORANGE).scale(0.5).next_to(linear_search_text, DOWN, buff=0.5)

        self.play(
            Write(linear_search_text),
            Write(binary_search_text),
            Write(linear_search_nb_operations),
            run_time=0.5,
        )
        self.wait(0.1)

        # Write another 10 billion under binary search with white
        bin_search_operations = [
            Text('10,000,000,000', color=WHITE).scale(0.5).next_to(binary_search_text, DOWN, buff=0.5),
        ]
        self.play(Write(bin_search_operations[-1], run_time=0.2))
        self.wait(0.1)

        bin_search_operations.append(
            Text('5,000,000,000', color=WHITE).scale(0.5).next_to(bin_search_operations[-1], DOWN, buff=0.2),
        )
        self.play(Write(bin_search_operations[-1], run_time=0.2))
        self.wait(0.1)

        bin_search_operations.append(
            Text('2,500,000,000', color=WHITE).scale(0.5).next_to(bin_search_operations[-1], DOWN, buff=0.2),
        )
        self.play(Write(bin_search_operations[-1], run_time=0.2))
        self.wait(0.1)

        bin_search_operations.append(
            Text('1,250,000,000', color=WHITE).scale(0.5).next_to(bin_search_operations[-1], DOWN, buff=0.2),
        )
        self.play(Write(bin_search_operations[-1], run_time=0.2))
        self.wait(0.1)

        bin_search_operations.append(
            Text('...', color=WHITE).scale(0.5).next_to(bin_search_operations[-1], DOWN, buff=0.3),
        )
        self.play(Write(bin_search_operations[-1], run_time=0.2))
        self.wait(0.1)

        bin_search_operations.append(
            Text('1', color=WHITE).scale(0.5).next_to(bin_search_operations[-1], DOWN, buff=0.3),
        )
        self.play(Write(bin_search_operations[-1], run_time=0.2))
        self.wait(0.1)

        bin_search_operations_brace = Brace(
            VGroup(bin_search_operations[0], bin_search_operations[-1]),
            buff=0.1,
            direction=RIGHT,
        )
        bin_search_operations_brace_text = bin_search_operations_brace.get_text('32').scale(0.7).shift(0.15 * LEFT).set_color(ORANGE)
        self.play(
            GrowFromCenter(bin_search_operations_brace),
            Write(bin_search_operations_brace_text),
            run_time=0.5,
        )
        self.wait(0.1)

        # Draw a clock
        clock = Clock(hh=3, mh=30).scale(0.2).shift(2 * DOWN)
        self.play(DrawBorderThenFill(clock, run_time=0.5))
        self.wait(0.1)

        clock.add_updaters()
        self.play(
            clock.ht.animate.set_value(10),
            run_time=2,
            rate_func=linear,
        )
        self.wait(0.1)

        skeleton = ImageMobject('binary_search/skeleton.webp').scale(0.3).next_to(linear_search_nb_operations, DOWN, buff=0.2)
        linear_search_nb_yars = Text('317 Years', color=WHITE, weight=BOLD).scale(0.5).next_to(skeleton, DOWN, buff=-0.2)
        self.play(
            clock.ht.animate.set_value(15),
            FadeIn(skeleton),
            Write(linear_search_nb_yars),
            run_time=1,
            rate_func=linear,
        )
        self.wait(0.1)

        self.play(FadeOut(clock), run_time=0.5)
        self.wait(0.1)

        # Remove all the numbers for the binary search and move 32 to the top (below the binary search title)
        self.play(
            *[FadeOut(operation) for operation in bin_search_operations],
            FadeOut(bin_search_operations_brace),
            bin_search_operations_brace_text.animate.next_to(binary_search_text, DOWN, buff=0.5),
            run_time=0.2,
        )
        self.wait(0.1)

        fast = ImageMobject('binary_search/fast.webp').scale(0.3).next_to(bin_search_operations_brace_text, DOWN, buff=0.2)
        bin_search_nb_seconds = Text('32 Seconds', color=WHITE, weight=BOLD).scale(0.5).next_to(fast, DOWN, buff=-0.2)
        self.play(
            FadeIn(fast),
            Write(bin_search_nb_seconds),
            run_time=0.5,
        )
        self.wait(0.1)

        # Clear the images and bring back the binary search operations
        self.play(
            FadeOut(skeleton),
            FadeOut(linear_search_nb_yars),
            FadeOut(fast),
            FadeOut(bin_search_nb_seconds),
            bin_search_operations_brace_text.animate.next_to(bin_search_operations_brace, RIGHT).shift(0.15 * LEFT),
            *[Write(operation) for operation in bin_search_operations],
            FadeIn(bin_search_operations_brace),
            run_time=0.5,
        )
        self.wait(0.1)

        # Replace 10 billion with 20 billion
        self.play(
            Transform(brace_text, brace.get_text('20,000,000,000').scale(0.7).shift(0.15 * UP)),
            run_time=0.2,
        )
        self.wait(0.1)

        # Remove char-by-char 10 billion of linear search and replace it with 20 billion
        self.play(RemoveTextLetterByLetter(linear_search_nb_operations, keep_final_state=True, run_time=0.5))
        linear_search_nb_operations = Text('20,000,000,000', color=ORANGE).scale(0.5).next_to(linear_search_text, DOWN, buff=0.5)
        self.play(AddTextLetterByLetter(linear_search_nb_operations, run_time=0.5))

        # Add 634 years under the linear search
        linear_search_nb_yars = Text('634 Years', color=WHITE, weight=BOLD).scale(0.5).next_to(linear_search_nb_operations, DOWN, buff=0.5)
        self.play(Write(linear_search_nb_yars), run_time=0.5)

        # Shift all the binary search operations down and add 20 billion at the top
        self.play(
            *[operation.animate.shift(0.5 * DOWN) for operation in bin_search_operations],
            bin_search_operations_brace_text.animate.shift(0.5 * DOWN),
            bin_search_operations_brace.animate.shift(0.5 * DOWN),
            run_time=0.5,
        )
        self.wait(0.1)

        bin_search_operations.insert(0, Text('20,000,000,000', color=WHITE).scale(0.5).next_to(binary_search_text, DOWN, buff=0.5))
        self.play(Write(bin_search_operations[0]), run_time=0.2)
        # The brace should include the 20 billion and 1
        new_bin_search_operations_brace = Brace(
            VGroup(bin_search_operations[0], bin_search_operations[-1]),
            buff=0.1,
            direction=RIGHT,
        )
        new_bin_search_operations_brace_text = new_bin_search_operations_brace.get_text('33').scale(0.7).shift(0.15 * LEFT).set_color(ORANGE)
        self.play(
            ReplacementTransform(bin_search_operations_brace, new_bin_search_operations_brace),
            ReplacementTransform(bin_search_operations_brace_text, new_bin_search_operations_brace_text),
            run_time=0.5,
        )
        self.wait(0.1)

        # Transition to the next scene
        self.play(
            FadeOut(linear_search_nb_operations),
            FadeOut(linear_search_nb_yars),
            ReplacementTransform(brace_text, brace.get_text('n').scale(0.7).shift(0.15 * UP)),
            ReplacementTransform(title, Title('Time Complexity', include_underline=False)),
            *[FadeOut(op) for op in bin_search_operations],
            FadeOut(new_bin_search_operations_brace),
            FadeOut(new_bin_search_operations_brace_text),
            run_time=0.5,
        )
        self.wait(0.1)


class FormalTimeComplexity(Scene):
    def construct(self):
        title = Title('Time Complexity', include_underline=False)
        self.add(title)

        array = Array([-7, -1, 3, 4, 6, 7, 10, 11, 15, 28, 33, '...'])
        array_mobj = array.get_mobject().center().shift(2 * UP)
        array.rectangles[-1].set_color(BLACK)
        a_text = Tex('a:').scale(0.8).next_to(array_mobj, LEFT)

        # Add a brace between the first and last element of the long array + Wright 10,000,000,000 at the bottom
        brace = Brace(VGroup(array.rectangles[0], array.rectangles[-1]), buff=0.1, direction=DOWN)
        brace_text = brace.get_text('n').scale(0.7).shift(0.15 * UP)

        # Add linear VS bin-search
        linear_search_text = Text('Linear Search', color=WHITE).scale(0.8).next_to(brace, DOWN, buff=1).shift(4 * LEFT)
        binary_search_text = Text('Binary Search', color=WHITE).scale(0.8).next_to(brace, DOWN, buff=1).shift(4 * RIGHT)

        self.add(array_mobj, a_text, brace, brace_text, linear_search_text, binary_search_text)

