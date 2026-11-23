from abc import ABC, abstractmethod

from observer.order_event import OrderEvent


class IObserver(ABC):
    @abstractmethod
    def on_order_event(self, event: OrderEvent) -> None:
        ...