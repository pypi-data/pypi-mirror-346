import pygame

font_cache: dict[tuple[str, int], pygame.Font] = {}
def load_font(name: str, size: int) -> pygame.Font:
	if (name, size) in font_cache:
		return font_cache[(name, size)]
	
	try:
		font = pygame.font.Font(name, size)
	except FileNotFoundError:
		font = pygame.font.SysFont(name, size)
	
	font_cache[(name, size)] = font

	return font