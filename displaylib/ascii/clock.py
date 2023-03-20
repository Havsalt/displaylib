from __future__ import annotations

import time


class Clock:
    def __init__(self, tps: int) -> None:
        """Initilizes the clock

        Args:
            tps (int): ticks per second
        """
        self._tps = tps
        self._delta = 1.0 / self.tps
        self._last_tick = time.perf_counter()
    
    @property
    def tps(self) -> int:
        return self._tps
    
    @tps.setter
    def tps(self, value: int) -> None:
        self._tps = value
        self._delta = 1.0 / self._tps
    
    def tick(self) -> float:
        """Pauses the clock temporay to achieve the desired framerate (tps)

        Returns:
            float: delta time since last tick
        """
        time.sleep(self._delta) # QUICKFIX
        return self._delta
        now = time.perf_counter()
        diff = now - self._last_tick
        remaining = self._delta - diff
        if remaining <= 0:
            return 0.0
        time.sleep(remaining)
        self._last_tick = time.perf_counter()
        return diff
