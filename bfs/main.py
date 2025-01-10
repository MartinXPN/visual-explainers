import math
import random
from collections import deque
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
        self.wait(2)

        def burn(vertex: int, run_time: float = 0.5):
            fire_icon = SVGMobject('bfs/fire.svg').scale(0.7).move_to(graph.vertices[vertex], DOWN)
            fire_icon.set_z_index(5)
            self.play(ShowIncreasingSubsets(fire_icon, run_time=run_time))
            fire_icon.add_updater(update_fire)
            return fire_icon

        def spread_fire(source: int, target: int, run_time: float = 0.5):
            sparkler = SVGMobject('bfs/sparks.svg').scale(0.25).move_to(graph.vertices[source], DOWN).set_fill('#ff9d33')
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
        spread_fire(7, 5, run_time=0.3)
        spread_fire(7, 6, run_time=0.3)
        self.wait(0.5)
        spread_fire(5, 8, run_time=0.2)
        spread_fire(5, 4, run_time=0.2)
        spread_fire(5, 3, run_time=0.2)
        self.wait(0.5)
        spread_fire(6, 10, run_time=0.2)
        spread_fire(8, 9, run_time=0.2)
        self.wait(0.4)
        spread_fire(10, 11, run_time=0.6)
        spread_fire(9, 2, run_time=0.3)
        self.wait(0.3)
        spread_fire(2, 0, run_time=0.1)
        spread_fire(2, 1, run_time=0.1)
        self.wait(5)


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
        self.play(Write(title), run_time=1)
        self.wait(0.25)

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
        self.play(Create(VGroup(*graph.vertices.values())), run_time=1)
        self.wait(2)

        # Create all the edges
        self.play(Create(VGroup(
            *[item.set_z_index(-1) for item in graph.edges.values()]
        )), *[
            label.animate.set_z_index(100000)
            for label in graph._labels.values()
        ], run_time=1)
        self.wait(2)

        # Indicate the graph
        self.play(Indicate(graph), run_time=1)
        self.wait(0.5)

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
        self.play(ReplacementTransform(graph, complete_graph), run_time=0.4)
        self.wait(0.5)

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
        self.play(ReplacementTransform(complete_graph, tree_graph), run_time=0.4)
        self.wait(1)

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
        self.play(FadeOut(tree_graph), run_time=0.2)
        self.play(Create(directed_graph), run_time=0.5)
        self.wait(6)


class Motivation(Scene):
    def construct(self):
        title = Title('Graph Applications', include_underline=False)
        self.play(Write(title), run_time=1)
        self.wait(2.5)

        # Draw a graph with one node in the center and 5 nodes around it (friends)
        vertices = list(range(6))
        edges = [(0, i) for i in range(1, 6)]
        graph = Graph(
            vertices, edges,
            layout='spring',
            layout_scale=3,
            vertex_config={'radius': 0.6, 'stroke_width': 4, 'fill_color': BLACK, 'stroke_color': WHITE},
            edge_config={'stroke_width': 5},
        ).shift(0.2 * DOWN).scale(0.8)

        person = SVGMobject('bfs/person.svg').scale(0.2)
        central = person.copy().move_to(graph.vertices[0]).set_fill(ORANGE)
        friends = VGroup(*[person.copy().move_to(graph.vertices[i]).set_fill(WHITE) for i in range(1, 6)])

        self.play(
            Create(graph),
            Create(central),
            *[Create(p) for p in friends],
            run_time=1,
        )
        self.wait(2)

        # Draw a graph of web page documents
        vertices = list(range(10))
        edges = [(0, i) for i in range(1, 6)]
        edges += [(1, 9), (0, 7), (5, 6), (5, 8), (8, 9), (9, 2)]
        web_graph = Graph(
            vertices, edges,
            layout='kamada_kawai',
            layout_scale=3,
            vertex_config={'radius': 0.6, 'stroke_width': 4, 'fill_color': BLACK, 'stroke_color': WHITE},
            edge_config={'stroke_width': 5},
        ).scale(0.8)
        webpage_icon = SVGMobject('bfs/webpage.svg').scale(0.2)
        webpages = [
            webpage_icon.copy().set_fill(ORANGE if i == 0 else YELLOW).move_to(web_graph.vertices[i])
            for i in range(10)
        ]

        self.play(
            ReplacementTransform(graph, web_graph),
            *[Create(p) for p in webpages],
            FadeOut(central, *friends),
            run_time=1,
        )
        self.wait(0.5)

        # Indicate nodes of web_graph + webpages
        self.play(
            *[Indicate(n, scale_factor=1.1) for n in web_graph.vertices.values()],
            *[Indicate(p, scale_factor=1.2, color=BLACK) for p in webpages],
            run_time=1,
        )
        self.wait(1)

        # Indicate the edges of web_graph
        self.play(
            *[Indicate(edge, scale_factor=1.5, color=ORANGE) for edge in web_graph.edges.values()],
            run_time=2,
        )

        vertices = list(range(len(g)))
        edges = [(i, j) for i, neighbors in enumerate(g) for j in neighbors]
        shortest_path_graph = Graph(
            vertices, edges,
            layout=layout,
            labels=True,
            vertex_config={'radius': 0.4, 'stroke_width': 0, 'fill_color': WHITE},
            edge_config={'stroke_width': 5},
        ).shift(1.5 * DOWN)

        self.play(
            ReplacementTransform(web_graph, shortest_path_graph),
            FadeOut(*webpages),
            run_time=0.5,
        )
        self.wait(0.5)

        # Highlight node 7 with yellow
        self.play(
            shortest_path_graph.vertices[7].animate.set_fill(YELLOW),
            shortest_path_graph._labels[7].animate.set_z_index(100000),
            run_time=0.5,
        )

        # Draw a dotted circle around node 2
        target = DashedVMobject(Circle(radius=0.6, color=ORANGE)).move_to(shortest_path_graph.vertices[2])
        self.play(Create(target), run_time=0.5)
        self.wait(0.5)

        # Show pass-through animation going through nodes 7 -> 5 -> 8 -> 9 -> 2
        path = [7, 5, 8, 9, 2]
        dot = Dot().set_fill(YELLOW).move_to(shortest_path_graph.vertices[7])
        for i in range(len(path) - 1):
            cur = path[i]
            to = path[i + 1]
            edge = Line(
                shortest_path_graph.vertices[cur].get_center(),
                shortest_path_graph.vertices[to].get_center(),
                buff=0.4,
            )
            burned_edge = VMobject()
            burned_edge.add_updater(lambda x: x.become(Line(
                edge.get_start(), dot.get_center(), stroke_width=6,
            ).set_color(YELLOW)))
            self.add(dot, burned_edge)

            self.play(MoveAlongPath(dot, edge, run_time=0.2, rate_func=linear), run_time=0.2)
            self.play(
                shortest_path_graph.vertices[to].animate.set_fill(YELLOW),
                shortest_path_graph._labels[to].animate.set_z_index(100000),
                shortest_path_graph.edges[cur, to].animate.set_color(YELLOW),
                shortest_path_graph.edges[to, cur].animate.set_color(YELLOW),
                run_time=0.05,
            )
            self.remove(burned_edge, edge)


        self.play(FadeOut(dot), run_time=0.2)
        self.wait(2)

        # Walk the path 7 -> 6 -> 10 -> 8 -> 9
        # Highlight node 7 with orange
        self.play(
            shortest_path_graph.vertices[7].animate.set_fill(ORANGE),
            shortest_path_graph._labels[7].animate.set_z_index(100000),
            run_time=0.2,
        )
        path = [7, 6, 10, 8, 9]
        dot = Dot().set_fill(ORANGE).move_to(shortest_path_graph.vertices[7])
        for i in range(len(path) - 1):
            cur = path[i]
            to = path[i + 1]
            edge = Line(
                shortest_path_graph.vertices[cur].get_center(),
                shortest_path_graph.vertices[to].get_center(),
                buff=0.4,
            )
            burned_edge = VMobject()
            burned_edge.add_updater(lambda x: x.become(Line(
                edge.get_start(), dot.get_center(), stroke_width=6,
            ).set_color(ORANGE)))
            self.add(dot, burned_edge)

            self.play(MoveAlongPath(dot, edge, run_time=0.2, rate_func=linear), run_time=0.4)
            self.play(
                shortest_path_graph.vertices[to].animate.set_fill(ORANGE),
                shortest_path_graph._labels[to].animate.set_z_index(100000),
                shortest_path_graph.edges[cur, to].animate.set_color(ORANGE),
                shortest_path_graph.edges[to, cur].animate.set_color(ORANGE),
                run_time=0.1,
            )
            self.remove(burned_edge, edge)

        self.play(FadeOut(dot), run_time=0.2)
        # Show a search icon and drop it on node 9
        search = (SVGMobject('bfs/search.svg')
                  .move_to(shortest_path_graph.vertices[9])
                  .shift(0.25 * DOWN).shift(0.25 * RIGHT)
                  .set_fill(RED).set_z_index(1000000))
        self.play(FadeIn(search), run_time=0.5)
        self.wait(1)
        self.play(FadeOut(search), run_time=0.2)

        # Draw a dotted line between node 9 and 14
        connection = DashedLine(
            shortest_path_graph.vertices[9].get_center(),
            shortest_path_graph.vertices[14].get_center(),
            dashed_ratio=0.5,
            dash_length=0.1,
            buff=0.4,
            color=RED,
        )
        self.play(Create(connection), run_time=0.5)
        self.wait(2)

        # Transition to the next scene
        self.play(
            *[edge.animate.set_color(WHITE) for edge in shortest_path_graph.edges.values()],
            *[vertex.animate.set_fill(WHITE) for vertex in shortest_path_graph.vertices.values()],
            *[label.animate.set_z_index(10) for label in shortest_path_graph._labels.values()],
            FadeOut(connection, target),
            run_time=1,
        )
        self.play(
            ReplacementTransform(title, Title('Breadth First Search', include_underline=False)),
            run_time=1,
        )
        self.wait(2)


class BFSOnGraph(Scene):
    def construct(self):
        title = Title('Breadth First Search', include_underline=False)
        vertices = list(range(len(g)))
        edges = [(i, j) for i, neighbors in enumerate(g) for j in neighbors]
        graph = Graph(
            vertices, edges,
            layout=layout,
            labels=True,
            vertex_config={'radius': 0.4, 'stroke_width': 0, 'fill_color': WHITE},
            edge_config={'stroke_width': 5},
        ).shift(1.5 * DOWN)

        self.add(title, graph)
        for label in graph._labels.values():
            label.set_z_index(10)
        self.wait(1)

        # Indicate the graph + node 7
        self.play(Indicate(graph, scale_factor=1.1), run_time=1)
        self.wait(2)
        self.play(
            Indicate(graph.vertices[7], color=ORANGE),
            graph._labels[7].animate.set_z_index(100000),
            run_time=4,
        )
        self.wait(0.5)

        def burn(vertex: int, run_time: float = 0.5):
            fire_icon = SVGMobject('bfs/fire.svg').scale(0.7).move_to(graph.vertices[vertex], DOWN)
            fire_icon.set_z_index(5)
            self.play(ShowIncreasingSubsets(fire_icon, run_time=run_time))
            fire_icon.add_updater(update_fire)
            return fire_icon

        def spread_fire(source: int, target: int, run_time: float = 0.5):
            sparkler = SVGMobject('bfs/sparks.svg').scale(0.25).move_to(graph.vertices[source], DOWN).set_fill('#ff9d33')
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
            return burning_target, burned_edge

        burning_icons = {}
        burning_icons[7] = burn(7)
        self.wait(1)
        burning_icons[5] = spread_fire(7, 5, run_time=0.6)
        burning_icons[6] = spread_fire(7, 6, run_time=0.6)
        self.wait(2)
        burning_icons[8] = spread_fire(5, 8, run_time=0.4)
        burning_icons[4] = spread_fire(5, 4, run_time=0.4)
        burning_icons[3] = spread_fire(5, 3, run_time=0.4)
        burning_icons[10] = spread_fire(6, 10, run_time=0.4)
        self.wait(1)
        burning_icons[9] = spread_fire(8, 9, run_time=0.5)
        burning_icons[11] = spread_fire(10, 11, run_time=0.4)
        self.wait(0.8)
        burning_icons[2] = spread_fire(9, 2, run_time=0.5)
        self.wait(0.8)
        burning_icons[0] = spread_fire(2, 0, run_time=0.4)
        burning_icons[1] = spread_fire(2, 1, run_time=0.4)
        self.wait(6)

        # Dotted circle around all the nodes accessible from 7
        accessible = [5, 6, 8, 4, 3, 10, 9, 11, 2, 0, 1]
        circles = []
        animations = []
        for v in accessible:
            circles.append(DashedVMobject(Circle(radius=0.6, color=YELLOW)).move_to(graph.vertices[v]))
            animations.append(FadeOut(*burning_icons[v]))
            animations.append(graph.vertices[v].animate.set_fill(YELLOW))
            animations.append(graph._labels[v].animate.set_z_index(100000))
            animations.append(Create(circles[-1]))
        self.play(LaggedStart(*animations, lag_ratio=0.5), run_time=1)
        self.wait(0.5)

        circle = DashedVMobject(Circle(radius=0.6, color=ORANGE)).move_to(graph.vertices[7])
        self.play(LaggedStart(
            FadeOut(*burning_icons[7]),
            graph.vertices[7].animate.set_fill(ORANGE),
            graph._labels[7].animate.set_z_index(100000),
            Create(circle),
            lag_ratio=0.7,
        ), run_time=1)
        self.wait(3)

        # Transition to the next scene
        self.play(
            FadeOut(*circles, circle),
            *[edge.animate.set_color(WHITE) for edge in graph.edges.values()],
            *[vertex.animate.set_fill(WHITE) for vertex in graph.vertices.values()],
            *[label.animate.set_z_index(10) for label in graph._labels.values()],
            ReplacementTransform(title, Title('BFS State', include_underline=False)),
            run_time=1,
        )
        self.wait(1)


