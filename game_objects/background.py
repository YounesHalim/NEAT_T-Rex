import pygame.sprite
from pygame._sprite import AbstractGroup

from game_sys import assets
from game_sys.layer import Layer
from game_sys.settings import GameSettings


class Background(pygame.sprite.Sprite):
    def __init__(self, *groups: AbstractGroup):
        self._layer = Layer.BACKGROUND
        self.sprite = assets.get_sprite('')
        self.scale = pygame.transform.scale(self.sprite,
                                            (GameSettings.SCREEN_WIDTH.value, GameSettings.SCREEN_HEIGHT.value))
        self.image = self.scale
        self.rect = self.image.get_rect(topleft=())
        super().__init__(*groups)

    def update(self, *args, **kwargs):
        pass