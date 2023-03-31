from __future__ import annotations

import time


class Clock:
    """`Clock` that pauses the program with adjusted `deltatime` based on execution time of a timeframe
    """
    
    def __init__(self, tps: int) -> None:
        """Initilizes the clock

        Args:
            tps (int): ticks per second
        """
        self.tps = tps
        self._target_delta = 1.0 / self.tps
        self._last_tick = time.perf_counter()
    
    @property
    def tps(self) -> int:
        return self._tps
    
    @tps.setter
    def tps(self, value: int) -> None:
        self._tps = value
        self._target_delta = 1.0 / self._tps
    
    def get_delta(self) -> float:
        """Returns the current deltatime since last clock tick

        Returns:
            float: time since last tick
        """
        return max(0.0, time.perf_counter() - self._last_tick)
    
    def tick(self) -> float:
        """Pauses the clock temporay to achieve the desired framerate (tps)

        Returns:
            float: delta time since last tick
        """
        now = time.perf_counter()
        diff = now - self._last_tick
        remaining = self._target_delta - diff
        if remaining <= 0:
            self._last_tick = now
            return 0.0
        time.sleep(remaining)
        self._last_tick = time.perf_counter()
        return diff
