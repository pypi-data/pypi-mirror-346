import shapely
import pygame

def polygon_bounding_box_check(a: shapely.geometry.Polygon, b: shapely.geometry.Polygon) -> bool:
	return a.bounds[0] < b.bounds[2] and a.bounds[2] > b.bounds[0] and a.bounds[1] < b.bounds[3] and a.bounds[3] > b.bounds[1]

def vector_abs(v: pygame.Vector2) -> pygame.Vector2:
	return pygame.Vector2(abs(v.x), abs(v.y))