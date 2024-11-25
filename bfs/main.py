import random

from manim import *


ORANGE = ManimColor('#fa541c')
random.seed(42)


class Introduction(Scene):
    def construct(self):
        vertices = [i for i in range(10)]
        edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),  # Cycle: 0-1-2-3-0
            (3, 4), (4, 5), (5, 6), (6, 3),  # Cycle: 3-4-5-6-3
            (2, 7), (7, 8), (8, 9), (9, 2),  # Cycle: 2-7-8-9-2
            (1, 7), (5, 9),                  # Cross connections
        ]

        # Define a custom layout for the graph
        layout = {
            0: [-2, 2, 0],
            1: [0, 2, 0],
            2: [2, 2, 0],
            3: [0, 0, 0],
            4: [2, 0, 0],
            5: [2, -2, 0],
            6: [0, -2, 0],
            7: [4, 2, 0],
            8: [4, 0, 0],
            9: [4, -2, 0],
        }

        # Create the graph with the specified layout
        graph = Graph(
            vertices, edges,
            layout=layout,
            labels=True,
            vertex_config={'radius': 0.4, 'stroke_width': 2, 'fill_color': BLUE},
            edge_config={'stroke_width': 2},
        )

        # Animate the creation of the graph
        self.play(Create(graph))
        self.wait(1)