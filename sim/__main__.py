import os
import neat
import visualize
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

    winner = p.run(eval_genomes, 1)
    node_names = {-1: 'A', -2: 'B', 0: 'A XOR B'}
    visualize.draw_net(config, winner, True, node_names=node_names)
    visualize.draw_net(config, winner, True, node_names=node_names, prune_unused=True)
    visualize.plot_stats(stats, ylog=False, view=True)
    visualize.plot_species(stats, view=True)
    print(f"Best genome: {winner}")


def eval_genomes(genomes, config):
    cyberzoo_sim = CyberZooSim(genomes, config)

    max_simulation_time = 10000
    start_time = pygame.time.get_ticks()

    while pygame.time.get_ticks() - start_time < max_simulation_time and len(cyberzoo_sim.drones) > 0:
        cyberzoo_sim.main_loop()
    for i, g in enumerate(genomes):
        g[1].fitness = cyberzoo_sim.ge[i].fitness


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    path = os.path.join(local_dir, "../neat/config.txt")

    run(path)
