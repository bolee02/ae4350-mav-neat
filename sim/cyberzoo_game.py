import pygame

from models import Drone, Pole
from utils import get_random_position, print_text
from pygame.math import Vector2


class CyberZooSim:
    MIN_DRONE_POLE_DISTANCE = 50
    MIN_POLE_POLE_DISTANCE = 100
    DRONE_START_POS = Vector2(400, 300)

    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((700, 700))
        self.clock = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()
        self.font = pygame.font.Font(None, 32)
        self.time = 0

        self.poles = []
        self.drone = Drone((400, 300))

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
        game_objects = [*self.poles]

        if self.drone:
            game_objects.append(self.drone)

        return game_objects

    def _process_game_logic(self):
        for game_object in self._get_game_objects():
            game_object.move(self.screen)

        if self.drone:
            self.drone.distance_travelled(self.time)

            for pole in self.poles:
                damage, bounce = pole.collides_with(self.drone)
                if damage:
                    self.drone = None
                    break
                if bounce:
                    self.drone.velocity.y = -self.drone.velocity.y
                    self.drone.velocity.x = -self.drone.velocity.x

    def _draw(self):
        self.screen.fill((0, 255, 0))

        for game_object in self._get_game_objects():
            game_object.draw(self.screen)

        self.time = (pygame.time.get_ticks() - self.start_time) / 1000
        print_text(self.screen, f"Time: {round(self.time, 2)}", self.font)

        if self.drone:
            print_text(self.screen, f"Distance travelled: {round(self.drone.distance, 2)}",
                       self.font, (0, 20))

        pygame.display.flip()
        self.clock.tick(60)