class BFSState(Scene):
    def construct(self):
        title = Title('BFS State', include_underline=False)
        vertices = list(range(len(g)))
        edges = [(i, j) for i, neighbors in enumerate(g) for j in neighbors]
        graph = Graph(
            vertices, edges,
            layout=layout,
            labels=True,
            vertex_config={'radius': 0.4, 'stroke_width': 0, 'fill_color': WHITE},
            edge_config={'stroke_width': 5},
        ).shift(1.5 * DOWN)

        self.add(title, graph)
        for label in graph._labels.values():
            label.set_z_index(10)
        self.wait(0.1)

        self.play(graph.animate.scale(0.25).next_to(title, DOWN, buff=0.5), run_time=0.5)
        self.wait(0.5)

        # Split the screen into 3 sections (below the graph)
        screen_width = config.frame_width
        section_width = screen_width / 3
        left = Line(
            start=section_width * LEFT / 2 + 3 * DOWN,
            end=section_width * LEFT / 2 + UP / 2,
        ).set_stroke(WHITE, 2)
        right = Line(
            start=section_width * RIGHT / 2 + 3 * DOWN,
            end=section_width * RIGHT / 2 + UP / 2,
        ).set_stroke(WHITE, 2)
        self.play(Create(left), Create(right), run_time=1)
        self.wait(3)

        # Write Burning state in the first column
        burning_title = Text('Burning State').scale(0.7).next_to(left, LEFT, buff=0.5).align_to(left, UP)
        self.play(Write(burning_title), run_time=1)
        self.wait(1)

        # Draw an untouched node and a burning node (O/🔥)
        untouched = Circle(radius=0.2, color=WHITE, fill_opacity=1).next_to(burning_title, 2 * DOWN).shift(LEFT)
        slash = Text('/').scale(1.5).next_to(untouched, RIGHT)
        burning = SVGMobject('bfs/fire.svg').scale(0.3).next_to(slash, RIGHT).shift(0.05 * UP)

        self.play(LaggedStart(Create(untouched), Write(slash), ShowIncreasingSubsets(burning), lag_ratio=0.5), run_time=1)
        burning.add_updater(update_fire)
        self.wait(2)

        # Write Burning Nodes in the second column
        burning_nodes_title = Text('Burning Nodes').scale(0.7).next_to(right, LEFT, buff=1).align_to(right, UP)
        self.play(Write(burning_nodes_title), run_time=1)

        def burn(vertex: int, run_time: float = 0.5):
            fire_icon = SVGMobject('bfs/fire.svg').scale(0.7 * 0.25).move_to(graph.vertices[vertex], DOWN)
            fire_icon.set_z_index(5)
            self.play(ShowIncreasingSubsets(fire_icon, run_time=run_time))
            fire_icon.add_updater(update_fire)
            return fire_icon

        def spread_fire(source: int, target: int, run_time: float = 0.5):
            sparkler = SVGMobject('bfs/sparks.svg').scale(0.3 * 0.25).move_to(graph.vertices[source], DOWN).set_fill('#ff9d33')
            sparkler.set_z_index(5)

            edge = Line(graph.vertices[source].get_center(), graph.vertices[target].get_center(), buff=0.4 * 0.25)
            burned_edge = VMobject()
            burned_edge.add_updater(lambda x: x.become(Line(
                edge.get_start(), sparkler.get_center(), stroke_width=6,
            ).set_color(DARK_GRAY)))
            self.add(sparkler, burned_edge)

            self.play(MoveAlongPath(sparkler, edge, run_time=run_time, rate_func=linear))
            self.remove(sparkler)
            burning_target = burn(target, run_time=run_time / 2)
            return burning_target, burned_edge

        burning_icons = {}
        burning_icons[7] = burn(7)
        self.wait(0.2)
        burning_icons[5] = spread_fire(7, 5, run_time=0.05)
        burning_icons[6] = spread_fire(7, 6, run_time=0.05)
        self.wait(0.2)
        burning_icons[8] = spread_fire(5, 8, run_time=0.05)
        burning_icons[4] = spread_fire(5, 4, run_time=0.05)
        burning_icons[3] = spread_fire(5, 3, run_time=0.05)
        burning_icons[10] = spread_fire(6, 10, run_time=0.05)
        self.wait(0.2)

        # Draw a queue with the burning nodes (8, 4, 3, 10)
        queue = []
        queue_texts = []
        def add2queue(vertex: int):
            nonlocal queue
            fire_icon = SVGMobject('bfs/fire.svg').scale(0.3)
            fire_icon.next_to(burning_nodes_title if len(queue) == 0 else queue[-1], DOWN, buff=0.4 if len(queue) == 0 else 0.2)
            fire_icon.set_z_index(5)
            queue.append(fire_icon)
            vertex_text = Text(str(vertex)).scale(0.4).set_color(BLACK).move_to(queue[-1]).shift(0.12 * DOWN).set_z_index(10)
            queue_texts.append(vertex_text)
            self.play(ShowIncreasingSubsets(queue[-1]), Write(vertex_text), run_time=0.2)
            queue[-1].add_updater(update_fire)

        add2queue(8)
        add2queue(4)
        add2queue(3)
        add2queue(10)
        self.wait(2)

        # Write Graph in the third column
        graph_title = Text('Graph').scale(0.7).next_to(right, RIGHT, buff=1).align_to(right, UP)
        self.play(Write(graph_title), run_time=1)

        code = Code(
            code=dedent('''
                g = [
                
                
                
                
                
                
                
                
                ]
            ''').strip(),
            tab_width=4,
            language='Python',
            line_spacing=0.6,
            font='Monospace',
            style='monokai',
        ).scale(0.7).next_to(graph_title, DOWN).shift(0.5 * LEFT).code

        for line in code.chars:
            if line:
                self.play(AddTextLetterByLetter(line, run_time=0.05 * len(line)))

        graph_copy = graph.copy()
        self.play(
            graph_copy.animate.scale(0.9).align_to(code, LEFT).align_to(code, DOWN).shift(0.6 * UP).shift(0.2 * RIGHT),
            run_time=0.5,
        )
        self.wait(1)

        # Indicate the 3rd column
        self.play(Indicate(graph_copy), Indicate(graph_title), Indicate(code), run_time=1)
        self.wait(0.5)

        # Transition to the next scene
        # Move the graph copy to the left (and make it bigger) + fade out the top graph
        # Move the graph_title to the top (make it the title)
        # Fade out the rest
        new_graph_title = Title('Graph', include_underline=False)
        self.play(LaggedStart(
            FadeOut(burning_title, burning_nodes_title, left, right, slash, burning, untouched, *queue, *queue_texts),
            FadeOut(title, graph, *[icon[0] for icon in burning_icons.values()], *[icon[1] for icon in burning_icons.values()]),
            graph_title.animate.align_to(new_graph_title, UP).align_to(new_graph_title, LEFT).scale(1.1),
            code.animate.scale(1.2).next_to(new_graph_title, DOWN, buff=1).shift(2.5 * RIGHT),
            graph_copy.animate.scale(2.5).next_to(new_graph_title, DOWN, buff=1).to_edge(LEFT, buff=1),
            lag_ratio=0.5,
            run_time=1,
        ))
        self.wait(0.01)


class GraphRepresentation(Scene):
    def construct(self):
        title = Title('Graph', include_underline=False)
        vertices = list(range(len(g)))
        edges = [(i, j) for i, neighbors in enumerate(g) for j in neighbors]
        graph = Graph(
            vertices, edges,
            layout=layout,
            labels=True,
            vertex_config={'radius': 0.4, 'stroke_width': 0, 'fill_color': WHITE},
            edge_config={'stroke_width': 5},
        ).scale(0.25 * 0.9 * 2.5).next_to(title, DOWN, buff=1).to_edge(LEFT, buff=1)

        self.add(title, graph)
        for label in graph._labels.values():
            label.set_z_index(10)

        old_code = Code(
            code=dedent('''
                g = [








                ]
            ''').strip(),
            tab_width=4,
            language='Python',
            line_spacing=0.6,
            font='Monospace',
            style='monokai',
        ).scale(0.7).code.scale(1.2).next_to(title, DOWN, buff=1).shift(2.5 * RIGHT)
        self.add(old_code)
        self.wait(3)

        code = Code(
            code=dedent('''
                g = [
                    # Connections of 0
                    # Connections of 1
                    # Connections of 2
                    # Connections of 3
                    # Connections of 4
                    # Connections of 5
                    # Connections of 6
                    # Connections of 7
                    # Connections of 8
                    # Connections of 9
                    # ...
                    # Connections of 14
                    # Connections of 15
                    # Connections of 16
                ]
            ''').strip(),
            tab_width=4,
            language='Python',
            line_spacing=0.6,
            font='Monospace',
            style='monokai',
        ).scale(0.7).code.scale(1.2).align_to(old_code, LEFT).align_to(old_code, UP)

        self.play(FadeOut(old_code[-1]), run_time=0.2)
        for line in code.chars:
            self.play(AddTextLetterByLetter(line, run_time=0.03 * len(line)))
        self.play(FadeOut(old_code[:-1]), run_time=0.5)
        self.wait(2)

        self.play(Indicate(code.chars[0][0], scale_factor=2.5), run_time=2)
        self.wait(2)

        code_list = Code(
            code=dedent('''
                g = [
                    [2],              # 0
                    [2],              # 1
                    [0, 1, 9],        # 2
                    [5],              # 3
                    [9, 8, 5],        # 4
                    [3, 4, 8, 6, 7],  # 5
                    [5, 7, 10],       # 6
                    [5, 6],           # 7
                    [4, 5, 9, 10],    # 8
                    [4, 8, 2],        # 9
                    # ...
                    [12, 13],         # 14
                    [16],             # 15
                    [15],             # 16
                ]
            ''').strip(),
            tab_width=4,
            language='Python',
            line_spacing=0.6,
            font='Monospace',
            style='monokai',
        ).scale(0.7).code.scale(1.2).align_to(old_code, LEFT).align_to(old_code, UP)

        self.play(RemoveTextLetterByLetter(code[1], run_time=0.01 * len(code[1])))
        self.wait(1)
        self.play(AddTextLetterByLetter(code_list[1], run_time=0.05 * len(code_list[1])))

        for i in range(2, 8):
            self.play(RemoveTextLetterByLetter(code[i], run_time=0.006 * len(code[i])))
            self.play(AddTextLetterByLetter(code_list[i], run_time=0.01 * len(code_list[i])))
        self.play(RemoveTextLetterByLetter(code[8], run_time=0.01 * len(code[8])))
        self.wait(0.5)
        self.play(AddTextLetterByLetter(code_list[8], run_time=0.1 * len(code_list[8])))
        self.play(RemoveTextLetterByLetter(code[9], run_time=0.01 * len(code[9])))
        self.wait(1.5)
        self.play(AddTextLetterByLetter(code_list[9], run_time=0.1 * len(code_list[9])))

        for i in range(10, 11):
            self.play(RemoveTextLetterByLetter(code[i], run_time=0.006 * len(code[i])))
            self.play(AddTextLetterByLetter(code_list[i], run_time=0.01 * len(code_list[i])))
        for i in range(-4, -1):
            self.play(RemoveTextLetterByLetter(code[i], run_time=0.006 * len(code[i])))
            self.play(AddTextLetterByLetter(code_list[i], run_time=0.01 * len(code_list[i])))

        # Highlight node 8 and node 9 + their connection
        connection_8_9 = DashedVMobject(Circle(radius=0.3, color=ORANGE)).move_to(code_list[9][8])
        connection_9_8 = DashedVMobject(Circle(radius=0.3, color=ORANGE)).move_to(code_list[10][5])
        self.play(LaggedStart(
            graph.vertices[8].animate.set_fill(ORANGE),
            graph._labels[8].animate.set_z_index(100000),
            Create(connection_8_9),
            graph.edges[8, 9].animate.set_color(ORANGE),
            graph.edges[9, 8].animate.set_color(ORANGE),
            graph.vertices[9].animate.set_fill(ORANGE),
            graph._labels[9].animate.set_z_index(100000),
            Create(connection_9_8),
            lag_ratio=0.5,
            run_time=2,
        ))
        self.wait(2)

        # Move from node 8 to node 9 and back
        dot = Dot().set_fill(YELLOW).move_to(graph.vertices[8])
        line_8_9 = Line(graph.vertices[8].get_center(), graph.vertices[9].get_center(), buff=0.22)
        line_9_8 = Line(graph.vertices[9].get_center(), graph.vertices[8].get_center(), buff=0.22)
        self.play(MoveAlongPath(dot, line_8_9, run_time=0.2, rate_func=linear), run_time=2)
        self.remove(dot)
        self.wait(0.1)
        self.play(MoveAlongPath(dot, line_9_8, run_time=0.2, rate_func=linear), run_time=1)
        self.remove(dot)
        self.wait(4)

        # Draw an arrow from 8 to 9
        arrow = Arrow(
            graph.vertices[8].get_center(),
            graph.vertices[9].get_center(),
            buff=0.22,
            color=YELLOW,
        )
        self.play(Create(arrow), run_time=1)
        self.wait(5)

        # Transition to the next scene
        scene_title = Title('BFS State', include_underline=False)
        screen_width = config.frame_width
        section_width = screen_width / 3
        left = Line(start=section_width * LEFT / 2 + 3 * DOWN, end=section_width * LEFT / 2 + UP / 2).set_stroke(WHITE, 2)
        right = Line(start=section_width * RIGHT / 2 + 3 * DOWN, end=section_width * RIGHT / 2 + UP / 2).set_stroke(WHITE, 2)

        self.play(LaggedStart(
            FadeOut(arrow),
            graph.vertices[8].animate.set_fill(WHITE),
            graph._labels[8].animate.set_z_index(100000),
            FadeOut(connection_8_9),
            graph.edges[8, 9].animate.set_color(WHITE),
            graph.edges[9, 8].animate.set_color(WHITE),
            graph.vertices[9].animate.set_fill(WHITE),
            graph._labels[9].animate.set_z_index(100000),
            FadeOut(connection_9_8),
            FadeOut(code),
            lag_ratio=0.5,
            run_time=0.5,
        ))
        self.wait(0.5)

        self.play(LaggedStart(
            code_list.animate.scale(0.8).to_edge(RIGHT, buff=1).to_edge(DOWN, buff=0.3),
            graph.animate.scale(0.45).next_to(title, DOWN, buff=0.5),
            ReplacementTransform(title, scene_title),
            FadeIn(left, right),
            lag_ratio=0.5,
            run_time=1,
        ))

        burning_title = Text('Burning State').scale(0.7).next_to(left, LEFT, buff=0.5).align_to(left, UP)
        burning_nodes_title = Text('Burning Nodes').scale(0.7).next_to(right, LEFT, buff=1).align_to(right, UP)
        self.play(Write(burning_title), Write(burning_nodes_title), run_time=0.2)

        # Draw an untouched node and a burning node (O/🔥)
        untouched = Circle(radius=0.2, color=WHITE, fill_opacity=1).next_to(burning_title, 2 * DOWN).shift(LEFT)
        slash = Text('/').scale(1.5).next_to(untouched, RIGHT)
        burning = SVGMobject('bfs/fire.svg').scale(0.3).next_to(slash, RIGHT).shift(0.05 * UP)

        self.add(untouched, slash, burning)
        burning.add_updater(update_fire)

        queue = []
        queue_texts = []
        def add2queue(vertex: int):
            nonlocal queue
            fire_icon = SVGMobject('bfs/fire.svg').scale(0.3)
            fire_icon.next_to(burning_nodes_title if len(queue) == 0 else queue[-1], DOWN, buff=0.4 if len(queue) == 0 else 0.2)
            fire_icon.set_z_index(5)
            queue.append(fire_icon)
            vertex_text = Text(str(vertex)).scale(0.4).set_color(BLACK).move_to(queue[-1]).shift(0.12 * DOWN).set_z_index(10)
            queue_texts.append(vertex_text)
            self.add(queue[-1], vertex_text)
            queue[-1].add_updater(update_fire)

        add2queue(8)
        add2queue(4)
        add2queue(3)
        add2queue(10)
        self.wait(1)

        # Move "Burning State" to be the title
        self.play(LaggedStart(
            FadeOut(scene_title),
            burning_title.animate.scale(1.1).center().align_to(scene_title, UP),
            FadeOut(burning_nodes_title, left, right, code_list, *queue_texts, *queue),
            graph.animate.scale(2.5).next_to(scene_title, DOWN, buff=1).to_edge(RIGHT, buff=1),
            FadeOut(untouched, slash, burning),
            lag_ratio=0.5,
            run_time=1,
        ))
        self.wait(0.5)


