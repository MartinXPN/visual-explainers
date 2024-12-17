import math
import random
from textwrap import dedent

import networkx as nx
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

class Introduction(Scene):
    def construct(self):
        vertices = list(range(len(g)))
        edges = [(i, j) for i, neighbors in enumerate(g) for j in neighbors]

        graph = Graph(
            vertices, edges,
            layout=layout,
            labels=True,
            vertex_config={'radius': 0.4, 'stroke_width': 0, 'fill_color': WHITE},
            edge_config={'stroke_width': 5},
        ).shift(1.5 * DOWN)

        self.add(graph)
        for label in graph._labels.values():
            label.set_z_index(10)
        self.wait(1)


        def update_fire(mobj, dt):
            if not hasattr(mobj, 'initialized'):
                mobj.initialized = True

                # The 3 small flames are the last 3 submobjects
                mobj.small_flames = mobj.submobjects[-3:]
                mobj.initial_positions = [f.get_center() for f in mobj.small_flames]

                mobj.original_height = mobj.height
                mobj.time_elapsed = 0.0

                # Initialize small flame data
                mobj.flame_data = []
                for i, f in enumerate(mobj.small_flames):
                    f.move_to(mobj.initial_positions[i] + np.array([random.uniform(-0.1, 0.1), 0, 0]))
                    f.set_fill(opacity=1.0)
                    f.set_stroke(opacity=1.0)

                    upward_speed = random.uniform(0.5, 1.0)
                    fade_speed = random.uniform(0.5, 1.0)
                    mobj.flame_data.append({
                        'upward_speed': upward_speed,
                        'fade_speed': fade_speed,
                    })

                # The 3 main flames are the first 3 submobjects
                mobj.main_flames = mobj.submobjects[0:3]

                # Initialize independent flicker parameters for each main flame layer
                mobj.main_flame_data = []
                for mf in mobj.main_flames:
                    mobj.main_flame_data.append({
                        'center': mf.get_center(),
                        'amplitude': random.uniform(0.01, 0.03),
                        'frequency': random.uniform(1.5, 3.0),
                        'phase': random.uniform(0, 2 * math.pi),
                        'current_angle': 0,
                        'time_since_flip': 0.0,
                        'next_flip_time': random.uniform(0.3, 1.0),
                        'flipped': False,
                    })

            mobj.time_elapsed += dt

            # Update the three main flame layers with independent rotations
            for i, (mf, mf_data) in enumerate(zip(mobj.main_flames, mobj.main_flame_data)):
                # Compute this flame's flicker angle
                local_time = mobj.time_elapsed
                angle = mf_data['amplitude'] * math.sin(local_time * mf_data['frequency'] * TAU + mf_data['phase'])

                # Rotate this flame about its own center
                delta = angle - mf_data['current_angle']
                mf.rotate(delta, about_point=mf_data['center'])
                mf_data['current_angle'] = angle

                # Update flipping only for the inner main flames (i.e., not the topmost one)
                if i in (1,):
                    mf_data['time_since_flip'] += dt
                    if mf_data['time_since_flip'] > mf_data['next_flip_time']:
                        # Time to flip horizontally => Flip about its center by scaling in X by -1
                        mf.scale([-1, 1, 1], about_point=mf_data['center'])
                        mf_data['flipped'] = not mf_data['flipped']
                        mf_data['time_since_flip'] = 0.0
                        mf_data['next_flip_time'] = (3 - i) * random.uniform(0.3, 1.0)


            # Update each small flame
            for i, f in enumerate(mobj.small_flames):
                data = mobj.flame_data[i]

                # Move upward
                f.shift(UP * data['upward_speed'] * dt)

                current_opacity = f.get_fill_opacity()
                new_opacity = current_opacity - data['fade_speed'] * dt

                f.set_fill(opacity=new_opacity)
                f.set_stroke(opacity=new_opacity)

                flame_pos = f.get_center()
                if new_opacity <= 0.0 or (flame_pos[1] - mobj.initial_positions[i][1]) > 0.5:
                    new_x = mobj.initial_positions[i][0] + random.uniform(-0.1, 0.1)
                    new_y = mobj.initial_positions[i][1] - random.uniform(0.05, 0.15)
                    f.move_to([new_x, new_y, 0])

                    f.set_fill(opacity=1.0)
                    f.set_stroke(opacity=1.0)

                    data['upward_speed'] = random.uniform(0.5, 1.0)
                    data['fade_speed'] = random.uniform(0.5, 1.0)


        def burn(vertex: int, run_time: float = 0.5):
            # Set node on fire (🔥)
            fire_icon = SVGMobject('bfs/fire.svg').scale(0.7).move_to(graph.vertices[vertex], DOWN)
            fire_icon.set_z_index(5)
            self.play(ShowIncreasingSubsets(fire_icon, run_time=run_time))

            # Add updater to the fire
            fire_icon.add_updater(update_fire)
            return fire_icon

        def spread_fire(source: int, target: int, run_time: float = 0.5):
            sparkler = SVGMobject('bfs/sparks.svg').scale(0.3).move_to(graph.vertices[source], DOWN).set_fill('#ff9d33')
            sparkler.set_z_index(5)

            edge = Line(graph.vertices[source].get_center(), graph.vertices[target].get_center(), buff=0.4)
            burned_edge = VMobject()
            burned_edge.add_updater(lambda x: x.become(Line(
                edge.get_start(), sparkler.get_center(), stroke_width=6,
            ).set_color(DARK_GRAY)))
            self.add(sparkler, burned_edge)

            self.play(MoveAlongPath(sparkler, edge, run_time=run_time, rate_func=linear))
            self.remove(sparkler)
            burning_target = burn(target, run_time=run_time / 2)
            return burning_target

        burn(7)
        self.wait(1)
        spread_fire(7, 5, run_time=0.5)
        spread_fire(7, 6, run_time=0.5)
        self.wait(1)
        spread_fire(5, 8, run_time=0.4)
        spread_fire(5, 3, run_time=0.4)
        spread_fire(5, 4, run_time=0.4)
        self.wait(1)
        spread_fire(6, 10, run_time=0.4)
        spread_fire(8, 9, run_time=0.4)
        self.wait(0.5)
        spread_fire(10, 11, run_time=0.5)
        spread_fire(9, 2, run_time=0.5)
        self.wait(0.5)
        spread_fire(2, 0, run_time=0.3)
        spread_fire(2, 1, run_time=0.3)
        self.wait(2)


