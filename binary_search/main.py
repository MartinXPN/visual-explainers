import random
from textwrap import dedent

from manim import *

from binary_search.array import Array, TransformMatchingCells
from binary_search.clock import Clock

a = [20, 22, 23, 23, 34, 49, 52, 55, 58]
ORANGE = ManimColor('#fa541c')


class ProblemStatement(Scene):
    def construct(self):
        title = Title('Find the Position of a Given Number', include_underline=False)

        array = Array(a, color=BLACK)
        array_mobj = array.get_mobject().center().shift(1.5 * UP)
        a_text = Tex('a:').scale(0.8).next_to(array_mobj, LEFT)

        indices = Array(
            [i for i in range(len(array))],
            width=array.width, height=array.height,
            spacing=array.spacing, scale_text=array.scale_text, stroke_color=BLACK,
        )
        indices_mobj = indices.get_mobject().center().next_to(array_mobj, 0.1 * UP)

        self.add(a_text)
        self.play(
            Create(array_mobj, run_time=2),
            Create(indices_mobj, run_time=2),
        )
        self.wait(3)

        q = Tex(r'q: 49', color=ORANGE).scale(0.8).next_to(array_mobj, 2 * DOWN).shift(DOWN)
        self.play(Write(q, run_time=1))

        self.play(Write(title, run_time=0.5))
        search_svg = SVGMobject(
            'binary_search/search.svg', color=ORANGE, fill_color=ORANGE, fill_opacity=0.9,
        ).scale(0.7).move_to(q).shift(0.15 * DOWN).shift(0.45 * RIGHT)
        self.play(DrawBorderThenFill(search_svg, run_time=1))

        # Loop from start to the index of 49 and move the search icon from element to element
        self.play(search_svg.animate.move_to(array.labels[0]).shift(0.16 * DOWN).shift(0.16 * RIGHT), run_time=0.5)
        self.play(array.labels[0].animate.set_color(WHITE), run_time=0.1)
        for i in range(5):
            self.play(
                search_svg.animate.shift((array.width + array.spacing) * RIGHT),
                array.labels[i + 1].animate.set_color(WHITE),
                array.labels[i].animate.set_color(BLACK),
                run_time=0.1,
            )
            self.wait(0.06)

        # Hide search and circumscribe 49
        self.play(FadeOut(search_svg, run_time=0.5))
        self.play(Circumscribe(VGroup(array.rectangles[5], indices.rectangles[5]), run_time=0.5))
        self.wait(1)

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
                run_time=0.2,
            )
            self.wait(0.1)

        self.play(FadeOut(search_svg, run_time=0.5))
        self.play(Indicate(indices.labels[5], run_time=1))
        self.wait(2)

        # Add a green tick to the left of the array
        tick = SVGMobject(
            'binary_search/tick.svg', color=GREEN, fill_color=GREEN, fill_opacity=1,
        ).scale(0.2).next_to(a_text, LEFT)
        self.play(DrawBorderThenFill(tick, run_time=0.5))
        self.wait(1.5)

        # Add another long array
        long = Array([-7, -1, 3, 4, 6, 7, 10, 11, 15, 28, '...', 97], color=BLACK)
        long_mobj = long.get_mobject().next_to(array_mobj, DOWN).align_to(array_mobj, LEFT)
        long.rectangles[-2].set_color(BLACK)
        long.labels[-2].set_color(WHITE)
        self.play(Create(long_mobj, run_time=0.5))
        self.wait(0.5)

        # Animate the search icon moving from left to right on the long array
        search_svg.move_to(long.labels[0]).shift(0.16 * DOWN).shift(0.16 * RIGHT)
        self.play(FadeIn(search_svg, run_time=0.2))
        self.play(long.labels[0].animate.set_color(WHITE), run_time=0.2)
        for i in range(10):
            self.play(
                search_svg.animate.shift((long.width + long.spacing) * RIGHT),
                long.labels[i + 1].animate.set_color(WHITE),
                long.labels[i].animate.set_color(BLACK),
                run_time=0.06,
            )
            self.wait(0.1)

        # Add a red cross near the long array
        cross = SVGMobject(
            'binary_search/cross.svg', color=RED, fill_color=RED, fill_opacity=1,
        ).scale(0.2).next_to(long_mobj, LEFT).align_to(tick, LEFT)
        self.play(DrawBorderThenFill(cross, run_time=0.5), FadeOut(search_svg, run_time=0.5))
        self.wait(1)

        self.play(
            FadeOut(tick),
            FadeOut(cross),
            FadeOut(long_mobj),
            run_time=0.2,
        )

        # Change the title to Binary search and make all the labels of the array WHITE
        self.play(
            Transform(title, Title('Binary Search', include_underline=False)),
            *[label.animate.set_color(WHITE) for label in array.labels],
            run_time=0.5,
        )
        self.wait(0.2)


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
        self.wait(2)

        # Circumscribe 2 halves of the array
        self.play(
            Circumscribe(VGroup(*array.rectangles[0:5]), color=RED, run_time=2),
            Circumscribe(VGroup(*array.rectangles[5:]), run_time=2),
        )
        self.wait(1)

        def highlight(left, right, color, run_time=0.3):
            self.play(
                *[FadeToColor(label, color) for label in array.labels[left:right]],
                *[rect.animate.set_stroke(color) for rect in array.rectangles[left:right]],
                *[FadeToColor(label, color) for label in indices.labels[left:right]],
                run_time=run_time,
            )

        highlight(0, 5, DARKER_GREY)
        self.wait(2)
        highlight(0, 5, WHITE)
        self.wait(1)

        # Highlight the middle element (index = 4)
        highlight(4, 5, ORANGE)
        self.play(Circumscribe(VGroup(array.rectangles[4], indices.rectangles[4]), run_time=0.5))
        self.wait(1)
        self.play(Indicate(q))
        self.wait(4)

        highlight(0, 5, DARKER_GREY, run_time=0.5)
        self.wait(2.5)

        self.play(Indicate(q))
        self.wait(4)

        # Highlight the current middle element (52 at index 6)
        highlight(6, 7, ORANGE)
        self.play(Circumscribe(VGroup(array.rectangles[6], indices.rectangles[6]), run_time=1))
        self.wait(2)

        self.play(Indicate(q))
        self.wait(2)

        highlight(6, 9, DARKER_GREY, run_time=0.5)
        self.wait(6)

        # Highlight the middle element (index = 5)
        highlight(5, 6, ORANGE)
        self.play(Circumscribe(VGroup(array.rectangles[5], indices.rectangles[5]), run_time=1))
        self.wait(2.5)

        self.play(Flash(
            array.rectangles[5], num_lines=15, flash_radius=0.7, line_length=0.3, run_time=1, rate_func=rush_from,
        ))
        self.wait(5)

        # undim the whole array
        self.play(FadeOut(q), run_time=0.5)
        highlight(0, 9, WHITE)
        self.wait(2)

        self.play(Circumscribe(VGroup(*array.rectangles[0:5]), run_time=1))
        self.play(Circumscribe(VGroup(*array.rectangles[5:]), run_time=1))
        self.wait(1)

        highlight(0, 5, DARKER_GREY, run_time=0.5)
        self.wait(0.5)
        self.play(Circumscribe(VGroup(*array.rectangles[5:7]), run_time=1))
        self.play(Circumscribe(VGroup(*array.rectangles[7:]), run_time=1))
        self.wait(1)

        highlight(7, 9, DARKER_GREY, run_time=0.5)
        self.wait(2)

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
            run_time=1,
        )
        self.wait(0.2)


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
        self.wait(2)

        search_svg = SVGMobject(
            'binary_search/search.svg', color=ORANGE, fill_color=ORANGE, fill_opacity=0.9,
        ).scale(0.7).center()
        self.play(DrawBorderThenFill(search_svg, run_time=0.5))

        # Animate the search icon moving from left to right on the long array
        self.play(search_svg.animate.move_to(array.labels[0]).shift(0.16 * DOWN).shift(0.16 * RIGHT), run_time=0.5)
        for i in range(11):
            self.play(search_svg.animate.shift((array.width + array.spacing) * RIGHT), run_time=0.1)
            self.wait(0.2)

        # Indicate the brace text
        self.play(Indicate(brace_text))
        self.wait(0.5)
        self.play(FadeOut(search_svg, run_time=0.5))

        # Split the screen in 2 parts
        linear_search_text = Text('Linear Search', color=WHITE).scale(0.8).next_to(brace, DOWN, buff=1).shift(4 * LEFT)
        binary_search_text = Text('Binary Search', color=WHITE).scale(0.8).next_to(brace, DOWN, buff=1).shift(4 * RIGHT)
        linear_search_nb_operations = Text('10,000,000,000', color=ORANGE).scale(0.5).next_to(linear_search_text, DOWN, buff=0.5)

        self.play(
            Write(linear_search_text),
            Write(linear_search_nb_operations),
            run_time=1,
        )
        self.play(
            Write(binary_search_text),
            run_time=1,
        )
        self.wait(5)

        # Write another 10 billion under binary search with white
        bin_search_operations = [
            Text('10,000,000,000', color=WHITE).scale(0.5).next_to(binary_search_text, DOWN, buff=0.5),
        ]
        self.play(Write(bin_search_operations[-1], run_time=0.5))
        self.wait(1)

        bin_search_operations.append(
            Text('5,000,000,000', color=WHITE).scale(0.5).next_to(bin_search_operations[-1], DOWN, buff=0.2),
        )
        self.play(Write(bin_search_operations[-1], run_time=0.5))
        self.wait(3)

        bin_search_operations.append(
            Text('2,500,000,000', color=WHITE).scale(0.5).next_to(bin_search_operations[-1], DOWN, buff=0.2),
        )
        self.play(Write(bin_search_operations[-1], run_time=0.5))
        self.wait(0.5)

        bin_search_operations.append(
            Text('1,250,000,000', color=WHITE).scale(0.5).next_to(bin_search_operations[-1], DOWN, buff=0.2),
        )
        self.play(Write(bin_search_operations[-1], run_time=0.5))
        self.wait(0.5)

        bin_search_operations.append(
            Text('...', color=WHITE).scale(0.5).next_to(bin_search_operations[-1], DOWN, buff=0.3),
        )
        self.play(Write(bin_search_operations[-1], run_time=0.5))

        bin_search_operations.append(
            Text('1', color=WHITE).scale(0.5).next_to(bin_search_operations[-1], DOWN, buff=0.3),
        )
        self.play(Write(bin_search_operations[-1], run_time=0.5))
        self.wait(1)

        bin_search_operations_brace = Brace(
            VGroup(bin_search_operations[0], bin_search_operations[-1]),
            buff=0.1,
            direction=RIGHT,
        )
        bin_search_operations_brace_text = bin_search_operations_brace.get_text('32').scale(0.7).shift(0.15 * LEFT).set_color(ORANGE)
        self.play(GrowFromCenter(bin_search_operations_brace), run_time=1)
        self.wait(0.5)
        self.play(Write(bin_search_operations_brace_text), run_time=0.5)
        self.wait(3)

        # Draw a clock
        clock = Clock(hh=3, mh=30).scale(0.2).shift(2 * DOWN)
        self.play(DrawBorderThenFill(clock, run_time=0.5))
        self.wait(3)

        clock.add_updaters()
        self.play(clock.ht.animate.set_value(10), run_time=5, rate_func=linear)

        skeleton = ImageMobject('binary_search/skeleton.webp').scale(0.3).next_to(linear_search_nb_operations, DOWN, buff=0.2)
        linear_search_nb_yars = Text('317 Years', color=WHITE, weight=BOLD).scale(0.5).next_to(skeleton, DOWN, buff=-0.2)
        self.play(
            clock.ht.animate.set_value(15),
            FadeIn(skeleton),
            Write(linear_search_nb_yars),
            run_time=2,
            rate_func=linear,
        )
        self.play(clock.ht.animate.set_value(30), run_time=3, rate_func=linear)
        self.play(FadeOut(clock), run_time=0.5)

        # Remove all the numbers for the binary search and move 32 to the top (below the binary search title)
        self.play(
            *[FadeOut(operation) for operation in bin_search_operations],
            FadeOut(bin_search_operations_brace),
            bin_search_operations_brace_text.animate.next_to(binary_search_text, DOWN, buff=0.5),
            run_time=0.5,
        )

        fast = ImageMobject('binary_search/fast.webp').scale(0.3).next_to(bin_search_operations_brace_text, DOWN, buff=0.2)
        bin_search_nb_seconds = Text('32 Seconds', color=WHITE, weight=BOLD).scale(0.5).next_to(fast, DOWN, buff=-0.2)
        self.play(
            FadeIn(fast),
            Write(bin_search_nb_seconds),
            run_time=0.5,
        )
        self.wait(3)

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
        self.wait(2)

        # Replace 10 billion with 20 billion
        self.play(Indicate(brace_text))
        new_brace_text = brace.get_text('20,000,000,000').scale(0.7).shift(0.15 * UP)
        self.play(ReplacementTransform(brace_text, new_brace_text), run_time=0.5)
        self.play(Indicate(new_brace_text))
        self.wait(3)

        # Remove char-by-char 10 billion of linear search and replace it with 20 billion
        self.play(RemoveTextLetterByLetter(linear_search_nb_operations, keep_final_state=True, run_time=0.5))
        linear_search_nb_operations = Text('20,000,000,000', color=ORANGE).scale(0.5).next_to(linear_search_text, DOWN, buff=0.5)
        self.play(AddTextLetterByLetter(linear_search_nb_operations, run_time=1))

        # Add 634 years under the linear search
        linear_search_nb_yars = Text('634 Years', color=WHITE, weight=BOLD).scale(0.5).next_to(linear_search_nb_operations, DOWN, buff=0.5)
        self.play(Write(linear_search_nb_yars), run_time=0.5)
        self.wait(2.5)

        # Shift all the binary search operations down and add 20 billion at the top
        self.play(
            *[operation.animate.shift(0.5 * DOWN) for operation in bin_search_operations],
            bin_search_operations_brace_text.animate.shift(0.5 * DOWN),
            bin_search_operations_brace.animate.shift(0.5 * DOWN),
            run_time=0.5,
        )
        self.wait(0.2)

        bin_search_operations.insert(0, Text('20,000,000,000', color=WHITE).scale(0.5).next_to(binary_search_text, DOWN, buff=0.5))
        self.play(Write(bin_search_operations[0]), run_time=0.2)
        self.wait(3)
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
        self.wait(3)

        # Transition to the next scene
        self.play(ReplacementTransform(new_brace_text, brace.get_text('n').scale(0.7).shift(0.15 * UP)), run_time=0.5)
        self.play(
            FadeOut(linear_search_nb_operations, linear_search_nb_yars),
            FadeOut(*bin_search_operations),
            FadeOut(new_bin_search_operations_brace, new_bin_search_operations_brace_text),
            run_time=0.5,
        )

        self.play(ReplacementTransform(title, Title('Time Complexity', include_underline=False)), run_time=0.5)
        self.wait(1)


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
        self.wait(3.5)

        # Search icon goes from first to last
        search_svg = SVGMobject(
            'binary_search/search.svg', color=ORANGE, fill_color=ORANGE, fill_opacity=0.9,
        ).scale(0.7).center()
        self.play(DrawBorderThenFill(search_svg, run_time=1))

        self.play(search_svg.animate.move_to(array.labels[0]).shift(0.16 * DOWN).shift(0.16 * RIGHT), run_time=0.2)
        for i in range(11):
            self.play(search_svg.animate.shift((array.width + array.spacing) * RIGHT), run_time=0.1)
            self.wait(0.1)

        # Write O(n)a
        linear_search_time_complexity = MathTex(
            r'\mathcal{O}(n)', color=ORANGE,
        ).scale(0.8).next_to(linear_search_text, DOWN, buff=0.5)
        self.play(FadeOut(search_svg, run_time=0.5))
        self.play(Write(linear_search_time_complexity, run_time=1))
        self.wait(3)

        # Add n/2, n/4, n/8, ... below n
        divisors = [Tex(f'n / {i}').scale(0.7).set_color(YELLOW) for i in [2, 4, 8]] + [Tex('...').scale(0.7).set_color(YELLOW)]
        divisors[0].next_to(brace_text, DOWN, buff=0.2)
        self.play(brace_text.animate.set_color(YELLOW), run_time=0.5)
        self.wait(0.6)
        self.play(Write(divisors[0]), run_time=0.5)
        self.wait(0.6)
        for i in range(1, len(divisors)):
            divisors[i].next_to(divisors[i - 1], DOWN, buff=0.2)
            self.play(Write(divisors[i]), run_time=0.5)
            self.wait(0.6)

        # Add O(log n) below binary search
        binary_search_time_complexity = MathTex(
            r'\mathcal{O}(\log{n})', color=ORANGE,
        ).scale(0.8).next_to(binary_search_text, DOWN, buff=0.5)
        self.play(Write(binary_search_time_complexity), run_time=1)
        self.wait(2)

        # Transition to the next scene
        self.play(
            FadeOut(brace, brace_text),
            FadeOut(linear_search_time_complexity, binary_search_time_complexity),
            FadeOut(*divisors),
            run_time=0.5,
        )
        self.wait(1)
        new_arr = Array(a).get_mobject().center().shift(2 * UP)
        indices = Array(
            [i for i in range(len(a))],
            width=array.width, height=array.height,
            spacing=array.spacing, scale_text=array.scale_text, stroke_color=BLACK,
        )
        indices_mobj = indices.get_mobject().center().next_to(new_arr, 0.1 * DOWN)

        self.play(
            ReplacementTransform(title, Title('Binary Search', include_underline=False)),
            ReplacementTransform(array_mobj, new_arr),
            Create(indices_mobj),
            ReplacementTransform(a_text, Tex('a:').scale(0.8).next_to(new_arr, LEFT)),
            FadeOut(linear_search_text),
            FadeOut(binary_search_text),
        )
        self.wait(1)


