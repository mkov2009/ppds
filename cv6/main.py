from fei.ppds import Mutex, Semaphore, print, Thread, Event
from time import sleep
from random import randint


class Barrier:
    def __init__(self, n):
        self.n = n
        self.count = 0
        self.mutex = Mutex()
        self.event = Event()

    def wait(self):
        self.mutex.lock()
        self.count += 1
        if self.count == self.n:
            self.event.signal()
        self.mutex.unlock()
        self.event.wait()


class Shared(object):
    def __init__(self):
        self.mutex = Mutex()
        self.oxygen = 0
        self.hydrogen = 0
        self.oxyQueue = Semaphore(1)
        self.hydroQueue = Semaphore(2)
        self.barrier = Barrier(3)

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
        print("Oxygen bonding")

        self.barrier.wait()
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
        print("Hydrogen bonding")
        self.barrier.wait()


threads = []
sh = Shared()
for i in range(10):
    t = Thread(sh.oxygen)
    threads.append(t)

for i in range(20):
    t = Thread(sh.hydrogen)
    threads.append(t)

for t in threads:
    t.join()

