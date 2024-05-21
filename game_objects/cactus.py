import pygame.sprite
from pygame import Vector2
from pygame._sprite import AbstractGroup
from pygame._sprite import LayeredUpdates


from game_objects.ground import Ground
from game_sys import assets
from game_sys.layer import Layer
from game_sys.settings import GameSettings


class Cactus(pygame.sprite.Sprite):
    def __init__(self, *groups: AbstractGroup | LayeredUpdates):
        self._layer = Layer.CACTUS
        self.ground: Ground = groups[0].get_sprites_from_layer(Layer.GROUND)[0]
        self.size = (148 * .30, 280 * .30)
        self.image = pygame.transform.scale(assets.get_sprite('cactus'), self.size).convert_alpha()
        self.rect = self.image.get_rect(
            topright=(GameSettings.SCREEN_WIDTH.value + self.image.get_width(), self.ground.rect.top - self.image.get_height()))
        self.mask = pygame.mask.from_surface(self.image)
        self._vel = Vector2(-5, 0)
        self.passed = False
        super().__init__(*groups)

    def update(self, *args, **kwargs):
        self.rect.move_ip(self._vel)
        if self.rect.right < 0:
            self.kill()

    @property
    def vel(self) -> Vector2:
        return self._vel

    @vel.setter
    def vel(self, vel: Vector2):
        if isinstance(vel, Vector2):
            self._vel = vel

