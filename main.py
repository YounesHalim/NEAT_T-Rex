import math
from os.path import dirname, join

import neat
import pygame.event
from pygame.sprite import spritecollide, collide_mask

from game_objects.t_rex import TRex
from game_sys.game_sys import Game
from game_sys.settings import GameSettings
from game_sys.ui import UI


def get_distance(first_pos, second_pos):
    dx = first_pos[0] - second_pos[0]
    dy = first_pos[1] - second_pos[1]
    return math.sqrt(dx ** 2 + dy ** 2)


gen = -1


def eval_genomes(genomes, configuration) -> None:
    global gen
    gen += 1
    nets = []
    ge = []
    dinosaurs = []
    game = Game()
    screen, clock, sprites, cacti = game.screen, game.clock, game.sprites, game.cacti
    ui = UI(sprites, alive=dinosaurs, generation=gen)
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, configuration)
        nets.append(net)
        dinosaurs.append(TRex(game.sprites))
        genome.fitness = 0
        ge.append(genome)

    while True:
        events = pygame.event.get()
        game.draw_cactus()
        for event in events:
            if (event.type == pygame.QUIT
                    or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
                pygame.quit()
                break

        ui.update_ui(alive=dinosaurs, generation=gen)

        if not dinosaurs:
            break

        cacti_index = 0
        if dinosaurs:
            if len(cacti) > 1 and dinosaurs[0].rect.x > cacti[0].rect.x + cacti[0].image.get_width():
                cacti_index = 1

        ui.velocity = abs(cacti[cacti_index].vel.x)
        for x, trex in enumerate(dinosaurs):
            ge[x].fitness += 1
            obstacle = cacti[cacti_index]
            output = nets[x].activate(
                (
                    trex.rect.y,
                    abs(obstacle.vel.x),
                    get_distance((trex.rect.x, trex.rect.y), obstacle.rect.midtop)
                )
            )
            if output[0] > .5:
                trex.jump()

        add_cacti = False
        for cactus in cacti:
            for x, trex in enumerate(dinosaurs):
                if spritecollide(trex, pygame.sprite.Group(cactus), False, collide_mask):
                    trex.kill()
                    ge[x].fitness -= 5
                    dinosaurs.pop(x)
                    nets.pop(x)
                    ge.pop(x)

                if cactus.rect.left == 0:
                    add_cacti = True

        if add_cacti:
            ui.score += 1
            for genome in ge:
                genome.fitness += 5

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
