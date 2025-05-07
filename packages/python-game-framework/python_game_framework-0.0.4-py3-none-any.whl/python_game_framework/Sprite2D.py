import pygame

from .GameObject2D import GameObject2D
from .Camera2D import Camera2D

class Sprite2D(GameObject2D):
	sprite: pygame.Surface

	def __init__(self, position: pygame.Vector2, angle: float, sprite: pygame.Surface) -> None:
		super().__init__(position, angle)
		self.sprite = sprite

	def update(self, delta_time: float, game_objects: list[GameObject2D], camera: Camera2D) -> None:
		camera.render(pygame.transform.rotate(self.sprite, -self.global_angle), self.global_position)