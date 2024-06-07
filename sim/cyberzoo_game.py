import pygame
import neat
import numpy as np

from models import Drone, Pole
from utils import get_random_position, print_text, normalize_array
from pygame.math import Vector2


class CyberZooSim:
    MIN_DRONE_POLE_DISTANCE = 50
    MIN_POLE_POLE_DISTANCE = 100
    DRONE_START_POS = Vector2(350, 350)
    POLE_MOVE_EVENT = pygame.USEREVENT + 1

    def __init__(self, genomes, config):
        self._init_pygame()
        self.screen = pygame.display.set_mode((700, 700))
        self.clock = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()
        self.font = pygame.font.Font(None, 32)
        self.time = 0
        self.event_count = 0
        self.move_to_event = False
        self.random_positions = []

        self.poles = []
        self.drones = []

        self.nets = []
        self.ge = []

        for _, g in genomes:
            net = neat.nn.RecurrentNetwork.create(g, config)
            self.nets.append(net)
            self.drones.append(Drone(self.DRONE_START_POS))
            g.fitness = 0
            self.ge.append(g)

        positions = []
        for _ in range(6):
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
            elif event.type == self.POLE_MOVE_EVENT:
                self.move_to_event = True
                self.random_positions = []
                if len(self.drones) < 5 or self.time > 10:
                    for i in range(len(self.poles)-1):
                        self.random_positions.append(get_random_position(self.screen))
                    self.random_positions.append(self.drones[0].position)
                else:
                    for i in range(len(self.poles)):
                        self.random_positions.append(get_random_position(self.screen))

        is_key_pressed = pygame.key.get_pressed()
        for i, drone in enumerate(self.drones):
            input_array_1 = np.array([
                drone.direction.x, drone.direction.y
            ])
            input_array_2 = np.array([
                drone.position.x, drone.position.y,
            ])
            input_array_3 = np.array([
                drone.velocity.x, drone.velocity.y
            ])
            input_array_4 = np.array([
                drone.position.distance_to(self.poles[0].position),
                drone.position.distance_to(self.poles[1].position),
                drone.position.distance_to(self.poles[2].position),
                drone.position.distance_to(self.poles[3].position),
                drone.position.distance_to(self.poles[4].position),
                drone.position.distance_to(self.poles[5].position)
            ])

            normalized_input = np.concatenate([normalize_array(input_array_1, -1, 1),
                                               normalize_array(input_array_2, 0, 700),
                                               normalize_array(input_array_3, -20, 20),
                                               normalize_array(input_array_4, -700, 700)])
            movement_output = self.nets[i].activate(normalized_input)

            if movement_output[0] > 0.5:
                drone.rotate(clockwise=True)
            if movement_output[1] > 0.5:
                drone.accelerate()
            if movement_output[2] > 0.5:
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

        for i, pole in enumerate(self.poles):
            if self.move_to_event:
                if pole.position.x < self.random_positions[i].x:
                    pole.position.x += 1
                elif pole.position.x > self.random_positions[i].x:
                    pole.position.x -= 1

                if pole.position.y < self.random_positions[i].y:
                    pole.position.y += 1
                elif pole.position.y > self.random_positions[i].y:
                    pole.position.y -= 1

        for i, drone in enumerate(self.drones):
            drone.distance_travelled(self.time)
            self.ge[i].fitness += drone.distance/1000

            if drone.position == Vector2(350, 350):
                self.ge[i].fitness -= 1

            screen_width, screen_height = self.screen.get_size()
            if drone.position.x - drone.radius < 0 or drone.position.x + drone.radius > screen_width:
                self.ge[i].fitness -= 200
            if drone.position.y - drone.radius < 0 or drone.position.y + drone.radius > screen_height:
                self.ge[i].fitness -= 200

            for pole in self.poles:
                damage, bounce = pole.collides_with(drone)
                if damage:
                    self.ge[i].fitness -= 200
                    self.nets.pop(i)
                    self.ge.pop(i)
                    self.drones.remove(drone)
                    break
                if bounce:
                    drone.velocity.y = -drone.velocity.y
                    drone.velocity.x = -drone.velocity.x
                if pole.position.distance_to(drone.position) > self.MIN_POLE_POLE_DISTANCE:
                    self.ge[i].fitness += 0.1

    def _draw(self):
        self.screen.fill((0, 255, 0))

        for game_object in self._get_game_objects():
            game_object.draw(self.screen)

        self.time = (pygame.time.get_ticks() - self.start_time) / 1000

        if self.event_count == 0:
            pygame.time.set_timer(self.POLE_MOVE_EVENT, 2000)
            self.event_count += 1

        print_text(self.screen, f"Time: {round(self.time, 2)}", self.font)

        max_distance = max((drone.distance for drone in self.drones), default=0)

        print_text(self.screen, f"Highest distance travelled: {round(max_distance, 2)}",
                   self.font, (0, 30))

        pygame.display.flip()
        self.clock.tick(6000)
