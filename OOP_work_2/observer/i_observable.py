from abc import ABC, abstractmethod

from observer.i_observer import IObserver
from observer.order_event import OrderEvent


class IObservable(ABC):
    @abstractmethod
    def subscribe(self, observer: IObserver) -> None:
        ...

    @abstractmethod
    def unsubscribe(self, observer: IObserver) -> None:
        ...

    @abstractmethod
    def notify(self, event: OrderEvent) -> None:
        ...