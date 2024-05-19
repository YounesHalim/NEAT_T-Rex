import pygame.sprite
from pygame._sprite import AbstractGroup

from game_sys import assets
from game_sys.layer import Layer


class Cactus(pygame.sprite.Sprite):
    def __init__(self, *groups: AbstractGroup):
        self._layer = Layer.OBSTACLE
        self.sprite = assets.get_sprite('cactus')
        self.image = pygame.transform.scale(self.sprite, ()).convert_alpha()
        self.rect = self.image.get_rect(topleft=())
        self.mask = pygame.mask.from_surface(self.image)
        super().__init__(*groups)

    def update(self, *args, **kwargs):
        pass


    def draw(self):
        pass