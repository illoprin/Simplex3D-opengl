import moderngl_window as mglw
from pathlib import Path

from src.settings import *
from src.engine import SimplexEngine


class SimplexView(mglw.WindowConfig):
    # resource_dir = (Path(__file__).parent / 'assets').resolve()
    gl_version = (4, 3)
    window_size = WIN_RES
    aspect_ratio = ASPECT
    title = BASE_TITLE
    resizable = False
    vsync = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # control setup
        self.wnd.mouse_exclusivity = True

        self.ctx.enable(OPENGL_STATEMENTS)
        self.ctx.multisample = True
        self.engine = SimplexEngine(self.ctx, self)
        
    def key_event(self, key, action, modifiers):
        if action == self.wnd.keys.ACTION_PRESS:
            if key == self.wnd.keys.TAB:
                self.wnd.mouse_exclusivity = not self.wnd.mouse_exclusivity
            if key == self.wnd.keys.F2:
                self.engine.scene.batcher.render_mode = mgl.LINES
            if key == self.wnd.keys.F3:
                self.engine.scene.batcher.render_mode = mgl.TRIANGLES
            if key == self.wnd.keys.F5:
                self.engine.take_screenshot()

        self.engine.player.handle_speed_modifer(action, key)

    def mouse_position_event(self, x, y, dx, dy):
        if self.wnd.mouse_exclusivity:
            self.engine.player.handle_rotation(dx, -dy)

    def render(self, time, frametime):
        self.engine.update(time, frametime)
        self.engine.render()

    def close(self):
        self.engine.destroy()

if __name__ == '__main__':
    mglw.run_window_config(SimplexView)