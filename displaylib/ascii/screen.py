from __future__ import annotations

import math
from typing import TYPE_CHECKING, Iterable

import sys

from ..math import Vec2, Vec2i
from ..template import Transform2D
from . import grapheme
from .camera import AsciiCamera
from .texture import Texture

if TYPE_CHECKING:
    from ..template import Node


class AsciiScreen:
    """`AsciiScreen` for displaying Ascii graphics

    Behaves like a surface. Has the option to write its content to the terminal
    """
    cell_transparant: str = " " # symbol used to indicate that a cell is transparent
    cell_default: str = " " # the default look of an empty cell

    def __init__(self, nodes: Iterable[Texture & Transform2D] = [], *, width: int = 16, height: int = 8) -> None:
        """Initialize surface from nodes given inside the given boundaries

        Args:
            nodes (Iterable[Node], optional): nodes to render onto surface. Defaults to an empty list.
            width (int, optional): width of surface. Defaults to 16.
            height (int, optional): height of surface. Defaults to 8.
        """
        self.width = width
        self.height = height
        self.texture = [[self.cell_transparant for _ in range(self.width)] for _ in range(self.height)] # 2D array

    def build(self, textures: Iterable[Texture & Transform2D] = []) -> None:
        """Rebuilds the surface from the texture of the nodes

        Args:
            nodes (Iterable[Node], optional): nodes to render (has to derive from `Texture`). Defaults to [].
            width (int, optional): surface width override. Defaults to 16.
            height (int, optional): surface height override. Defaults to 8.
        """
        self.texture = [[self.cell_transparant for _ in range(self.width)] for _ in range(self.height)] # 2D array

        camera: AsciiCamera = AsciiCamera.current # should never be None
        half_size = Vec2i(self.width // 2, self.height // 2)
        camera_rotation = camera.global_rotation
        cos_rotation_camera = math.cos(-camera_rotation)
        sin_rotation_camera = math.sin(-camera_rotation)

        for textured in textures:
            if not textured.visible:
                continue
            if not textured.texture:
                continue
            if not textured.texture[0]: # check if has first row
                continue
            lines = len(textured.texture)
            longest = len(max(textured.texture, key=len))
            position = textured.global_position - camera.global_position
            rotation = textured.global_rotation # FIXME: implement camera rotation the right way
            # if rotation != 0: # TODO: rotate around center if flagged
            #     position = rotate(position, rotation)

            if camera.mode == AsciiCamera.CENTERED:
                position += half_size
            elif camera.mode == AsciiCamera.INCLUDE_SIZE:
                position -= Vec2(longest, lines) // 2
            elif camera.mode == AsciiCamera.CENTERED_AND_INCLUDE_SIZE:
                position += half_size
                position -= Vec2(longest, lines) // 2

            if rotation != 0 and camera_rotation != 0: # node and camera rotation
                x_offset = longest / 2
                y_offset = lines / 2
                cos_rotation = math.cos(-rotation)
                sin_rotation = math.sin(-rotation)
                for h, line in enumerate(textured.texture):
                    for w, char in enumerate(line):
                        x_diff = w - x_offset
                        y_diff = h - y_offset
                        x_position = x_offset + position.x + cos_rotation * x_diff - sin_rotation * y_diff
                        y_position = y_offset + position.y + sin_rotation * x_diff + cos_rotation * y_diff
                        x_diff = half_size.x - w
                        y_diff = half_size.y - h
                        x_position = round(half_size.x + x_position + cos_rotation_camera * x_diff - sin_rotation_camera * y_diff)
                        y_position = round(half_size.y + y_position + sin_rotation_camera * x_diff + cos_rotation_camera * y_diff)
                        if not ((self.height) > y_position >= 0): # out of screen
                            continue
                        if not ((self.width) > x_position >= 0): # out of screen
                            continue
                        if char != self.cell_transparant:
                            self.texture[y_position][x_position] = grapheme.rotate(char, rotation - camera_rotation)

            elif rotation != 0: # node rotation
                x_offset = longest / 2
                y_offset = lines / 2
                cos_rotation = math.cos(-rotation)
                sin_rotation = math.sin(-rotation)
                for h, line in enumerate(textured.texture):
                    for w, char in enumerate(line):
                        x_diff = w - x_offset
                        y_diff = h - y_offset
                        x_position = round(x_offset + position.x + cos_rotation * x_diff - sin_rotation * y_diff)
                        y_position = round(y_offset + position.y + sin_rotation * x_diff + cos_rotation * y_diff)
                        if not ((self.height) > y_position >= 0): # out of screen
                            continue
                        if not ((self.width) > x_position >= 0): # out of screen
                            continue
                        if char != self.cell_transparant:
                            self.texture[y_position][x_position] = grapheme.rotate(char, rotation)
            
            elif camera_rotation != 0: # camera rotation
                for h, line in enumerate(textured.texture):
                    for w, char in enumerate(line):
                        x_diff = half_size.x - w
                        y_diff = half_size.y - h
                        x_position = round(half_size.x + position.x + cos_rotation_camera * x_diff - sin_rotation_camera * y_diff)
                        y_position = round(half_size.y + position.y + sin_rotation_camera * x_diff + cos_rotation_camera * y_diff)
                        if not ((self.height) > y_position >= 0): # out of screen
                            continue
                        if not ((self.width) > x_position >= 0): # out of screen
                            continue
                        if char != self.cell_transparant:
                            self.texture[y_position][x_position] = grapheme.rotate(char, camera_rotation)

            else: # no rotation
                for h, line in enumerate(textured.texture):
                    y_position = int(h + position.y)
                    if not ((self.height) > y_position >= 0): # out of screen
                        continue
                    for w, char in enumerate(line):
                        x_position = int(w + position.x)
                        if not ((self.width) > x_position >= 0): # out of screen
                            continue
                        if char != self.cell_transparant:
                            self.texture[y_position][x_position] = char

    def clear(self) -> None:
        """Clears the surface. Sets its texture to `AsciiSurface.cell_transparant`
        """
        self.texture = [[self.cell_transparant for _ in range(self.width)] for _ in range(self.height)] # 2D array
    
    def show(self) -> None:
        """Displays the screen to the terminal
        """
        out = ""
        lines = len(self.texture)
        for idx, line in enumerate(self.texture):
            rendered = "".join(letter if letter != self.cell_transparant else self.cell_default for letter in (line))
            out += (rendered + " " + ("\n" if idx != lines else ""))
        out += ("\u001b[A" * len(self.texture) + "\r") # "\u001b[A" is ANSI code for UP
        sys.stdout.write(out)
        sys.stdout.flush()
