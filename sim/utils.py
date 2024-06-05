import random

from pygame.image import load
from pygame import Color
from pygame.math import Vector2


def load_sprite(name, with_alpha=True):
    path = f"sim/sprites/{name}.png"
    loaded_sprite = load(path)

    if with_alpha:
        return loaded_sprite.convert_alpha()
    else:
        return loaded_sprite.convert()


def get_random_position(surface):
    return Vector2(
        random.randrange(surface.get_width()),
        random.randrange(surface.get_height()),
    )


def get_random_velocity(min_speed, max_speed):
    speed = random.randint(min_speed, max_speed)
    angle = random.randrange(0, 360)
    return Vector2(speed, 0).rotate(angle)


def print_text(surface, text, font, position=(0, 0), color=Color("black")):
    text_surface = font.render(text, True, color)

    surface.blit(text_surface, position)
