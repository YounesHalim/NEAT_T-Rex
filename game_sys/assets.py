import os
import pygame
from pygame.surface import Surface, SurfaceType

sprites = {}


def load_sprites() -> None:
    path = os.path.join(os.path.abspath(''), "assets/sprites")
    for file in os.listdir(path):
        try:
            sprites[file.split('.')[0]] = pygame.image.load(os.path.join(path, file))
        except pygame.error:
            pass


def get_sprite(name: str) -> Surface | SurfaceType:
    return sprites[name]

