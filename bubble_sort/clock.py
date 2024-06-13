from manim import *


class Clock(VGroup):
    def __init__(self, hh=0, mh=0, radius=3, **kwargs):
        super().__init__(**kwargs)

        # Define body
        body = Circle(radius=radius, color=WHITE)
        body.flip()
        body.rotate(- 4 * 360 / 12 * DEGREES)
        self.body = body
        center_body = Dot(body.get_center())
        numbers = self.get_numbers(body)
        ticks = self.get_ticks(body)

        # Define hour
        hour = hh + mh / 60
        hour_tracker = ValueTracker(hour)
        self.ht = hour_tracker

        # Define hands
        minute_hand = self.get_minute_hand(body, hour_tracker.get_value() % 1 * 60)
        hour_hand = self.get_hour_hand(body, hour_tracker.get_value())

        self.hh = hour_hand
        self.mh = minute_hand

        self.add(
            body,
            ticks,
            numbers,
            minute_hand,
            hour_hand,
            center_body,
        )

    def add_updaters(self):
        self.mh.add_updater(
            lambda mob: mob.become(
                self.get_minute_hand(self.body, self.ht.get_value() % 1 * 60))
        )
        self.hh.add_updater(
            lambda mob: mob.become(
                self.get_hour_hand(
                    self.body,
                    self.ht.get_value()
                )
            )
        )

    def suspend_updaters(self):
        for mob in [self.mh, self.hh, self.dl]:
            mob.suspend_updating()

    def resume_updaters(self):
        for mob in [self.mh, self.hh, self.dl]:
            mob.resume_updating()

    def get_hour_hand(self, body: Circle, hour, a_prop=0.5):
        prop = hour / 12
        guide_line = Line(
            body.get_center(),
            body.point_from_proportion(prop % 1)
        )
        hour_hand = Arrow(
            body.get_center(),
            guide_line.point_from_proportion(a_prop),
            buff=0,
            color=RED
        )
        hour_hand.rotate(2 * PI / 12, about_point=body.get_center())
        return hour_hand

    def get_minute_hand(self, body: Circle, minutes, a_prop=0.8):
        prop = minutes / 60
        guide_line = Line(
            body.get_center(),
            body.point_from_proportion(prop % 1)
        )
        hour_hand = Arrow(
            body.get_center(),
            guide_line.point_from_proportion(a_prop),
            buff=0,
            color=YELLOW
        )
        hour_hand.rotate(2 * PI / 12, about_point=body.get_center())
        return hour_hand

    @staticmethod
    def get_numbers(body: Circle, prop=0.85, scale=0.8):
        numbers = VGroup(*[Tex(f'{i}') for i in list(range(1, 13))])
        for i, n in enumerate(numbers):
            point = body.point_from_proportion(i / 12)
            guide_line = Line(body.get_center(), point)
            n.scale(scale)
            n.move_to(guide_line.point_from_proportion(prop))
        return numbers

    @staticmethod
    def get_ticks(body: Circle, size_prop=0.04):
        ticks = VGroup()
        for i in range(60):
            point = body.point_from_proportion(i / 60)
            guide_line = Line(body.get_center(), point)
            size = size_prop * 2 if i % 5 == 0 else size_prop
            tick = Line(
                guide_line.point_from_proportion(1 - size),
                point
            )
            ticks.add(tick)
        return ticks
