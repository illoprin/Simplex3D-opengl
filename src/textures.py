from src.settings import *
import pygame as pg
import pathlib
import re
import os

class TextureManager:

	def __init__(self, ctx: mgl.Context, program: mgl.Program):
		self.ctx = ctx
		self.exists = False
		if not self.exists:
			array_path = build_texture_array('assets/textures/dev', 'dev_array.png')
			self.exists = True
		array = self.load_array('dev_array.png')
		program.set_uniform('standard', 'texture_array', 0)

	
	def load_array(self, file_path: str, alpha=False) -> int:
		i_format = 'RGBA' if alpha else 'RGB'
		i_comp = 4 if alpha else 3

		image = pg.image.load(f'cache/{file_path}')
		image = pg.transform.flip(image, flip_x=False, flip_y=False)
		print(f'Texture Manager: Texture array {file_path} loaded')

		units_num = image.get_height() // image.get_width()
		texture = self.ctx.texture_array(
			size=(image.get_width(), image.get_height() // units_num, units_num),
			components=i_comp,
			data=pg.image.tostring(image, i_format, False)
		)
		texture.anisotropy = 32.0
		texture.build_mipmaps()
		texture.filter = (mgl.NEAREST, mgl.NEAREST)
		texture.use(0)
		return texture



def build_texture_array(load_path, array_filename, file_format='jpg', tex_size=256):
	'''
		Square Textures ONLY
	'''
	save_path = os.path.realpath('cache/' + array_filename)
	load_path = os.path.realpath(load_path)
	texture_paths = [
		item for item in pathlib.Path(load_path).rglob(f'*.{file_format}') if item.is_file()
	]
	texture_paths = sorted(
		texture_paths,
		key=lambda tex_path: int(re.search('\\d+', str(tex_path)).group(0))
	)
	print (*texture_paths)

	# Create empty surface
	texture_array = pg.Surface([tex_size, tex_size*len(texture_paths)], pg.SRCALPHA, 32)

	for i, path in enumerate(texture_paths):
		image = pg.image.load(path)
		image = pg.transform.flip(image, flip_x=False, flip_y=True)
		texture_array.blit(image, (0, i*tex_size))

	pg.image.save(texture_array, save_path)
	print (f'Texture Manager: Array {array_filename} was built')
	return save_path
