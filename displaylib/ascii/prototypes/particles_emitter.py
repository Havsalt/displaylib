from __future__ import annotations

import math
import random
from typing import TYPE_CHECKING, cast

from ...math import Vec2
from ...template.type_hints import MroNext, NodeType, AnyNode
from .. import color
from ..node import AsciiNode2D
from ..texture import Texture
from ..colored import Color
from ..color import WHITE, ColorValue

if TYPE_CHECKING:
    from ...template.type_hints import AnyNode


def randf(a: float, b: float) -> float:
    return random.random() * (b - a) + a


class ParticlesMaterial: # Component (mixin class)
    amount: int = 8
    lifetime_min: float = 1.0
    lifetime_max: float = 1.0
    initial_velocity: float = 0.0
    direction: Vec2 = Vec2(1, 0)
    spread: float = 0
    gravity: Vec2 = Vec2(0, -1)
    colors: list[ColorValue] | tuple[ColorValue, ...] | ColorValue = WHITE
    textures: list[list[list[str]]] | tuple[list[list[str]], ...] | list[list[str]] = [["+"]]
    emitting: bool = False
    # explosiveness: float = 0.0,
    # local_coords: bool = False,
    # one_shot: bool = False,
    # preprocess: float = 0.0,
    # speed_scale: float = 1.0,

    def __new__(cls: type[NodeType], *args, **kwargs) -> NodeType:
        mro_next = cast(MroNext[ParticlesMaterial], super())
        instance = mro_next.__new__(cls, *args, **kwargs)
        instance.direction = instance.direction.normalized().copy()
        instance.gravity = instance.gravity.copy()
        if not isinstance(instance.colors, ColorValue): # check if is multiple color
            instance.colors = [color for color in instance.colors] # copy list
        return cast(NodeType, instance)


class Particle(Color, Texture, AsciiNode2D):
    texture = [["+"]]
    acceleration: float = 0
    direction: Vec2 = Vec2(1, 0)
    lifetime: float = 1.0
    gravity: Vec2 = Vec2(0, -1)
    speed: Vec2 = Vec2(0, 0)
    _time_elapsed: float = 0

    def __init__(self, parent: AnyNode | None = None, *, x: float = 0, y: float = 0, texture: list[list[str]] = [["+"]], color: ColorValue = WHITE, force_sort: bool = True) -> None:
        ... # interface

    def _update(self, delta: float) -> None:
        self._time_elapsed += delta
        if self._time_elapsed >= self.lifetime:
            self.queue_free()
        self.speed += self.direction * self.acceleration * delta
        self.speed -= self.gravity * delta
        self.position += self.speed * delta


class ParticlesEmitter(AsciiNode2D):
        def __init__(self, parent: AnyNode | None = None, *, x: float = 0, y: float = 0, force_sort: bool = True) -> None:
            self.force_sort = force_sort
            self._particles: list[Particle] = []
            self._time_elapsed = 0
            self._spawn_interval = 1.0 / self.amount
        
        def _update(self, delta: float) -> None:
            self._time_elapsed += delta
            if self._time_elapsed >= self._spawn_interval:
                self._time_elapsed -= self._spawn_interval
                # spawn particle
                if isinstance(self.textures, (list, tuple)):
                    texture = random.choice(self.textures)
                else:
                    texture = self.textures
                if isinstance(self.colors, (list, tuple)):
                    albedo = random.choice(self.colors)
                else:
                    albedo = self.colors
                texture = cast(list[list[str]], texture)
                particle = Particle(texture=texture, color=albedo)
                particle.set_global_position(self.get_global_position())
                particle.lifetime = randf(self.lifetime_min, self.lifetime_max)
                relative_spread = self.spread * random.random()
                if random.random() < 0.50:
                    relative_spread = -relative_spread
                particle.direction = self.direction.rotated(relative_spread)
                particle.acceleration = self.initial_velocity
                particle.speed = self.direction * self.initial_velocity
                particle.gravity = self.gravity # pass by referance so it can be updated smoothly
                self._particles.append(particle)



if __name__ == "__main__":
    class CustomParticlesMaterial(ParticlesMaterial):
        initial_velocity = 5.0
        spread = math.radians(90)
        gravity = Vec2(0, 0)
        lifetime_min = 2
        lifetime_max = 3
        colors = (
            color.ROYAL_BLUE,
            color.LIME_GREEN,
            color.MAGENTA
        )
        textures = (
            [
                [*" _"],
                [*"-+-"],
                [*" ¨"]
            ],
            [
                [*" ."],
                [*"-*-"],
                [*" '"],
            ]
        )
