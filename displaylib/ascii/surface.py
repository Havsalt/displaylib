from __future__ import annotations

import math
from typing import TYPE_CHECKING, Iterable

from ..math import Vec2, Vec2i
from ..template import Node2D
from . import grapheme
from .camera import ASCIICamera
from .texture import Texture

if TYPE_CHECKING:
    from ..template import Node


class ASCIISurface:
    """ASCIISurface for displaying nodes
    """
    cell_transparant: str = " " # type used to indicate that a cell is transparent
    cell_default: str = " " # the default look of an empty cell

    def __init__(self, nodes: Iterable[Node] = [], width: int = 16, height: int = 8) -> None:
        """Initialize surface from nodes given inside the given boundaries

        Args:
            nodes (Iterable[ASCIINode], optional): nodes to render onto surface. Defaults to an empty list.
            width (int, optional): width of surface. Defaults to 16.
            height (int, optional): height of surface. Defaults to 8.
        """
        self._width = width
        self._height = height
        self.rebuild(nodes, width, height) # initial build

    @property
    def width(self) -> int:
        return self._width
    
    @width.setter
    def width(self, value: int) -> None:
        self._width = value
        self.texture = [[self.cell_transparant for _ in range(self._width)] for _ in range(self._height)] # 2D array

    @property
    def height(self) -> int:
        return self._height
    
    @height.setter
    def height(self, value: int) -> None:
        self._height = value
        self.texture = [[self.cell_transparant for _ in range(self._width)] for _ in range(self._height)] # 2D array

    def rebuild(self, nodes: Iterable[Node] = [], width: int = 16, height: int = 8) -> None:
        """Rebuilds the surface from the texture of the nodes

        Args:
            nodes (Iterable[Node], optional): nodes to render. Defaults to [].
            width (int, optional): surface width. Defaults to 16.
            height (int, optional): surface height. Defaults to 8.
        """
        self.texture = [[self.cell_transparant for _ in range(width)] for _ in range(height)] # 2D array

        camera: ASCIICamera = ASCIICamera.current # should never be None
        half_size = Vec2i(self._width // 2, self._height // 2)
        camera_rotation = camera.global_rotation
        cos_rotation_camera = math.cos(-camera_rotation)
        sin_rotation_camera = math.sin(-camera_rotation)

        for node in nodes:
            if not isinstance(node, Texture) or not isinstance(node, Node2D):
                continue
            if not node.visible:
                continue
            if not node.texture:
                continue
            if not node.texture[0]: # check if has first row
                continue
            lines = len(node.texture)
            longest = len(max(node.texture, key=len))
            position = node.global_position - camera.global_position
            rotation = node.global_rotation # FIXME: implement camera rotation the right way
            # if rotation != 0: # TODO: rotate around center if flagged
            #     position = rotate(position, rotation)

            if camera.mode == ASCIICamera.CENTERED:
                position += half_size
            elif camera.mode == ASCIICamera.INCLUDE_SIZE:
                position -= Vec2(longest, lines) // 2
            elif camera.mode == ASCIICamera.CENTERED_AND_INCLUDE_SIZE:
                position += half_size
                position -= Vec2(longest, lines) // 2

            if rotation != 0 and camera_rotation != 0: # node and camera rotation
                x_offset = longest / 2
                y_offset = lines / 2
                cos_rotation = math.cos(-rotation)
                sin_rotation = math.sin(-rotation)
                for h, line in enumerate(node.texture):
                    for w, char in enumerate(line):
                        x_diff = w - x_offset
                        y_diff = h - y_offset
                        x_position = x_offset + position.x + cos_rotation * x_diff - sin_rotation * y_diff
                        y_position = y_offset + position.y + sin_rotation * x_diff + cos_rotation * y_diff
                        x_diff = half_size.x - w
                        y_diff = half_size.y - h
                        x_position = round(half_size.x + x_position + cos_rotation_camera * x_diff - sin_rotation_camera * y_diff)
                        y_position = round(half_size.y + y_position + sin_rotation_camera * x_diff + cos_rotation_camera * y_diff)
                        if not ((self._height) > position.y >= 0): # out of screen
                            continue
                        if not ((self._width) > position.x >= 0): # out of screen
                            continue
                        if char != self.cell_transparant:
                            self.texture[y_position][x_position] = grapheme.rotate(char, rotation - camera_rotation)

            elif rotation != 0: # node rotation
                x_offset = longest / 2
                y_offset = lines / 2
                cos_rotation = math.cos(-rotation)
                sin_rotation = math.sin(-rotation)
                for h, line in enumerate(node.texture):
                    for w, char in enumerate(line):
                        x_diff = w - x_offset
                        y_diff = h - y_offset
                        x_position = round(x_offset + position.x + cos_rotation * x_diff - sin_rotation * y_diff)
                        y_position = round(y_offset + position.y + sin_rotation * x_diff + cos_rotation * y_diff)
                        if not ((self._height) > position.y >= 0): # out of screen
                            continue
                        if not ((self._width) > position.x >= 0): # out of screen
                            continue
                        if char != self.cell_transparant:
                            self.texture[y_position][x_position] = grapheme.rotate(char, rotation)
            
            elif camera_rotation != 0: # camera rotation
                for h, line in enumerate(node.texture):
                    for w, char in enumerate(line):
                        x_diff = half_size.x - w
                        y_diff = half_size.y - h
                        x_position = round(half_size.x + position.x + cos_rotation_camera * x_diff - sin_rotation_camera * y_diff)
                        y_position = round(half_size.y + position.y + sin_rotation_camera * x_diff + cos_rotation_camera * y_diff)
                        if not ((self._height) > position.y >= 0): # out of screen
                            continue
                        if not ((self._width) > position.x >= 0): # out of screen
                            continue
                        if char != self.cell_transparant:
                            self.texture[y_position][x_position] = grapheme.rotate(char, camera_rotation)
            
            else: # no rotation
                for h, line in enumerate(node.texture):
                    if not ((self._height) > position.y >= 0): # out of screen
                        continue
                    y_position = int(h + position.y)
                    for w, char in enumerate(line):
                        if not ((self._width) > position.x >= 0): # out of screen
                            continue
                        x_position = int(w + position.x)
                        if char != self.cell_transparant:
                            self.texture[y_position][x_position] = char

    def clear(self) -> None:
        """Clears the surface. Sets its texture to `ASCIISurface.cell_transparant`
        """
        self.texture = [[self.cell_transparant for _ in range(self._width)] for _ in range(self._height)] # 2D array
    
    def blit(self, surface: ASCIISurface, position: Vec2 = Vec2(0, 0), transparent: bool = False) -> None:
        """Blits the texture of this surface onto the other surface

        Args:
            surface (ASCIISurface): surface to blit onto
            position (Vec2, optional): starting point of blit. Defaults to Vec2(0, 0).
            transparent (bool, optional): whether to override blank areas. Defaults to False.
        """
        lines = len(surface.texture)
        longest = len(max(surface.texture, key=len))
        if position.x > longest and position.y > lines: # completely out of screen
            return
        for h, line in enumerate(surface.texture):
            if self._height < h + position.y or position.y < 0: # line out of screen
                continue
            for w, char in enumerate(line):
                if self._width < w + position.x or position.x < 0: # char out of screen
                    continue

                current = self.texture[int(h+position.y)][int(w+position.x)]
                if current == self.cell_default: # empty rendered cell
                    if not transparent:
                        self.texture[int(h+position.y)][int(w+position.x)] = char
                        continue
                self.texture[int(h+position.y)][int(w+position.x)] = char