class Implementation(Scene):
    def construct(self):
        title = Title('Binary Search', include_underline=False)
        self.add(title)

        array = Array(a)
        array_mobj = array.get_mobject().center().shift(2 * UP)
        a_text = Tex('a:').scale(0.8).next_to(array_mobj, LEFT)
        indices = Array(
            [i for i in range(len(array))],
            width=array.width, height=array.height,
            spacing=array.spacing, scale_text=array.scale_text, stroke_color=BLACK,
        )
        indices_mobj = indices.get_mobject().center().next_to(array_mobj, 0.1 * DOWN)
        self.add(array_mobj, a_text, indices_mobj)
        self.wait(6)

        left = Tex('l', color=ORANGE).scale(0.8).next_to(array.rectangles[1], UP).shift(0.1 * DOWN)
        right = Tex('r', color=ORANGE).scale(0.8).next_to(array.rectangles[5], UP).shift(0.1 * DOWN)
        self.play(Write(left), Write(right), run_time=0.5)
        self.wait(8)

        self.play(left.animate.next_to(array.rectangles[0], UP).shift(0.1 * DOWN), run_time=1)
        self.wait(1)
        self.play(right.animate.next_to(array.rectangles[-1], UP).shift(0.1 * DOWN), run_time=1.5)
        self.wait(7)
        l_inclusive = Tex('[', color=ORANGE).scale(0.8).next_to(left, LEFT, buff=0.05)
        r_exclusive = Tex(')', color=ORANGE).scale(0.8).next_to(right, RIGHT, buff=0.05)
        self.play(Write(l_inclusive), run_time=0.5)
        self.wait(1)
        self.play(Write(r_exclusive), run_time=0.5)
        self.wait(2)
        left = VGroup(l_inclusive, left)
        right = VGroup(right, r_exclusive)

        # Circumscribe l and the first element of the array
        self.play(Circumscribe(VGroup(left, array.rectangles[0], indices.rectangles[0]), run_time=1))
        self.wait(1.5)
        self.play(right.animate.set_color(DARKER_GREY), run_time=0.5)
        self.wait(8)
        # Move r one element to the right
        self.play(
            right.animate.shift((array.width + array.spacing) * RIGHT).set_color(ORANGE),
            run_time=0.5,
        )

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
        ).next_to(indices_mobj, DOWN).code

        # Type the first line of the code
        self.play(AddTextLetterByLetter(code.chars[0], run_time=0.1 * len(code.chars[0])))
        self.wait(6)
        self.play(AddTextLetterByLetter(code.chars[1], run_time=0.1 * len(code.chars[1])))
        self.wait(3)
        # Type 3rd line and add mid
        self.play(AddTextLetterByLetter(code.chars[2], run_time=0.1 * len(code.chars[2])))
        mid = Tex('mid', color=YELLOW).scale(0.8).next_to(array.rectangles[4], UP).shift(0.1 * DOWN)
        self.play(Write(mid), run_time=0.5)
        self.wait(3)

        def highlight(l, r, col):
            return [
                *[FadeToColor(label, col) for label in array.labels[l:r]],
                *[rect.animate.set_stroke(col) for rect in array.rectangles[l:r]],
                *[FadeToColor(label, col) for label in indices.labels[l:r]],
            ]

        # Type 4th line and 5th lines
        self.play(AddTextLetterByLetter(code.chars[3], run_time=0.1 * len(code.chars[3])))
        self.wait(3)
        # Bring r to mid and fade out mid
        self.play(
            right.animate.next_to(array.rectangles[4], UP).shift(0.1 * DOWN),
            FadeOut(mid),
            *highlight(4, len(array), DARKER_GREY),
            run_time=0.5,
        )
        self.wait(2)
        self.play(AddTextLetterByLetter(code.chars[4], run_time=0.1 * len(code.chars[4])))
        self.wait(15)

        # Add info about the other approach
        another_code = Code(
            code=dedent('''
                l, r = 0, len(a)
                while r >= l:
                    mid = (l + r) // 2
                    if a[mid] > q:
                        r = mid - 1
                    elif a[mid] < q:
                        l = mid + 1
                    else:
                        print(mid)

                print(l if a[l] == q else -1)
            ''').strip(),
            tab_width=4,
            language='Python',
            line_spacing=0.6,
            font='Monospace',
            style='monokai',
        ).next_to(indices_mobj, DOWN).code
        self.play(TransformMatchingShapes(code.chars[4], another_code.chars[4]), run_time=0.5)
        self.wait(0.5)
        self.play(TransformMatchingShapes(another_code.chars[4], code.chars[4]), run_time=0.5)

        # Move r to the end of the array
        mid = Tex('mid', color=YELLOW).scale(0.8).next_to(array.rectangles[4], UP).shift(0.1 * DOWN)
        self.play(
            right.animate.next_to(array.rectangles[-1], UP).shift(0.1 * DOWN).shift((array.width + array.spacing) * RIGHT),
            Write(mid),
            *highlight(4, len(array), WHITE),
            run_time=0.5,
        )

        # Write the 6th line
        self.play(AddTextLetterByLetter(code.chars[5], run_time=0.1 * len(code.chars[5])))
        self.wait(2.5)

        # Bring l to mid and fade out mid
        self.play(
            left.animate.next_to(array.rectangles[4], UP).shift(0.1 * DOWN),
            FadeOut(mid),
            *highlight(0, 4, DARKER_GREY),
            run_time=0.5,
        )
        self.wait(1)

        self.play(AddTextLetterByLetter(code.chars[6], run_time=0.1 * len(code.chars[6])))
        self.wait(4)

        # Bring l one element to the right
        self.play(
            left.animate.shift((array.width + array.spacing) * RIGHT),
            *highlight(4, 5, DARKER_GREY),
            run_time=1,
        )
        self.play(RemoveTextLetterByLetter(code.chars[6], run_time=0.1))
        self.play(RemoveTextLetterByLetter(code.chars[5], run_time=0.1))
        self.play(RemoveTextLetterByLetter(code.chars[4], run_time=0.1))
        self.play(AddTextLetterByLetter(another_code.chars[4], run_time=0.1 * len(another_code.chars[4])))
        self.play(AddTextLetterByLetter(another_code.chars[5], run_time=0.1 * len(another_code.chars[5])))
        self.play(AddTextLetterByLetter(another_code.chars[6], run_time=0.1 * len(another_code.chars[6])))
        self.play(AddTextLetterByLetter(another_code.chars[7], run_time=0.1 * len(another_code.chars[7])))
        self.play(AddTextLetterByLetter(another_code.chars[8], run_time=0.1 * len(another_code.chars[8])))
        self.wait(2)
        self.play(RemoveTextLetterByLetter(code.chars[1]), run_time=0.1)
        self.play(AddTextLetterByLetter(another_code.chars[1], run_time=0.1 * len(another_code.chars[2])))
        self.wait(4)

        # Bring l back
        self.play(
            left.animate.shift((array.width + array.spacing) * LEFT),
            *highlight(4, 5, WHITE),
            run_time=1,
        )
        self.wait(1)
        self.play(RemoveTextLetterByLetter(another_code.chars[1], run_time=0.1))
        self.play(AddTextLetterByLetter(code.chars[1], run_time=0.1 * len(code.chars[2])))
        self.play(RemoveTextLetterByLetter(another_code.chars[8], run_time=0.1))
        self.play(RemoveTextLetterByLetter(another_code.chars[7], run_time=0.1))
        self.play(RemoveTextLetterByLetter(another_code.chars[6], run_time=0.1))
        self.play(RemoveTextLetterByLetter(another_code.chars[5], run_time=0.1))
        self.play(RemoveTextLetterByLetter(another_code.chars[4], run_time=0.1))
        self.play(AddTextLetterByLetter(code.chars[4], run_time=0.1 * len(code.chars[4])))
        self.play(AddTextLetterByLetter(code.chars[5], run_time=0.1 * len(code.chars[5])))
        self.play(AddTextLetterByLetter(code.chars[6], run_time=0.1 * len(code.chars[6])))
        self.wait(1)

        # Bring l to 49 and r to 52
        self.play(
            left.animate.next_to(array.rectangles[5], UP).shift(0.1 * DOWN),
            right.animate.next_to(array.rectangles[6], UP).shift(0.1 * DOWN),
            *highlight(0, 5, DARKER_GREY),
            *highlight(5, 6, WHITE),
            *highlight(6, len(array), DARKER_GREY),
            run_time=0.5,
        )

        # Write the last line of the code
        self.wait(2)
        self.play(AddTextLetterByLetter(code.chars[-1], run_time=0.15 * len(code.chars[-1])))
        self.wait(6)

        # Transition to the next scene
        self.play(
            left.animate.next_to(array.rectangles[0], UP).shift(0.1 * DOWN),
            right.animate.next_to(array.rectangles[-1], UP).shift(0.1 * DOWN).shift((array.width + array.spacing) * RIGHT),
            *highlight(0, len(array), WHITE),
            run_time=0.5,
        )
        self.wait(1)


