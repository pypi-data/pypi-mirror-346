import src.python_game_framework as pgf
import pygame
import shapely

pygame.init()

pgf.Vars.physics_substeps = 8

window = pygame.display.set_mode((800, 600), pygame.RESIZABLE)

camera = pgf.Camera2D(pygame.Vector2(0, 0), window, 1.0)

s = pygame.Surface((40, 40), pygame.SRCALPHA)
s.fill((255, 0, 0))

game_objects: list[pgf.GameObject2D] = [
	pgf.GameObject2D(
		pygame.Vector2(-100, 0),
		0
	),
	pgf.Sprite2D(
		pygame.Vector2(0, 0),
		0,
		s
	),
	pgf.RigidBody2D(
		pygame.Vector2(93, 100),
		pygame.Vector2(0, 0),
		0,
		10,
		1,
		1,
		shapely.geometry.Polygon([
			(-20, -20),
			(20, -20),
			(20, 20),
			(-20, 20)
		])
	),
	pgf.Sprite2D(
		pygame.Vector2(0, 0),
		0,
		s
	),
	pgf.RigidBody2D(
		pygame.Vector2(146, 100),
		pygame.Vector2(0, 0),
		0,
		300,
		1,
		1,
		shapely.geometry.Polygon([
			(-20, -20),
			(20, -20),
			(20, 20),
			(-20, 20)
		])
	),
	pgf.ClippedTexture2D(
		pygame.Vector2(0, 0),
		0,
		s,
		shapely.geometry.Polygon([
			(0, 0),
			(40, 0),
			(40, 40),
			(0, 40),
			(20, 20)
		])
	)
]

game_objects[1].set_parent(game_objects[2])
game_objects[3].set_parent(game_objects[4])

clock = pygame.time.Clock()

while True:
	dt = clock.tick() / 1000

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		
		elif event.type == pygame.KEYDOWN:
			game_objects[2].set_parent(game_objects[0])

	window.fill((0, 0, 0))

	for game_object in game_objects:
		game_object.update(dt, game_objects, camera)
	
	window.blit(pgf.Gui.load_font("Times new roman", 20).render(f"FPS: {clock.get_fps():.2f}", True, (255, 255, 255)))

	pygame.display.flip()