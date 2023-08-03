from __future__ import annotations

import time


class Clock:
    """`Clock` that pauses the program with adjusted `delta time` based on execution time of a timeframe
    """
    
    def __init__(self, tps: int) -> None:
        """Initilizes the clock with a given tps

        Args:
            tps (int): ticks per second
        """
        self.tps = tps
        self.delta_time = 1.0 / self.tps # initial delta time (optimal)
        self._target_delta = 1.0 / self.tps
        self._last_tick = time.perf_counter()
    
    @property
    def tps(self) -> int:
        return self._tps
    
    @tps.setter
    def tps(self, value: int) -> None:
        self._tps = value
        self._target_delta = 1.0 / self._tps
    
    def tick(self) -> None:
        """Pauses the clock temporay to achieve the desired framerate (tps)
        """
        current_time = time.perf_counter()
        elapsed_time = current_time - self._last_tick
        sleep_time = self._target_delta - elapsed_time
        if sleep_time > 0:
            time.sleep(sleep_time)
            self._last_tick = time.perf_counter()
        else:
            self._last_tick = current_time
        self.delta_time = max(0, sleep_time)
