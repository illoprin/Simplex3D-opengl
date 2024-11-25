from PIL import Image
from datetime import datetime

from src.settings import *
from src.shader_program import ShaderManager
from src.player.base_player import Player
from src.world.scene import Scene
from src.textures import TextureManager
from src.world_objects.game_object_types import *
from src.light.point_light import PointLight

class SimplexEngine():
	def __init__(self, ctx, app):
		self.ctx = ctx
		self.app = app
		self.delta_time = 0
		self.fps = 0
		self.time = 0

		# init filesystem
		self.init_filesystem()

		self.program = ShaderManager(self.ctx)
		self.player = Player(
		    self.app, self.program.programs['standard'], rotation=glm.vec2(0, -90)
		)
		self.tm = TextureManager(self.ctx, self.program)

		# Create scene instance
		self.scene = Scene(self.ctx, self.program, self.program.programs['axis'])
		# Add objects to scene
		self.init_scene()

		# Create framebuffer for screenshots
		self.main_fbo = self.ctx.simple_framebuffer((int(WIN_RES.x), int(WIN_RES.y)))

		# scene needs batch before render
		self.scene.batch()

	def init_scene(self):
		# Add scene objects (debug)
		self.scene.add_s(TestLevel())
		self.scene.add_s(Cube_N(pos=(25, -4, 0), rot=(0, -90, 0), texture=1))
		self.scene.add_s(Sphere(pos=(25, -4, 4), rot=(0, 180, 0), texture=4))

		self.scene.static_ls = [
			PointLight((0, 0, 0), (0.41, 0.43, .47), 10.0, 5, intensity=1),
			PointLight((14, 0, 15), (0.41, 0.35, .23), 7.0, 5, intensity=1),
		]
		self.blue_light = PointLight((23, -1, 2), (0.41, 0.35, .65), 7.0, 2, intensity=1)
		self.scene.add_dl(self.blue_light)
		#############################

	def init_filesystem(self):
		if not os.path.isdir(PATH_SCREENSHOTS):
			os.mkdir(PATH_SCREENSHOTS)
			print ('Simplex Engine: Screenshots folder created')
		if not os.path.isdir(PATH_CACHE):
			os.mkdir(PATH_CACHE)
			print ('Simplex Engine: Cache folder created')


	def update(self, time, frametime):
		if self.app.wnd.mouse_exclusivity:
			self.player.move()
			self.program.set_uniform('standard', 'player_position', self.player.position)
		self.player.update()
		self.program.set_byte_data('axis', 'm_projection', self.player.projection)
		self.program.set_byte_data('axis', 'm_view', self.player.view)
		self.update_statements(time, frametime)

	def update_statements(self, time, frametime):
		self.time = time
		self.delta_time = frametime
		self.fps = 1 / self.delta_time if frametime else 60

		if self.time % 1 < 0.02:
			self.app.wnd.title = f'{BASE_TITLE} | FPS: {self.fps: .1f}'

	def render(self):
		# write render code here
		self.blue_light.set_position([23, -1, 2 + glm.sin(self.time)*2.35])
		#######################
		# RENDERING
		# set clear color
		self.ctx.clear(*CLEAR_COLOR)
		self.scene.render(self.time)

	def take_screenshot(self):
		self.main_fbo.clear(0.0, 0.0, 0.0, 1.0)
		self.main_fbo.use()
		self.scene.render()
		file_path = f'{PATH_SCREENSHOTS}/{datetime.now().strftime("%d-%m-%YT%H_%M-%S")}.jpg' 
		image = Image.frombytes('RGB', self.main_fbo.size, self.main_fbo.read(), 'raw', 'RGB', 0, -1)
		image.save(file_path, format='JPEG', quality=80)

	def destroy(self):
		self.scene.clear()
		self.program.clear()
		self.main_fbo.release()