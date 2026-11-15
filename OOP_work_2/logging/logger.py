from datetime import datetime
from logging.logging_source import LoggingSource

class Logger:
    _instance = None

    def __new__(cls) -> "Logger":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._records = []
        return cls._instance

    def log(self, source: LoggingSource, message: str) -> None:
        timestamp = datetime.now().strftime("%H:%M:%S")
        record = f"[{timestamp}] {source.value}: {message}"
        self._records.append(record)
        print(record)

    @property
    def records(self) -> tuple[str, ...]:
        return tuple(self._records)
