from abc import ABC, abstractmethod


class Handler(ABC):
    def __init__(self):
        self._next = None

    def set_next(self, handler):
        self._next = handler
        return handler

    @abstractmethod
    def handle(self, cmd):
        ...
