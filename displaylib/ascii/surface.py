from __future__ import annotations

import math
from typing import TYPE_CHECKING, Iterable

from ..math import Vec2
from . import grapheme
from .node import ASCIINode
from .camera import ASCIICamera

if TYPE_CHECKING:
    from ..template import Node


class ASCIISurface:
    """ASCIISurface for displaying nodes
    """

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
        self.content = [[ASCIINode.cell_transparant for _ in range(self._width)] for _ in range(self._height)] # 2D array

    @property
    def height(self) -> int:
        return self._height
    
    @height.setter
    def height(self, value: int) -> None:
        self._height = value
        self.content = [[ASCIINode.cell_transparant for _ in range(self._width)] for _ in range(self._height)] # 2D array

    def rebuild(self, nodes: Iterable[Node] = [], width: int = 16, height: int = 8) -> None:
        """Rebuilds the surface from the content of the nodes

        Args:
            nodes (Iterable[Node], optional): nodes to render. Defaults to [].
            width (int, optional): surface width. Defaults to 16.
            height (int, optional): surface height. Defaults to 8.
        """
        self.content = [[ASCIINode.cell_transparant for _ in range(width)] for _ in range(height)] # 2D array

        camera: ASCIICamera = ASCIICamera.current # should never be None
        half_size = Vec2(self._width, self._height) // 2
        for node in nodes:
            if getattr(node, "__logical__") == True:
                continue
            if not node.visible:
                continue
            if not node.content:
                continue
            lines = len(node.content)
            longest = len(max(node.content, key=len))
            position = node.global_position - camera.global_position
            rotation = node.global_rotation + camera.global_rotation # FIXME: implement camera rotation the right way
            # if rotation != 0: # TODO: rotate around center if flagged
            #     position = rotate(position, rotation)
            if position.y + lines < 0 or position.y > self._height: # out of screen
                continue
            if position.x + longest < 0 or position.x > self._width: # out of screen
                continue

            if camera.mode == ASCIICamera.CENTERED:
                position += half_size
            elif camera.mode == ASCIICamera.INCLUDE_SIZE:
                position -= Vec2(longest, lines) // 2
            elif camera.mode == ASCIICamera.CENTERED_AND_INCLUDE_SIZE:
                position += half_size
                position -= Vec2(longest, lines) // 2
            
            if rotation != 0:
                x_offset = longest / 2
                y_offset = lines / 2
                cos_rotation = math.cos(-rotation)
                sin_rotation = math.sin(-rotation)
            for h, line in enumerate(node.content):
                # if not ((self._height) > (h + position.y) >= 0): # out of screen
                #     continue
                for w, char in enumerate(line):
                    if rotation != 0:
                        x_diff = w - x_offset
                        y_diff = h - y_offset
                        x_position = round(x_offset + position.x + cos_rotation * x_diff - sin_rotation * y_diff)
                        y_position = round(y_offset + position.y + sin_rotation * x_diff + cos_rotation * y_diff)
                    else:
                        x_position = int(w + position.x)
                        y_position = int(h + position.y)
                    if not ((self._height) > y_position >= 0): # out of screen
                        continue
                    if not ((self._width) > x_position >= 0): # out of screen
                        continue
                    if char != ASCIINode.cell_transparant:
                        if rotation != 0:
                            self.content[y_position][x_position] = grapheme.rotate(char, rotation)
                        else:
                            self.content[y_position][x_position] = char

    def clear(self) -> None:
        """Clears the surface. Sets its content to `ASCIINode.cell_transparant`
        """
        self.content = [[ASCIINode.cell_transparant for _ in range(self._width)] for _ in range(self._height)] # 2D array
    
    def blit(self, surface: ASCIISurface, position: Vec2 = Vec2(0, 0), transparent: bool = False) -> None:
        """Blits the content of this surface onto the other surface

        Args:
            surface (ASCIISurface): surface to blit onto
            position (Vec2, optional): starting point of blit. Defaults to Vec2(0, 0).
            transparent (bool, optional): whether to override blank areas. Defaults to False.
        """
        lines = len(surface.content)
        longest = len(max(surface.content, key=len))
        if position.x > longest and position.y > lines: # completely out of screen
            return
        for h, line in enumerate(surface.content):
            if self._height < h + position.y or position.y < 0: # line out of screen
                continue
            for w, char in enumerate(line):
                if self._width < w + position.x or position.x < 0: # char out of screen
                    continue

                current = self.content[int(h+position.y)][int(w+position.x)]
                if current == ASCIINode.cell_default: # empty rendered cell
                    if not transparent:
                        self.content[int(h+position.y)][int(w+position.x)] = char
                        continue
                self.content[int(h+position.y)][int(w+position.x)] = char
