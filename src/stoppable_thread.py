import threading


class StoppableThread(threading.Thread):
    def __init__(self, function, arguments):
        super().__init__(target=function, args=[*arguments, self.stopped])
        self._cancelled = threading.Event()

    def stop(self):
        self._cancelled.set()

    def stopped(self):
        return self._cancelled.isSet()

