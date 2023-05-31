from __future__ import annotations

import threading
from winsound import PlaySound as play_sound, SND_MEMORY
from typing import TypeVar, ClassVar

from ..util import pull
from ..template import Node

Self = TypeVar("Self")


@pull("stream", "max_sound_count")
class AudioStreamPlayer(Node):
    """`AudioStreamPlayer` for playing sounds from disk. Can play multiple instances of the sound simultaneously

    Known Issues:
        - `Globally, only one sound can be played at the same time, the rest is queued for when the current sound finishes`
        - `Attribute 'is_playing' is True when calling '.play()', and False when finished`
    """
    stream_default: ClassVar[bytes] = bytes()
    max_sound_count_default: ClassVar[int] = 1 # number of sounds this AudioStreamPlayer can play at the same time

    @classmethod
    def load(cls, file_path: str, /) -> AudioStreamPlayer:
        """Returns an AudioStreamPlayer with its data loaded from the give file

        Args:
            file_path (str): location of the `.wav` file

        Returns:
            AudioStreamPlayer: AudioStreamPlayer with its data loaded from disk
        """
        wave_file = open(file_path, "rb")
        audio_stream = wave_file.read()
        wave_file.close()
        return cls(stream=audio_stream)

    def __init__(self, parent: Node | None = None, *, stream: bytes = stream_default, max_sound_count: int = max_sound_count_default, force_sort: bool = True) -> None:
        super().__init__(parent, force_sort=force_sort)
        self.stream = stream
        self.max_sound_count = max_sound_count
        self.is_playing = False # True when calling .play(), and False when finished
        self._active_sound_count = 0
    
    @property
    def active_sound_count(self) -> int:
        return self._active_sound_count
    
    def play(self) -> bool:
        """Starts a new thread and plays the sound.
        The maximum amount of sounds that can be played simultaneously is determined by `.max_sound_count`

        Returns:
            bool: whether it succeeded - returns True if `.active_sound_count` < `.max_sound_count`, False otherwise
        """
        self.is_playing = True
        failed = self._active_sound_count >= self.max_sound_count
        if failed:
            return False
        self._active_sound_count += 1
        threading.Thread(target=self._handler).start()
        return True
    
    def _handler(self) -> None:
        """Threaded handler function responsible for decrementing 
        """
        play_sound(self.stream, SND_MEMORY)
        self._active_sound_count -= 1 # should never go below 0
        if self._active_sound_count == 0:
            self.is_playing = False
