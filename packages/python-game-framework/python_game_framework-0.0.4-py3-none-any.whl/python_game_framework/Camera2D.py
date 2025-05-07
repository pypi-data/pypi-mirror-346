import pygame
import shapely

from . import Utils

class Camera2D:
	position: pygame.Vector2
	surface: pygame.Surface
	zoom: float

	def __init__(self, position: pygame.Vector2, surface: pygame.Surface, zoom: float) -> None:
		self.position = position
		self.surface = surface
		self.zoom = zoom
	
	def screen_to_world(self, position: pygame.Vector2) -> pygame.Vector2:
		return (position - pygame.Vector2(self.surface.get_size()) / 2) / self.zoom + self.position

	def world_to_screen(self, position: pygame.Vector2) -> pygame.Vector2:
		return (position - self.position) * self.zoom + pygame.Vector2(self.surface.get_size()) / 2
	
	def render(self, surface: pygame.Surface, position: pygame.Vector2) -> None:
		screen_position = self.world_to_screen(position)
		scaled = pygame.transform.scale(surface, pygame.Vector2(surface.get_size()) * self.zoom)
		self.surface.blit(scaled, screen_position - pygame.Vector2(scaled.get_size()) / 2)

	def draw_polygon(self, polygon: shapely.geometry.Polygon, offset: pygame.Vector2, color: pygame.Color, width: int = 0) -> None:
		surface = pygame.Surface((polygon.bounds[2] - polygon.bounds[0], polygon.bounds[3] - polygon.bounds[1]), pygame.SRCALPHA)

		coords = [pygame.Vector2(point) + pygame.Vector2((polygon.bounds[2] - polygon.bounds[0]) / 2, (polygon.bounds[3] - polygon.bounds[1]) / 2) for point in polygon.exterior.coords]

		pygame.draw.polygon(surface, color, coords, width)

		surface.set_alpha(color.a)

		self.render(surface, offset)
	
	def draw_line(self, start: pygame.Vector2, end: pygame.Vector2, color: pygame.Color, width: int = 3) -> None:
		pygame.draw.line(self.surface, color, self.world_to_screen(start), self.world_to_screen(end), width)