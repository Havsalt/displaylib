import sys
from typing import Iterable
from typing_extensions import Self
from ..math import Vec2
from .node import ASCIINode
from .camera import ASCIICamera
from .constants import *


class ASCIISurface:
    """ASCIISurface for displaying nodes
    """

    def __init__(self, nodes: Iterable[ASCIINode] = [], width: int = 16, height: int = 8) -> None:
        self._width = width
        self._height = height
        self.content = [[ASCIINode.cell_transparant for _ in range(width)] for _ in range(height)] # 2D array

        camera: ASCIICamera = ASCIICamera.current
        for node in nodes:
            if not node.visible:
                continue
            if not node.content:
                continue
            lines = len(node.content)
            position = node.global_position - camera.global_position
            if position.y + lines < 0 or position.y > self._height:
                continue
            longest = len(max(node.content, key=len))
            if position.x + longest < 0 or position.x > self._width:
                continue
            for h, line in enumerate(node.content):
                if not ((self._height) > (h + position.y) >= 0): # out of screen
                    continue
                for w, char in enumerate(line):
                    if not ((self._width) > (w + position.x) >= 0): # out of screen
                        continue
                    if char != ASCIINode.cell_transparant:
                        self.content[h+position.y][w+position.x] = char

    def clear(self) -> None:
        self.content = [[ASCIINode.cell_transparant for _ in range(self._width)] for _ in range(self._height)] # 2D array

    def display(self):
        lines = len(self.content)
        for idx, line in enumerate(self.content):
            rendered = "".join(letter if letter != ASCIINode.cell_transparant else ASCIINode.cell_default for letter in (line))
            sys.stdout.write(rendered + " " + ("\n" if idx != lines else ""))
        sys.stdout.write(ANSI_UP * len(self.content) + "\r")
        sys.stdout.flush()
    
    # FIXME: blit order in ASCIIEngine
    def blit(self, surface: Self, position: Vec2 = Vec2(0, 0), transparent: bool = False):
        lines = len(surface.content)
        longest = len(max(surface.content, key=len))
        if position.x > longest and position.y > lines: # completely out of screen
            return
        for h, line in enumerate(surface.content):
            if self._height < h + position.y <= 0: # line out of screen
                continue
            for w, char in enumerate(line):
                if self._width < w + position.x <= 0: # char out of screen
                    continue

                current = self.content[h+position.y][w+position.x]
                if current == ASCIINode.cell_default: # empty rendered cell
                    if not transparent:
                        self.content[h+position.y][w+position.x] = char
                        continue
                self.content[h+position.y][w+position.x] = char
