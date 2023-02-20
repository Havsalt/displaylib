import sys
from .node import ASCIINode
from .surface import ASCIISurface


class ASCIIScreen(ASCIISurface):
    """Screen for displaying ASCII graphics

    Behaves like a surface. Has the option to write its content to the terminal
    """

    def show(self) -> None:
        out = ""
        lines = len(self.content)
        for idx, line in enumerate(self.content):
            rendered = "".join(letter if letter != ASCIINode.cell_transparant else ASCIINode.cell_default for letter in (line))
            out += (rendered + " " + ("\n" if idx != lines else ""))
        out += ("\u001b[A" * len(self.content) + "\r") # "\u001b[A" is ANSI code for UP
        sys.stdout.write(out)
        sys.stdout.flush()
