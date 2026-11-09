class OrderEvent:
    def __init__(self) -> None:
        self._order_id = 0
        self._old_status = 0
        self._new_status = 0
        self._time_stamp = 0