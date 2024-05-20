import pygame
from pygame import Surface
from pygame._sprite import LayeredUpdates
from pygame.time import Clock

from game_objects.background import Background
from game_objects.cactus import Cactus
from game_sys import assets
from game_sys.settings import GameSettings


class Game:
    def __init__(self):
        pygame.init()
        self.__screen = pygame.display.set_mode((GameSettings.SCREEN_WIDTH.value, GameSettings.SCREEN_HEIGHT.value))
        self.__clock = pygame.time.Clock()
        self.__sprites = LayeredUpdates()
        self.init_game()
        self.cacti = [Cactus(self.sprites)]

    def init_game(self):
        assets.load_sprites()
        Background(0, self.sprites)
        Background(1, self.sprites)
        pygame.display.set_caption('T-Rex AI')
        pygame.display.set_icon(assets.get_sprite('game_icon'))

    def draw_cactus(self):
        if self.cacti:
            last_cactus = self.cacti[-1]
            if not last_cactus.alive() and last_cactus.rect.left < 0:
                cactus = Cactus(self.sprites)
                cactus.vel = last_cactus.vel
                cactus.vel.x -= .25
                self.cacti.append(cactus)
                self.cacti.remove(last_cactus)

    @property
    def sprites(self) -> LayeredUpdates:
        return self.__sprites

    @property
    def screen(self) -> Surface:
        return self.__screen

    @property
    def clock(self) -> Clock:
        return self.__clock
