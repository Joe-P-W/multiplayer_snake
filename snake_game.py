import pygame
from game_files import logic

pygame.init()

resolution = (600, 600)
squares = 20

screen = pygame.display.set_mode(resolution)
font = pygame.font.SysFont('Arial', 30)

logic.main_menu(screen, squares, resolution, font)
