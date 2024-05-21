import pygame.sprite
from pygame import Vector2
from pygame._sprite import AbstractGroup

from game_sys.layer import Layer
from game_sys.settings import GameSettings
from pygame._sprite import LayeredUpdates


class Ground(pygame.sprite.Sprite):
    __max_velocity = -10

    def __init__(self, index: int, *groups: AbstractGroup | LayeredUpdates):
        self._layer = Layer.GROUND
        self.index = index
        self._color = pygame.Color('black')
        self._width = GameSettings.SCREEN_WIDTH.value
        self._height = GameSettings.SCREEN_HEIGHT.value
        self.image = pygame.Surface((self._width, 1), pygame.SRCALPHA).convert_alpha()
        self._start_pos = (0, 0)
        self._end_pos = (self._width * 1, 0)
        self.line = pygame.draw.aaline(self.image, self._color, self._start_pos, self._end_pos, blend=1)
        self.rect = self.image.get_rect(topleft=(self._width * index, self._height * .85))
        self.vel = Vector2(-2, 0)
        super().__init__(*groups)

    def update(self, *args, **kwargs):
        self.rect.move_ip(self.vel)
        if self.rect.right <= 0:
            self.rect.left = GameSettings.SCREEN_WIDTH.value

