import math
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
            vertex_config={'radius': 0.4, 'stroke_width': 0, 'fill_color': WHITE},
            edge_config={'stroke_width': 5},
        ).shift(DOWN)

        self.add(graph)
        for label in graph._labels.values():
            label.set_z_index(10)
        self.wait(0.2)


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

        burn(7)
        self.wait(1)

        def spread_fire(source: int, target: int):
            sparkler = SVGMobject('bfs/sparks.svg').scale(0.3).move_to(graph.vertices[source], DOWN).set_fill('#ff9d33')
            sparkler.set_z_index(5)

            edge = Line(graph.vertices[source].get_center(), graph.vertices[target].get_center(), buff=0.4)
            burned_edge = VMobject()
            burned_edge.add_updater(lambda x: x.become(Line(
                edge.get_start(), sparkler.get_center(), stroke_width=6,
            ).set_color(DARK_GRAY)))
            self.add(sparkler, burned_edge)

            self.play(MoveAlongPath(sparkler, edge, run_time=0.6, rate_func=linear))
            self.remove(sparkler)
            burning_target = burn(target)
            return burning_target

        spread_fire(7, 5)
        spread_fire(7, 6)
        spread_fire(5, 8)
        spread_fire(5, 3)
        spread_fire(5, 4)
        spread_fire(6, 10)
        spread_fire(8, 9)
        spread_fire(10, 11)
        spread_fire(9, 2)
        spread_fire(2, 0)
        spread_fire(2, 1)
        self.wait(3)
