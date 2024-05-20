import pygame
import pygame.font
from pygame.sprite import AbstractGroup

from game_sys.layer import Layer
from game_sys.settings import GameSettings


class UI(pygame.sprite.Sprite):
    def __init__(self, *groups: AbstractGroup, alive: list, generation: int):
        self._layer = Layer.UI
        self._font = pygame.font.Font(pygame.font.get_default_font(), 15)
        self.alive = len(alive)
        self.score = 0
        self.generation = generation
        self.velocity = 0
        self._surface = pygame.display.get_surface()
        self.image = pygame.Surface((GameSettings.SCREEN_WIDTH.value, 100), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(10, 10))
        super().__init__(*groups)

    def _draw_ui(self) -> None:
        self.image.fill((255, 255, 255, 0))
        dino_text = self._font.render(f"TRex alive: {self.alive}", 1, 'black')
        self.image.blit(dino_text, (0, 0))
        gen_text = self._font.render(f"Generation: {self.generation}", 1, 'black')
        self.image.blit(gen_text, (0, 20))
        score = self._font.render(f"XP: {self.score}", 1, 'red')
        self.image.blit(score, (0, 40))
        score = self._font.render(f"Velocity: {self.velocity:.2f}", 1, 'black')
        self.image.blit(score, (0, 60))
        pygame.display.update()

    def update_ui(self, alive: list, generation: int) -> None:
        self.alive = len(alive)
        self.generation = generation
        self._draw_ui()