class SimulatingNormalCase(Scene):
    def construct(self):
        title = Title('Binary Search', include_underline=False)
        self.add(title)

        array = Array(a)
        array_mobj = array.get_mobject().center().shift(2 * UP)
        a_text = Tex('a:').scale(0.8).next_to(array_mobj, LEFT)
        indices = Array(
            [i for i in range(len(array) + 1)],
            width=array.width, height=array.height,
            spacing=array.spacing, scale_text=array.scale_text, stroke_color=BLACK,
        )
        indices_mobj = indices.get_mobject().center().next_to(array_mobj, 0.1 * DOWN).align_to(array_mobj, LEFT)
        indices.labels[-1].set_color(BLACK)
        self.add(array_mobj, a_text, indices_mobj)

        left = Tex('l', color=ORANGE).scale(0.8)
        right = Tex('r', color=ORANGE).scale(0.8)
        l_inclusive = Tex('[', color=ORANGE).scale(0.8).next_to(left, LEFT, buff=0.05)
        r_exclusive = Tex(')', color=ORANGE).scale(0.8).next_to(right, RIGHT, buff=0.05)
        left = VGroup(l_inclusive, left).next_to(array.rectangles[0], UP).shift(0.1 * DOWN)
        right = VGroup(right, r_exclusive).next_to(array.rectangles[-1], UP).shift(0.1 * DOWN).shift((array.width + array.spacing) * RIGHT)
        self.add(left, right)

        def highlight(l, r, col):
            return [
                *[FadeToColor(label, col) for label in array.labels[l:r]],
                *[rect.animate.set_stroke(col) for rect in array.rectangles[l:r]],
                *[FadeToColor(label, col) for label in indices.labels[l:r]],
            ]

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
        ).next_to(array_mobj, DOWN).shift((indices_mobj.height + 0.02) * DOWN).code
        self.add(code.chars)
        self.wait(4)

        q = Tex(r'q: 49', color=ORANGE).scale(0.8).next_to(code.chars, RIGHT).align_to(code.chars, UP)
        self.play(Write(q, run_time=0.5))
        self.wait(2)

        # Arrow to show which part of the code is being executed
        arrow = Arrow(
            start=LEFT, end=RIGHT, color=RED, buff=0.1,
            stroke_width=10, max_stroke_width_to_length_ratio=15,
            max_tip_length_to_length_ratio=0.5, tip_length=0.2,
        ).scale(0.3).next_to(code, LEFT).align_to(code, UP).shift(0.08 * DOWN)
        self.play(Create(arrow), run_time=0.5)
        self.wait(3)

        self.play(arrow.animate.shift(0.4 * DOWN), run_time=0.3)
        self.wait(2)

        # Calculate mid
        self.play(arrow.animate.shift(0.4 * DOWN), run_time=0.3)
        self.play(Circumscribe(VGroup(left, indices.rectangles[0]), run_time=0.5))
        self.play(Circumscribe(VGroup(right, indices.rectangles[-1]), run_time=1))
        self.wait(2)
        mid = Tex('mid', color=YELLOW).scale(0.8).next_to(array.rectangles[4], UP).shift(0.1 * DOWN)
        self.play(Write(mid), run_time=0.5)
        self.wait(2)

        # Move the arrow to l = mid, bring l to mid and fade out mid
        self.play(arrow.animate.shift(0.4 * DOWN), run_time=0.2)
        self.wait(4)
        self.play(arrow.animate.shift(1.2 * DOWN), run_time=0.2)
        self.wait(2)
        self.play(left.animate.next_to(array.rectangles[4], UP).shift(0.1 * DOWN), FadeOut(mid), run_time=0.5)
        self.wait(1)
        self.play(*highlight(0, 4, DARKER_GREY), run_time=0.2)
        self.wait(4)

        # Move the arrow to the start of the while loop
        self.play(arrow.animate.shift(2 * UP), run_time=0.5)
        self.wait(8)
        self.play(arrow.animate.shift(0.4 * DOWN), run_time=0.3)
        self.wait(3)
        self.play(Circumscribe(VGroup(left, indices.rectangles[4]), run_time=0.5))
        self.play(Circumscribe(VGroup(right, indices.rectangles[-1]), run_time=1))
        self.wait(3)

        self.play(Write(mid.next_to(array.rectangles[6], UP).shift(0.1 * DOWN)), run_time=0.5)
        self.wait(2)

        self.play(arrow.animate.shift(0.4 * DOWN), run_time=0.3)
        self.wait(3)
        self.play(arrow.animate.shift(0.4 * DOWN), run_time=0.3)
        self.wait(0.5)
        self.play(
            *highlight(6, len(array), DARKER_GREY),
            right.animate.next_to(array.rectangles[6], UP).shift(0.1 * DOWN),
            FadeOut(mid),
            run_time=0.5,
        )
        self.wait(2)

        # Move the arrow to the start of the while loop
        self.play(arrow.animate.shift(1.2 * UP), run_time=0.5)
        self.wait(3)
        self.play(arrow.animate.shift(0.4 * DOWN), run_time=0.3)
        self.wait(2)
        self.play(Write(mid.next_to(array.rectangles[5], UP).shift(0.1 * DOWN)), run_time=0.3)
        self.wait(4)

        self.play(arrow.animate.shift(0.4 * DOWN), run_time=0.3)
        self.wait(4)
        self.play(
            arrow.animate.shift(1.2 * DOWN),
            left.animate.next_to(array.rectangles[5], UP).shift(0.1 * DOWN),
            FadeOut(mid),
            run_time=0.5,
        )
        self.wait(1)
        self.play(*highlight(4, 5, DARKER_GREY), run_time=0.2)
        self.wait(1)

        # Move the arrow to the start of the while loop
        self.play(arrow.animate.shift(2 * UP), run_time=0.5)
        self.wait(9)

        self.play(arrow.animate.shift(2.8 * DOWN), run_time=0.5)
        self.wait(1.5)
        self.play(Circumscribe(VGroup(left, array.rectangles[5], indices.rectangles[5]), run_time=1))
        self.wait(1.5)
        self.play(Indicate(code.chars[-1]), run_time=1)
        self.wait(3)

        # Transition to the next scene
        self.play(FadeOut(arrow), run_time=0.5)
        self.wait(3)

        # Move l and r to start and end of the array
        self.play(
            left.animate.next_to(array.rectangles[0], UP).shift(0.1 * DOWN),
            right.animate.next_to(array.rectangles[-1], UP).shift(0.1 * DOWN).shift((array.width + array.spacing) * RIGHT),
            *highlight(0, len(array), WHITE),
            run_time=1,
        )
        self.wait(1)

        self.play(
            ReplacementTransform(q, Tex(r'q: 57', color=ORANGE).scale(0.8).next_to(code.chars, RIGHT).align_to(code.chars, UP)),
            run_time=0.5,
        )
        self.wait(1)