class UsedState(Scene):
    def construct(self):
        title = Title('Burning State', include_underline=False)
        vertices = list(range(len(g)))
        edges = [(i, j) for i, neighbors in enumerate(g) for j in neighbors]
        graph = Graph(
            vertices, edges,
            layout=layout,
            labels=True,
            vertex_config={'radius': 0.4, 'stroke_width': 0, 'fill_color': WHITE},
            edge_config={'stroke_width': 5},
        ).scale(0.25 * 2.5).next_to(title, DOWN, buff=1).to_edge(RIGHT, buff=1)

        self.add(title, graph)
        for label in graph._labels.values():
            label.set_z_index(10)

        code = Code(
            code=dedent('''
                used = [
                    False,  # 0
                    False,  # 1
                    False,  # 2
                    False,  # 3
                    False,  # 4
                    False,  # 5
                    False,  # 6
                    False,  # 7
                    False,  # 8
                    False,  # 9
                    # ...
                    False,  # 14
                    False,  # 15
                    False,  # 16
                ]
            ''').strip(),
            tab_width=4,
            language='Python',
            line_spacing=0.6,
            font='Monospace',
            style='monokai',
        ).scale(0.7).code.scale(1.2).to_edge(LEFT, buff=1.5).to_edge(DOWN, buff=0.7)
        self.wait(4)
        self.play(AddTextLetterByLetter(code[0], run_time=0.1 * len(code[0])))
        self.wait(2)
        self.play(AddTextLetterByLetter(code[-1], run_time=0.1 * len(code[-1])))
        self.wait(1)
        self.play(Indicate(code[0], scale_factor=1.5), run_time=2)
        self.wait(4)

        for line in code.chars[1:-1]:
            self.play(AddTextLetterByLetter(line, run_time=0.01 * len(line)))
        self.wait(1)


        def burn(vertex: int, run_time: float = 0.5, scale: float = 0.6):
            fire_icon = SVGMobject('bfs/fire.svg').scale(0.7 * scale).move_to(graph.vertices[vertex], DOWN)
            fire_icon.set_z_index(5)
            self.play(ShowIncreasingSubsets(fire_icon, run_time=run_time))
            fire_icon.add_updater(update_fire)
            return fire_icon

        def spread_fire(source: int, target: int, run_time: float = 0.5, scale: float = 0.6):
            sparkler = SVGMobject('bfs/sparks.svg').scale(0.3 * scale).move_to(graph.vertices[source], DOWN).set_fill('#ff9d33')
            sparkler.set_z_index(5)

            edge = Line(graph.vertices[source].get_center(), graph.vertices[target].get_center(), buff=0.4 * scale)
            burned_edge = VMobject()
            burned_edge.add_updater(lambda x: x.become(Line(
                edge.get_start(), sparkler.get_center(), stroke_width=6,
            ).set_color(DARK_GRAY)))
            self.add(sparkler, burned_edge)

            self.play(MoveAlongPath(sparkler, edge, run_time=run_time, rate_func=linear))
            self.remove(sparkler)
            burning_target = burn(target, run_time=run_time / 2, scale=scale)
            return burning_target, burned_edge

        burning_icons = {}
        burning_icons[7] = burn(7)
        self.play(Circumscribe(code.chars[8], buff=0.02), run_time=1)

        true_code = Code(
            code=dedent('''
                used = [
                    True,   # 0
                    True,   # 1
                    True,   # 2
                    True,   # 3
                    True,   # 4
                    True,   # 5
                    True,   # 6
                    True,   # 7
                    True,   # 8
                    True,   # 9
                    # ...
                    True,   # 14
                    True,   # 15
                    True,   # 16
                ]
            ''').strip(),
            tab_width=4,
            language='Python',
            line_spacing=0.6,
            font='Monospace',
            style='monokai',
        ).scale(0.7).code.scale(1.2).to_edge(LEFT, buff=1.5).to_edge(DOWN, buff=0.7)

        self.play(RemoveTextLetterByLetter(code[8], run_time=0.01 * len(code[8])))
        self.play(AddTextLetterByLetter(true_code[8], run_time=0.05 * len(true_code[8])))
        self.wait(3)

        self.play(Indicate(true_code[8], scale_factor=1.5), run_time=2)
        self.wait(2)

        # Bring back the full scene with 3 sections
        scene_title = Title('BFS State', include_underline=False)
        screen_width = config.frame_width
        section_width = screen_width / 3
        left = Line(start=section_width * LEFT / 2 + 3 * DOWN, end=section_width * LEFT / 2 + UP / 2).set_stroke(WHITE, 2)
        right = Line(start=section_width * RIGHT / 2 + 3 * DOWN, end=section_width * RIGHT / 2 + UP / 2).set_stroke(WHITE, 2)

        code_list = Code(
            code=dedent('''
                g = [
                    [2],              # 0
                    [2],              # 1
                    [0, 1, 9],        # 2
                    [5],              # 3
                    [9, 8, 5],        # 4
                    [3, 4, 8, 6, 7],  # 5
                    [5, 7, 10],       # 6
                    [5, 6],           # 7
                    [4, 5, 9, 10],    # 8
                    [4, 8, 2],        # 9
                    # ...
                    [12, 13],         # 14
                    [16],             # 15
                    [15],             # 16
                ]
            ''').strip(),
            tab_width=4,
            language='Python',
            line_spacing=0.6,
            font='Monospace',
            style='monokai',
        ).scale(0.7).code.scale(0.95).to_edge(RIGHT, buff=1).to_edge(DOWN, buff=0.3)

        true_code = true_code.scale(0.8).to_edge(LEFT, buff=1).to_edge(DOWN, buff=0.3)
        self.play(
            code.animate.scale(0.8).to_edge(LEFT, buff=1).to_edge(DOWN, buff=0.3),
            true_code[8].animate.scale(1),
            run_time=0.1,
        )
        self.wait(1)
        self.play(LaggedStart(
            FadeOut(burning_icons[7]),
            graph.animate.scale(0.45).next_to(title, DOWN, buff=0.5),
            ReplacementTransform(title, scene_title),
            FadeIn(left, right),
            lag_ratio=0.5,
            run_time=1,
        ))

        burning_nodes_title = Text('Burning Nodes').scale(0.7).next_to(right, LEFT, buff=1).align_to(right, UP)
        self.play(Write(burning_nodes_title), FadeIn(code_list), run_time=0.2)
        self.wait(1)

        queue = []
        queue_texts = []
        def add2queue(vertex: int):
            nonlocal queue
            fire_icon = SVGMobject('bfs/fire.svg').scale(0.2)
            fire_icon.next_to(burning_nodes_title if len(queue) == 0 else queue[-1], DOWN, buff=0.4 if len(queue) == 0 else 0.2)
            fire_icon.set_z_index(5)
            queue.append(fire_icon)
            vertex_text = Text(str(vertex)).scale(0.3).set_color(BLACK).move_to(queue[-1]).shift(0.08 * DOWN).set_z_index(10)
            queue_texts.append(vertex_text)
            self.add(queue[-1], vertex_text)
            queue[-1].add_updater(update_fire)

        burning_icons: dict[int, tuple[SVGMobject, VMobject | None]] = {
            7: (burn(7, scale=0.3), None),
        }
        used = {7: True}
        add2queue(7)
        self.wait(1)

        def spread_from_source(vertex: int):
            # Circle around the queue front
            circle = DashedVMobject(Circle(radius=0.3, color=ORANGE)).move_to(queue_texts[0]).shift(0.1 * UP)
            self.play(Create(circle), run_time=0.2)
            self.wait(0.2)

            for to in g[vertex]:
                if used.get(to, False):
                    continue
                used[to] = True
                burning_icons[to] = spread_fire(vertex, to, scale=0.3)
                add2queue(to)
                self.wait(0.2)

            # Remove vertex from the queue front
            self.play(FadeOut(queue[0], queue_texts[0], circle), run_time=0.2)
            queue.pop(0)
            queue_texts.pop(0)
            animations = []
            for icon, text in zip(queue, queue_texts):
                icon.clear_updaters()
                delattr(icon, 'initialized')
                animations.append(AnimationGroup(
                    icon.animate.shift(0.6 * UP),
                    text.animate.shift(0.6 * UP),
                ))
            self.play(LaggedStart(*animations, lag_ratio=0.2, run_time=0.5))
            # Add updaters to burning queue elements
            for icon in queue:
                icon.add_updater(update_fire)

        spread_from_source(7)
        self.wait(1)
        spread_from_source(5)
        self.wait(1)
        spread_from_source(6)
        self.wait(2)

        # Replace the "burning nodes" text with Queue
        queue_title = Text('Queue').scale(0.7).move_to(burning_nodes_title)
        self.play(ReplacementTransform(burning_nodes_title, queue_title), run_time=1)
        self.wait(1)
        spread_from_source(3)
        self.wait(0.5)
        spread_from_source(4)
        self.wait(0.5)
        spread_from_source(8)
        self.wait(0.5)
        spread_from_source(10)
        self.wait(1)
        spread_from_source(9)
        self.wait(2)

        queue_code = Code(
            code=dedent('''
                from collections import deque
            ''').strip(),
            tab_width=4,
            language='Python',
            line_spacing=0.6,
            font='Monospace',
            style='monokai',
        ).scale(0.7).code.scale(0.95).move_to(queue_title)
        self.play(ReplacementTransform(queue_title, queue_code), run_time=1)
        self.wait(3)

        spread_from_source(11)
        self.wait(2)
        spread_from_source(2)
        self.wait(4)

        # Transition to the next scene
        self.play(LaggedStart(
            FadeOut(code, true_code[8]),
            FadeOut(queue_code, *queue, *queue_texts),
            FadeOut(
                *[icon[0] for icon in burning_icons.values()],
                *[icon[1] for icon in burning_icons.values() if icon[1] is not None],
            ),
            FadeOut(left, right),
            graph.animate.scale(1.4).next_to(scene_title, DOWN, buff=0.5).to_edge(LEFT, buff=1),
            code_list.animate.scale(1.2).next_to(scene_title, DOWN, buff=0.5).align_to(ORIGIN, LEFT),
            ReplacementTransform(scene_title, Title('BFS Implementation', include_underline=False)),
            run_time=2,
            lag_ratio=0.5,
        ))
        self.wait(1)


class Implementation(Scene):
    def construct(self):
        title = Title('BFS Implementation', include_underline=False)
        vertices = list(range(len(g)))
        edges = [(i, j) for i, neighbors in enumerate(g) for j in neighbors]
        graph = Graph(
            vertices, edges,
            layout=layout,
            labels=True,
            vertex_config={'radius': 0.4, 'stroke_width': 0, 'fill_color': WHITE},
            edge_config={'stroke_width': 5},
        ).scale(0.39375).next_to(title, DOWN, buff=0.5).to_edge(LEFT, buff=1)

        graph_code = Code(
            code=dedent('''
                g = [
                    [2],              # 0
                    [2],              # 1
                    [0, 1, 9],        # 2
                    [5],              # 3
                    [9, 8, 5],        # 4
                    [3, 4, 8, 6, 7],  # 5
                    [5, 7, 10],       # 6
                    [5, 6],           # 7
                    [4, 5, 9, 10],    # 8
                    [4, 8, 2],        # 9
                    # ...
                    [12, 13],         # 14
                    [16],             # 15
                    [15],             # 16
                ]
            ''').strip(),
            tab_width=4,
            language='Python',
            line_spacing=0.6,
            font='Monospace',
            style='monokai',
        ).scale(0.7).code.scale(1.14).next_to(title, DOWN, buff=0.5).align_to(ORIGIN, LEFT)

        self.add(title, graph, graph_code)
        for label in graph._labels.values():
            label.set_z_index(10)
        self.wait(3.5)

        used_init_code = Code(
            code=dedent('''
                used = [False] * len(g)
            ''').strip(),
            tab_width=4,
            language='Python',
            line_spacing=0.6,
            font='Monospace',
            style='monokai',
        ).scale(0.7).code.scale(1.14).next_to(graph_code, DOWN, buff=0.2).align_to(ORIGIN, LEFT)
        self.play(AddTextLetterByLetter(used_init_code[0], run_time=0.1 * len(used_init_code[0])))
        self.wait(4)


        bfs_code = Code(
            code=dedent('''
                from collections import deque
                
                used[7] = True
                q = deque([7])
                
                while q:
                    v = q.popleft()
                    for to in g[v]:
                        if not used[to]:
                            q.append(to)
                            used[to] = True
                            
                for node in range(len(g)):
                    if used[node]:
                        print(node)
            ''').strip(),
            tab_width=4,
            language='Python',
            line_spacing=0.6,
            font='Monospace',
            style='monokai',
        ).scale(0.7).code.scale(1.14).next_to(title, DOWN, buff=0.5).align_to(ORIGIN, LEFT)

        def burn(vertex: int, run_time: float = 0.5, scale: float = 0.6):
            fire_icon = SVGMobject('bfs/fire.svg').scale(0.7 * scale).move_to(graph.vertices[vertex], DOWN)
            fire_icon.set_z_index(5)
            self.play(ShowIncreasingSubsets(fire_icon, run_time=run_time))
            fire_icon.add_updater(update_fire)
            return fire_icon

        def spread_fire(source: int, target: int, run_time: float = 0.5, scale: float = 0.6):
            sparkler = SVGMobject('bfs/sparks.svg').scale(0.3 * scale).move_to(graph.vertices[source], DOWN).set_fill('#ff9d33')
            sparkler.set_z_index(5)

            edge = Line(graph.vertices[source].get_center(), graph.vertices[target].get_center(), buff=0.4 * scale)
            burned_edge = VMobject()
            burned_edge.add_updater(lambda x: x.become(Line(
                edge.get_start(), sparkler.get_center(), stroke_width=6,
            ).set_color(DARK_GRAY)))
            self.add(sparkler, burned_edge)

            self.play(MoveAlongPath(sparkler, edge, run_time=run_time, rate_func=linear))
            self.remove(sparkler)
            burning_target = burn(target, run_time=run_time / 2, scale=scale)
            return burning_target, burned_edge

        queue = []
        queue_texts = []
        burning_nodes_title = Text('Queue:').scale(0.5).next_to(graph, DOWN, buff=0.25)
        def add2queue(vertex: int):
            nonlocal queue
            fire_icon = SVGMobject('bfs/fire.svg').scale(0.25)
            fire_icon.next_to(burning_nodes_title if len(queue) == 0 else queue[-1], DOWN, buff=0.3 if len(queue) == 0 else 0.15)
            fire_icon.set_z_index(5)
            queue.append(fire_icon)
            vertex_text = Text(str(vertex)).scale(0.33).set_color(BLACK).move_to(queue[-1]).shift(0.08 * DOWN).set_z_index(10)
            queue_texts.append(vertex_text)
            self.add(queue[-1], vertex_text)
            queue[-1].add_updater(update_fire)

        burning_icons: dict[int, tuple[SVGMobject, VMobject | None]] = {
            7: (burn(7, scale=0.4), None),
        }
        used = {7: True}
        # Remove the code by moving it up
        self.wait(0.5)
        self.play(
            graph_code.animate.shift(7 * UP),
            used_init_code.animate.shift(7 * UP),
            run_time=0.5,
        )
        self.play(AddTextLetterByLetter(bfs_code[2], run_time=0.1 * len(bfs_code[2])))
        self.wait(1)

        self.play(AddTextLetterByLetter(bfs_code[0], run_time=0.05 * len(bfs_code[0])))
        self.play(AddTextLetterByLetter(bfs_code[3], run_time=0.05 * len(bfs_code[3])))
        self.wait(1)

        self.play(Write(burning_nodes_title), run_time=1)
        add2queue(7)
        self.wait(2)

        def spread_from_source(vertex: int, run_time=0.2):
            # Circle around the queue front
            circle = DashedVMobject(Circle(radius=0.4, color=ORANGE)).move_to(queue_texts[0]).shift(0.1 * UP)
            self.play(Create(circle), run_time=run_time)
            self.wait(run_time)

            for to in g[vertex]:
                if used.get(to, False):
                    continue
                used[to] = True
                burning_icons[to] = spread_fire(vertex, to, scale=0.4, run_time=2 * run_time)
                add2queue(to)
                self.wait(run_time)

            # Remove vertex from the queue front
            self.play(FadeOut(queue[0], queue_texts[0], circle), run_time=run_time)
            queue.pop(0)
            queue_texts.pop(0)
            animations = []
            for icon, text in zip(queue, queue_texts):
                icon.clear_updaters()
                delattr(icon, 'initialized')
                animations.append(AnimationGroup(
                    icon.animate.shift(0.65 * UP),
                    text.animate.shift(0.65 * UP),
                ))
            if len(animations) > 0:
                self.play(LaggedStart(*animations, lag_ratio=0.2, run_time=run_time))
            # Add updaters to burning queue elements
            for icon in queue:
                icon.add_updater(update_fire)

        spread_from_source(7)
        self.wait(1)

        self.play(AddTextLetterByLetter(bfs_code[5], run_time=0.1 * len(bfs_code[5])))
        self.wait(1)
        self.play(AddTextLetterByLetter(bfs_code[6], run_time=0.1 * len(bfs_code[6])))
        self.wait(2.7)
        self.play(AddTextLetterByLetter(bfs_code[7], run_time=0.1 * len(bfs_code[7])))
        self.play(AddTextLetterByLetter(bfs_code[8], run_time=0.1 * len(bfs_code[8])))
        self.play(AddTextLetterByLetter(bfs_code[9], run_time=0.07 * len(bfs_code[9])))
        self.play(AddTextLetterByLetter(bfs_code[10], run_time=0.07 * len(bfs_code[10])))
        self.wait(1)

        # Indicate the burning nodes (5 and 6)
        self.play(
            Indicate(burning_icons[5][0], scale_factor=1.5),
            Indicate(burning_icons[6][0], scale_factor=1.5),
            run_time=2,
        )
        self.wait(1)

        # Circumscribe the `if not used[to]` line
        self.play(Circumscribe(bfs_code[8].copy().shift(0.1 * DOWN), buff=0.02, stroke_width=6), run_time=2)
        self.wait(0.5)

        spread_from_source(5, run_time=0.09)
        spread_from_source(6, run_time=0.09)
        spread_from_source(3, run_time=0.08)
        spread_from_source(4, run_time=0.08)
        spread_from_source(8, run_time=0.07)
        spread_from_source(10, run_time=0.07)
        spread_from_source(9, run_time=0.06)
        spread_from_source(11, run_time=0.06)
        spread_from_source(2, run_time=0.06)
        spread_from_source(0, run_time=0.05)
        spread_from_source(1, run_time=0.05)

        # Write the last 3 lines of code
        for line in bfs_code[-3:]:
            self.play(AddTextLetterByLetter(line, run_time=0.03 * len(line)))

        # Indicate all the burned nodes
        self.play(*[
            Indicate(burning_icons[node][0], scale_factor=1.5)
            for node in used.keys()
        ], run_time=1)
        self.wait(1)

        # Transition to the next scene
        self.play(LaggedStart(
            # Clear the graph burning nodes
            AnimationGroup(*[FadeOut(icon[0]) for icon in burning_icons.values()]),
            AnimationGroup(*[FadeOut(icon[1]) for icon in burning_icons.values() if icon[1] is not None]),
            ReplacementTransform(title, Title('Breadth First Search', include_underline=False)),
            lag_ratio=0.5,
            run_time=1,
        ))
        self.wait(1)


