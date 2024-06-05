import os
import neat

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

    winner = p.run(CyberZooSim, 50)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    path = os.path.join(local_dir, "neat/config.txt")

    cyberzoo_sim = CyberZooSim()
    cyberzoo_sim.main_loop()
