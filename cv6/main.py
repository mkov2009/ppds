from fei.ppds import Mutex, Semaphore, print, Thread
from time import sleep
from random import randint


class Shared(object):
    def __init__(self):
        self.mutex = Mutex()
        self.oxygen = 0
        self.hydrogen = 0
        self.oxyQueue = Semaphore(1)
        self.hydroQueue = Semaphore(2)

    def oxygen(self):
        self.mutex.lock()
        self.oxygen += 1
        if self.hydrogen < 2:
            self.mutex.unlock()
        else:
            self.oxygen -= 1
            self.hydrogen -= 2
            self.oxyQueue.signal()
            self.hydroQueue.signal(2)

        self.oxyQueue.wait()
        self.mutex.unlock()

    def hydrogen(self):
        self.mutex.lock()
        self.hydrogen += 1
        if self.hydrogen < 2 or self.oxygen < 1:
            self.mutex.unlock()
        else:
            self.oxygen -= 1
            self.hydrogen -= 2
            self.oxyQueue.signal()
            self.hydroQueue.signal(2)

        self.hydroQueue.wait()
