from settings import *
from mesh.meshes import *
from world_objects.game_object import GameObject
from shader_program import ShaderManager
from world_objects.debug_objects import *

class SceneBatcher():
    def __init__(self, ctx: mgl.Context, program: ShaderManager, debug_program: mgl.Program):
        self.ctx = ctx
        self.shader_mgr = program
        self.debug_program = debug_program
        # scene objects
        self.dynamic_lights = []
        self.static_lights = []
        self.go_static_vaos = []

        self.go_dynamic_vaos = []
        self.go_dynamic = []


        self.debug = True

    def batch_lights(self, static_lights, dynamic_lights):
        self.dynamic_lights = dynamic_lights
        self.static_lights = static_lights
        self.dynamic_lights_offset = 0
        self.send_static_info(self.static_lights)

    def send_static_info(self, static: list):
        # ALL static objects reading
        for num, light in enumerate(static):
            # PARTICULAR object attributes reading
            for name, value in light.attributes.items():
                if name == 'type':
                    type = value
                    continue
                self.shader_mgr.set_uniform(
                    'standard', f'{type}[{num}].{name}', value
                )
            self.dynamic_lights_offset += 1

    def send_dynamic_info(self, dynamic: list):
        # ALL dynamic objects reading
        for num, light in enumerate(dynamic):
            # PARTICULAR object attributes reading
            for name, value in light.attributes.items():
                if name == 'type':
                    type = value
                    continue
                self.shader_mgr.set_uniform(
                    'standard', f'{type}[{num+self.dynamic_lights_offset}].{name}', value
                )

    @staticmethod
    def get_axis_of_all(objects: list[GameObject, ...]):
        debug_objects = []
        for go in objects:
            debug_objects.append(GizmoAxis(m_model=go.m_model/go.origin))
        return debug_objects


    def batch_scene(self, static_objects=[], dynamic_objects=[], static_lights=[], dynamic_lights=[]):
        if self.debug:
            debug_objects = self.get_axis_of_all(static_objects)
            self.batch_debug_meshes(debug_objects)

        # Static objects
        # Sorting template
        # "mesh_name": list(GameObject)
        go_static = self.get_sorted_data(static_objects)
        # list of tuples for static GameObjects
        # (number of objects, VAO)
        self.go_static_vaos = self.get_static_vaos(go_static)

        # Dynamic objects
        self.go_dynamic = self.get_sorted_data(dynamic_objects)
        self.go_dynamic_vaos = self.get_dynamic_vaos(self.go_dynamic)


        self.batch_lights(static_lights, dynamic_lights)
        self.set_statements()


    def batch_debug_meshes(self, axis_objects):
        sorted_debug_objects = self.get_sorted_data(axis_objects)
        # list of tuples for debug Objects such as Axis, Bound lines and etc
        self.d_vaos = self.get_static_vaos(sorted_debug_objects, self.debug_program)

    @staticmethod
    def get_sorted_data(object_list: list[GameObject, ...]):
        sorted = {}
        for obj in object_list:
            if obj.mesh.name in sorted.keys():
                sorted[obj.mesh.name].append(obj)
            else:
                sorted[obj.mesh.name] = [obj]
        print(sorted)
        return sorted


    @staticmethod
    def get_GO_models_list(go_list):
        models = []
        for game_object in go_list:
            models.append(np.hstack(game_object.m_model.to_list(), dtype='f4'))
        models = np.array(models, dtype='f4')
        return models

    @staticmethod
    def get_GO_texture_ids_list(go_list):
        ids = []
        for game_object in go_list:
            ids.append(game_object.texture)
        ids = np.array(ids, dtype='i4')
        return ids

    def get_GO_list_data(self, mesh_name, go_list):
        models = SceneBatcher.get_GO_models_list(go_list)
        vertex_data = np.hstack([data for data in go_list[0].mesh.data.values()], dtype='f4')
        texture_ids = SceneBatcher.get_GO_texture_ids_list(go_list)
        print(f'Scene Batcher: vertex data for {mesh_name} is {vertex_data}')

        mesh = go_list[0].mesh
        format_data = mesh.format_data
        attributes = mesh.attributes

        print (f'Scene Batcher: models for {mesh_name} is {models}')
        print (f'Scene Batcher: texture_ids for {mesh_name} is {texture_ids}')

        model_vbo = self.ctx.buffer(models)
        vertex_vbo = self.ctx.buffer(vertex_data)
        textures_vbo = self.ctx.buffer(texture_ids)

        current_vao = self.get_vao(
            vertex_vbo, attributes, format_data, model_vbo, textures_vbo, self.shader_mgr.programs['standard']
        )
        return {
            'vertex': vertex_vbo,
            'textures': textures_vbo,
            'model': model_vbo,
            'vao': current_vao
        }



    def get_static_vaos(self, sorted_object_list):
        vaos = []
        for mesh_name, game_object_list in sorted_object_list.items():
            data = self.get_GO_list_data(mesh_name, game_object_list)
            vaos.append((len(game_object_list), data['vao']))
        print(f'Scene Batcher: VAOs array generated {vaos}')
        return vaos

    def get_dynamic_vaos(self, sorted_go_list):
        # Generates: list[(Num of Instances, VAO, MODELS_VBO)]
        vaos = []
        for mesh_name, go_list in sorted_go_list.items():
            data = self.get_GO_list_data(mesh_name, go_list)
            vaos.append((len(go_list), data['vao'], data['models'], mesh_name))
        print (f'Scene Batcher: Dynamic GO VAO array generated: {vaos}')
        return vaos

    def get_vao(self, vertex_vbo, attributes, format_data, model_vbo, textures_vbo, program):
        vao = self.ctx.vertex_array(
            program,
            [
                (vertex_vbo, f'{format_data} /v', *attributes),
                (model_vbo, '16f /i', 'in_model'),
                (textures_vbo, '1i /i', 'in_tex_id')
            ]
        )
        return vao

    def set_statements(self):
        self.render_mode = 0x0004

    def render(self):

        #### Static Objects ####
        # 0 index in vaos array - number of instances
        # 1 index in vaos array - VAO
        # 2 index in vaos array - draw mode
        for instances, vao in self.go_static_vaos:
            
            vao.render(instances=instances, mode=self.render_mode)
        #######################

        #### Dynamic Objects ####
        for instances, vao, models_vbo, mesh_name in self.go_dynamic_vaos:
            models_vbo.write(SceneBatcher.get_GO_models_list(self.go_dynamic[mesh_name]))
            vao.render(instances=instances, mode=self.render_mode)
        #######################

        # DEBUG
        if self.debug:
            for instances, vao in self.d_vaos:
                vao.render(instances=instances, mode=mgl.LINES)
        #######

        # SEND DYNAMIC LIGHTS INFO TO SHADER
        self.send_dynamic_info(self.dynamic_lights)
        # print(f'Scene Bather: draw calls proceed {len(self.vaos)}')

    def clear(self):
        [vao.release() for instances, vao in self.go_static_vaos]
        [vao.release() for instances, vao, models_vbo, mesh_name in self.go_dynamic_vaos]

        if self.debug:
            [vao.release() for instances, vao in self.d_vaos]

        print('Scene Batcher: All VAOs cleared')