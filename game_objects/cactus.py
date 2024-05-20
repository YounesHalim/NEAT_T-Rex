import pygame.sprite
from pygame import Vector2
from pygame._sprite import AbstractGroup

from game_sys import assets
from game_sys.layer import Layer
from game_sys.settings import GameSettings


class Cactus(pygame.sprite.Sprite):
    __max_velocity = 5

    def __init__(self, *groups: AbstractGroup):
        self._layer = Layer.CACTUS
        self.image = pygame.transform.scale(assets.get_sprite('cactus'), (148 // 2, 280 // 2)).convert_alpha()
        self.rect = self.image.get_rect(
            topright=(GameSettings.SCREEN_WIDTH.value + self.image.get_width(), GameSettings.SCREEN_HEIGHT // 2))
        self.mask = pygame.mask.from_surface(self.image)
        self._vel = Vector2(-2, 0)
        super().__init__(*groups)

    def update(self, *args, **kwargs):
        self._velocity_limit()
        self.rect.move_ip(self._vel)
        if self.rect.right + self.image.get_width() < 0:
            self.kill()

    @property
    def vel(self) -> Vector2:
        return self._vel

    @vel.setter
    def vel(self, vel: Vector2):
        if isinstance(vel, Vector2):
            self._vel = vel

    def _velocity_limit(self):
        if self.vel.x >= self.__max_velocity:
            self.vel.x = self.__max_velocity

