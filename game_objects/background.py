import pygame.sprite
from pygame import Vector2
from pygame._sprite import AbstractGroup

from game_sys import assets
from game_sys.layer import Layer
from game_sys.settings import GameSettings


class Background(pygame.sprite.Sprite):

    def __init__(self, index: int, *groups: AbstractGroup):
        self._layer = Layer.BACKGROUND
        self.image = pygame.transform.scale(assets.get_sprite('bg'),
                                            (GameSettings.SCREEN_WIDTH.value,
                                             GameSettings.SCREEN_HEIGHT.value))
        self.rect = self.image.get_rect(topleft=(GameSettings.SCREEN_WIDTH.value * index, 0))
        self.vel = Vector2(-2, 0)
        super().__init__(*groups)

    def update(self, *args, **kwargs):
        self.rect.move_ip(self.vel)
        if self.rect.right <= 0:
            self.rect.x = GameSettings.SCREEN_WIDTH.value
