from __future__ import annotations

import pygame
import shapely

from . import Utils
from .Vars import debug, physics_substeps

from .Camera2D import Camera2D
from .GameObject2D import GameObject2D

class RigidBody2D(GameObject2D):
	velocity: pygame.Vector2
	angular_velocity: float
	mass: float
	inertia: float
	hitbox: shapely.geometry.Polygon
	position_locked: bool = False
	rotation_locked: bool = False

	def get_hitbox(self) -> shapely.geometry.Polygon:
		return shapely.affinity.translate(shapely.affinity.rotate(self.hitbox, self.global_angle), self.global_position.x, self.global_position.y)

	def __init__(self, position: pygame.Vector2, velocity: pygame.Vector2, angle: float, angular_velocity: float, mass: float, inertia: float, hitbox: shapely.geometry.Polygon) -> None:
		super().__init__(position, angle)
		self.velocity = velocity
		self.angular_velocity = angular_velocity
		self.mass = mass
		self.inertia = inertia
		self.hitbox = hitbox
	
	def update(self, delta_time: float, game_objects: list[GameObject2D], camera: Camera2D) -> None:
		for _ in range(physics_substeps):
			self.update_physics(delta_time / physics_substeps)
			self.resolve_collisions(game_objects)
		self.render(camera)

	def update_physics(self, delta_time: float) -> None:
		if self.position_locked:
			self.velocity = pygame.Vector2(0, 0)

		if self.rotation_locked:
			self.angular_velocity = 0

		self.position += self.velocity * delta_time
		self.angle += self.angular_velocity * delta_time
	
	def resolve_collisions(self, game_objects: list[GameObject2D]) -> None:
		for game_object in game_objects:
			if type(game_object) is not RigidBody2D:
				continue

			if game_object is self:
				continue

			self_hitbox = self.get_hitbox()
			game_object_hitbox = game_object.get_hitbox()

			if not Utils.polygon_bounding_box_check(self_hitbox, game_object_hitbox):
				continue

			if not self_hitbox.intersects(game_object_hitbox):
				continue
			
			print("RigidBody2D collision not implemented")
	
	def render(self, camera: Camera2D) -> None:
		if debug:
			camera.draw_polygon(shapely.affinity.rotate(self.hitbox, self.global_angle), self.global_position, pygame.Color(0, 0, 255, 128))