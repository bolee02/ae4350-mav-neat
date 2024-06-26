import pygame
import math
from utils import load_sprite, get_random_velocity
from pygame.math import Vector2
from pygame.transform import rotozoom

UP = Vector2(0, -1)


class GameObject:
    def __init__(self, position, sprite, velocity):
        self.position = Vector2(position)
        self.sprite = pygame.transform.scale(sprite, (75, 75))
        self.radius = self.sprite.get_width() / 2
        self.velocity = Vector2(velocity)

    def draw(self, surface):
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)

    def move(self, surface):
        self.position += self.velocity
        screen_width, screen_height = surface.get_size()

        if self.position.x - self.radius < 0 or self.position.x + self.radius > screen_width:
            self.velocity.x = -self.velocity.x
            self.position.x = max(self.radius, min(self.position.x, screen_width - self.radius))
        if self.position.y - self.radius < 0 or self.position.y + self.radius > screen_height:
            self.velocity.y = -self.velocity.y
            self.position.y = max(self.radius, min(self.position.y, screen_height - self.radius))

    def collides_with(self, other):
        distance = self.position.distance_to(other.position)
        damage = False
        bounce = False
        if (distance + 20 < self.radius + other.radius
                and math.sqrt(other.velocity.y**2 + other.velocity.x**2) > -1):
            damage = True
            return damage, bounce
        """
        elif (distance + 20 < self.radius + other.radius
                and math.sqrt(other.velocity.y**2 + other.velocity.x**2) < 3):
            bounce = True
            return damage, bounce
        """
        return damage, bounce


class Drone(GameObject):
    MANEUVERABILITY = 3
    ACCELERATION = 0.2

    def __init__(self, position):
        self.direction = Vector2(UP)
        super().__init__(position, load_sprite("drone"), Vector2(0))
        self.sprite = pygame.transform.scale(self.sprite, (50, 50))
        self.distance = 0

    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * sign
        self.direction.rotate_ip(angle)

    def draw(self, surface):
        angle = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)

    def accelerate(self):
        self.velocity += self.direction * self.ACCELERATION

    def decelerate(self):
        self.velocity -= self.direction * self.ACCELERATION

    def distance_travelled(self, time):
        self.distance += math.sqrt(self.velocity.y**2 + self.velocity.x**2) * time / 100


class Pole(GameObject):
    def __init__(self, position):
        super().__init__(
            position, load_sprite("pole"), Vector2(0)
        )
        self.sprite = pygame.transform.scale(self.sprite, (75, 75))

    def move_to(self, new_position):
        self.velocity = Vector2(5, 5)
        if self.position.x < new_position.x:
            self.position.x += self.velocity.x
        elif self.position.x > new_position.x:
            self.position.x -= self.velocity.x

        if self.position.y < new_position.y:
            self.position.y += self.velocity.y
        elif self.position.y > new_position.y:
            self.position.y -= self.velocity.y