class Simulation(Scene):
    def construct(self):
        title = Title('Breadth First Search', include_underline=False)
        vertices = list(range(len(g)))
        edges = [(i, j) for i, neighbors in enumerate(g) for j in neighbors]
        graph = Graph(
            vertices, edges,
            layout=layout,
            labels=True,
            vertex_config={'radius': 0.4, 'stroke_width': 0, 'fill_color': WHITE},
            edge_config={'stroke_width': 5},
        ).scale(0.39375).next_to(title, DOWN, buff=0.5).to_edge(LEFT, buff=1)

        self.add(title, graph)
        for label in graph._labels.values():
            label.set_z_index(10)
        queue_title = Text('Queue:').scale(0.5).next_to(graph, DOWN, buff=0.25)
        self.add(queue_title)

        code = Code(
            code=dedent('''
                from collections import deque

                used[7] = True
                q = deque([7])

                while q:
                    v = q.popleft()
                    for to in g[v]:
                        if not used[to]:
                            q.append(to)
                            used[to] = True

                for node in range(len(g)):
                    if used[node]:
                        print(node)
            ''').strip(),
            tab_width=4,
            language='Python',
            line_spacing=0.6,
            font='Monospace',
            style='monokai',
        ).scale(0.7).code.scale(1.14).next_to(title, DOWN, buff=0.5).align_to(ORIGIN, LEFT)
        self.add(code)
        self.wait(1)

        # Arrow to show which part of the code is being executed
        arrow = Arrow(
            start=LEFT, end=RIGHT, color=RED, buff=0.1,
            stroke_width=10, max_stroke_width_to_length_ratio=15,
            max_tip_length_to_length_ratio=0.5, tip_length=0.2,
        ).scale(0.3).next_to(code[2], LEFT)
        self.play(Create(arrow), run_time=1)

        def burn(vertex: int, run_time: float = 0.5, scale: float = 0.6):
            fire_icon = SVGMobject('bfs/fire.svg').scale(0.7 * scale).move_to(graph.vertices[vertex], DOWN)
            fire_icon.set_z_index(5)
            self.play(ShowIncreasingSubsets(fire_icon, run_time=run_time))
            fire_icon.add_updater(update_fire)
            return fire_icon

        def spread_fire(source: int, target: int, run_time: float = 0.5, scale: float = 0.6):
            sparkler = SVGMobject('bfs/sparks.svg').scale(0.3 * scale).move_to(graph.vertices[source], DOWN).set_fill('#ff9d33')
            sparkler.set_z_index(5)

            edge = Line(graph.vertices[source].get_center(), graph.vertices[target].get_center(), buff=0.4 * scale)
            burned_edge = VMobject()
            burned_edge.add_updater(lambda x: x.become(Line(
                edge.get_start(), sparkler.get_center(), stroke_width=6,
            ).set_color(DARK_GRAY)))
            self.add(sparkler, burned_edge)

            self.play(MoveAlongPath(sparkler, edge, run_time=run_time, rate_func=linear))
            self.remove(sparkler)
            burning_target = burn(target, run_time=run_time / 2, scale=scale)
            return burning_target, burned_edge

        queue = []
        queue_texts = []
        def add2queue(vertex: int):
            nonlocal queue
            fire_icon = SVGMobject('bfs/fire.svg').scale(0.25)
            fire_icon.next_to(queue_title if len(queue) == 0 else queue[-1], DOWN, buff=0.3 if len(queue) == 0 else 0.15)
            fire_icon.set_z_index(5)
            queue.append(fire_icon)
            vertex_text = Text(str(vertex)).scale(0.33).set_color(BLACK).move_to(queue[-1]).shift(0.08 * DOWN).set_z_index(10)
            queue_texts.append(vertex_text)
            self.add(queue[-1], vertex_text)
            queue[-1].add_updater(update_fire)

        burning_icons: dict[int, tuple[SVGMobject, VMobject | None]] = {
            7: (burn(7, scale=0.4), None),
        }
        used = {7: True}
        self.play(arrow.animate.next_to(code[3], LEFT), run_time=0.5)
        add2queue(7)
        self.wait(1)

        def spread_from_source(vertex: int):
            # Circle around the queue front
            circle = DashedVMobject(Circle(radius=0.4, color=ORANGE)).move_to(queue_texts[0]).shift(0.1 * UP)
            self.play(LaggedStart(
                arrow.animate.next_to(code[6], LEFT).shift(0.1 * DOWN),
                Create(circle),
                lag_ratio=0.5,
                run_time=0.6,
            ))
            self.wait(0.5)

            for to in g[vertex]:
                to_circle = DashedVMobject(Circle(radius=0.35, color=YELLOW)).move_to(graph.vertices[to]).shift(0.05 * UP)
                self.play(arrow.animate.next_to(code[7], LEFT).shift(0.1 * DOWN), run_time=0.5)
                self.wait(0.5)
                self.play(LaggedStart(
                    arrow.animate.next_to(code[8], LEFT).shift(0.12 * DOWN),
                    Create(to_circle),
                    lag_ratio=0.5,
                    run_time=0.6,
                ))
                if used.get(to, False):
                    self.play(FadeOut(to_circle), run_time=0.2)
                    continue
                used[to] = True
                burning_icons[to] = spread_fire(vertex, to, scale=0.4)
                self.play(arrow.animate.next_to(code[9], LEFT).shift(0.15 * DOWN), run_time=0.5)
                self.wait(0.5)
                add2queue(to)
                self.play(arrow.animate.next_to(code[10], LEFT).shift(0.15 * DOWN), run_time=0.5)
                self.play(FadeOut(to_circle), run_time=0.2)

            # Remove vertex from the queue front
            self.play(FadeOut(queue[0], queue_texts[0], circle), run_time=0.2)
            queue.pop(0)
            queue_texts.pop(0)
            animations = []
            for icon, text in zip(queue, queue_texts):
                icon.clear_updaters()
                delattr(icon, 'initialized')
                animations.append(AnimationGroup(
                    icon.animate.shift(0.65 * UP),
                    text.animate.shift(0.65 * UP),
                ))
            self.play(LaggedStart(*animations, lag_ratio=0.2, run_time=0.6))
            # Add updaters to burning queue elements
            for icon in queue:
                icon.add_updater(update_fire)

            # Move the arrow to the while loop
            self.play(arrow.animate.next_to(code[5], LEFT), run_time=0.5)
            self.wait(1)

        # Move the arrow to the while loop
        self.play(arrow.animate.next_to(code[5], LEFT), run_time=0.5)
        self.wait(1)

        spread_from_source(7)
        spread_from_source(5)
        spread_from_source(6)
        spread_from_source(3)
        spread_from_source(4)
        spread_from_source(8)
        spread_from_source(10)
        spread_from_source(9)
        spread_from_source(11)
        spread_from_source(2)
        spread_from_source(0)
        spread_from_source(1)
        self.play(arrow.animate.next_to(code[12], LEFT), run_time=0.5)
        self.wait(1)
        self.play(arrow.animate.next_to(code[13], LEFT).shift(0.1 * DOWN), run_time=0.5)
        self.wait(1)
        self.play(LaggedStart(
            *[Indicate(burning_icons[node][0], scale_factor=1.5) for node in used.keys()],
            run_time=1,
        ))
        self.wait(1)

        self.play(Indicate(burning_icons[7][0], scale_factor=1.5), run_time=1)
        self.wait(1)

        self.play(LaggedStart(
            *[
                AnimationGroup(
                    Indicate(graph.vertices[node], scale_factor=1.5, color=RED),
                    graph._labels[node].animate.set_z_index(100000),
                ) for node in range(17) if node not in used
            ],
            run_time=2,
        ))
        self.wait(1)

        # Transition to the next scene
        self.play(LaggedStart(
            FadeOut(arrow),
            FadeOut(code, queue_title, *queue, *queue_texts),
            FadeOut(
                *[icon[0] for icon in burning_icons.values()],
                *[icon[1] for icon in burning_icons.values() if icon[1] is not None],
            ),
            FadeOut(graph),
            ReplacementTransform(title, Title('BFS on Grids', include_underline=False)),
            run_time=1,
            lag_ratio=0.5,
        ))
        self.wait(1)


