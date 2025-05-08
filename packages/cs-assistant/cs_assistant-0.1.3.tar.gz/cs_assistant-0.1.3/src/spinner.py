import sys
import threading
import itertools
import time
from typing import Optional

class Spinner:
    """A simple console spinner animation."""
    def __init__(self, message: str = "") -> None:
        self._spinner = itertools.cycle(["|", "/", "-", "\\"])
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._message = message

    def start(self) -> None:
        """Start the spinner in a separate thread."""
        self._running = True
        self._thread = threading.Thread(target=self._spin, daemon=True)
        self._thread.start()

    def _spin(self) -> None:
        """Spin the spinner until stopped."""
        while self._running:
            sys.stdout.write(f"\r{self._message} {next(self._spinner)}")
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write("\r")
        sys.stdout.flush()

    def stop(self) -> None:
        """Stop the spinner."""
        self._running = False
        if self._thread:
            self._thread.join() 