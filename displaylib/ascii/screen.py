from __future__ import annotations

import sys

from .surface import AsciiSurface


class AsciiScreen(AsciiSurface):
    """`AsciiScreen` for displaying Ascii graphics

    Behaves like a surface. Has the option to write its content to the terminal
    """
    def show(self) -> None:
        out = ""
        lines = len(self.texture)
        for idx, line in enumerate(self.texture):
            rendered = "".join(letter if letter != self.cell_transparant else self.cell_default for letter in (line))
            out += (rendered + " " + ("\n" if idx != lines else ""))
        out += ("\u001b[A" * len(self.texture) + "\r") # "\u001b[A" is ANSI code for UP
        sys.stdout.write(out)
        sys.stdout.flush()
