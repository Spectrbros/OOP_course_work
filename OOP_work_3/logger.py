from datetime import datetime
from logging.logging_source import LoggingSource

_GREEN = "\033[92m"
_RESET = "\033[0m"

class Logger:
    _instance = None

    def __new__(cls) -> "Logger":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._records = []
            cls._instance._enabled = True
        return cls._instance

    def log(self, source: LoggingSource, message: str) -> None:
        timestamp = datetime.now().strftime("%H:%M:%S")
        record = f"[{timestamp}] {source.value}: {message}"
        self._records.append(record)
        print(f"{_GREEN}{record}{_RESET}")
        if self._enabled:
            print(f"{_GREEN}{record}{_RESET}")

    def set_enabled(self, enabled: bool) -> None:
        self._enabled = enabled

    def clear(self) -> None:
        self._records = []

    @property
    def records(self) -> tuple[str, ...]:
        return tuple(self._records)
