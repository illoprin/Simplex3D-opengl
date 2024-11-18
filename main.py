from settings import *
from shader_program import ShaderManager
from player.base_player import Player
from world.scene import Scene
from textures import TextureManager

from pathlib import Path

class SimplexEngine(mglw.WindowConfig):
    resource_dir = (Path(__file__).parent / 'assets').resolve()
    gl_version = (4, 3)
    window_size = WIN_RES
    aspect_ratio = ASPECT
    title = BASE_TITLE
    resizable = False
    vsync = True


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.time = .001
        self.delta_time = .001
        self.fps = 1

        # control setup
        self.wnd.mouse_exclusivity = True

        self.ctx.enable(OPENGL_STATEMENTS)
        self.ctx.multisample = True
        self.on_init()


    def on_init(self):
        self.program = ShaderManager(self.ctx)
        self.player = Player(
            self, self.program.programs['standard'], rotation=glm.vec2(0, -90)
        )
        self.tm = TextureManager(self.ctx, self.program)

        self.scene = Scene(self.ctx, self.program, self.program.programs['axis'])


    def render(self, time, frametime):
        self.time = time
        self.ctx.clear(*CLEAR_COLOR)
        # update display values
        self.update_statements(frametime)
        # update world statements
        self.update_scene()

        # write render code here
        self.scene.render(self.time)

    def update_scene(self):
        if self.wnd.mouse_exclusivity:
            self.player.move()
            self.program.set_uniform('standard', 'player_position', self.player.position)
        self.player.update()
        self.program.set_byte_data('axis', 'm_projection', self.player.projection)
        self.program.set_byte_data('axis', 'm_view', self.player.view)


    def update_statements(self, frametime: float):
        self.delta_time = frametime
        self.fps = 1 / self.delta_time if frametime else 60
        if self.time % 1 < 0.02:
            self.wnd.title = f'{BASE_TITLE} | FPS: {self.fps: .1f}'

    def key_event(self, key, action, modifiers):
        if action == self.wnd.keys.ACTION_PRESS:
            if key == self.wnd.keys.TAB:
                self.wnd.mouse_exclusivity = not self.wnd.mouse_exclusivity
            if key == self.wnd.keys.F2:
                self.scene.batcher.render_mode = mgl.LINES
            if key == self.wnd.keys.F3:
                self.scene.batcher.render_mode = mgl.TRIANGLES

        self.player.handle_event(action, key)

    def mouse_position_event(self, x, y, dx, dy):
        if self.wnd.mouse_exclusivity:
            self.player.handle_rotation(dx, -dy)


    def close(self):
        self.scene.clear()
        self.program.clear()


if __name__ == '__main__':
    mglw.run_window_config(SimplexEngine)