class IntroductionImplementation(Scene):
    def construct(self):
        code = Code(
            code=dedent('''
                used[start] = True
                q = deque([start])

                while q:
                    v = q.popleft()
                    for to in g[v]:
                        if not used[to]:
                            q.append(to)
                            used[to] = True
            ''').strip(),
            tab_width=4,
            language='Python',
            line_spacing=0.6,
            font='Monospace',
            style='monokai',
        ).center().code

        for line in code.chars:
            if line:
                self.play(AddTextLetterByLetter(line, run_time=0.1 * len(line)))
        self.wait(2)


class DisplayMultipleGraphs(Scene):
    def construct(self):
        graphs = [
            (nx.complete_graph(5), 'Complete Graph K5'),
            (nx.cycle_graph(6), 'Cycle Graph C6'),
            (nx.star_graph(5), 'Star Graph'),
            (nx.wheel_graph(6), 'Wheel Graph W6'),
            (nx.path_graph(6), 'Path Graph P6'),
            (nx.erdos_renyi_graph(10, 0.4, seed=42), 'Erdős-Rényi Graph'),
        ]

        for graph, name in graphs:
            title = Text(name).scale(0.7).to_edge(UP)
            g = Graph(
                list(graph.nodes),
                list(graph.edges),
                layout='spring',
                labels=True,
                layout_scale=3,
                vertex_config={'radius': 0.4, 'stroke_width': 0, 'fill_color': WHITE},
                edge_config={'stroke_width': 5},
            ).next_to(title, DOWN)

            self.play(Create(g), Write(title))
            self.wait(2)
            self.play(FadeOut(g), FadeOut(title), run_time=0.2)
            self.wait(0.5)


class GraphDefinition(Scene):
    def construct(self):
        title = Title('Graphs', include_underline=False)
        self.play(Write(title), run_time=0.2)

        vertices = list(range(len(g)))
        edges = [(i, j) for i, neighbors in enumerate(g) for j in neighbors]

        graph = Graph(
            vertices, edges,
            layout=layout,
            labels=True,
            vertex_config={'radius': 0.4, 'stroke_width': 0, 'fill_color': WHITE},
            edge_config={'stroke_width': 5},
        ).shift(1.5 * DOWN).scale(0.8)

        # Create all the vertices (not edges yet)
        self.play(Create(VGroup(*graph.vertices.values())), run_time=0.2)
        self.wait(0.1)

        # Create all the edges
        self.play(Create(VGroup(
            *[item.set_z_index(-1) for item in graph.edges.values()]
        )), *[
            label.animate.set_z_index(100000)
            for label in graph._labels.values()
        ], run_time=0.1)
        self.wait(0.2)

        # Indicate the graph
        self.play(Indicate(graph), run_time=0.1)
        self.wait(0.2)

        # Replace the graph with a complete graph
        complete = nx.complete_graph(6)
        complete_graph = Graph(
            list(complete.nodes),
            list(complete.edges),
            layout='spring',
            labels=True,
            layout_scale=3,
            vertex_config={'radius': 0.4, 'stroke_width': 0, 'fill_color': WHITE},
            edge_config={'stroke_width': 5},
        ).move_to(graph).scale(0.8)
        self.play(ReplacementTransform(graph, complete_graph), run_time=0.1)
        self.wait(0.2)

        # Replace the complete graph with a tree
        tree = nx.balanced_tree(2, 3)
        tree_graph = Graph(
            list(tree.nodes),
            list(tree.edges),
            root_vertex=0,
            layout='tree',
            labels=True,
            layout_scale=3,
            vertex_config={'radius': 0.4, 'stroke_width': 0, 'fill_color': WHITE},
            edge_config={'stroke_width': 5},
        ).move_to(complete_graph).scale(0.8)
        self.play(ReplacementTransform(complete_graph, tree_graph), run_time=0.1)
        self.wait(0.2)

        # Replace the tree with a directed graph
        vertices = [i for i in range(5)]
        edges = [(0, 1), (1, 2), (3, 2), (3, 4), (4, 0), (4, 2)]
        directed_graph = DiGraph(
            vertices, edges,
            layout='circular',
            labels=True,
            layout_scale=3,
            vertex_config={'radius': 0.4, 'stroke_width': 0, 'fill_color': WHITE},
            edge_config={'stroke_width': 5},
        ).move_to(tree_graph).scale(0.8)
        self.play(FadeOut(tree_graph), run_time=0.1)
        self.play(Create(directed_graph), run_time=1)
        self.wait(2)

