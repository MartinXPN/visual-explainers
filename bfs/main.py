import random

from manim import *


ORANGE = ManimColor('#fa541c')
random.seed(42)

g = [
    [2],
    [2],
    [0, 1, 9],
    [5],
    [9, 8, 5],
    [3, 4, 8, 6, 7],
    [5, 7, 10],
    [5, 6],
    [4, 5, 9, 10],
    [4, 8, 2],
    [8, 6, 11],
    [10],
    [13, 14],
    [12, 14],
    [12, 13],
    [16],
    [15],
]


class Introduction(Scene):
    def construct(self):
        vertices = list(range(len(g)))
        edges = [(i, j) for i, neighbors in enumerate(g) for j in neighbors]

        layout = {
            0: [-5.5, -1.5, 0],
            1: [-3.5, -1.5, 0],
            2: [-4.5, 0, 0],
            3: [1, -1.5, 0],
            4: [-0.5, 0, 0],
            5: [4, -1.5, 0],
            6: [4, 2, 0],
            7: [6, 0, 0],
            8: [2, 0, 0],
            9: [0.5, 3, 0],
            10: [3, 4, 0],
            11: [5, 4, 0],
            12: [-3.5, 4, 0],
            13: [-4.5, 2, 0],
            14: [-1, 4, 0],
            15: [-2.5, 0, 0],
            16: [-1.5, -1.5, 0],
        }

        graph = Graph(
            vertices, edges,
            layout=layout,
            labels=True,
            vertex_config={'radius': 0.4, 'stroke_width': 2, 'fill_color': WHITE},
            edge_config={'stroke_width': 4},
        ).shift(DOWN)

        self.add(graph)
        self.wait(1)
