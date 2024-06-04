import pygame

from models import GameObject
from utils import load_sprite


class CyberZooSim:
    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((800, 800))
        self.drone = GameObject(
            (300, 300), load_sprite("drone"), (0, 0)
        )

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

    def _process_game_logic(self):
        self.drone.move()

    def _draw(self):
        self.screen.fill((0, 255, 0))
        self.drone.draw(self.screen)
        pygame.display.flip()

