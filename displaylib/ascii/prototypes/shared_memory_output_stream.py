from __future__ import annotations

import sys
from io import StringIO
from multiprocessing.shared_memory import SharedMemory
from typing import TYPE_CHECKING, Protocol, TextIO, cast

from ..screen import AsciiScreen
from ...template.type_hints import MroNext, EngineType, EngineMixin

if TYPE_CHECKING:
    from displaylib.ascii.screen import AsciiScreen


class MemoryStreamedEngineProtocol(EngineMixin, Protocol):
    @property
    def screen(self) -> MemoryStreamedScreen: ...
    @screen.setter
    def screen(self, value: MemoryStreamedScreen) -> None: ...


MEMORY_SIZE = 4096


class SharedStream(StringIO):
    _MEMORY_INFO_END = 2
    _counter: int
    _shared_memory: SharedMemory

    def __new__(cls) -> SharedStream:
        instance = super().__new__(cls)
        instance._counter = cls._MEMORY_INFO_END
        instance._shared_memory = SharedMemory(name="SharedStream", create=True, size=MEMORY_SIZE)
        return instance
    
    def write(self, string: str) -> int:
        chunk = bytearray(string, encoding="utf-8")
        chunk_size = len(chunk)
        start = self._counter
        stop = self._counter + chunk_size
        # with open("msg.txt", "w", encoding="utf-8") as f:
        #     f.write(str(len(self._shared_memory.buf[start:stop])) + " / " + str(len(bytearray(string, encoding="utf-8"))))
        self._shared_memory.buf[start:stop] = chunk
        self._counter += chunk_size
        return StringIO.write(self, string)

    def clear(self) -> None:
        self._counter = self._MEMORY_INFO_END
        for idx in range(self._MEMORY_INFO_END, MEMORY_SIZE):
            self._shared_memory.buf[idx] = 0
    
    def set_screen_size(self, width: int, height: int) -> None:
        self._shared_memory.buf[0] = width # width int
        self._shared_memory.buf[1] = height # height int
    

class MemoryStreamedScreen(AsciiScreen):
    def show(self) -> None:
        stdout = cast(SharedStream, sys.stdout)
        stdout.clear()
        stdout.set_screen_size(self.width, self.height)
        # ---
        out = ""
        lines = len(self.texture)
        for idx, line in enumerate(self.texture):
            rendered = "".join(letter if letter != self.cell_transparant else self.cell_default for letter in (line))
            out += (rendered + " " + ("\n" if idx != lines else ""))
        sys.stdout.write(out)
        sys.stdout.flush()


class SharedMemoryOutputStream:
    _shared_stream: SharedStream
    _old_stdout: TextIO

    def __new__(cls: type[EngineType], **config) -> EngineType:
        mro_next = cast(MroNext[SharedMemoryOutputStream], super())
        instance = mro_next.__new__(cls, **config)
        instance._shared_stream = SharedStream()
        instance._old_stdout = sys.stdout
        sys.stdout = instance._shared_stream
        instance = cast(MemoryStreamedEngineProtocol, instance)
        instance.screen = MemoryStreamedScreen(width=instance.screen.width, height=instance.screen.height)
        return cast(EngineType, instance)
