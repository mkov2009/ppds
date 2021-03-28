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
        self.mutex = Semaphore(1)
        self.oxygenCount = 0
        self.hydrogenCount = 0
        self.oxyQueue = Semaphore(1)
        self.hydroQueue = Semaphore(2)
        self.barrier = Barrier(3)

    def oxygen(self):
        sleep(randint(1, 10) / 10)
        self.mutex.wait()
        self.oxygenCount += 1
        if self.hydrogenCount < 2:
            self.mutex.signal()
        else:
            self.oxygenCount -= 1
            self.hydrogenCount -= 2
            self.oxyQueue.signal()
            self.hydroQueue.signal(2)

        self.oxyQueue.wait()
        print("Oxygen bonding")

        self.barrier.wait()
        self.mutex.signal()

    def hydrogen(self):
        sleep(randint(1, 10) / 10)
        self.mutex.wait()
        self.hydrogenCount += 1
        if self.hydrogenCount < 2 or self.oxygenCount < 1:
            self.mutex.signal()
        else:
            self.oxygenCount -= 1
            self.hydrogenCount -= 2
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

