import pygame
from pygame import Surface
from pygame._sprite import LayeredUpdates
from pygame.time import Clock

from game_objects.background import Background
from game_objects.t_rex import TRex
from game_sys import assets
from game_sys.settings import GameSettings


class Game:
    def __init__(self):
        pygame.init()
        self.__screen = pygame.display.set_mode((GameSettings.SCREEN_WIDTH.value, GameSettings.SCREEN_HEIGHT.value))
        self.__clock = pygame.time.Clock()
        self.__sprites = LayeredUpdates()
        self.init_game()
        pygame.display.set_caption('Asteroid Survivor Simulation')
        pygame.display.set_icon(assets.get_sprite('game_icon'))

    def init_game(self):
        TRex(self.sprites)
        Background(self.sprites)

        pass

    @property
    def sprites(self) -> LayeredUpdates:
        return self.__sprites

    @property
    def screen(self) -> Surface:
        return self.__screen

    @property
    def clock(self) -> Clock:
        return self.__clock
