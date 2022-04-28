import time

"""
The Limiter is a queue that will keep track of the 
time that each request is made. As times exceed the 60 second
mark, they are dequeued.
"""
class Limiter:

    def __init__(self):
        self.requests = list()
        self.limit = 20

    def print(self):
        for i in range(len(self.requests)):
            if (i % 5 == 0):
                print()
            else:
                print("{:.2f} ".format(time.perf_counter() - self.requests[i]), end="")


    """
    Remove all requests that were made over 60
    seconds in the past. Returns false if no values
    could be trimmed from the queue.
    """
    def trim(self):
        difference = time.perf_counter() - self.requests[-1]
        if difference >= 60:
            while difference >= 60:
                self.requests.pop()
                difference = time.perf_counter() - self.requests[-1]
            return True
        return False

    """
    Checks if there is room in the queue
    for more requests.
    """
    def check(self):
        if len(self.requests) < self.limit or self.trim():
            return True
        return False

    def add(self):
        self.requests.insert(0,time.perf_counter())

