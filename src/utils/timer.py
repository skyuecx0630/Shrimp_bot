from time import time


class Timer:
    def __init__(self):
        self.start_time = time()

    def start(self):
        self.start_time = time()

    def end(self):
        """
        It returns (hour, minute, second)
        """

        time_elapsed = time() - self.start_time

        return (time_elapsed // 3600, (time_elapsed // 60) % 60, time_elapsed % 60)
