import threading


class StoppableThread(threading.Thread):
    def __init__(self, function, *arguments, on_complete=lambda: None):
        def threadedfunction():
            function(*arguments, self.stopped)
            on_complete()

        super().__init__(target=threadedfunction)
        self._cancelled = threading.Event()

    def stop(self):
        self._cancelled.set()

    def stopped(self):
        return self._cancelled.isSet()