class BFSOnGrids(Scene):
    def construct(self):
        title = Title('BFS on Grids', include_underline=False)
        self.add(title)
        self.wait(0.1)

        grid_code = Code(
            code=dedent('''
                g = [
                    '~~~~~~~~#~',
                    '~##~~~~###',
                    '~#~~~~~~~~',
                    '~~~~~~###~',
                    '~~~~#####~',
                    '~#~~~##~~~',
                    '#~~~~~#~~~',
                ]
            ''').strip(),
            tab_width=4,
            language='Python',
            line_spacing=0.6,
            font='Monospace',
            style='monokai',
        ).code.scale(1.2).next_to(title, DOWN, buff=1)
        self.play(Write(grid_code), run_time=0.5)
        self.wait(0.1)

        grid = [
            '~~~~~~~~#~',
            '~##~~~~###',
            '~#~~~~~~~~',
            '~~~~~~###~',
            '~~~~#####~',
            '~#~~~##~~~',
            '#~~~~~#~~~',
        ]
        used = [[False] * len(grid[0]) for _ in range(len(grid))]

        # Indicate the hashtags
        hashtags = [(r + 1, c + 2) for r in range(len(grid)) for c in range(len(grid[0])) if grid[r][c] == '#']
        tildas = [(r + 1, c + 2) for r in range(len(grid)) for c in range(len(grid[0])) if grid[r][c] == '~']
        self.play(*[Indicate(grid_code[r][c], scale_factor=1.5, color=ORANGE) for r, c in hashtags], run_time=1)
        self.wait(0.1)
        self.play(*[Indicate(grid_code[r][c], scale_factor=1.5, color=BLUE) for r, c in tildas], run_time=1)
        self.wait(0.1)

        self.play(LaggedStart(
            Indicate(grid_code[5][8], scale_factor=1.5, color=YELLOW),
            AnimationGroup(
                Indicate(grid_code[6][8], scale_factor=1.5, color=ORANGE),
                Indicate(grid_code[4][8], scale_factor=1.5, color=ORANGE),
                Indicate(grid_code[5][9], scale_factor=1.5, color=ORANGE),
                Indicate(grid_code[5][7], scale_factor=1.5, color=ORANGE),
            ),
            lag_ratio=0.1,
            run_time=1,
        ))
        self.wait(0.1)

        left_question_mark = Text('?', font_size=100).next_to(grid_code, LEFT, buff=1).rotate(PI / 8)
        right_question_mark = Text('?', font_size=100).next_to(grid_code, RIGHT, buff=2).rotate(-PI / 8)
        self.play(Wiggle(left_question_mark), Wiggle(right_question_mark), run_time=1)
        self.play(FadeOut(left_question_mark, right_question_mark), run_time=0.5)
        self.wait(0.1)

        # Animate the BFS process on the bottom island
        self.play(LaggedStart(
            Indicate(grid_code[5][8], scale_factor=1.5, color=ORANGE),
            AnimationGroup(
                Indicate(grid_code[6][8], scale_factor=1.5, color=ORANGE),
                Indicate(grid_code[4][8], scale_factor=1.5, color=ORANGE),
                Indicate(grid_code[5][9], scale_factor=1.5, color=ORANGE),
                Indicate(grid_code[5][7], scale_factor=1.5, color=ORANGE),
            ),
            AnimationGroup(
                Indicate(grid_code[7][8], scale_factor=1.5, color=ORANGE),
                Indicate(grid_code[6][7], scale_factor=1.5, color=ORANGE),
                Indicate(grid_code[5][6], scale_factor=1.5, color=ORANGE),
                Indicate(grid_code[5][10], scale_factor=1.5, color=ORANGE),
                Indicate(grid_code[4][9], scale_factor=1.5, color=ORANGE),
            ),
            AnimationGroup(
                Indicate(grid_code[4][10], scale_factor=1.5, color=ORANGE),
            ),
            lag_ratio=0.2,
            run_time=1,
        ))
        self.wait(0.1)

        self.play(*[
            Wiggle(grid_code[i][j], scale_value=1.3, rotation_angle=0.04 * TAU, n_wiggles=5)
            for i in range(1, len(grid) + 1)
            for j in range(2, len(grid[0]) + 2)
        ], run_time=2)
        self.wait(0.1)
        # hashtags = [(r + 1, c + 2) for r in range(len(grid)) for c in range(len(grid[0])) if grid[r][c] == '#']

        def burn(row: int, col: int):
            fire_icon = SVGMobject('bfs/fire.svg').scale(0.2).move_to(grid_code[row + 1][col + 2])
            fire_icon.set_z_index(5)
            self.add(fire_icon)
            fire_icon.add_updater(update_fire)
            return fire_icon

        def spread_fire(row: int, col: int):
            """ Perform a BFS starting from the given cell """
            q = deque([(row, col)])
            fire_icons = []
            while q:
                r, c = q.popleft()
                for dr, dc in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] == '#' and not used[nr][nc]:
                        used[nr][nc] = True
                        q.append((nr, nc))
                        fire_icons.append(burn(nr, nc))
                        self.wait(0.1)
            return fire_icons

        # Iterate through the grid and perform BFS from each island cell
        all_fire_icons = []
        iteration_animations = []
        for r in range(len(grid)):
            for c in range(len(grid[0])):
                iteration_animations.append(Indicate(grid_code[r + 1][c + 2], scale_factor=1.5, color=YELLOW))
                if grid[r][c] == '#' and not used[r][c]:
                    self.play(LaggedStart(
                        *iteration_animations,
                        lag_ratio=0.3,
                        run_time=0.1 * len(iteration_animations),
                    ))
                    used[r][c] = True
                    all_fire_icons.append(burn(r, c))
                    all_fire_icons += spread_fire(r, c)
                    iteration_animations.clear()
                    self.wait(0.5)
        self.play(LaggedStart(
            *iteration_animations,
            lag_ratio=0.3,
            run_time=0.1 * len(iteration_animations),
        ))
        iteration_animations.clear()
        self.wait(0.1)

        # Transition to the next scene
        self.play(
            FadeOut(*all_fire_icons),
            run_time=0.5,
        )
        self.wait(1)


class BFSOnGridsImplementation(Scene):
    def construct(self):
        title = Title('BFS on Grids', include_underline=False)
        grid_code = Code(
            code=dedent('''
                g = [
                    '~~~~~~~~#~',
                    '~##~~~~###',
                    '~#~~~~~~~~',
                    '~~~~~~###~',
                    '~~~~#####~',
                    '~#~~~##~~~',
                    '#~~~~~#~~~',
                ]
            ''').strip(),
            tab_width=4,
            language='Python',
            line_spacing=0.6,
            font='Monospace',
            style='monokai',
        ).code.scale(1.2).next_to(title, DOWN, buff=1)
        self.add(title, grid_code)
        self.play(grid_code.animate.scale(1 / 1.2).next_to(title, DOWN, buff=1).shift(2 * LEFT))

        def get_initialization_code(counter: int):
            return Code(
            code=dedent(f'''
                used = [[False] * len(line) for line in g]
                islands = {counter}
            ''').strip(),
            tab_width=4,
            language='Python',
            line_spacing=0.6,
            font='Monospace',
            style='monokai',
        ).code.next_to(grid_code, DOWN, buff=0.2).align_to(grid_code, LEFT)

        initialization_code = {i: get_initialization_code(i) for i in range(6)}
        self.play(AddTextLetterByLetter(initialization_code[0][0], run_time=0.01 * len(initialization_code[0][0])))
        self.wait(0.1)
        self.play(AddTextLetterByLetter(initialization_code[0][1], run_time=0.01 * len(initialization_code[0][1])))
        self.wait(0.1)

        # Highlight each island one by one and increment the islands counter
        self.play(LaggedStart(
            LaggedStart(
                Indicate(grid_code[1][10], scale_factor=1.5, color=ORANGE),
                Indicate(grid_code[2][10], scale_factor=1.5, color=ORANGE),
                AnimationGroup(
                    Indicate(grid_code[2][9], scale_factor=1.5, color=ORANGE),
                    Indicate(grid_code[2][11], scale_factor=1.5, color=ORANGE),
                ),
                lag_ratio=0.1,
            ),
            TransformMatchingShapes(initialization_code[0], initialization_code[1]),
            lag_ratio=0.1,
            run_time=0.5,
        ))

        self.play(LaggedStart(
            LaggedStart(
                Indicate(grid_code[2][3], scale_factor=1.5, color=ORANGE),
                AnimationGroup(
                    Indicate(grid_code[2][4], scale_factor=1.5, color=ORANGE),
                    Indicate(grid_code[3][3], scale_factor=1.5, color=ORANGE),
                ),
                lag_ratio=0.1,
            ),
            TransformMatchingShapes(initialization_code[1], initialization_code[2]),
            lag_ratio=0.1,
            run_time=0.5,
        ))

        self.play(LaggedStart(
            LaggedStart(
                Indicate(grid_code[5][8], scale_factor=1.5, color=ORANGE),
                AnimationGroup(
                    Indicate(grid_code[6][8], scale_factor=1.5, color=ORANGE),
                    Indicate(grid_code[4][8], scale_factor=1.5, color=ORANGE),
                    Indicate(grid_code[5][9], scale_factor=1.5, color=ORANGE),
                    Indicate(grid_code[5][7], scale_factor=1.5, color=ORANGE),
                ),
                AnimationGroup(
                    Indicate(grid_code[7][8], scale_factor=1.5, color=ORANGE),
                    Indicate(grid_code[6][7], scale_factor=1.5, color=ORANGE),
                    Indicate(grid_code[5][6], scale_factor=1.5, color=ORANGE),
                    Indicate(grid_code[5][10], scale_factor=1.5, color=ORANGE),
                    Indicate(grid_code[4][9], scale_factor=1.5, color=ORANGE),
                ),
                Indicate(grid_code[4][10], scale_factor=1.5, color=ORANGE),
                lag_ratio=0.1,
            ),
            TransformMatchingShapes(initialization_code[2], initialization_code[3]),
            lag_ratio=0.1,
            run_time=1,
        ))

        self.play(LaggedStart(
            Indicate(grid_code[6][3], scale_factor=1.5, color=ORANGE),
            TransformMatchingShapes(initialization_code[3], initialization_code[4]),
            lag_ratio=0.1,
            run_time=0.5,
        ))

        self.play(LaggedStart(
            Indicate(grid_code[7][2], scale_factor=1.5, color=ORANGE),
            TransformMatchingShapes(initialization_code[4], initialization_code[5]),
            lag_ratio=0.1,
            run_time=1,
        ))
        self.wait(0.1)

        # Reset the counter to 0
        self.play(TransformMatchingShapes(initialization_code[5], initialization_code[0]), run_time=0.5)
        self.wait(0.1)

        self.play(
            grid_code.animate.scale(0.8).next_to(title, DOWN, buff=0.5).to_edge(RIGHT, buff=2),
            FadeOut(initialization_code[0]),
            run_time=0.5,
        )
        self.wait(0.1)

        loops_code = Code(
            code=dedent('''
                for i in range(len(g)):
                    for j in range(len(g[i])):
                        if g[i][j] == '#' and not used[i][j]:
                            bfs(i, j)
                            islands += 1
            ''').strip(),
            tab_width=4,
            language='Python',
            line_spacing=0.6,
            font='Monospace',
            style='monokai',
        ).code.scale(0.75).next_to(title, DOWN, buff=0.5).to_edge(LEFT, buff=1)
        iteration_animations = []
        grid = [
            '~~~~~~~~#~',
            '~##~~~~###',
            '~#~~~~~~~~',
            '~~~~~~###~',
            '~~~~#####~',
            '~#~~~##~~~',
            '#~~~~~#~~~',
        ]
        for c in range(len(grid[0])):
            iteration_animations.append(Indicate(grid_code[1][c + 2], scale_factor=1.5, color=YELLOW))
            if grid[0][c] == '#':
                break
        self.play(AddTextLetterByLetter(loops_code[0], run_time=0.01 * len(loops_code[0])))
        self.play(AddTextLetterByLetter(loops_code[1], run_time=0.01 * len(loops_code[1])))
        self.wait(0.1)
        self.play(LaggedStart(*iteration_animations, lag_ratio=0.1), run_time=1)
        self.wait(0.1)
        self.play(AddTextLetterByLetter(loops_code[2], run_time=0.01 * len(loops_code[2])))
        self.wait(0.1)
        self.play(AddTextLetterByLetter(loops_code[3], run_time=0.01 * len(loops_code[3])))
        self.play(AddTextLetterByLetter(loops_code[4], run_time=0.01 * len(loops_code[4])))
        self.wait(0.1)


        bfs_code = Code(
            code=dedent('''
                def bfs(row, col):
                    from collections import deque
                    
                    used[row][col] = True
                    q = deque([(row, col)])
                    
                    while q:
                        r, c = q.popleft()
                        
                        if 0 <= r - 1 < len(g) and g[r - 1][c] == '#' and not used[r - 1][c]:
                            used[r - 1][c] = True
                            q.append((r - 1, c))
                        if 0 <= r + 1 < len(g) and g[r + 1][c] == '#' and not used[r + 1][c]:
                            used[r + 1][c] = True
                            q.append((r + 1, c))
                        if 0 <= c - 1 < len(g[r]) and g[r][c - 1] == '#' and not used[r][c - 1]:
                            used[r][c - 1] = True
                            q.append((r, c - 1))
                        if 0 <= c + 1 < len(g[r]) and g[r][c + 1] == '#' and not used[r][c + 1]:
                            used[r][c + 1] = True
                            q.append((r, c + 1))
            ''').strip(),
            tab_width=4,
            language='Python',
            line_spacing=0.6,
            font='Monospace',
            style='monokai',
        ).code.scale(0.75).next_to(loops_code, DOWN, buff=0.5).to_edge(LEFT, buff=1)
        self.play(AddTextLetterByLetter(bfs_code[0], run_time=0.01 * len(bfs_code[0])))
        self.play(AddTextLetterByLetter(bfs_code[1], run_time=0.01 * len(bfs_code[1])))
        self.wait(0.1)

        self.play(AddTextLetterByLetter(bfs_code[3], run_time=0.01 * len(bfs_code[3])))
        self.play(AddTextLetterByLetter(bfs_code[4], run_time=0.01 * len(bfs_code[4])))
        self.wait(0.1)

        self.play(
            loops_code.animate.shift(2 * UP).set_opacity(0),
            VGroup(*bfs_code[0: 5]).animate.next_to(title, DOWN, buff=0.5).to_edge(LEFT, buff=1),
            run_time=0.5,
        )
        VGroup(*bfs_code[5:]).next_to(bfs_code[4], DOWN, buff=0).align_to(bfs_code[4], LEFT)
        self.wait(0.1)

        self.play(AddTextLetterByLetter(bfs_code[6], run_time=0.01 * len(bfs_code[6])))
        self.play(AddTextLetterByLetter(bfs_code[7], run_time=0.01 * len(bfs_code[7])))
        self.wait(0.1)

        self.play(AddTextLetterByLetter(bfs_code[9], run_time=0.01 * len(bfs_code[9])))
        self.wait(0.1)
        self.play(AddTextLetterByLetter(bfs_code[10], run_time=0.01 * len(bfs_code[10])))
        self.play(AddTextLetterByLetter(bfs_code[11], run_time=0.01 * len(bfs_code[11])))
        self.wait(0.1)

        self.play(AddTextLetterByLetter(bfs_code[12], run_time=0.01 * len(bfs_code[12])))
        self.play(AddTextLetterByLetter(bfs_code[13], run_time=0.01 * len(bfs_code[13])))
        self.play(AddTextLetterByLetter(bfs_code[14], run_time=0.01 * len(bfs_code[14])))
        self.wait(0.1)

        self.play(AddTextLetterByLetter(bfs_code[15], run_time=0.01 * len(bfs_code[15])))
        self.play(AddTextLetterByLetter(bfs_code[16], run_time=0.01 * len(bfs_code[16])))
        self.play(AddTextLetterByLetter(bfs_code[17], run_time=0.01 * len(bfs_code[17])))
        self.wait(0.1)

        self.play(AddTextLetterByLetter(bfs_code[18], run_time=0.01 * len(bfs_code[18])))
        self.play(AddTextLetterByLetter(bfs_code[19], run_time=0.01 * len(bfs_code[19])))
        self.play(AddTextLetterByLetter(bfs_code[20], run_time=0.01 * len(bfs_code[20])))
        self.wait(0.1)

        # Highlight the diagonal neighbors
        self.play(LaggedStart(
            Indicate(grid_code[5][8], scale_factor=1.5, color=ORANGE),
            AnimationGroup(
                Indicate(grid_code[6][8], scale_factor=1.5, color=YELLOW),
                Indicate(grid_code[4][8], scale_factor=1.5, color=YELLOW),
                Indicate(grid_code[5][9], scale_factor=1.5, color=YELLOW),
                Indicate(grid_code[5][7], scale_factor=1.5, color=YELLOW),
            ),
            AnimationGroup(
                Indicate(grid_code[6][9], scale_factor=1.5, color=RED),
                Indicate(grid_code[4][7], scale_factor=1.5, color=RED),
                Indicate(grid_code[4][9], scale_factor=1.5, color=RED),
                Indicate(grid_code[6][7], scale_factor=1.5, color=RED),
            ),
            lag_ratio=0.1,
            run_time=1,
        ))
        self.wait(0.1)

        # Indicate the if statements
        self.play(LaggedStart(
            Indicate(bfs_code[9]),
            Indicate(bfs_code[12]),
            Indicate(bfs_code[15]),
            Indicate(bfs_code[18]),
            lag_ratio=0.2,
            run_time=0.5,
        ))
        self.wait(0.1)


        # Wave the if statements
        self.play(LaggedStart(
            ApplyWave(bfs_code[9]),
            ApplyWave(bfs_code[12]),
            ApplyWave(bfs_code[15]),
            ApplyWave(bfs_code[18]),
            lag_ratio=0.2,
            run_time=0.5,
        ))
        self.wait(0.1)

        # Transition to the next scene
        init = get_initialization_code(0).scale(0.75).next_to(title, DOWN, buff=0.5).to_edge(LEFT, buff=1).shift(2 * UP)
        self.play(
            bfs_code.animate.shift(2 * DOWN).set_opacity(0),
            init.animate.shift(2 * DOWN),
            loops_code.animate.next_to(init, DOWN, buff=0.5).align_to(init, LEFT).shift(2 * DOWN).set_opacity(1),
            run_time=0.5,
        )
        self.wait(0.1)


