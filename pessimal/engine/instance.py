# pragma: exclude file
# instance requires OpenGL

from OpenGL.GL import *
from .math_support import *
from .model import Model


class Instance:
	def __init__(self):
		self.model = None
		self.transform = m44_get_identity()
		self.colour_tint = None
		self.x_pos, self.y_pos, self.z_pos = [0.0, 0.0, 0.0]
		self.textures = {}
		self.shader = None

	def set_model(self, model: Model):
		self.model = model

	def set_transform(self, transform: list):
		assert(len(transform) == 16)
		self.transform = transform

	def set_colour(self, colour: list):
		assert(len(colour) in [3, 4])
		self.colour_tint = colour

	def set_transform_y_rotation(self, y):
		self.transform = m44_get_y_rot(y)[:12] + [self.x_pos, self.y_pos, self.z_pos, 1.0]

	def set_transform_pos(self, pos):
		self.x_pos, self.y_pos, self.z_pos = pos
		self.transform = self.transform[:12] + pos + [1.0]

	def set_shader(self, new_shader):
		self.shader = new_shader

	def set_texture(self, texture, slot):
		self.textures[slot] = texture

	def render(self):
		if self.shader is not None:
			for slot, texture in self.textures.items():
				self.shader.set_texture(slot, texture)
			self.shader.draw_model(self.model, self.transform, self.colour_tint)

class InstanceSet(Instance):
	def __init__(self):
		super().__init__()
		self.positions = []
		self.positions_data = None
		self.positions_vbo = glGenBuffers(1)

	def get_instance_vbo(self):
		if self.positions_data is None:
			import time
			start = time.time()
			self.positions_data = np.array(self.positions, dtype=np.float16)
			glBindBuffer(GL_ARRAY_BUFFER, self.positions_vbo)
			glBufferData(GL_ARRAY_BUFFER, self.positions_data, GL_STATIC_DRAW)
			end = time.time()
			#print(f"Took {int((end-start)*1000)}ms to upload position data")

		return self.positions_vbo

	def clear_instances(self):
		self.positions = []
		self.positions_data = None

	def add_pos(self, pos):
		self.positions.append(pos)
		self.positions_data = None

	def render(self):
		if self.shader is not None:
			self.shader.draw_model(self.model, self.transform, self.colour_tint, self.get_instance_vbo(), len(self.positions))
