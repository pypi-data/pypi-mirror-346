from __future__ import annotations

import abc
import pygame

from .Camera2D import Camera2D

class GameObject2D:
	position: pygame.Vector2
	angle: float
	children: list[GameObject2D]
	parent: GameObject2D | None

	@property
	def global_position(self) -> pygame.Vector2:
		if self.parent is None:
			return self.position
		return self.parent.global_position + self.position.rotate(self.parent.angle)

	@property
	def global_angle(self) -> float:
		if self.parent is None:
			return self.angle
		return self.parent.global_angle + self.angle

	def __init__(self, position: pygame.Vector2, angle: float) -> None:
		self.position = position
		self.angle = angle
		self.children = []
		self.parent = None

	def set_parent(self, parent: GameObject2D) -> None:
		self.parent = parent
		parent.children.append(self)
	
	def add_child(self, child: GameObject2D) -> None:
		self.children.append(child)
		child.parent = self
	
	def remove_child(self, index: int) -> None:
		child = self.children[index]
		child.parent = None
		self.children.pop(index)

	@abc.abstractmethod
	def update(self, delta_time: float, game_objects: list[GameObject2D], camera: Camera2D) -> None:
		...