import os
import neat
import pygame
import matplotlib.pyplot as plt

from cyberzoo_game import CyberZooSim


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                config_path)
    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(eval_genomes, 10000)

    best_fitness = [c.fitness for c in stats.most_fit_genomes]
    generation_fitness = stats.get_fitness_mean()

    # Create a figure with 2 subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

    # Plot best fitness on the first subplot
    ax1.plot(best_fitness, color='blue')
    ax1.set_title('Best Fitness Over Generations')
    ax1.set_xlabel('Generation')
    ax1.set_ylabel('Best Fitness')

    # Plot mean fitness on the second subplot
    ax2.plot(generation_fitness, color='green')
    ax2.set_title('Mean Fitness Over Generations')
    ax2.set_xlabel('Generation')
    ax2.set_ylabel('Mean Fitness')

    # Adjust layout to prevent overlap
    plt.tight_layout()

    # Display the plots
    plt.show()


def eval_genomes(genomes, config):
    cyberzoo_sim = CyberZooSim(genomes, config)

    max_simulation_time = 10000
    start_time = pygame.time.get_ticks()

    while pygame.time.get_ticks() - start_time < max_simulation_time and len(cyberzoo_sim.drones) > 0:
        cyberzoo_sim.main_loop()


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    path1 = os.path.join(local_dir, "../neat/config1.txt")
    path2 = os.path.join(local_dir, "../neat/config2.txt")
    path3 = os.path.join(local_dir, "../neat/config3.txt")
    path4 = os.path.join(local_dir, "../neat/config4.txt")
    run(path1)
    run(path2)
    run(path3)
    run(path4)
