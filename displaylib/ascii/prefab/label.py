from __future__ import annotations

from typing import TYPE_CHECKING

from ...util import pull
from ..node import ASCIINode2D
from ..texture import Texture

if TYPE_CHECKING:
    from ...template import Node


@pull("text")
class ASCIILabel(Texture, ASCIINode2D):
    """Prefabricated `Label` node where a new line is created for each `\\n`
    
    Components:
        `Texture`: allows the node to be shown
    """
    def __init__(self, parent: Node | None = None, *, x: int = 0, y: int = 0, text: str = "", z_index: int = 0, force_sort: bool = True) -> None:
        super().__init__(parent, x=x, y=y, force_sort=force_sort)
        self.z_index = z_index
        self.text = text
    
    @property
    def text(self) -> str:
        """Returns a string from texture

        Returns:
            str: content as string
        """
        return "\n".join("".join(line) for line in self.texture)
    
    @text.setter
    def text(self, text: str) -> None:
        """Set content from string. Argument `text` is run through `str` in the process

        Args:
            text (str): string to be converted to content
        """
        self.texture = [list(line) for line in str(text).split("\n")]