class SimulatingEdgeCase(Scene):
    def construct(self):
        title = Title('Binary Search', include_underline=False)
        self.add(title)

        array = Array(a)
        array_mobj = array.get_mobject().center().shift(2 * UP)
        a_text = Tex('a:').scale(0.8).next_to(array_mobj, LEFT)
        indices = Array(
            [i for i in range(len(array) + 1)],
            width=array.width, height=array.height,
            spacing=array.spacing, scale_text=array.scale_text, stroke_color=BLACK,
        )
        indices_mobj = indices.get_mobject().center().next_to(array_mobj, 0.1 * DOWN).align_to(array_mobj, LEFT)
        indices.labels[-1].set_color(BLACK)
        self.add(array_mobj, a_text, indices_mobj)

        left = Tex('l', color=ORANGE).scale(0.8)
        right = Tex('r', color=ORANGE).scale(0.8)
        l_inclusive = Tex('[', color=ORANGE).scale(0.8).next_to(left, LEFT, buff=0.05)
        r_exclusive = Tex(')', color=ORANGE).scale(0.8).next_to(right, RIGHT, buff=0.05)
        left = VGroup(l_inclusive, left).next_to(array.rectangles[0], UP).shift(0.1 * DOWN)
        right = VGroup(right, r_exclusive).next_to(array.rectangles[-1], UP).shift(0.1 * DOWN).shift((array.width + array.spacing) * RIGHT)
        self.add(left, right)

        def highlight(l, r, col):
            return [
                *[FadeToColor(label, col) for label in array.labels[l:r]],
                *[rect.animate.set_stroke(col) for rect in array.rectangles[l:r]],
                *[FadeToColor(label, col) for label in indices.labels[l:r]],
            ]

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
        ).next_to(array_mobj, DOWN).shift((indices_mobj.height + 0.02) * DOWN).code
        self.add(code.chars)

        q = Tex(r'q: 57', color=ORANGE).scale(0.8).next_to(code.chars, RIGHT).align_to(code.chars, UP)
        self.add(q)
        self.wait(1)

        # Arrow to show which part of the code is being executed
        arrow = Arrow(
            start=LEFT, end=RIGHT, color=RED, buff=0.1,
            stroke_width=10, max_stroke_width_to_length_ratio=15,
            max_tip_length_to_length_ratio=0.5, tip_length=0.2,
        ).scale(0.3).next_to(code, LEFT).align_to(code, UP).shift(0.08 * DOWN)
        self.play(Create(arrow), run_time=1)
        self.wait(3)

        self.play(arrow.animate.shift(0.4 * DOWN), run_time=0.3)
        self.wait(1)

        # Calculate mid
        self.play(arrow.animate.shift(0.4 * DOWN), run_time=0.3)
        self.wait(3)
        mid = Tex('mid', color=YELLOW).scale(0.8).next_to(array.rectangles[4], UP).shift(0.1 * DOWN)
        self.play(Write(mid), run_time=0.3)
        self.wait(2)

        self.play(arrow.animate.shift(0.4 * DOWN), run_time=0.3)
        self.wait(3)

        self.play(arrow.animate.shift(1.2 * DOWN), run_time=0.3)
        self.wait(1)
        self.play(left.animate.next_to(array.rectangles[4], UP).shift(0.1 * DOWN), FadeOut(mid), run_time=0.5)
        self.wait(0.5)
        self.play(*highlight(0, 4, DARKER_GREY), run_time=0.3)
        self.wait(3)

        # Move the arrow to the start of the while loop
        self.play(arrow.animate.shift(2 * UP), run_time=0.5)
        self.wait(0.5)
        self.play(arrow.animate.shift(0.4 * DOWN), run_time=0.3)
        self.wait(2)

        self.play(Write(mid.next_to(array.rectangles[6], UP).shift(0.1 * DOWN)), run_time=0.3)
        self.wait(2)

        self.play(arrow.animate.shift(0.4 * DOWN), run_time=0.3)
        self.wait(4)
        self.play(arrow.animate.shift(1.2 * DOWN), run_time=0.5)
        self.wait(1)
        self.play(
            left.animate.next_to(array.rectangles[6], UP).shift(0.1 * DOWN),
            FadeOut(mid),
            *highlight(4, 6, DARKER_GREY),
            run_time=0.5,
        )
        self.wait(2)

        # Move the arrow to the start of the while loop
        self.play(arrow.animate.shift(2 * UP), run_time=0.3)
        self.wait(0.5)
        self.play(arrow.animate.shift(0.4 * DOWN), run_time=0.3)
        self.wait(1)

        self.play(Write(mid.next_to(array.rectangles[7], UP).shift(0.1 * DOWN)), run_time=0.5)
        self.wait(2.5)

        self.play(arrow.animate.shift(0.4 * DOWN), run_time=0.2)
        self.wait(4)
        self.play(arrow.animate.shift(1.2 * DOWN), run_time=0.2)
        self.wait(1)
        self.play(
            left.animate.next_to(array.rectangles[7], UP).shift(0.1 * DOWN),
            FadeOut(mid),
            *highlight(6, 7, DARKER_GREY),
            run_time=0.5,
        )
        self.wait(2)

        # Move the arrow to the start of the while loop
        self.play(arrow.animate.shift(2 * UP), run_time=0.5)
        self.wait(0.5)
        self.play(arrow.animate.shift(0.4 * DOWN), run_time=0.3)
        self.wait(0.5)

        self.play(Write(mid.next_to(array.rectangles[8], UP).shift(0.1 * DOWN)), run_time=0.3)
        self.wait(4)

        self.play(arrow.animate.shift(0.4 * DOWN), run_time=0.3)
        self.wait(4)
        self.play(arrow.animate.shift(0.4 * DOWN), run_time=0.3)
        self.wait(1)
        self.play(
            right.animate.next_to(array.rectangles[8], UP).shift(0.1 * DOWN),
            FadeOut(mid),
            *highlight(8, len(array), DARKER_GREY),
            run_time=0.5,
        )
        self.wait(1)

        # Move the arrow to the start of the while loop
        self.play(arrow.animate.shift(1.2 * UP), run_time=0.5)
        self.wait(4)
        self.play(arrow.animate.shift(2.8 * DOWN), run_time=0.5)
        self.wait(0.5)
        self.play(Circumscribe(VGroup(left, array.rectangles[7], indices.rectangles[7]), run_time=1))
        self.wait(6)

        # Finish the scene
        self.play(FadeOut(arrow), run_time=0.5)
        self.play(ReplacementTransform(title, Title('Practice', include_underline=False)))
        self.wait(4)
        self.play(ReplacementTransform(q, Tex(r'q: 20, 23, 100', color=ORANGE).scale(0.8).next_to(code.chars, RIGHT).align_to(code.chars, UP)))
        self.wait(4)
        self.play(Wiggle(code, rotation_angle=0.005 * TAU, run_time=1))
        self.wait(2)


