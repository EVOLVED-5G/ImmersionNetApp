import threading


# Simple thread extension with a boolean to control "politely" the execution
class PoliteThread(threading.Thread):

    def __init__(self):
        super().__init__()
        self.must_run = True

    def polite_stop(self):
        self.must_run = False

