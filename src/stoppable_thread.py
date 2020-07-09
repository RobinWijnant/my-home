import threading
import ctypes


class StoppableThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        print(args, kwargs)
        super().__init__(self, *args, **kwargs)

    def raise_exception(self):
        thread_id = self.get_ident()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
            thread_id, ctypes.py_object(SystemExit)
        )
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print("Exception raise failure")

