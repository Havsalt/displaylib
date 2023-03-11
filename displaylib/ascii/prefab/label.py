from __future__ import annotations

from typing import TYPE_CHECKING

from ..node import ASCIINode

if TYPE_CHECKING:
    from ...template import Node


class ASCIILabel(ASCIINode):
    """Prefabricated `Label` node

    A new line is created for each `\\n`
    """
    def __init__(self, parent: Node | None = None, x: int = 0, y: int = 0, text: str = "", z_index: int = 0, force_sort: bool = True) -> None:
        super().__init__(parent, x, y, z_index, force_sort)
        self.text = text
    
    @property
    def text(self) -> str:
        """Returns a string from content

        Returns:
            str: content as string
        """
        return "\n".join("".join(line) for line in self.content)
    
    @text.setter
    def text(self, text: str) -> None:
        """Set content from string

        Args:
            text (str): string to be converted to content
        """
        self.content = [list(line) for line in text.split("\n")]
