import time

class Timer:

    def __init__(self):
        self.startTime = 0
        self.elapsed = 0

    def start(self):
        self.startTime = time.perf_counter()

    def end(self):
        self.elapsed = time.perf_counter() - self.startTime

    def peak(self):
        return time.perf_counter() - self.startTime

    def __str__(self):
        return "Elapsed Time: {}".format(self.elapsed)