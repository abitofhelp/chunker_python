import multiprocessing

class AtomicCounter:
    def __init__(self, initial=0):
        self.value = multiprocessing.Value('i', initial)
        self.lock = multiprocessing.Lock()

    def increment(self, num=1):
        with self.lock:
            self.value.value += num

    def decrement(self, num=1):
        with self.lock:
            self.value.value -= num

    def get(self):
        with self.lock:
            return self.value.value