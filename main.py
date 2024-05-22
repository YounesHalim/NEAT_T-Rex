import math
import sys
from os.path import dirname, join

import neat
import pygame.event
from pygame.sprite import spritecollide, collide_mask

from game_objects.t_rex import TRex
from game_sys.game_sys import Game
from game_sys.settings import GameSettings
from game_sys.ui import UI

GEN = -1


def eval_genomes(genomes, configuration) -> None:
    global GEN
    GEN += 1
    nets = []
    ge = []
    dinosaurs = []
    game = Game()
    screen, clock, sprites, cacti = game.screen, game.clock, game.sprites, game.cacti
    ui = UI(sprites, alive=dinosaurs, generation=GEN)
    for _, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, configuration)
        nets.append(net)
        dinosaurs.append(TRex(game.sprites))
        genome.fitness = 0
        ge.append(genome)

    while True:
        events = pygame.event.get()
        game.draw_cactus(ge)
        for event in events:
            if (event.type == pygame.QUIT
                    or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
                pygame.quit()
                sys.exit()

        if not dinosaurs:
            break

        cactus_index = 0
        if dinosaurs:
            if len(cacti) > 1 and dinosaurs[0].rect.x > cacti[0].rect.x + cacti[0].image.get_width():
                cactus_index = 1

        ui.velocity = abs(cacti[cactus_index].vel.x)
        for x, trex in enumerate(dinosaurs):
            ge[x].fitness += .05
            obstacle = cacti[cactus_index]
            output = nets[x].activate(
                (
                    trex.rect.y,
                    abs(obstacle.vel.x),
                    math.sqrt((trex.rect.x - obstacle.rect.midtop[0]) ** 2 + (trex.rect.y - obstacle.rect.midtop[1]) ** 2)
                )
            )
            if output[0] > .5:
                trex.jump()

        for cactus in cacti:
            for x, trex in enumerate(dinosaurs):
                if spritecollide(trex, pygame.sprite.Group(cactus), False, collide_mask):
                    trex.kill()
                    ge[x].fitness -= 5
                    dinosaurs.pop(x)
                    nets.pop(x)
                    ge.pop(x)
                if cactus.rect.left < 0:
                    cactus.passed = True

        ui.update_ui(alive=dinosaurs, generation=GEN)

        screen.fill(0)
        sprites.draw(screen)
        sprites.update()
        pygame.display.flip()
        clock.tick(GameSettings.FPS.value)


def run(config_file):
    config_loader = neat.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                config_file)

    population = neat.Population(config_loader)

    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    winner = population.run(eval_genomes, 50)

    print(f'\nBest genome:\n{winner}')


if __name__ == '__main__':
    config_path = join(dirname(__file__), 'feedforward.txt')
    run(config_path)