class BFSOnGridsSimulation(Scene):
    def construct(self):
        title = Title('BFS on Grids', include_underline=False)
        grid_code = Code(
            code=dedent('''
                g = [
                    '~~~~~~~~#~',
                    '~##~~~~###',
                    '~#~~~~~~~~',
                    '~~~~~~###~',
                    '~~~~#####~',
                    '~#~~~##~~~',
                    '#~~~~~#~~~',
                ]
            ''').strip(),
            tab_width=4,
            language='Python',
            line_spacing=0.6,
            font='Monospace',
            style='monokai',
        ).code.scale(0.8).next_to(title, DOWN, buff=0.5).to_edge(RIGHT, buff=2)
        self.add(title, grid_code)

        init_code = Code(
            code=dedent(f'''
                used = [[False] * len(line) for line in g]
                islands = 0
            ''').strip(),
            tab_width=4,
            language='Python',
            line_spacing=0.6,
            font='Monospace',
            style='monokai',
        ).code.scale(0.75).next_to(title, DOWN, buff=0.5).to_edge(LEFT, buff=1)

        loops_code = Code(
            code=dedent('''
                for i in range(len(g)):
                    for j in range(len(g[i])):
                        if g[i][j] == '#' and not used[i][j]:
                            bfs(i, j)
                            islands += 1
            ''').strip(),
            tab_width=4,
            language='Python',
            line_spacing=0.6,
            font='Monospace',
            style='monokai',
        ).code.scale(0.75).next_to(init_code, DOWN, buff=0.5).to_edge(LEFT, buff=1)
        self.add(init_code, loops_code)
        self.play(grid_code.animate.scale(0.72 / 0.8).shift(LEFT), run_time=0.5)
        self.wait(0.1)

        arrow = Arrow(
            start=LEFT, end=RIGHT, color=RED, buff=0.1,
            stroke_width=10, max_stroke_width_to_length_ratio=15,
            max_tip_length_to_length_ratio=0.5, tip_length=0.2,
        ).scale(0.3).next_to(init_code[0], LEFT)
        self.play(Create(arrow), run_time=0.2)
        self.wait(0.1)

        self.play(arrow.animate.next_to(init_code[1], LEFT), run_time=0.2)
        self.wait(0.1)

        self.play(
            arrow.animate.next_to(loops_code[0], LEFT),
            FadeOut(init_code[0]),
            init_code[1].animate.next_to(grid_code, UP, buff=0.1).align_to(grid_code, LEFT),
            run_time=0.2,
        )
        self.wait(0.1)
        self.play(arrow.animate.next_to(loops_code[1], LEFT).shift(0.1 * DOWN), run_time=0.2)
        self.wait(0.1)

        bfs_code = Code(
            code=dedent('''
                def bfs(row, col):
                    from collections import deque

                    used[row][col] = True
                    q = deque([(row, col)])

                    while q:
                        r, c = q.popleft()

                        if 0 <= r - 1 < len(g) and g[r - 1][c] == '#' and not used[r - 1][c]:
                            used[r - 1][c] = True
                            q.append((r - 1, c))
                        if 0 <= r + 1 < len(g) and g[r + 1][c] == '#' and not used[r + 1][c]:
                            used[r + 1][c] = True
                            q.append((r + 1, c))
                        if 0 <= c - 1 < len(g[r]) and g[r][c - 1] == '#' and not used[r][c - 1]:
                            used[r][c - 1] = True
                            q.append((r, c - 1))
                        if 0 <= c + 1 < len(g[r]) and g[r][c + 1] == '#' and not used[r][c + 1]:
                            used[r][c + 1] = True
                            q.append((r, c + 1))
            ''').strip(),
            tab_width=4,
            language='Python',
            line_spacing=0.6,
            font='Monospace',
            style='monokai',
        ).code.scale(0.75).next_to(title, DOWN, buff=0.5).to_edge(LEFT, buff=1)

        grid = [
            '~~~~~~~~#~',
            '~##~~~~###',
            '~#~~~~~~~~',
            '~~~~~~###~',
            '~~~~#####~',
            '~#~~~##~~~',
            '#~~~~~#~~~',
        ]
        used = [[False] * len(grid[0]) for _ in range(len(grid))]

        queue_texts = []
        def add2queue(row: int, col: int):
            # fire_icon.next_to(burning_nodes_title if len(queue) == 0 else queue[-1], DOWN, buff=0.4 if len(queue) == 0 else 0.2)
            vertex_text = Text(f'({row}, {col})').scale(0.4).next_to(queue_text if len(queue_texts) == 0 else queue_texts[-1], DOWN, buff=0.2 if len(queue_texts) == 0 else 0.1)
            queue_texts.append(vertex_text)
            self.play(Write(queue_texts[-1]), run_time=0.1)

        def remove_from_queue():
            animations = []
            for text, prev_text in zip(queue_texts[1:], queue_texts):
                animations.append(text.animate.move_to(prev_text))
            self.play(LaggedStart(FadeOut(queue_texts[0]), *animations, lag_ratio=0.3, run_time=0.2))
            queue_texts.pop(0)

        def burn(row: int, col: int):
            fire_icon = SVGMobject('bfs/fire.svg').scale(0.15).move_to(grid_code[row + 1][col + 2])
            fire_icon.set_z_index(5)
            self.add(fire_icon)
            fire_icon.add_updater(update_fire)
            return fire_icon

        def spread_fire(row: int, col: int):
            """ Perform a BFS starting from the given cell """
            q = deque([(row, col)])

            self.play(arrow.animate.next_to(bfs_code[0], LEFT), run_time=0.2)
            self.wait(0.1)
            self.play(arrow.animate.next_to(bfs_code[1], LEFT).shift(0.1 * DOWN), run_time=0.2)
            self.play(arrow.animate.next_to(bfs_code[3], LEFT).shift(0.1 * DOWN), run_time=0.2)
            self.wait(0.1)
            self.play(arrow.animate.next_to(bfs_code[4], LEFT).shift(0.1 * DOWN), run_time=0.2)
            add2queue(row, col)
            self.wait(0.1)

            self.play(arrow.animate.next_to(bfs_code[6], LEFT).shift(0.1 * DOWN), run_time=0.2)
            fire_icons = []
            while q:
                r, c = q.popleft()

                # Add circle around the current cell
                circle = DashedVMobject(Circle(radius=0.2, color=ORANGE)).move_to(grid_code[r + 1][c + 2])
                self.play(arrow.animate.next_to(bfs_code[7], LEFT).shift(0.12 * DOWN), Create(circle), run_time=0.1)
                remove_from_queue()
                self.wait(0.1)

                for statement, (dr, dc) in enumerate(((-1, 0), (1, 0), (0, -1), (0, 1))):
                    nr, nc = r + dr, c + dc
                    to_circle = None
                    self.play(arrow.animate.next_to(bfs_code[9 + 3 * statement], LEFT).shift(0.12 * DOWN), run_time=0.1)
                    if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
                        to_circle = DashedVMobject(Circle(radius=0.2, color=YELLOW)).move_to(grid_code[nr + 1][nc + 2])
                        self.play(Create(to_circle), run_time=0.1)
                        self.wait(0.1)
                    if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] == '#' and not used[nr][nc]:
                        self.play(arrow.animate.next_to(bfs_code[10 + 3 * statement], LEFT).shift(0.12 * DOWN), run_time=0.1)
                        used[nr][nc] = True
                        self.play(arrow.animate.next_to(bfs_code[11 + 3 * statement], LEFT).shift(0.12 * DOWN), run_time=0.1)
                        add2queue(nr, nc)
                        q.append((nr, nc))
                        fire_icons.append(burn(nr, nc))
                        self.wait(0.1)
                    if to_circle is not None:
                        self.remove(to_circle)
                self.play(FadeOut(circle), run_time=0.1)

            self.play(FadeOut(arrow))
            return fire_icons

        islands_counter_mobj = init_code[1]
        def get_islands(counter: int):
            return Code(
            code=dedent(f'''
                islands = {counter}
            ''').strip(),
            tab_width=4,
            language='Python',
            line_spacing=0.6,
            font='Monospace',
            style='monokai',
        ).code.scale(0.75).align_to(islands_counter_mobj, LEFT).align_to(islands_counter_mobj, UP)


        # Iterate through the grid and perform BFS from each island cell
        queue_text = Text('Queue:').scale(0.5).next_to(islands_counter_mobj, RIGHT, buff=1.5)
        all_fire_icons = []
        iteration_animations = []
        found_islands = 0
        for r in range(len(grid)):
            for c in range(len(grid[0])):
                iteration_animations.append(Indicate(grid_code[r + 1][c + 2], scale_factor=1.5, color=YELLOW))
                if grid[r][c] == '#' and not used[r][c]:
                    self.play(LaggedStart(
                        *iteration_animations,
                        *([
                            loops_code.animate.shift(2 * UP).set_opacity(0),
                            arrow.animate.next_to(bfs_code[0], LEFT),
                            FadeIn(bfs_code),
                            Write(queue_text),
                        ] if r == 0 else []),
                        lag_ratio=0.3,
                        run_time=2 if r == 0 else 0.1 * len(iteration_animations),
                    ))
                    used[r][c] = True
                    all_fire_icons.append(burn(r, c))
                    all_fire_icons += spread_fire(r, c)
                    found_islands += 1
                    new_init_code = get_islands(found_islands)
                    self.play(TransformMatchingShapes(islands_counter_mobj, new_init_code), run_time=0.2)
                    islands_counter_mobj = new_init_code
                    iteration_animations.clear()
                    self.wait(0.2)
        self.play(LaggedStart(
            *iteration_animations,
            lag_ratio=0.3,
            run_time=0.1 * len(iteration_animations),
        ))
        iteration_animations.clear()
        self.wait(0.1)

        # Transition to the next scene
        self.play(LaggedStart(
            FadeOut(*all_fire_icons),
            FadeOut(bfs_code, queue_text),
            FadeOut(grid_code),
            islands_counter_mobj.animate.center().scale(3),
            lag_ratio=0.5,
            run_time=1,
        ))
        self.wait(0.5)

        self.play(LaggedStart(FadeOut(title), FadeOut(islands_counter_mobj), lag_ratio=0.5, run_time=0.5))
        self.wait(0.1)


class ShortestPath(Scene):
    def construct(self):
        title = Title('Shortest Path', include_underline=False)
        self.play(Write(title), run_time=0.5)
        self.wait(0.1)

        vertices = list(range(len(g)))
        edges = [(i, j) for i, neighbors in enumerate(g) for j in neighbors]
        graph = Graph(
            vertices, edges,
            layout=layout,
            vertex_config={'radius': 0.4, 'stroke_width': 0, 'fill_color': WHITE},
            edge_config={'stroke_width': 5},
        ).scale(0.9).shift(1.5 * DOWN)

        clock = SVGMobject('bfs/clock.svg').scale(0.3)
        clocks = VGroup(*[
            clock.copy().move_to(graph.vertices[i]).set_fill(ORANGE if i == 7 else BLACK) for i in range(len(g))
        ])
        burning_times = {7: 0}
        burning_times_mobjects = {}
        burned_edges = []

        self.play(Create(graph), *[Create(p) for p in clocks], run_time=0.5)
        self.wait(0.2)

        def burn(vertex: int, run_time: float = 0.5):
            fire_icon = SVGMobject('bfs/fire.svg').scale(0.6).move_to(graph.vertices[vertex], DOWN)
            fire_icon.set_z_index(5)
            self.play(ShowIncreasingSubsets(fire_icon, run_time=run_time))
            fire_icon.add_updater(update_fire)
            self.wait(run_time)

            burning_times_mobjects[vertex] = Text(f'{burning_times[vertex]}').scale(0.8).move_to(graph.vertices[vertex]).set_z_index(100000).set_color(ORANGE)
            self.play(FadeOut(clocks[vertex]), ReplacementTransform(fire_icon, burning_times_mobjects[vertex]), run_time=run_time)

        def spread_fire(source: int, target: int, run_time: float = 0.5):
            sparkler = SVGMobject('bfs/sparks.svg').scale(0.2).move_to(graph.vertices[source], DOWN).set_fill('#ff9d33')
            sparkler.set_z_index(5)
            burning_times[target] = burning_times[source] + 1

            edge = Line(graph.vertices[source].get_center(), graph.vertices[target].get_center(), buff=0.36)
            burned_edge = VMobject()
            burned_edge.add_updater(lambda x: x.become(Line(
                edge.get_start(), sparkler.get_center(), stroke_width=6,
            ).set_color(DARK_GRAY)))
            self.add(sparkler, burned_edge)
            burned_edges.append(burned_edge)

            self.play(MoveAlongPath(sparkler, edge, run_time=run_time, rate_func=linear))
            self.remove(sparkler)
            burn(target, run_time=run_time / 2)

        burn(7)
        self.wait(0.5)
        spread_fire(7, 5, run_time=0.3)
        spread_fire(7, 6, run_time=0.3)
        self.wait(0.5)
        spread_fire(5, 8, run_time=0.2)
        spread_fire(5, 4, run_time=0.2)
        spread_fire(5, 3, run_time=0.2)
        self.wait(0.5)
        spread_fire(6, 10, run_time=0.2)
        spread_fire(8, 9, run_time=0.2)
        self.wait(0.2)
        spread_fire(10, 11, run_time=0.3)
        spread_fire(9, 2, run_time=0.3)
        self.wait(0.2)
        spread_fire(2, 0, run_time=0.1)
        spread_fire(2, 1, run_time=0.1)
        self.wait(0.5)

        # Highlight the path 7 -> 5 -> 8 -> 9 -> 2 with ShowPassingFlash with LaggedStart
        path = [7, 5, 8, 9, 2]
        path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
        self.play(LaggedStart(*[
            ShowPassingFlash(edge.copy().set_z_index(100000).set_color(ORANGE).set_stroke(width=9), time_width=0.5)
            for edge in VGroup(*[graph.edges[edge] for edge in path_edges])
        ],
            lag_ratio=0.4,
            run_time=2,
        ))
        self.wait(0.5)

        # Transition to the next scene
        grid_code = Code(
            code=dedent('''
                g = [
                    '#####...#',
                    '#..#..#.E',
                    '#.##....#',
                    '#..#.#...',
                    '.....##.#',
                    '#...#...#',
                    '#.S...###',
                ]
            ''').strip(),
            tab_width=4,
            language='Python',
            line_spacing=0.6,
            font='Monospace',
            style='monokai',
        ).code.scale(1.2).next_to(title, DOWN, buff=1)

        self.play(LaggedStart(
            FadeOut(*burning_times_mobjects.values()),
            FadeOut(*[clocks[vertex] for vertex in range(len(g)) if vertex not in burning_times]),
            FadeOut(*burned_edges),
            FadeOut(graph),
            Write(grid_code),
            lag_ratio=0.2,
            run_time=1,
        ))
        self.wait(0.1)


