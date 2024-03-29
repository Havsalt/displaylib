from __future__ import annotations

from typing import TYPE_CHECKING, cast

from ...math import Vec2
from ...template.type_hints import MroNext, NodeType
from ..node import AsciiNode2D
from ..texture import Texture
from ..colored import Color
from ..color import WHITE

if TYPE_CHECKING:
    from ...template.type_hints import AnyNode
    from ..color import ColorValue


class AsciiLabel(Color, Texture, AsciiNode2D):
    """Prefabricated `Label` node where a new line is created for each `\\n` (or by changing the `delimiter` argument)
    
    Components:
        - `Texture`: allows the node to be shown
        - `Color`: applies color to the texture
    """
    text: str # type: ignore
    delimiter: str = "\n"
    tab_size: int = 4
    tab_char: str = "\t"
    tab_fill: str = " "

    def __new__(cls: type[NodeType], *args, text: str = "", delimiter = None, **kwargs) -> NodeType:
        mro_next = cast(MroNext[AsciiLabel], super())
        instance = mro_next.__new__(cls, *args, **kwargs)
        # override -> immutable class value (default)
        if delimiter is not None: # handle before `.text`!
            instance.delimiter = delimiter
        # override -> class value -> default
        if text or not hasattr(instance, "text"):
            instance.text = text
        return cast(NodeType, instance)
    
    def __init__(self, parent: AnyNode | None = None, *, x: float = 0, y: float = 0, text: str = "", color: ColorValue = WHITE, delimiter: str = "\n", offset: Vec2 = Vec2(0, 0), centered: bool = False, z_index: int = 0, force_sort: bool = True) -> None:
        """Initializes the label

        Args:
            parent (Node | None, optional): parent node. Defaults to None.
            x (float, optional): local x position. Defaults to 0.
            y (float, optional): local y position. Defaults to 0.
            text (str, optional): initial text. Defaults to "".
            color (ColorValue, optional): texture color. Defaults to WHITE.
            delimiter (str, optional): where to split the lines. Defaults to "\n".
            z_index (int, optional): layer to render on. Defaults to 0.
            force_sort (bool, optional): whether to sort based on 'z_index' and 'process_priority'. Defaults to True.
        """
    
    @property
    def text(self) -> str:
        """Returns a string from texture

        Returns:
            str: content as string
        """
        return self.delimiter.join("".join(line).replace(self.tab_fill * self.tab_size, self.tab_char)
                                   for line in self.texture)
    
    @text.setter
    def text(self, text: str) -> None:
        """Set content from string. Argument `text` is run through `str` in the process

        Args:
            text (str): string to be converted to content
        """
        if not text:
            self.texture = []
        else:
            self.texture = [list(line)
                            for line in str(text.replace(self.tab_char,
                                                         self.tab_fill * self.tab_size)
                                                         ).split(self.delimiter)]
