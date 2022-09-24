import pygame
import random

class grid_quadry_tree:
    def __init__(self, pos, size) -> None:
        self.size = size
        self.image = pygame.surface.Surface((size, size))
        self.rect = self.image.get_rect(topleft = pos)
        self.center = self.rect.center
        self.vector = None

        # branches
        self.top_left = None
        self.top_right = None
        self.bottom_left = None
        self.bottom_right = None
    
    def set_vector(self, position, direction):
        self.vector = {
            "pos": position,
            "dir": direction,
        }