class ShortestPathOnGrids(Scene):
    def construct(self):
        title = Title('Shortest Path', include_underline=False)
        grid_code = Code(
            code=dedent('''
                g = [
                    '#####...#',
                    '#..#..#.E',
                    '#.##....#',
                    '#..#.#...',
                    '.....##.#',
                    '#...#...#',
                    '#.S...###',
                ]
            ''').strip(),
            tab_width=4,
            language='Python',
            line_spacing=0.6,
            font='Monospace',
            style='monokai',
        ).code.scale(1.2).next_to(title, DOWN, buff=1)
        dist_code = Code(
            code=dedent('''
                d = [
                    '#####9ⅩⅪ#',
                    '#67#78#ⅩⅪ',
                    '#5##6789#',
                    '#43#5#989',
                    '43234##7#',
                    '#212#456#',
                    '#10123###',
                ]
            ''').strip(),
            tab_width=4,
            language='Python',
            line_spacing=0.6,
            font='Monospace',
            style='monokai',
        ).code.scale(1.2).next_to(title, DOWN, buff=1)
        self.add(title, grid_code)
        self.wait(0.1)

        grid = [
            '#####...#',
            '#..#..#.E',
            '#.##....#',
            '#..#.#...',
            '.....##.#',
            '#...#...#',
            '#.S...###',
        ]

        paths = [(r + 1, c + 2) for r in range(len(grid)) for c in range(len(grid[0])) if grid[r][c] == '.']
        walls = [(r + 1, c + 2) for r in range(len(grid)) for c in range(len(grid[0])) if grid[r][c] == '#']
        self.play(*[Indicate(grid_code[r][c], scale_factor=2.5, color=YELLOW) for r, c in paths], run_time=0.2)
        self.wait(0.1)
        self.play(*[Indicate(grid_code[r][c], scale_factor=1.5, color=RED) for r, c in walls], run_time=0.2)
        self.wait(0.1)

        # Highlight the starting coordinate and then the ending one
        self.play(Indicate(grid_code[7][4], scale_factor=1.5, color=ORANGE), run_time=0.2)
        self.wait(0.1)
        self.play(Indicate(grid_code[2][10], scale_factor=1.5, color=ORANGE), run_time=0.2)
        self.wait(0.1)

        # Pass-through (ShowPassingFlash) from start to end
        path = [(7, 4), (6, 4), (5, 4), (5, 5), (5, 6), (4, 6), (3, 6), (3, 7), (3, 8), (3, 9), (2, 9), (2, 10)]
        self.play(LaggedStart(*[
            ShowPassingFlash(Line(grid_code[u[0]][u[1]].get_center(), grid_code[v[0]][v[1]].get_center(), color=ORANGE, stroke_width=10), time_width=0.9)
            for u, v in zip(path, path[1:])
        ], lag_ratio=0.2, run_time=0.5))
        self.wait(0.1)

        def burn(row: int, col: int, shift: float = 0):
            fire_icon = SVGMobject('bfs/fire.svg').scale(0.2).move_to(grid_code[row + 1][col + 2])
            fire_icon.set_z_index(5)
            animations = [ShowIncreasingSubsets(fire_icon.shift(shift * UP))]
            return fire_icon, animations


        dist = [[-1] * len(grid[0]) for _ in range(len(grid))]
        def spread_fire(row: int, col: int, max_dist: int = 2, replace_grid_with_distance: bool = True):
            """ Perform a BFS starting from the given cell """
            dist[row][col] = 0
            q = deque([(row, col)])
            fire_icons, all_animations = {}, []
            fire, animations = burn(row, col, shift=0)
            fire_icons[(row, col)] = fire
            all_animations += animations
            while q:
                r, c = q.popleft()
                for dr, dc in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and (grid[nr][nc] == '.' or grid[nr][nc] == 'E') and dist[nr][nc] == -1:
                        dist[nr][nc] = dist[r][c] + 1
                        if dist[nr][nc] > max_dist:
                            continue
                        q.append((nr, nc))
                        fire, animations = burn(nr, nc, shift=0.1 if grid[nr][nc] != 'E' else 0)
                        fire_icons[(nr, nc)] = fire
                        all_animations += animations
                if replace_grid_with_distance:
                    all_animations += [FadeOut(grid_code[r + 1][c + 2]), FadeIn(dist_code[r + 1][c + 2])]
                all_animations.append(FadeOut(fire_icons[(r, c)]))

            return fire_icons, all_animations

        all_fires, all_anims = spread_fire(6, 2, max_dist=2)
        self.play(LaggedStart(*all_anims, lag_ratio=0.7, run_time=1))
        self.wait(0.5)

        dist_initial_grid = Code(
            code=dedent('''
                d = [
                    [-1, -1, -1, -1, -1, -1, -1, -1, -1],
                    [-1, -1, -1, -1, -1, -1, -1, -1, -1],
                    [-1, -1, -1, -1, -1, -1, -1, -1, -1],
                    [-1, -1, -1, -1, -1, -1, -1, -1, -1],
                    [-1, -1, -1, -1, -1, -1, -1, -1, -1],
                    [-1, -1, -1, -1, -1, -1, -1, -1, -1],
                    [-1, -1, -1, -1, -1, -1, -1, -1, -1],
                ]
            ''').strip(),
            tab_width=4,
            language='Python',
            line_spacing=0.6,
            font='Monospace',
            style='monokai',
        ).code.next_to(title, DOWN, buff=1).to_edge(RIGHT, buff=1)

        dist_grid = Code(
            code=dedent('''
                d = [
                    [-1, -1, -1, -1, -1,  9, 10, 11, -1],
                    [-1,  6,  7, -1,  7,  8, -1, 10, 11],
                    [-1,  5, -1, -1,  6,  7,  8,  9, -1],
                    [-1,  4,  3, -1,  5, -1,  9,  8,  9],
                    [ 4,  3,  2,  3,  4, -1, -1,  7, -1],
                    [-1,  2,  1,  2, -1,  4,  5,  6, -1],
                    [-1,  1,  0,  1,  2,  3, -1, -1, -1],
                ]
            ''').strip(),
            tab_width=4,
            language='Python',
            line_spacing=0.6,
            font='Monospace',
            style='monokai',
        ).code.next_to(title, DOWN, buff=1).to_edge(RIGHT, buff=1)

        self.remove(
            dist_code[7][3], dist_code[7][4], dist_code[7][5], dist_code[7][6],
            dist_code[6][3], dist_code[6][4], dist_code[6][5],
            dist_code[5][4],
        )
        self.play(grid_code.animate.scale(1 / 1.2).next_to(title, DOWN, buff=1).to_edge(LEFT, buff=1), run_time=0.2)
        self.wait(0.1)

        self.play(Indicate(grid_code[7][4], color=ORANGE, scale_factor=1.5), run_time=0.2)
        self.wait(0.1)

        self.play(Write(dist_initial_grid), run_time=0.2)
        self.wait(0.1)

        # Wiggle all the -1 cells
        self.play(*[
            Wiggle(VGroup(line[i], line[i + 1]), scale_value=1.5, rotation_angle=0.02 * TAU)
            for line in dist_initial_grid[1:-1]
            for i in range(2, len(line) - 1, 4)
        ], run_time=0.5)
        self.wait(0.1)

        # Replace the -1 of the starting coordinate with 0
        dist_initial_grid.save_state()
        self.play(ReplacementTransform(dist_initial_grid[7][10:12], dist_grid[7][10:12]), run_time=0.5)
        self.wait(0.1)

        # Indicate the neighbors
        self.play(
            Indicate(dist_initial_grid[7][6:8], scale_factor=1.5),
            Indicate(dist_initial_grid[6][10:12], scale_factor=1.5),
            Indicate(dist_initial_grid[7][14:16], scale_factor=1.5),
            run_time=0.2,
        )
        self.wait(0.1)

        # Set the neighbor values to 1 (dist_grid)
        self.play(
            ReplacementTransform(dist_initial_grid[7][6:8], dist_grid[7][6:8]),
            ReplacementTransform(dist_initial_grid[6][10:12], dist_grid[6][10:12]),
            ReplacementTransform(dist_initial_grid[7][14:16], dist_grid[7][14:16]),
            run_time=0.2,
        )
        self.wait(0.1)

        # Pass-through (ShowPassingFlash) from start to end
        self.play(LaggedStart(*[
            ShowPassingFlash(Line(grid_code[u[0]][u[1]].get_center(), grid_code[v[0]][v[1]].get_center(), color=ORANGE, stroke_width=10), time_width=0.9)
            for u, v in zip(path, path[1:])
        ], lag_ratio=0.2, run_time=0.5))
        self.wait(0.1)


        init_code = Code(
            code=dedent('''
                d = [[-1] * len(line) for line in g]
                d[6][2] = 0
                q = deque([(6, 2)])
            ''').strip(),
            tab_width=4,
            language='Python',
            line_spacing=0.6,
            font='Monospace',
            style='monokai',
        ).code.to_edge(DOWN, buff=1)

        # Bring back the distance code
        self.play(AddTextLetterByLetter(init_code[0]), run_time=0.01 * len(init_code[0]))
        self.play(
            FadeOut(dist_grid[7][10:12], dist_grid[7][6:8], dist_grid[6][10:12], dist_grid[7][14:16]),
            Restore(dist_initial_grid),
            run_time=0.1,
        )
        self.wait(0.1)

        # Replace the -1 of the starting coordinate with 0
        self.play(AddTextLetterByLetter(init_code[1]), run_time=0.01 * len(init_code[1]))
        self.play(ReplacementTransform(dist_initial_grid[7][10:12], dist_grid[7][10:12]), run_time=0.5)
        self.wait(0.1)

        self.play(AddTextLetterByLetter(init_code[2]), run_time=0.01 * len(init_code[2]))
        self.wait(0.1)

        wide_grid_code = Code(
            code=dedent('''
                g = [
                    ' #   #   #   #   #   .   .   .   #',
                    ' #   .   .   #   .   .   #   .   E',
                    ' #   .   #   #   .   .   .   .   #',
                    ' #   .   .   #   .   #   .   .   .',
                    ' .   .   .   .   .   #   #   .   #',
                    ' #   .   .   .   #   .   .   .   #',
                    ' #   .   S   .   .   .   #   #   #',
                ]
            ''').strip(),
            tab_width=4,
            language='Python',
            line_spacing=0.6,
            font='Monospace',
            style='monokai',
        ).code.scale(0.8).next_to(title, DOWN, buff=0.5).to_edge(RIGHT, buff=0.7)
        self.play(FadeOut(dist_grid[7][10:12]), run_time=0.01)
        self.play(
            TransformMatchingShapes(grid_code, wide_grid_code),
            init_code.animate.scale(0.8).next_to(title, DOWN, buff=0.5).to_edge(LEFT, buff=0.7),
            dist_initial_grid.animate.scale(0.8).to_edge(RIGHT, buff=0.7).to_edge(DOWN, buff=1),
            run_time=0.5,
        )
        self.wait(0.1)

        bfs_code = Code(
            code=dedent(r'''
                while q:
                    r, c = q.popleft()
                    if 0 <= r - 1 < len(g) and \
                            g[r - 1][c] == '.' and \
                            d[r - 1][c] == -1:
                        d[r - 1][c] = d[r][c] + 1
                        q.append((r - 1, c))
                        
                    if 0 <= r + 1 < len(g) and    ...
                    if 0 <= c - 1 < len(g[r]) and ...
                    if 0 <= c + 1 < len(g[r]) and ...
            ''').strip(),
            tab_width=4,
            language='Python',
            line_spacing=0.6,
            font='Monospace',
            style='monokai',
        ).code.scale(0.8).next_to(init_code, DOWN, buff=0.5).align_to(init_code, LEFT)

        self.play(AddTextLetterByLetter(bfs_code[0], run_time=0.01 * len(bfs_code[0])))
        self.wait(0.1)
        self.play(AddTextLetterByLetter(bfs_code[1], run_time=0.01 * len(bfs_code[1])))
        self.wait(0.1)

        # Write the first if statement
        self.play(AddTextLetterByLetter(bfs_code[2], run_time=0.01 * len(bfs_code[2])))
        self.wait(0.1)
        self.play(AddTextLetterByLetter(bfs_code[3], run_time=0.01 * len(bfs_code[3])))
        self.wait(0.1)
        self.play(AddTextLetterByLetter(bfs_code[4], run_time=0.01 * len(bfs_code[4])))
        self.wait(0.1)
        self.play(AddTextLetterByLetter(bfs_code[5], run_time=0.01 * len(bfs_code[5])))
        self.wait(0.1)
        self.play(AddTextLetterByLetter(bfs_code[6], run_time=0.01 * len(bfs_code[6])))
        self.wait(0.1)

        # Write the other 3 if statements
        self.play(AddTextLetterByLetter(bfs_code[8], run_time=0.01 * len(bfs_code[8])))
        self.wait(0.1)
        self.play(AddTextLetterByLetter(bfs_code[9], run_time=0.01 * len(bfs_code[9])))
        self.wait(0.1)
        self.play(AddTextLetterByLetter(bfs_code[10], run_time=0.01 * len(bfs_code[10])))
        self.wait(0.1)

        self.play(
            init_code.animate.scale(0.9).next_to(title, DOWN, buff=0.5).to_edge(LEFT, buff=0.7),
            bfs_code.animate.scale(0.9).next_to(init_code, DOWN, buff=0.5).to_edge(LEFT, buff=0.7),
            wide_grid_code.animate.scale(0.9).next_to(title, DOWN, buff=0.5).to_edge(RIGHT, buff=0.7),
            dist_initial_grid.animate.scale(0.9).to_edge(RIGHT, buff=0.7).to_edge(DOWN, buff=1),
            run_time=0.2,
        )
        self.wait(0.1)

        # Create the queue
        vline1 = DashedLine(3 * UP, 3 * DOWN).next_to(init_code, RIGHT, buff=0.5).align_to(init_code, UP).set_color(ORANGE)
        vline2 = DashedLine(3 * UP, 3 * DOWN).next_to(wide_grid_code, LEFT, buff=0.2).align_to(wide_grid_code, UP).set_color(ORANGE)
        queue_text = Text('Queue:').scale(0.4).next_to(vline1, RIGHT, buff=0.2).align_to(vline1, UP)
        self.play(Create(vline1), Create(vline2), Write(queue_text), run_time=0.5)

        # Highlight the starting coordinate (both in the grid and the distance grid) and add it to the queue
        queue_texts = []
        q = deque()
        def add2queue(row: int, col: int):
            vertex_text = Text(f'({row}, {col})').scale(0.4).next_to(queue_text if len(queue_texts) == 0 else queue_texts[-1], DOWN, buff=0.2 if len(queue_texts) == 0 else 0.1)
            queue_texts.append(vertex_text)
            q.append((row, col))
            self.play(Write(queue_texts[-1]), run_time=0.1)

        def remove_from_queue():
            animations = []
            for text, prev_text in zip(queue_texts[1:], queue_texts):
                animations.append(text.animate.move_to(prev_text))
            self.play(LaggedStart(FadeOut(queue_texts[0]), *animations, lag_ratio=0.3, run_time=0.2))
            queue_texts.pop(0)

        add2queue(6, 2)
        self.wait(0.2)

        # Redefine the `burn` function to use the wide_grid_code
        def burn(row: int, col: int, shift: float = 0):
            fire_icon = SVGMobject('bfs/fire.svg').scale(0.2).move_to(wide_grid_code[row + 1][4 * col + 6])
            fire_icon.set_z_index(50)
            animations = [ShowIncreasingSubsets(fire_icon.shift(shift * UP))]
            return fire_icon, animations

        arrow = Arrow(
            start=LEFT, end=RIGHT, color=RED, buff=0.1,
            stroke_width=10, max_stroke_width_to_length_ratio=15,
            max_tip_length_to_length_ratio=0.5, tip_length=0.2,
        ).scale(0.3).next_to(bfs_code[1], LEFT).shift(0.1 * DOWN)
        dist_grid.scale(0.8 * 0.9).move_to(dist_initial_grid)
        distance = [[-1] * len(grid[0]) for _ in range(len(grid))]

        def bfs_step(r: int, c: int):
            # Add circle around the current cell
            grid_circle = DashedVMobject(Circle(radius=0.2, color=ORANGE)).move_to(wide_grid_code[r + 1][4 * c + 6])
            distance_circle = DashedVMobject(Circle(radius=0.2, color=ORANGE)).move_to(dist_initial_grid[r + 1][4 * c + 3])
            self.play(LaggedStart(
                arrow.animate.next_to(bfs_code[1], LEFT).shift(0.08 * DOWN),
                queue_texts[0].animate.set_color(ORANGE),
                Create(grid_circle), Create(distance_circle),
                lag_ratio=0.5,
                run_time=0.2,
            ))
            self.wait(0.1)

            for statement, (dr, dc) in enumerate([(-1, 0), (1, 0), (0, -1), (0, 1)]):
                nr, nc = r + dr, c + dc
                to_grid_mobj = None
                to_dist_mobj = None
                line = 1 + statement + (1 if statement == 0 else 6)
                self.play(arrow.animate.next_to(bfs_code[line], LEFT).shift(0.06 * DOWN), run_time=0.1)
                if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
                    to_grid_mobj = wide_grid_code[nr + 1][4 * nc + 3 : 4 * nc + 5]
                    to_dist_mobj = dist_initial_grid[nr + 1][4 * nc + 2 : 4 * nc + 4]
                    to_grid_mobj.save_state()
                    to_dist_mobj.save_state()
                    self.play(
                        to_grid_mobj.animate.set_color(WHITE).scale(4 if grid[nr][nc] == '.' else 1.5).set_z_index(100000),
                        to_dist_mobj.animate.set_color(WHITE).scale(1.5).set_z_index(100000),
                        run_time=0.1,
                    )
                    self.wait(0.1)
                if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and (grid[nr][nc] == '.' or grid[nr][nc] == 'E') and distance[nr][nc] == -1:
                    if statement == 0:
                        self.play(arrow.animate.next_to(bfs_code[line + 3], LEFT).shift(0.12 * DOWN), run_time=0.1)
                        self.wait(0.1)
                        distance[nr][nc] = distance[r][c] + 1
                        self.play(arrow.animate.next_to(bfs_code[line + 4], LEFT).shift(0.12 * DOWN), run_time=0.1)
                        self.wait(0.2)
                    self.play(
                        ReplacementTransform(
                            dist_initial_grid[nr + 1][4 * nc + 2: 4 * nc + 4],
                            dist_grid[nr + 1][4 * nc + 2: 4 * nc + 4]
                        ),
                        run_time=0.1,
                    )
                    to_dist_mobj = None
                    add2queue(nr, nc)
                    self.wait(0.2)
                if to_grid_mobj is not None:
                    self.play(Restore(to_grid_mobj), run_time=0.1)
                if to_dist_mobj is not None:
                    self.play(Restore(to_dist_mobj), run_time=0.1)


            self.play(FadeOut(grid_circle, distance_circle), run_time=0.1)
            remove_from_queue()
            self.play(arrow.animate.next_to(bfs_code[0], LEFT), run_time=0.1)
            self.wait(0.1)

        bfs_step(*q.popleft())
        bfs_step(*q.popleft())
        self.play(FadeOut(arrow), run_time=0.2)

        dist = [[-1] * len(grid[0]) for _ in range(len(grid))]
        all_fires, all_anims = spread_fire(6, 2, max_dist=3, replace_grid_with_distance=False)
        self.play(LaggedStart(*all_anims, lag_ratio=0.4, run_time=1))
        self.wait(0.2)

        bfs_step(*q.popleft())
        bfs_step(*q.popleft())
        self.play(FadeOut(arrow), run_time=0.2)

        # Indicate the distance grid (non-minus-one cells):
        # (r, c) => r + 1, 4 * c + 3: 4 * c + 4
        # (6, 2) => 7, 11:12
        # (5, 2) => 6, 11:12
        # (6, 3) => 7, 15:16
        # (6, 1) => 7, 7:8
        self.play(LaggedStart(
            Indicate(dist_initial_grid[7][11:12], scale_factor=1.5),
            AnimationGroup(
                Indicate(dist_initial_grid[6][11:12], scale_factor=1.5),
                Indicate(dist_initial_grid[7][15:16], scale_factor=1.5),
                Indicate(dist_initial_grid[7][7:8], scale_factor=1.5),
            ),
            AnimationGroup(
                Indicate(dist_initial_grid[6][7:8], scale_factor=1.5),
                Indicate(dist_initial_grid[5][11:12], scale_factor=1.5),
                Indicate(dist_initial_grid[6][15:16], scale_factor=1.5),
                Indicate(dist_initial_grid[7][19:20], scale_factor=1.5),
            ),

            lag_ratio=0.2,
            run_time=2,
        ))
        self.wait(0.1)

        # while q:
        #     bfs_step(*q.popleft())
        self.play(FadeOut(arrow), run_time=0.2)
        self.wait(0.1)

        # Transition to the next scene
        self.play(
            ReplacementTransform(title, Title('Breadth First Search', include_underline=False)),
            FadeOut(dist_initial_grid, wide_grid_code, bfs_code, init_code, queue_text, vline1, vline2, *queue_texts),
            run_time=0.5,
        )


