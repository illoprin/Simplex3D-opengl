from src.settings import *

class ShaderManager():

    def __init__(self, context: mgl.Context):
        self.ctx = context
        self.programs = {
            'standard': self.load_shader('base_mesh', 'phong'),
            'axis': self.load_shader('axis', 'axis')
        }

    def set_byte_data(self, program_name: str, uniform_name: str, value: any):
        self.programs[program_name][uniform_name].write(value)

    def set_uniform(self, program_name: str, uniform_name: str, value):
        self.programs[program_name][uniform_name] = value

    def load_shader(self, vert, frag):
        with open(f'src/shaders/{vert}.vert') as file:
            vertex_shader = file.read()

        with open(f'src/shaders/{frag}.frag') as file:
            fragment_shader = file.read()

        program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        print(f"ShaderProgram: Shader {vert}.vert loaded")
        print(f"ShaderProgram: Shader {frag}.frag loaded")
        return program

    def clear(self):
        [program.release() for program in self.programs.values()]
        print("Shader Program: All programs cleared")
