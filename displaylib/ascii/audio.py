from __future__ import annotations

import sys

if sys.platform != "win32": # if not on Windows, implement a skeleton, which raises NotImplemented
    class AudioStreamPlayer:
        """Raises NotImplemented. Only implemented for Windows (win32)
        """
        @classmethod
        def load(cls, file_path: str, /) -> NotImplemented:
            raise NotImplemented("AudioStreamPlayer only implemented for Windows (win32)")
        
        def __init__(self, file_path: str, /, *, max_sound_count: int = max_sound_count_default, force_sort: bool = True) -> NotImplemented:
            raise NotImplemented("AudioStreamPlayer only implemented for Windows (win32)")

        @property
        def active_sound_count(self) -> NotImplemented:
            raise NotImplemented("AudioStreamPlayer only implemented for Windows (win32)")
        
        @property
        def is_playing(self) -> NotImplemented:
            raise NotImplemented("AudioStreamPlayer only implemented for Windows (win32)")

        def play(self) -> NotImplemented:
            raise NotImplemented("AudioStreamPlayer only implemented for Windows (win32)")

        # def stop(self) -> NotImplemented:
        #     raise NotImplemented("AudioStreamPlayer only implemented for Windows (win32)")
else:
    import threading
    # import atexit
    from winsound import PlaySound as play_sound, SND_FILENAME, SND_PURGE
    from typing import TypeVar, ClassVar

    Self = TypeVar("Self")


    class AudioStreamPlayer:
        """`AudioStreamPlayer` for playing sounds from disk. Can play multiple instances of the sound simultaneously

        Known Issues:
            - `Globally, only one sound can be played at the same time, the rest is queued for when the current sound finishes`
        """
        max_sound_count_default: ClassVar[int] = 1 # number of sounds this AudioStreamPlayer can play at the same time

        def __init__(self, file_path: str, /, *, max_sound_count: int = max_sound_count_default, force_sort: bool = True) -> None:
            self.file_path = file_path
            self.max_sound_count = max_sound_count
            self._active_sound_count = 0 # read only
            self._sound_threads: list[threading.Thread] = []
            self._terminate_event = threading.Event()
            # atexit.register(self.stop)
        
        # def __del__(self) -> None:
        #     atexit.unregister(self.stop)
        
        @property
        def is_playing(self) -> bool:
            """Returns whether there are sounds currently playing

            Returns:
                bool: current state
            """
            return self._active_sound_count > 0
        
        @property
        def active_sound_count(self) -> int: # read only
            return self._active_sound_count
        
        def play(self) -> bool:
            """Starts a new thread and plays the sound.
            The maximum amount of sounds that can be played simultaneously is determined by `.max_sound_count`

            Returns:
                bool: whether it succeeded - returns True if `.active_sound_count` < `.max_sound_count`, False otherwise
            """
            failed = self._active_sound_count >= self.max_sound_count
            if failed:
                return False
            self._active_sound_count += 1
            thread = threading.Thread(target=self._handler, daemon=True)
            self._sound_threads.append(thread)
            thread.start()
            return True
        
        # def stop(self) -> None:
        #     """Stops all sounds playing and queued
        #     """
        #     self._terminate_event.set() # purges inside the _handler method
        #     # for thread in self._sound_threads:
        #     #     thread.join(0.01)
        #     self._active_sound_count = 0
        
        def _handler(self) -> None:
            """Threaded handler function responsible for decrementing `.active_sound_count`
            """
            play_sound(self.file_path, SND_FILENAME)
            self._terminate_event.wait()
            play_sound(None, SND_PURGE)
            self._active_sound_count -= 1 # should never go below 0