class ComplexityAnalysis(Scene):
    def construct(self):
        title = Title('Breadth First Search', include_underline=False)
        self.add(title)
        self.wait(0.1)

        vertices = list(range(len(g)))
        edges = [(i, j) for i, neighbors in enumerate(g) for j in neighbors]

        graph = Graph(
            vertices, edges,
            layout=layout,
            labels=True,
            vertex_config={'radius': 0.4, 'stroke_width': 0, 'fill_color': WHITE},
            edge_config={'stroke_width': 5},
        ).scale(0.5).next_to(title, DOWN, buff=1).to_edge(LEFT, buff=1)

        self.play(Create(graph), run_time=0.5)
        for label in graph._labels.values():
            label.set_z_index(10)
        self.wait(0.2)

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
        ).code.scale(0.9).next_to(title, DOWN, buff=1).to_edge(RIGHT, buff=1.5)

        for line in code.chars:
            if line:
                self.play(AddTextLetterByLetter(line, run_time=0.01 * len(line)))
        self.wait(0.1)

        vertices_text = Text('V vertices').scale(0.6).next_to(graph, DOWN, buff=0.5).align_to(graph, LEFT)
        edges_text = Text('E edges').scale(0.6).next_to(vertices_text, DOWN, buff=0.2).align_to(vertices_text, LEFT)

        self.play(LaggedStart(
            Write(vertices_text),
            AnimationGroup(
                *[Indicate(graph.vertices[i], scale_factor=1.5, color=ORANGE) for i in range(len(g))],
                *[label.animate.set_z_index(100) for label in graph._labels.values()],
            ),
            lag_ratio=0.5,
            run_time=0.5,
        ))

        self.play(LaggedStart(
            Write(edges_text),
            AnimationGroup(
                *[Indicate(edge, scale_factor=1, color=RED) for edge in graph.edges.values()],
            ),
            lag_ratio=0.5,
            run_time=0.5,
        ))

        # Highlight the not used parts of the if statement
        self.play(Indicate(code[6]), run_time=0.2)
        self.wait(0.1)

        # Highlight the for loop
        self.play(Indicate(code[5]), run_time=0.2)
        self.wait(0.1)

        # Move from node 7 to node 6
        dot = Dot(radius=0.1, color=ORANGE).move_to(graph.vertices[7])
        line = Line(graph.vertices[7], graph.vertices[6], color=ORANGE, stroke_width=5, buff=0.1)
        self.play(MoveAlongPath(dot, line), run_time=0.5)
        self.wait(0.1)
        self.play(MoveAlongPath(dot, line.rotate(PI), run_time=0.5))
        self.play(FadeOut(dot), run_time=0.1)

        time_complexity = Tex(r'Time Complexity: $\mathcal{O}(V + E)$').scale(0.8).align_to(code, LEFT).align_to(vertices_text, UP)
        self.play(Write(time_complexity), run_time=0.2)

        memory_complexity = Tex(r'{{Memory Complexity:}} {{$\mathcal{O}(V)$}}').scale(0.8).align_to(code, LEFT).align_to(edges_text, UP)
        self.play(Write(memory_complexity[0]), run_time=0.2)

        # Indicate the graph
        self.play(Indicate(graph), *[label.animate.set_z_index(10) for label in graph._labels.values()], run_time=0.2)
        self.wait(0.1)

        # Indicate the used array
        self.play(Indicate(code[0][:5]), run_time=0.5)
        self.wait(0.1)

        # Indicate the queue
        self.play(Indicate(code[1]), run_time=0.5)
        self.wait(0.1)

        self.play(Write(memory_complexity[2]), run_time=0.2)
        self.wait(0.1)

        # Transition to the next scene
        self.play(
            ReplacementTransform(title, Title('BFS', include_underline=False)),
            FadeOut(graph, code, time_complexity, memory_complexity, vertices_text, edges_text),
            run_time=0.5,
        )
        self.wait(0.1)


class Practice(Scene):
    def construct(self):
        title = Title('BFS', include_underline=False)
        self.add(title)
        self.wait(0.1)

        # Arrow from the title to “Math”
        math_text = Text('Math').scale(0.7).next_to(title, DOWN, buff=1).to_edge(LEFT, buff=2)
        math_arrow = Arrow(
            title.get_center(), math_text.get_center(), buff=0.7, color=RED,
            stroke_width=6, max_stroke_width_to_length_ratio=15,
            max_tip_length_to_length_ratio=0.5, tip_length=0.25,
        )
        math_subtitle = Text('Get A ⮕ B', color=YELLOW).scale(0.6).next_to(math_text, DOWN, buff=0.5)
        self.play(LaggedStart(
            Create(math_arrow),
            Write(math_text),
            Write(math_subtitle),
            lag_ratio=0.5,
            run_time=0.5,
        ))
        self.wait(0.1)

        check = SVGMobject('bfs/check.svg').scale(0.3).set_fill(GREEN).next_to(math_subtitle, DOWN, buff=0.5)
        self.play(Create(check), run_time=0.2)
        self.wait(0.1)
        self.play(FadeOut(check), run_time=0.2)
        self.wait(0.1)

        # Arrow from title to “Multi-Dimensional”
        multi_text = Text('Multi-Dimensional').scale(0.7).next_to(math_text, RIGHT, buff=0.5).shift(2 * DOWN)
        multi_arrow = Arrow(
            title.get_center(), multi_text.get_center(), buff=0.6, color=RED,
            stroke_width=6, max_stroke_width_to_length_ratio=15,
            max_tip_length_to_length_ratio=0.5, tip_length=0.25,
        )
        multi_subtitle = Text('used[][][][]', color=YELLOW).scale(0.6).next_to(multi_text, DOWN, buff=0.5)
        self.play(LaggedStart(
            Create(multi_arrow),
            Write(multi_text),
            Write(multi_subtitle),
            lag_ratio=0.5,
            run_time=0.5,
        ))
        self.wait(0.1)

        # Arrow from title to “Multi-Source”
        multi_source_text = Text('Multi-Source').scale(0.7).next_to(multi_text, RIGHT, buff=0.5)
        multi_source_arrow = Arrow(
            title.get_center(), multi_source_text.get_center(), buff=0.6, color=RED,
            stroke_width=6, max_stroke_width_to_length_ratio=15,
            max_tip_length_to_length_ratio=0.5, tip_length=0.25,
        )
        multi_source_subtitle = Text('O O O O', color=YELLOW).scale(0.6).next_to(multi_source_text, DOWN, buff=0.5)
        self.play(LaggedStart(
            Create(multi_source_arrow),
            Write(multi_source_text),
            Write(multi_source_subtitle),
            lag_ratio=0.5,
            run_time=0.5,
        ))
        self.wait(0.1)

        # Arrow from title to “Much More…”
        much_more_text = Text('Much More…').scale(0.7).next_to(title, DOWN, buff=1).to_edge(RIGHT, buff=2)
        much_more_arrow = Arrow(
            title.get_center(), much_more_text.get_center(), buff=0.7, color=RED,
            stroke_width=6, max_stroke_width_to_length_ratio=15,
            max_tip_length_to_length_ratio=0.5, tip_length=0.25,
        )
        much_more_subtitle = Text('...', color=YELLOW).scale(0.6).next_to(much_more_text, DOWN, buff=0.5)
        self.play(LaggedStart(
            Create(much_more_arrow),
            Write(much_more_text),
            Write(much_more_subtitle),
            lag_ratio=0.5,
            run_time=0.5,
        ))
        self.wait(0.1)



class ClosingScene(Scene):
    def construct(self):
        title = Title('Breadth First Search', include_underline=False)
        self.add(title)

        vertices = list(range(len(g)))
        edges = [(i, j) for i, neighbors in enumerate(g) for j in neighbors]

        graph = Graph(
            vertices, edges,
            layout=layout,
            labels=True,
            vertex_config={'radius': 0.4, 'stroke_width': 0, 'fill_color': WHITE},
            edge_config={'stroke_width': 5},
        ).scale(0.5).next_to(title, DOWN, buff=1).to_edge(LEFT, buff=1)
        self.add(graph)

        for label in graph._labels.values():
            label.set_z_index(10)

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
        ).code.scale(0.9).next_to(title, DOWN, buff=1).to_edge(RIGHT, buff=1.5)

        self.add(code)

        vertices_text = Text('V vertices').scale(0.6).next_to(graph, DOWN, buff=0.5).align_to(graph, LEFT)
        edges_text = Text('E edges').scale(0.6).next_to(vertices_text, DOWN, buff=0.2).align_to(vertices_text, LEFT)
        time_complexity = Tex(r'Time Complexity: $\mathcal{O}(V + E)$').scale(0.8).align_to(code, LEFT).align_to(vertices_text, UP)
        memory_complexity = Tex(r'{{Memory Complexity:}} {{$\mathcal{O}(V)$}}').scale(0.8).align_to(code, LEFT).align_to(edges_text, UP)
        self.add(vertices_text, edges_text, time_complexity, memory_complexity)
        self.wait(0.1)

        # Re-implement the BFS algorithm
        self.play(FadeOut(code), run_time=0.5)
        for line in code:
            if line:
                self.play(AddTextLetterByLetter(line, run_time=0.01 * len(line)))
        self.wait(0.1)