class OverflowIssue(Scene):
    def construct(self):
        title = Title('Binary Search', include_underline=False)
        self.add(title)

        array = Array(a)
        array_mobj = array.get_mobject().center().shift(2 * UP)
        a_text = Tex('a:').scale(0.8).next_to(array_mobj, LEFT)
        indices = Array(
            [i for i in range(len(array) + 1)],
            width=array.width, height=array.height,
            spacing=array.spacing, scale_text=array.scale_text, stroke_color=BLACK,
        )
        indices_mobj = indices.get_mobject().center().next_to(array_mobj, 0.1 * DOWN).align_to(array_mobj, LEFT)
        indices.labels[-1].set_color(BLACK)
        self.add(array_mobj, a_text, indices_mobj)

        left = Tex('l', color=ORANGE).scale(0.8)
        right = Tex('r', color=ORANGE).scale(0.8)
        l_inclusive = Tex('[', color=ORANGE).scale(0.8).next_to(left, LEFT, buff=0.05)
        r_exclusive = Tex(')', color=ORANGE).scale(0.8).next_to(right, RIGHT, buff=0.05)
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
        ).next_to(indices_mobj, DOWN).code
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
        segment = Line(start=5 * LEFT, end=5 * RIGHT, color=WHITE).center().shift(2 * UP)
        minimum = Integer(0).set_color(ORANGE).scale(0.7)     # -2_147_483_648
        maximum = Integer(0).set_color(ORANGE).scale(0.7)     # 2_147_483_647
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
        l_arrow = Arrow(start=DOWN, end=UP, tip_length=0.2, color=YELLOW).scale(0.5).next_to(segment, DOWN).align_to(segment, RIGHT).shift(1.2 * LEFT)
        r_arrow = Arrow(start=DOWN, end=UP, tip_length=0.2, color=YELLOW).scale(0.5).next_to(segment, DOWN).align_to(segment, RIGHT).shift(0.5 * LEFT)
        l_label = Text('l', color=YELLOW).scale(0.5).next_to(l_arrow, DOWN)
        r_label = Text('r', color=YELLOW).scale(0.6).next_to(r_arrow, DOWN)
        self.play(Write(l_arrow), Write(l_label), run_time=0.5)
        self.wait(0.5)
        self.play(Write(r_arrow), Write(r_label), run_time=0.5)
        self.wait(6)

        sum_arrow = Arrow(start=DOWN, end=UP, tip_length=0.2, color=RED).scale(0.5).next_to(segment, DOWN).align_to(segment, RIGHT).shift(RIGHT)
        sum_label = Text('l + r', color=RED).scale(0.5).next_to(sum_arrow, DOWN)
        self.play(Write(sum_label), run_time=0.5)
        self.wait(1)
        self.play(Write(sum_arrow), run_time=0.5)
        self.wait(6)

        # Move l + r to the start of the segment
        self.play(VGroup(sum_arrow, sum_label).animate.next_to(segment, DOWN).align_to(segment, LEFT).shift(1.2 * RIGHT), run_time=2)
        self.wait(3)

        self.play(FadeOut(sum_arrow), FadeOut(sum_label), run_time=0.4)

        new_code = Code(
            code=dedent('''
                l, r = 0, len(a)
                while r - l > 1:
                    mid = l + (r - l) // 2
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
        ).next_to(indices_mobj, DOWN).code

        # Brace between l and r
        brace = Brace(VGroup(l_label, r_label), buff=0.05, direction=DOWN, color=YELLOW, sharpness=3)
        brace_label = brace.get_text(r'$\frac{r - l}{2}$').shift(0.1 * UP)
        self.play(Write(brace), Write(brace_label), run_time=0.5)
        self.wait(4)

        # Remove the mid calculation and add the new one
        self.play(RemoveTextLetterByLetter(code.chars[2]), run_time=0.1)
        self.play(AddTextLetterByLetter(new_code.chars[2], run_time=0.1 * len(new_code.chars[2])))
        self.wait(18)

        # Add a search icon and move it from start of mid calculation to the end
        search_icon = SVGMobject(
            'binary_search/search.svg', color=WHITE, fill_color=WHITE, fill_opacity=1,
        ).scale(0.5).align_to(new_code.chars[3], LEFT).align_to(new_code.chars[3], DOWN).shift(0.5 * LEFT)
        self.play(DrawBorderThenFill(search_icon), run_time=0.2)
        self.play(search_icon.animate.next_to(new_code.chars[3], RIGHT).align_to(new_code.chars[3], DOWN).shift(0.5 * LEFT), run_time=2)
        self.play(FadeOut(search_icon), run_time=0.4)


class LinearVSBinary(Scene):
    def construct(self):
        title = Title('Linear Search VS Binary Search', include_underline=False)
        self.add(title)

        array = Array(a)
        array_mobj = array.get_mobject().center().shift(2.2 * UP)
        a_text = Tex('a:').scale(0.8).next_to(array_mobj, LEFT)
        indices = Array(
            [i for i in range(len(array) + 1)],
            width=array.width, height=array.height,
            spacing=array.spacing, scale_text=array.scale_text, stroke_color=BLACK,
        )
        indices_mobj = indices.get_mobject().center().next_to(array_mobj, 0.1 * DOWN).align_to(array_mobj, LEFT)
        indices.labels[-1].set_color(BLACK)
        self.add(array_mobj, a_text, indices_mobj)

        linear_code = Code(
            code=dedent('''
                for i, x in enumerate(a):
                    if x == q:
                        print(i)
                        break
                else:
                    print(-1)
            ''').strip(),
            tab_width=4,
            language='Python',
            line_spacing=0.6,
            font='Monospace',
            style='monokai',
        ).scale(0.8).next_to(indices_mobj, DOWN, buff=0.5).to_edge(LEFT, buff=1).code

        for line in linear_code.chars:
            if line:
                self.play(AddTextLetterByLetter(line), run_time=0.012 * len(line))
        self.wait(0.5)

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
        ).scale(0.8).next_to(indices_mobj, DOWN, buff=0.5).to_edge(RIGHT, buff=1).code
        for line in code.chars:
            if line:
                self.play(AddTextLetterByLetter(line), run_time=0.012 * len(line))
        self.wait(0.2)

        # Create a yellow rectangle that highlights the first 4 elements of the array
        memory_chunk = Rectangle(
            width=4 * array.width + 5 * array.spacing,
            height=array.height + 2 * array.spacing,
            stroke_color=YELLOW, stroke_width=6,
        ).align_to(array_mobj, DOWN).align_to(array_mobj, LEFT).shift(0.1 * DOWN).shift(0.1 * LEFT)
        self.play(Create(memory_chunk), run_time=0.3)
        self.wait(0.5)

        self.play(memory_chunk.animate.shift((4 * array.width + 4 * array.spacing) * RIGHT), run_time=0.2)
        self.wait(0.5)
        self.play(memory_chunk.animate.shift((4 * array.width + 4 * array.spacing) * RIGHT), run_time=0.2)
        self.wait(0.5)
        self.play(FadeOut(memory_chunk), run_time=0.4)

        # Add arc arrows from for to if and from if to for
        for_to_if = CurvedArrow(linear_code.chars[0].get_left(), linear_code.chars[0].get_left() + 0.4 * DOWN, color=WHITE, angle=TAU / 3, tip_length=0.1)
        if_to_for = CurvedArrow(linear_code.chars[0].get_right() + 0.4 * DOWN + 0.1 * RIGHT, linear_code.chars[0].get_right() + 0.1 * RIGHT, color=WHITE, angle=TAU / 3, tip_length=0.1)
        self.play(Create(for_to_if), run_time=0.2)
        self.play(Create(if_to_for), run_time=0.2)
        self.wait(0.2)

        # Add lightning icon to the right of if to for
        lightning_icon = SVGMobject(
            'binary_search/lightning.svg', color=YELLOW, fill_color=YELLOW, fill_opacity=1,
        ).scale(0.3).next_to(if_to_for, RIGHT)
        self.add(lightning_icon)
        self.play(
            Wiggle(lightning_icon, run_time=2),
            ShowPassingFlash(for_to_if.copy().set_color(YELLOW), time_width=0.5, run_time=1),
            ShowPassingFlash(if_to_for.copy().set_color(YELLOW), time_width=0.5, run_time=2),
        )
        self.wait(1)

        self.play(FadeOut(lightning_icon), FadeOut(for_to_if), FadeOut(if_to_for), run_time=0.4)
        self.wait(1)

        # Shuffle the array
        random.seed(42)
        shuffled_array = a.copy()
        random.shuffle(shuffled_array)
        shuffled_array = Array(shuffled_array)
        shuffled_array_mobj = shuffled_array.get_mobject().center().shift(2.2 * UP)

        self.play(TransformMatchingCells(array_mobj, shuffled_array_mobj, path_arc=PI/2), run_time=2)
        self.wait(5)

        q = Tex(r'q: 20, 23, 50, 100, ...', color=ORANGE).scale(0.8).next_to(linear_code, DOWN, buff=0.5).align_to(linear_code, LEFT)
        self.play(Write(q), run_time=2)
        self.wait(5)

        # Write "Sort: O(n log(n))"
        sort = MathTex(
            r'\mathrm{Sort:} \, \mathcal{O}(n \cdot \log{n})', color=WHITE,
        ).scale(0.8).next_to(q, DOWN).align_to(q, LEFT)
        self.play(Write(sort), run_time=1)
        self.wait(5)

        # Replace q with "q: 20"
        new_q = Tex(r'q: 20', color=ORANGE).scale(0.8).next_to(linear_code, DOWN, buff=0.5).align_to(linear_code, LEFT)
        self.play(ReplacementTransform(q, new_q), run_time=0.5)
        self.wait(5)

        # Replace q with "q: 20, 23, 50, 100, ..."
        q = Tex(r'q: 20, 23, 50, 100, ...', color=ORANGE).scale(0.8).next_to(linear_code, DOWN, buff=0.5).align_to(linear_code, LEFT)
        self.play(ReplacementTransform(new_q, q))
        self.wait(2)

        self.play(TransformMatchingCells(shuffled_array_mobj, array_mobj, path_arc=PI/2), run_time=2)
        self.wait(2)

        # Transition to the next scene
        self.play(
            ReplacementTransform(title, Title('Binary Search', include_underline=False)),
            FadeOut(linear_code, q, sort),
            code.animate.center().next_to(indices_mobj, DOWN, buff=0.5),
            run_time=1,
        )
        self.wait(1)


class BinarySearchAsGenericIdea(Scene):
    def construct(self):
        title = Title('Binary Search', include_underline=False)
        self.add(title)

        array = Array(a)
        array_mobj = array.get_mobject().center().shift(2.2 * UP)
        a_text = Tex('a:').scale(0.8).next_to(array_mobj, LEFT)
        indices = Array(
            [i for i in range(len(array) + 1)],
            width=array.width, height=array.height,
            spacing=array.spacing, scale_text=array.scale_text, stroke_color=BLACK,
        )
        indices_mobj = indices.get_mobject().center().next_to(array_mobj, 0.1 * DOWN).align_to(array_mobj, LEFT)
        indices.labels[-1].set_color(BLACK)
        self.add(array_mobj, a_text, indices_mobj)

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
        ).scale(0.8).center().next_to(indices_mobj, DOWN, buff=0.5).code
        self.add(code)
        self.wait(0.1)

        self.play(Indicate(code, run_time=0.5))
        self.wait(0.1)

        def highlight(l, r, col):
            return [
                *[FadeToColor(label, col) for label in array.labels[l:r]],
                *[rect.animate.set_stroke(col) for rect in array.rectangles[l:r]],
                *[FadeToColor(label, col) for label in indices.labels[l:r]],
            ]

        self.play(*highlight(0, 4, DARKER_GREY), run_time=0.5)
        self.wait(0.1)

        self.play(Circumscribe(code, run_time=0.5))
        new_title = Title('Binary Search Variations', include_underline=False)
        self.play(
            ReplacementTransform(title, new_title),
            run_time=0.5,
        )
        self.wait(0.1)
        self.play(FadeOut(array_mobj), FadeOut(indices_mobj), FadeOut(a_text), run_time=0.2)
        self.wait(0.5)

        # sqrt
        sqrt = MathTex(
            r'\sqrt{7}: [0, 7] \rightarrow [0, 3.5] \rightarrow [1.75, 3.5] \rightarrow [2.625, 3.5] \rightarrow ...'
        ).scale(0.8).next_to(title, DOWN)
        self.play(Write(sqrt), run_time=0.5)
        self.wait(0.1)

        self.play(FadeOut(sqrt), run_time=0.2)
        self.wait(0.1)

        self.play(*highlight(0, 4, WHITE), run_time=0.00001)
        self.play(FadeIn(array_mobj), FadeIn(indices_mobj), FadeIn(a_text), run_time=0.1)
        self.play(VGroup(array_mobj, indices_mobj, a_text).animate.shift(0.5 * DOWN), run_time=0.1)
        self.wait(0.1)

        # Add (l and r] at the top of the array
        left = Tex('(l', color=ORANGE).scale(0.8).next_to(array.rectangles[2], UP)
        right = Tex('r]', color=ORANGE).scale(0.8).next_to(array.rectangles[7], UP)
        self.play(Write(left), Write(right), *highlight(0, 3, DARKER_GREY), *highlight(8, len(array), DARKER_GREY), run_time=0.5)
        self.wait(0.1)

        self.play(
            FadeOut(left, right),
            *highlight(0, len(array), WHITE),
            ReplacementTransform(new_title, Title('Binary Search', include_underline=False)),
            run_time=0.5,
        )

        self.play(ApplyWave(code, run_time=2))
        self.wait(1)
