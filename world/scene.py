import numpy as np

from world.scene_batcher import SceneBatcher
from world_objects.game_object_types import *
from shader_program import ShaderManager
from light.point_light import PointLight

class Scene:
    def __init__ (self, ctx: mgl.Context, program: ShaderManager, debug_program: mgl.Program):
        self.ctx = ctx
        self.program = program
        # GAME OBJECT LISTS
        self.static_objects= []
        self.dynamic_objects = []

        # LIGHTS LISTS
        self.static_ls = []
        self.dynamic_ls = []

        self.adding_objects()

        self.batcher = SceneBatcher(self.ctx, self.program, debug_program)
        self.batcher.debug = False
        self.batcher.batch_scene(self.static_objects, self.dynamic_objects, self.static_ls, self.dynamic_ls)

    def adding_objects(self):
        # self.static_objects = [
        #     Cube_N(pos=(-4, 0, 0)),
        #     Sphere(pos=(2, 0, 0)),
        #     Plane(scl=(20, 20, 20)),
        #     Cone(pos=(10, 0, -10), scl=(10, 10, 10))
        # ]
        # self.dynamic_cude = Cube_N(pos=(3, 0, -2))
        # self.add_d(self.dynamic_cude)

        self.add_s(TestLevel())
        self.add_s(Cube_N(pos=(25, -4, 0), rot=(0, -90, 0),texture=1))
        self.add_s(Sphere(pos=(25, -4, 4), rot=(0, 180, 0), texture=4))

        self.static_ls = [
            PointLight((0, 0, 0), (0.41, 0.43, .47), 10.0, 5, intensity=1),
            PointLight((14, 0, 15), (0.41, 0.35, .23), 7.0, 5, intensity=1),
        ]
        self.blue_light = PointLight((23, -1, 2), (0.41, 0.35, .65), 7.0, 2, intensity=1)

        self.add_dl(self.blue_light)

    def add_s(self, obj: GameObject):
        self.static_objects.append(obj)

    def add_d(self, obj: GameObject):
        self.dynamic_objects.append(obj)

    def add_sl (self, s_light: PointLight):
        self.static_ls.append(s_light)
    def add_dl (self, d_light: PointLight):
        self.dynamic_ls.append(d_light)

    def render(self, time):
        # write render code here
        self.blue_light.set_position((23, -1, (np.sin(time)+2)*2))

        # last func
        # render scene with all changes
        self.batcher.render()

    def clear(self):
        self.batcher.clear()
