import shapely
import pygame

from .GameObject2D import GameObject2D
from .Camera2D import Camera2D

class ClippedTexture2D(GameObject2D):
	texture: pygame.Surface
	clip_shape: shapely.geometry.base.BaseGeometry
	calculated: pygame.Surface

	def __init__(self, position: pygame.Vector2, angle: float, texture: pygame.Surface, clip_shape: shapely.geometry.base.BaseGeometry) -> None:
		super().__init__(position, angle)
		self.clip_shape = clip_shape
		self.texture = texture
		self.calculated = pygame.Surface((texture.get_width(), texture.get_height()), pygame.SRCALPHA)
		self.recalculate()

	def recalculate(self) -> None:
		for x in range(self.texture.get_width()):
			for y in range(self.texture.get_height()):
				if self.clip_shape.contains(shapely.geometry.Point(x, y)):
					self.calculated.set_at((x, y), self.texture.get_at((x, y)))
				else:
					self.calculated.set_at((x, y), (0, 0, 0, 0))
		
		self.calculated = pygame.transform.rotate(self.calculated, -self.global_angle)

	def update(self, delta_time: float, game_objects: list[GameObject2D], camera: Camera2D) -> None:
		camera.render(self.calculated, self.global_position)