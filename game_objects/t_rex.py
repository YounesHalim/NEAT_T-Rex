import pygame.sprite
from pygame import Vector2
from pygame._sprite import AbstractGroup

from game_objects.cactus import Cactus
from game_sys import assets
from game_sys.layer import Layer
from game_sys.settings import GameSettings


class TRex(pygame.sprite.Sprite):
    def __init__(self, *groups: AbstractGroup):
        self._layer = Layer.DINO
        self.index = 0
        self.gravity = GameSettings.GRAVITY.value
        self.dy = 3
        self.on_ground = True
        self.is_jumping = False
        self.is_falling = False
        self.images = [
            pygame.transform.scale(assets.get_sprite('dino0'), (64, 64)).convert_alpha(),
            pygame.transform.scale(assets.get_sprite('dino1'), (64, 64)).convert_alpha(),
            pygame.transform.scale(assets.get_sprite('dino2'), (64, 64)).convert_alpha()
        ]
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(topleft=(0, GameSettings.SCREEN_HEIGHT // 2 + self.image.get_height()))
        self.mask = pygame.mask.from_surface(self.image)
        self.fall_stop = self.rect.y
        self.jump_stop = 20
        self._last_cacti = None
        self.vel = Vector2(2, 0)
        super().__init__(*groups)

    def update(self, *args, **kwargs):
        self.start_animation()
        # jumping
        if self.is_jumping:
            self.rect.y -= self.dy
            if self.rect.y <= self.jump_stop:
                self._fall()

        # falling
        elif self.is_falling:
            self.rect.y += self.gravity * self.dy
            if self.rect.y >= self.fall_stop:
                self._stop()

        # walking animation
        self._animate()

    def _animate(self):
        self.index += .1
        if self.index < len(self.images):
            self.image = self.images[int(self.index)]
        if self.index > len(self.images):
            self.index = 0

    def jump(self):
        if self.on_ground:  # Check if the TRex is on the ground
            self.is_jumping = True
            self.on_ground = False

    def _fall(self):
        self.is_jumping = False
        self.is_falling = True

    def _stop(self):
        self.is_falling = False
        self.on_ground = True
        self.rect.y = self.fall_stop

    def start_animation(self):
        if self.rect.x >= self.rect.width:
            self.rect.x = self.rect.width

    @property
    def last_cacti(self):
        return self._last_cacti

    @last_cacti.setter
    def last_cacti(self, value: Cactus):
        self._last_cacti = value

    def move_forward(self):
        self.rect.move_ip(self.vel)

    def move_backward(self):
        self.vel = Vector2(-2, 0)
        self.rect.move_ip(self.vel)

    def invisible_death(self) -> bool:
        return self.rect.right >= GameSettings.SCREEN_WIDTH // 2 or self.rect.left < 0
