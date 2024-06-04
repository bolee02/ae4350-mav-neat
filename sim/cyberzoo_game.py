import pygame

from models import Drone


class CyberZooSim:
    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((800, 800))
        self.clock = pygame.time.Clock()
        self.drone = Drone((400, 300))

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

        if is_key_pressed[pygame.K_RIGHT]:
            self.drone.rotate(clockwise=True)
        if is_key_pressed[pygame.K_UP]:
            self.drone.accelerate()
        elif is_key_pressed[pygame.K_LEFT]:
            self.drone.rotate(clockwise=False)

    def _process_game_logic(self):
        self.drone.move(self.screen)

    def _draw(self):
        self.screen.fill((0, 255, 0))
        self.drone.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(60)
