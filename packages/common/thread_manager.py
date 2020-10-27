import threading

from stoppable_thread import StoppableThread


class ThreadManager:
    def __init__(self):
        self.current_thread = None

    def execute(self, *args, **kwargs):
        self.stop()
        self.current_thread = StoppableThread(*args, **kwargs)
        self.current_thread.start()

    def stop(self):
        if self.current_thread is not None:
            self.current_thread.stop()

