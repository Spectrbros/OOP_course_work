from abc import ABC, abstractmethod


class Command(ABC):

    def __init__(self, facade):
        self._facade = facade

    @abstractmethod
    def execute(self):
        ...