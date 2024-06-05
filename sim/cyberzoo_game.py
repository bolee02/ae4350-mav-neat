import pygame

from models import Drone, Pole
from utils import get_random_position


class CyberZooSim:
    MIN_DRONE_POLE_DISTANCE = 100
    MIN_POLE_POLE_DISTANCE = 100

    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((700, 700))
        self.clock = pygame.time.Clock()

        self.pole = []
        self.drone = Drone((400, 300))

        positions = []
        for _ in range(6):
            while True:
                position = get_random_position(self.screen)
                if (
                    position.distance_to(self.drone.position)
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

            self.pole.append(Pole(position))
            positions.append(position)

    def main_loop(self):
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()

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

        if self.drone:
            if is_key_pressed[pygame.K_RIGHT]:
                self.drone.rotate(clockwise=True)
            if is_key_pressed[pygame.K_UP]:
                self.drone.accelerate()
            elif is_key_pressed[pygame.K_LEFT]:
                self.drone.rotate(clockwise=False)

    def _get_game_objects(self):
        game_objects = [*self.pole]

        if self.drone:
            game_objects.append(self.drone)

        return game_objects

    def _process_game_logic(self):
        for game_object in self._get_game_objects():
            game_object.move(self.screen)

        if self.drone:
            for pole in self.pole:
                if pole.collides_with(self.drone):
                    self.drone = None
                    break

    def _draw(self):
        self.screen.fill((0, 255, 0))

        for game_object in self._get_game_objects():
            game_object.draw(self.screen)

        pygame.display.flip()
        self.clock.tick(60)
