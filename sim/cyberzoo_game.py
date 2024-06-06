import pygame
import neat

from models import Drone, Pole
from utils import get_random_position, print_text
from pygame.math import Vector2


class CyberZooSim:
    MIN_DRONE_POLE_DISTANCE = 50
    MIN_POLE_POLE_DISTANCE = 100
    DRONE_START_POS = Vector2(400, 300)

    def __init__(self, genomes, config):
        self._init_pygame()
        self.screen = pygame.display.set_mode((700, 700))
        self.clock = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()
        self.font = pygame.font.Font(None, 32)
        self.time = 0

        self.poles = []
        self.drones = []

        self.nets = []
        self.ge = []

        for _, g in genomes:
            net = neat.nn.RecurrentNetwork.create(g, config)
            self.nets.append(net)
            self.drones.append(Drone((400, 300)))
            g.fitness = 0
            self.ge.append(g)

        positions = []
        for _ in range(4):
            while True:
                position = get_random_position(self.screen)
                if (
                    position.distance_to(self.DRONE_START_POS)
                    > self.MIN_DRONE_POLE_DISTANCE
                ):
                    counter = 0
                    check = False
                    for pos in positions:
                        if position.distance_to(pos) > self.MIN_POLE_POLE_DISTANCE:
                            counter += 1
                        if counter == len(positions):
                            check = True
                            break
                    if check or len(positions) == 0:
                        break

            self.poles.append(Pole(position))
            positions.append(position)

    def main_loop(self):
        running = True

        while running:
            self._handle_input()
            self._process_game_logic()
            self._draw()

            if len(self.drones) == 0:
                running = False

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("CyberZoo Simulation")

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                quit()

        is_key_pressed = pygame.key.get_pressed()
        for i, drone in enumerate(self.drones):
            movement_output = self.nets[i].activate((drone.position.x, drone.position.y,
                                                     drone.direction.x, drone.direction.y
                                                     , drone.velocity.x, drone.velocity.y,
                                                     self.poles[0].position.x, self.poles[0].position.y,
                                                     self.poles[1].position.x, self.poles[1].position.y,
                                                     self.poles[2].position.x, self.poles[2].position.y,
                                                     self.poles[3].position.x, self.poles[3].position.y))
            if movement_output[0] > 0.5:
                self.ge[i].fitness += 1
                drone.rotate(clockwise=True)
            if movement_output[1] > 0.5:
                self.ge[i].fitness += 1
                drone.accelerate()
            if movement_output[2] > 0.5:
                self.ge[i].fitness += 1
                drone.rotate(clockwise=False)

            if is_key_pressed[pygame.K_RIGHT]:
                drone.rotate(clockwise=True)
            if is_key_pressed[pygame.K_UP]:
                drone.accelerate()
            elif is_key_pressed[pygame.K_LEFT]:
                drone.rotate(clockwise=False)

    def _get_game_objects(self):
        game_objects = [*self.poles]

        for drone in self.drones:
            game_objects.append(drone)

        return game_objects

    def _process_game_logic(self):
        for game_object in self._get_game_objects():
            game_object.move(self.screen)
        for i, drone in enumerate(self.drones):
            drone.distance_travelled(self.time)
            self.ge[i].fitness = drone.distance

            for pole in self.poles:
                damage, bounce = pole.collides_with(drone)
                if damage:
                    self.ge[i].fitness -= 10
                    self.drones.remove(drone)
                    break
                if bounce:
                    drone.velocity.y = -drone.velocity.y
                    drone.velocity.x = -drone.velocity.x

    def _draw(self):
        self.screen.fill((0, 255, 0))

        for game_object in self._get_game_objects():
            game_object.draw(self.screen)

        self.time = (pygame.time.get_ticks() - self.start_time) / 1000
        print_text(self.screen, f"Time: {round(self.time, 2)}", self.font)

        max_distance = max((drone.distance for drone in self.drones), default=0)

        print_text(self.screen, f"Highest distance travelled: {round(max_distance, 2)}",
                   self.font, (0, 30))

        pygame.display.flip()
        self.clock.tick(60)
