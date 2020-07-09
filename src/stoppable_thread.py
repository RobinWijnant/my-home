import threading


class StoppableThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, args=[*kwargs[args], self.stopped])
        self._cancelled = threading.Event()

    def stop(self):
        self._cancelled.set()

    def stopped(self):
        return self._cancelled.isSet()

