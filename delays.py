import numpy as np
import time

'''
Status codes:
1: normal
2: fast
3: slow
'''

class Delay:
    def __init__(self, logger):
        self.delay = 0.3
        self.MIN = 0.15
        self.MAX = 0.5
        self.status = 1
        self.keepStatusFor = None
        self.logger = logger

    def setStatus(self, newStatus: int, keepStatusFor: int):
        self.status, self.keepStatusFor = newStatus, keepStatusFor
        
    def next(self):
        if self.keepStatusFor == 0:
            self.logger.log("Entering normal mode")
            self.keepStatusFor = None
            self.status = 1
            self.delay = 0.3

        if self.status == 1:
            dt = np.random.standard_normal() * 0.04
            self.delay = np.clip(self.delay + dt, self.MIN, self.MAX)
        elif self.status == 2:
            self.delay = max(np.random.standard_normal() * 0.05 + 0.15, 0.05)
            self.keepStatusFor -= 1
        elif self.status == 3:
            self.delay = max(np.random.standard_normal() * 0.1 + 0.55, 0.35)
            self.keepStatusFor -= 1

    def fullstop(self):
        self.logger.log("PAUSE: Full stop")
        self.wait(np.random.uniform(0.6, 1))

    def comma(self):
        self.wait(np.random.uniform(0.35, 0.5))

    def backspace(self):
        self.wait(np.random.uniform(0.2, 0.35))

    def enter(self):
        self.logger.log("PAUSE: Enter")
        self.wait(np.random.uniform(0.5, 1.5))

    def thinking(self):
        self.logger.log("PAUSE: Thinking...")
        self.wait(np.random.uniform(1, 3))

    def wait(self, specialDelay: float | None = None):
        time.sleep(specialDelay if specialDelay else self.delay)