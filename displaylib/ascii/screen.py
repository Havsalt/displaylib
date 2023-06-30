from __future__ import annotations

import math
from typing import Iterable

import sys

from ..math import Vec2i
from ..template import Transform2D, Node
from . import grapheme
from .camera import AsciiCamera
from .texture import Texture

class Transform2DTextureNode(Transform2D, Texture, Node):
    """Type hint for classes deriving from: `Transform2D`, `Texture`, `Node`
    """


class AsciiScreen:
    """`AsciiScreen` for displaying Ascii graphics

    Behaves like a surface. Has the option to write its content to the terminal
    """
    cell_transparant: str = " " # symbol used to indicate that a cell is transparent
    cell_default: str = " " # the default look of an empty cell

    def __init__(self, width: int = 16, height: int = 8) -> None:
        """Initialize surface from nodes given inside the given boundaries

        Args:
            width (int, optional): width of surface. Defaults to 16.
            height (int, optional): height of surface. Defaults to 8.
        """
        self.width = width
        self.height = height
        self.texture = [[self.cell_transparant for _ in range(self.width)] for _ in range(self.height)] # 2D array

    def build(self, textured_nodes: Iterable[Transform2DTextureNode] = [], /) -> None:
        """Builds the screen from the texturse of the `nodes with Texture` component

        Args:
            textured_nodes (Iterable[Transform2D & Texture & Node], optional): nodes to render (`textured_nodes` has to derive from `Transform2D`, `Texture` and `Node`). Defaults to [].
            width (int, optional): surface width override. Defaults to 16.
            height (int, optional): surface height override. Defaults to 8.
        """
        self.texture = [[self.cell_transparant for _ in range(self.width)] for _ in range(self.height)] # 2D array

        camera: AsciiCamera = AsciiCamera.current # should never be None
        half_size = Vec2i(self.width // 2, self.height // 2)
        camera_rotation = camera.get_global_rotation()
        cos_camera_rotation = math.cos(-camera_rotation)
        sin_camera_rotation = math.sin(-camera_rotation)
        viewport_global_position = camera.get_global_position()
        # include size of camera parent when including size
        if camera.parent is not None and isinstance(camera.parent, Texture):
            if camera.mode & AsciiCamera.INCLUDE_SIZE:
                camera_parent_lines = len(camera.parent.texture)
                camera_parent_longest = len(max(camera.parent.texture, key=len))
                viewport_global_position.x += camera_parent_longest
                viewport_global_position.y += camera_parent_lines

        for textured in textured_nodes:
            if not textured.is_globally_visible():
                continue
            texture = textured._get_final_texture() # may apply color
            if not texture: # check if has not empty texture
                continue
            if not texture[0]: # check if has first row
                continue
            
            # compute screen space transform
            position = textured._get_texture_global_position() - viewport_global_position
            rotation = textured.get_global_rotation()
            # FIXME: implement camera rotation the right way
            # NOTE: camera rotation is experimental
            # if rotation != 0: # TODO: rotate around center if flagged
            #     position = rotate(position, rotation)

            if camera.mode & AsciiCamera.CENTERED:
                position += half_size

            if rotation != 0 and camera_rotation != 0: # node and camera rotation
                cos_rotation = math.cos(-rotation)
                sin_rotation = math.sin(-rotation)
                for h, line in enumerate(texture):
                    for w, char in enumerate(line):
                        x_position = position.x + cos_rotation * w - sin_rotation * h
                        y_position = position.y + sin_rotation * w + cos_rotation * h
                        x_diff = half_size.x - w
                        y_diff = half_size.y - h
                        x_position = round(half_size.x + x_position + cos_camera_rotation * x_diff - sin_camera_rotation * y_diff)
                        y_position = round(half_size.y + y_position + sin_camera_rotation * x_diff + cos_camera_rotation * y_diff)
                        if not ((self.height) > y_position >= 0): # out of screen
                            continue
                        if not ((self.width) > x_position >= 0): # out of screen
                            continue
                        if char != self.cell_transparant:
                            self.texture[y_position][x_position] = grapheme.rotate(char, rotation - camera_rotation)

            elif rotation != 0: # node rotation
                cos_rotation = math.cos(-rotation)
                sin_rotation = math.sin(-rotation)
                y_offset = len(texture) // 2 if textured.centered else 0 - textured.offset.y
                x_offset = len(max(texture, key=len)) // 2 if textured.centered else 0 - textured.offset.x
                for h, line in enumerate(texture):
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
                for h, line in enumerate(texture):
                    for w, char in enumerate(line):
                        x_diff = half_size.x - w
                        y_diff = half_size.y - h
                        x_position = round(half_size.x + position.x + cos_camera_rotation * x_diff - sin_camera_rotation * y_diff)
                        y_position = round(half_size.y + position.y + sin_camera_rotation * x_diff + cos_camera_rotation * y_diff)
                        if not ((self.height) > y_position >= 0): # out of screen
                            continue
                        if not ((self.width) > x_position >= 0): # out of screen
                            continue
                        if char != self.cell_transparant:
                            self.texture[y_position][x_position] = grapheme.rotate(char, camera_rotation)

            else: # no rotation
                for h, line in enumerate(texture):
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
