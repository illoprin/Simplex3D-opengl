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

        self.batcher = SceneBatcher(self.ctx, self.program, debug_program)
        self.batcher.debug = False

    def batch(self):
        self.batcher.batch_scene(self.static_objects, self.dynamic_objects, self.static_ls, self.dynamic_ls) 
        

    # Add static object
    def add_s(self, obj: GameObject):
        self.static_objects.append(obj)

    # Add dynamic obeject
    def add_d(self, obj: GameObject):
        self.dynamic_objects.append(obj)

    # Add static light
    def add_sl (self, s_light: PointLight):
        self.static_ls.append(s_light)
    
    # Add dynamic light
    def add_dl (self, d_light: PointLight):
        self.dynamic_ls.append(d_light)

    # Render func can be called after appying all changes to the scene
    def render(self, time=0):
        # render scene with all changes
        self.batcher.render()

    def clear(self):
        self.batcher.clear()
