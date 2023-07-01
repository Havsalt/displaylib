from __future__ import annotations

from typing import TYPE_CHECKING

from ...util import pull
from ..node import AsciiNode2D
from ..texture import Texture
from ..colored import Color
from ..color import WHITE, _Color

if TYPE_CHECKING:
    from ...template import Node


@pull("text", "delimiter")
class AsciiLabel(Color, Texture, AsciiNode2D):
    """Prefabricated `Label` node where a new line is created for each `\\n`
    
    Components:
        - `Texture`: allows the node to be shown
        - `Color`: applies color to the texture
    """
    def __init__(self, parent: Node | None = None, *, x: float = 0, y: float = 0, text: str = "", color: _Color = WHITE, delimiter: str = "\n", z_index: int = 0, force_sort: bool = True) -> None:
        super().__init__(parent, x=x, y=y, force_sort=force_sort)
        self.delimiter = delimiter # has to be set before '.delimiter' is set and defined
        self.text = text
        self.color = color
        self.z_index = z_index
    
    @property
    def text(self) -> str:
        """Returns a string from texture

        Returns:
            str: content as string
        """
        return self.delimiter.join("".join(line) for line in self.texture)
    
    @text.setter
    def text(self, text: str) -> None:
        """Set content from string. Argument `text` is run through `str` in the process

        Args:
            text (str): string to be converted to content
        """
        self.texture = [list(line) for line in str(text).split(self.delimiter)]
