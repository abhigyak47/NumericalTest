"""
Timer class for managing test timing.
"""

import time
import tkinter as tk
from typing import Optional, Callable


class Timer:
    """Timer class for managing test timing"""

    def __init__(self, initial_seconds: int,
                 tick_callback: Optional[Callable[[int], None]] = None,
                 finish_callback: Optional[Callable[[], None]] = None):
        self.initial_seconds = initial_seconds
        self.remaining_seconds = initial_seconds
        self.tick_callback = tick_callback
        self.finish_callback = finish_callback
        self.is_running = False
        self.start_time = None
        self.elapsed_seconds = 0

    def start(self):
        """Start the timer"""
        self.is_running = True
        self.start_time = time.time()
        self._tick()

    def stop(self):
        """Stop the timer"""
        self.is_running = False

    def pause(self):
        """Pause the timer"""
        if self.is_running and self.start_time:
            self.elapsed_seconds += time.time() - self.start_time
            self.is_running = False

    def resume(self):
        """Resume the timer"""
        if not self.is_running:
            self.start_time = time.time()
            self.is_running = True
            self._tick()

    def _tick(self):
        """Internal tick method"""
        if not self.is_running:
            return

        if self.initial_seconds > 0:  # Countdown mode
            elapsed = time.time() - self.start_time if self.start_time else 0
            total_elapsed = self.elapsed_seconds + elapsed
            self.remaining_seconds = max(0, self.initial_seconds - total_elapsed)

            if self.tick_callback:
                self.tick_callback(self.remaining_seconds)

            if self.remaining_seconds <= 0:
                self.stop()
                if self.finish_callback:
                    self.finish_callback()
                return
        else:  # Elapsed mode
            elapsed = time.time() - self.start_time if self.start_time else 0
            total_elapsed = self.elapsed_seconds + elapsed

            if self.tick_callback:
                self.tick_callback(total_elapsed)

        # Schedule next tick
        self.timer_id = tk.Tk.after(tk._default_root, 1000, self._tick)

    def get_elapsed_time(self) -> float:
        """Get total elapsed time in seconds"""
        if self.start_time:
            return self.elapsed_seconds + (time.time() - self.start_time if self.is_running else 0)
        return self.elapsed_seconds