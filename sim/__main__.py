import os
import neat
import pygame

from cyberzoo_game import CyberZooSim


def run(config_path):
    config = neat.config.Config(
        neat.DefaultGenome, neat.DefaultReproduction,
        neat.DefaultSpeciesSet, neat.DefaultStagnation,
        config_path
                                )
    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(eval_genomes, 100000)
    print(f"Best genome: {winner}")


def eval_genomes(genomes, config):
    cyberzoo_sim = CyberZooSim(genomes, config)

    max_simulation_time = 10000
    start_time = pygame.time.get_ticks()

    while pygame.time.get_ticks() - start_time < max_simulation_time and len(cyberzoo_sim.drones) > 0:
        cyberzoo_sim.main_loop()


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    path = os.path.join(local_dir, "../neat/config.txt")

    run(path)
